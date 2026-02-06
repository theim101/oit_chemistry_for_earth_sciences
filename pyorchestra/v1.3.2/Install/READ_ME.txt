#-------------------------------#
DESCRIPTION OF FOLDERS 
1. ORCHESTRA_GUI: the graphical user interface to create a chemical input file for ORCHESTRA
1. Example/ : example of how to use the module
2. setup_package/ : folder with setup.py file that the user needs to run to obtain the module

#-------------------------------#
REQUIREMENTS 
1. Check if pip and python is installed
For this module to be installed correctly, we use python and the pip package manager. 
A quick check to see if you have pip installed (works on every device):
- open terminal
- Type: pip --version

If not, install python from https://www.python.org/downloads/ 
When installing python, pip is installed automatically (it is checked by default).

2. Install C++ (for windows)
- go to https://visualstudio.microsoft.com/downloads/
- download Build Tools for Visual Studio 2022
- open visual studio installer
- click on 'modify'
- select the 'Desktop development with C++' and press 'download'. As a check, the average size should be in the order of 6.8 gb.
- C++ is now ready to be used!!

#-------------------------------#
INSTALLING MODULE
1. in command prompt or terminal. Navigate to the directory containing setup.py file (in setup_package).
2. To check whether you are in the right directory type 'dir' (Windows) or 'ls' (Mac/Linux). this should show the available files in your working directory (including setup.py)
3. To install the ORCHESTRA package for python, type: pip install .
4. Installing might take up to a minute
5. If done correctly, the module called "PyORCHESTRA-1.0.1" should be installed

#-------------------------------#
USING THE MODULE
A quick check to see if the module works is by running the main.py file (in example) using python. Depending on the environment, type either 'python main.py' or 'python3 main.py'.

In main.py file the general usage of the created module is described! 



