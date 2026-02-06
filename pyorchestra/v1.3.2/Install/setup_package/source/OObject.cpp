#include "OObject.h"
#include "ParameterList.h"
#include "OObjectPieceOfText.h"

namespace orchestracpp
{

	std::string OObject::readObjectName(OrchestraReader *in)// throw(IOException)
	{
		// strip leading spaces and tabs
		std::string tempVar{' ', '\t'};
		in->readWhile(tempVar);
		// read name, do not remove end character
		std::string tempVar2{' ', '\t', '(', '\n', '\r', '{'};
		return in->readUntil(tempVar2);
	}

	ParameterList *OObject::readParameterList(OrchestraReader *in)
	{
		return new ParameterList(in);
	}

	std::string OObject::readDocumentation(OrchestraReader *in)// throw(IOException)
	{
		return in->readUntil("{");
	}

	std::string OObject::readBlock(OrchestraReader *in) //throw(IOException)
	{
		bool originalStripComment = in->stripComment;
		in->stripComment = false;
		std::string tmpText = "";
		int c;

		bool ready = false;
		do
		{
			c = in->read();
			switch (c)
			{
				case -1:
				case '}':
					ready = true;
					break; // so the final '}' is removed!
				case '{':  // we encounter a starting { and include this block recursively
					tmpText+=  ('{') + readBlock(in) + ('}');
					break;
		//---      
				// fixed a bug when s} was encountered by simply unread characters when 
				// reading after "sw
				case 's':
				case 'S': // check for sweep
				{
					tmpText+= c; // first we write the "s"
					// read the second character and check if it is a 'W'
					char *input = new char[5];
					input[0] = in->read();

					if (input[0] == 'w' || input[0] == 'W')
					{
						// second character is a "w" so check the next 4
						char *sweep = new char[5]{'w', 'e', 'e', 'p', ':'};
						char *sweep2 = new char[5]{'W', 'E', 'E', 'P', '{'};

						bool issweep = true;

						for (int j = 1; j < 5; j++)
						{ // check whether word is sweep:
							input[j] = in->read();
							if ((input[j] != sweep[j]) && (input[j] != sweep2[j]))
							{
								issweep = false;
							}
						}

						if (issweep)
						{ // this was a sweep
							// replace Sweep: with Sweep{ and read block
							tmpText += ("weep{");
							tmpText += (readBlock(in));
							tmpText += ('}');
						}
						else
						{ // not a sweep, so unrease the characters (is the order correct?)
							in->unread(input[0]);
							in->unread(input[1]);
							in->unread(input[2]);
							in->unread(input[3]);
							in->unread(input[4]);
						}
					}
					else
					{
						// second character is not a "w" so unread and quit
						in->unread(input[0]);
					}

					break;

				}
				default:
					tmpText += c;
					break;
			}
		} while (!ready);

		in->stripComment = originalStripComment;

		return tmpText;
	}

	std::string OObject::readBodytext(OrchestraReader *in)// throw(IOException)
	{
		in->readUntil("{"); // in case we do not read comment we start here
		in->readWhile("{"); // remove starting '{'

		std::string tmptext = readBlock(in); // without closing }
		if (StringHelper::startsWith(tmptext, "%") && StringHelper::endsWith(tmptext, "%"))
		{
			return tmptext.substr(1, (tmptext.length() - 1) - 1);
		}
		else
		{
			return tmptext;
		}
	}

	OObject::OObject(const std::string &name1) : name(name1), bodytext("")
	{
	}

	OObject::OObject(const std::string &name, ParameterList *placeholders, const std::string &documentation, const std::string &bodytext)
	{
		this->name = name;
		this->placeholders = placeholders;
		this->documentation = documentation;
		this->bodytext = bodytext;

		for (int n = 0; n < placeholders->size(); n++)
		{
			// create empty pieces of text
			placeHolderPointer.push_back(new OObjectPieceOfText(""));
		}
	}

	std::string OObject::getName()
	{
		return name;
	}

	std::string OObject::getKey()
	{
		return name + "__" + std::to_string(placeholders->size());
	}

	std::string OObject::getIdentifier()
	{
		if (placeholders == nullptr)
		{
			return name + "()";
		}
		else
		{
			return name + placeholders->toString();
		}
	}

	std::string OObject::getPlaceholders()
	{
		return placeholders->toString();
	}

	std::string OObject::getDocumentation()
	{
		return documentation;
	}

	std::string OObject::getBodytext()
	{
		return bodytext;
	}

	int OObject::getNrParam()
	{
		return placeholders->size();
	}

	bool OObject::identifierOK(const std::string &name, int nrp)
	{
		return (this->name == name && (nrp == getNrParam()));
	}

	void OObject::append(OrchestraReader *in)// throw(IOException)
	{
		readDocumentation(in);
		bodytext = bodytext + readBodytext(in);
		initialiseTextPointers();
	}

	void OObject::insert(OrchestraReader *in) //throw(IOException)
	{
		readDocumentation(in);
		bodytext = readBodytext(in) + bodytext;
		initialiseTextPointers();
	}

	void OObject::initialiseTextPointers()
	{
		// we should clear the list of textpointers in the C++ version
		// The java version simply creates a new one.
		textPointers.clear();

		std::string tmptext = bodytext;
		std::string splitToken = "!"; // goes wrong when parameter names contain '!'. In text is no problem
		//textPointers = new std::vector<OObjectPieceOfText*>();

		// 1) replace the original "<>" placeholder delimiters by single "!" character 
		for (int n = 0; n < placeholders->size(); n++)
		{
			tmptext = StringHelper::replace(tmptext, "<" + placeholders->get(n) + ">", splitToken + placeholders->get(n) + splitToken);
			placeHolderPointer[n] = new OObjectPieceOfText("?");
		}
			   
		// so we split the text in a set of tokens consisting of 
		// a sequence of text, parameter, text , parameter ....
		std::vector<std::string> tokens = StringHelper::split(tmptext, '!');


		// the textpointers can point to a fixed piece of text, or to 
		// a piece of text managed by a placeholderpointer
		// the latter pieces of text are updated with new parameters 
		// when expanded
		for (auto token : tokens)
		{
			bool tokenIsParameter = false;

			// try to find the token in the list of placeholders
			for (int n = 0; n < placeholders->size(); n++)
			{
	    		if (token == placeholders->get(n))
				{
					tokenIsParameter = true;
					textPointers.push_back(placeHolderPointer[n]);
					break;
				}
			}

			if (!tokenIsParameter)
			{
				textPointers.push_back(new OObjectPieceOfText(token));
			}

		}
	}

	std::string OObject::getSubstitutedBodytext(ParameterList *parameters)
	{
		
		if (textPointers.empty())
		{
			initialiseTextPointers();
		}

		// substitute the text of the parameters
		for (int n = 0; n < parameters->size(); n++)
		{
			placeHolderPointer[n]->text = parameters->get(n);
		}

		std::string totalText;

		// append all the pieces of text to a total substituted text
		for (auto v : textPointers){
			totalText +=  v->text;
		}
	
		return totalText;
	}
}
