---
title: "Week 3.1, Tutorial 1: Prepare your python-environment for this class"
authors:
  - name: Timo Heimovaara
---


# Week 3.1, Tutorial 1: Prepare your python-environment for this class

## Motivation
For this course we make use of course notes presented to you with an interactive python book implementd in Jupyter-book. Many of the assignments will be introduced in this book and you need to download some of the Jupyter-notebooks to your own computer to do the assignments. Furthermore we would like you to carry out your calculations using python, in stead of using your hand held calculator. Of course you need develop your strategy to solve the problem using pen and paper!

---
## Downloading Python
For this course we will the Anaconda distribution. This [link](https://www.anaconda.com/download) brings you to the Anaconda website where you can down load the package. Packages are available for Windows, Mac and Linux. 
When landing on the download page you see the following.

```{figure} ./images/Screenshot_Anaconda_Download.png
:label: Anaconda_Download
:align: center
:width: 100%
Figure 1: Download page of the Anaconda website.
```


If you click on the green "Get Started" icon the website will ask you to set up an account. You can find the benefits of such an account in the inform using the links to the left. However you can also scroll to the bottom of the page where see a black button "Download Miniconda Installer":

```{figure} ./images/Screenshot_Miniconda.png
:label: Miniconda_button
:align: center
:width: 100%
Download button for Miniconda.
```
When you click this button you will land on a page where you can download either the Anaconda or the Miniconda package with out the need for further registration. Please make sure you select the correct version for your operating system.

```{figure} ./images/Screenshot_Download_Links.png
:label: Miniconda_button
:align: center
:width: 100%
Download links for Miniconda. Please ensure you have selected the correct operating system before 
```

The Anaconda distribution is a much larger file than the Miniconda distribution. With Anaconda you get a large amount of additional packages from Python universe. With the miniconda distribution you only get a base version for a python environment. The difference in size is huge: Miniconda is about 90 Mbytes, where Anaconda is about 1.1 Gbyte. The Anaconda distribution comes with an extensive menu, the miniconda distribution is best managed from the command line. You are free to choose which version to use as the next steps in this document are similar for both.

For this manual I suggest you download the Miniconda pacakge and I will explain the process for Windows. I choose Miniconda because it is compact, and I will explain how to setup the python environment for this course using the command line (or console). Using a console to run your python pacakges gives you much more insight where your files are stored on your computer and as a result it is easier to manage your work.

Start by downloading one of the two packages. Once the download is complete, double click on the package to start the installer. Accept check the agreement and click "I Agree". Accept that you only install for yourself (click Next), accept the default directory (click Next), allow the creation of shortcuts and click "Install". Once the installation is complete, depending on your choices, you will end on the Anaconda website again where you can go through the tutorial to make your self acquainted with this distribution. You can always come back this site later if you want to!

---
## Preparing the python environment for this class

The conda package manager is a little slow. Instead we will be using the mamba package manager which we first need to download and install with conda. To do this you open the "Anaconda Prompt" from the Windows menu. In this console type:
```{code}
conda install -c conda-forge mamba
```
This command pulls the mamba package from the "conda-forge" repository and installs in the base environment of your Conda installation. Please note this command can take quite some time, but live with it. After the installation has completed we will update the packages in the "base" environment to the newest versions by running:
```{code}
mamba update --all
```

### Install the ECTB1230 python environment
For the next step you need to download the ECTB1230-env.yaml file from the Brightspace course website to a folder on your computer. You install this file in the "Anaconda Prompt" from the folder with file with:
```{code}
mamba create -f ECTB1230-env.yaml
```

In order to be able to start working in this python environment you need to first **activate** it using"
```{code}
conda activate ECTB1230-env
``` 
For this class we will use ORCHESTRA, a chemical equilibrium solver which allows us to work with very complicated chemical systems. In order be able to use ORCHESTRA we need to install the pyOrchestra package. As this package is still under development, it is not yet available in the Conda or the Pip repositories online, you need to download it from Brightspace and then install it yourself. You need to carry out the following steps:

1. download the pyorchestra.zip file from Brightspace;
2. unzip the file in a folder on your computer;
3. Open the "Anaconda Prompt" and change in to the folder with pyorchestra files.
4. Change to the pyorchestra/v1.3.2/Install/setup_package folder with:
```{code}
cd v1.3.2\Install\setup_package
``` 
Check that you see a setup.py file in the setup_package folder. Then install pyorchestra with:
```{code}
pip install .
```
Do not forget the ., as this implies pip to install using the setup.py file in the current directory.

---
## Some changes to Windows to make your Anaconda prompt accessible from any directory using right mouse click.
To make navigating easier with on windows you can tweak windows to start the Anaconda Prompt from you file browser using your right mouse button using the explanation found [here](https://www.codegenes.net/blog/adding-open-anaconda-prompt-here-to-context-menu-windows/#google_vignette).

---
## Install vscode for coding
It is possible to carry out all the programming in this course using Jypyter-lab, you just have to type Jupyter-lab in the Anaconda Prompt after having activated ECTB1230-env. However, it is in many cases more convenient to code in a so-called Integrated Development Environment or IDE. VScode is an advanced IDE that allows you to work with plain python and Jupyter notebooks. I can be downloaded [here](https://code.visualstudio.com/Download).

