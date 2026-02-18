---
title: "Week plan 3.2: Working with the command prompt"
authors:
  - name: Timo Heimovaara
---

# Week 3.2: Working with the command prompt on Windows and Mac

Understanding the basics of how the operating system of you laptop  works with files and applications will allow you to be self supporting when you run in to problems. 

A large number of sites are available providing guidance how to work with the command prompt. An example is 
[win geek site for command prompt](https://wingeek.org/cmd-for-windows-11/), and if you search you should be able to find many more. Of course you can also ask and AI to help you.

Similar sites can be found for the Mac. You probably can also find videos on YouTube explaining how the operating system organizes its file system.

For working with the Anaconda prompt you need to organize your file system so that when working with Jupyter-lab or Visual Studio Code you should be able to find your files easily. I suggest the following structure, and I already have seen some of you do something similar:

You have a user home folder on your machine. In this folder you create the following structure:
```{code}
\TUDelft_ECTB
..\ECTB1230_chemistry
..\..\Installation_Files
..\..\Week 3.1
..\..\Week 3.2
etc...
```

When you open the Anaconda Prompt, make sure that you are in your user folder where you have installed \TUDelft_ECTB.

Then you start
```{code}
conda activate ECTB1230-env    # activate your ECTB1230-environment
jupyter-lab                    # starts the jupyter-lab server
```

