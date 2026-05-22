# Week 4.6 & 4.7: Group Projects Landfill Leachate

**Reference:** Introduction Sustainable Aftercare for Landfills
<https://duurzaamstortbeheer.nl/>  (#iDS)

**Format:**  
- 4 afternoons of group work (Wed & Thu) – 4 hrs each  

---

## Learning Goals

By the end of the project, students should:

1. have experienced how to analyze a real world data set using the theory from this course and using pyORCHESTRA.  
2. Understand how to, and be able to evaluate the simulation results and process the results to create graphs.  
---

## 🗓 Weekly Overview

| Component | Duration | Focus | Method |
|------------|-----------|--------|--------|
| **Group work day 1 (27-05-2026)** | 4 hrs | Understand the provided template notebook, get acquainted with the data provided| Study, Practice & Review earlier content, import and process data |
| **Group work day 2 (28-05-2026)** | 4 hrs | Prepare and apply a geochemical analysis on a selected sample with pyOrchestra.| Practice & Review earlier content, process data with pyOrchestra |
| **Group work day 3 (03-06-2026)** | 4 hrs | Assess temporal changes in the data set.| Practice & Review earlier content, process data with pyOrchestra |
| **Group work day 4 (04-06-2026)** | 4 hrs | Write a report.| Review results and write a report |

---
## Description of the project
**Introduction**

Within the Netherlands we have been carrying out a project called "Introduction of Sustainable Aftercare of Landfills" or in Dutch: Introductie Duurzaam Stortbeheer [iDS](https://duurzaamstortbeheer.nl/). The aim of this project is to investigate if we can reduce the emission potential of a wastebody by active treatment using infiltration of water aeration. Infiltration is hypothesized to increase the flushing of dissolved contaminants from the wastebody, aeration is hypothesized to simulate the biodegradation of organic matter in the waste body. Both approaches will eventually lead to lower contaminant concentrations in the leachate.

Sanitary engineered landfills are technical facilities which allow us to store waste indefinitely. In order to protect the environment and human health from emissions, these sites are fitted with impermeable bottom liners with a drainage systems for leachate collection, and gas extraction systems within the waste body for collection of methane and other greenhouse gases being produced in the waste body. After the landfilling has been completed the current regulations require the wastebody to be capped with a water tight liner so that no rainfall can infiltrate. As a result, the driving force for leachate emissions is no longer present. The drawback, however, is that this coverliner needs to be replaced every 75 years. This is nicely illustrated with the animation you can find on [iDS](https://duurzaamstortbeheer.nl/) at the bottom of the page.

Pilot projects are being carried out within the context of iDS at three landfills: Kragge near Bergen op Zoom, Braambergen near Almere and Wieringermeer near Wieringermeer. A large amount of background information can be found in the ["background"](https://duurzaamstortbeheer.nl/achtergrond/) section of the iDS website. Here you can find information on the three pilot projects in the section ["Project documents"](https://duurzaamstortbeheer.nl/projectstukken/) and a number of [publications](https://duurzaamstortbeheer.nl/publicaties/) that have been written in the course of the project. 

In the ["Project documents"](https://duurzaamstortbeheer.nl/projectstukken/) section of the iDS website, you can find the original plans for the pilot projects. The general overview of the iDS projects is given in the ["Integraal Plan van Aanpak"](https://duurzaamstortbeheer.nl/wp-content/uploads/2023/09/IENM-BSK-2014-116919-Def-concept-IPvA-versie-mei-2014.pdf). The site specific plans can be found in the documents starting with "Deel van Aanpak". You can also find two documents in English giving similar information: "Project plan Sustainable Landfill Management...".


Leachate quality from the three pilot projects have been measured with a relatively high frequency since 2012, the start of the base-line monitoring. Preparation of the active treatment began in 2016 and the treatment was started in 2018 and will continue until 2029. 

**Research questions**

Your task is to analyze a leachate data set in order to answer the following questions:
1. What is the likely composition of the leachate within the waste body?
2. How much solids will precipitate from the leachate once it is exposed to air in the water treatment plant?
3. How much solids will have precipitated as the leachate moved from the bulk of the waste to the water treatment system?
4. Do these processes vary over time.


**Project assignment**

The assignment that you need to do is to carry out an analysis of a dataset that is provided to you. In many cases where routine interpretations are done, it is most efficient to start with a pre-existing approach or script for your analysis and then modify the approach to your specific needs. This is also the approach you need to do here. The notebooks provided to you, show a similar analysis so you can apply this notebook as your template. 

Your responsibility is to adapt the notebook and the interpretation where necessary. At the same time you need to understand what you are doing. The generated results need to be included in your final report.


## Day 1: Import and understand provided data set

Before you can start working on analyzing the dataset, you have to familiarize yourself with the data provided to you. The data is provided in an Excel sheet. The data is an export from a single waste body from one of the pilot projects and contains the date a sample was taken and the results of a chemical analysis in the laboratory.

First you need to obtain an overview of the data. Your assignment for this day is to:
1. Import the data;
2. Get a quick over view of the content and the structure of the dataset;
3. Understand how to plot the time series in the data set, save the figures to a file and create an overview report;
4. Need to calculate molar concentrations from mg/l values;
5. Think about what questions you want to resolve with this data?
    - Saturation status of the samples as they are;
    - What were mostly likely conditions where the samples originated?
    - What will happen to the samples if the leachate would be discharged to a system at atmospheric conditions.
5. Prepare the interface to PyOrchestra, have a look at provided GUI of Orchestra and the corresponding Chemistry File

The provided notebook demonstrates how to make time series plots. You are requested to also have a look at other characteristics of the data commonly used for exploratory data analysis.

## Day 2: Apply a geochemical analysis on one of the water samples in the data set

The first day you looked at the data provided to you and selected a data from a single sample on which you will do your first analysis. After that you have been thinking about a strategy to analyze the data and make some interpretations. On the second day you will carry out a full interpretation of the selected sample.

The steps you need to do on this day are:
1. Prepare the interface to PyOrchestra, have a look at provided GUI of Orchestra and the corresponding Chemistry File;
2. Decide on how many Chemistry files you require for your analysis;
3. Implement the input and output arrays required to interface with pyOrchestra for each Chemistry file;
4. Decide on which output you want to use from pyOrchestra for your interpretation
5. Put all this together in code for pyOrchestra calculations;
6. Run three types of pyOrchestra calculations to answer the three questions:
    - what is the initial state of the sample?, 
    - what happens if it is equilibrated with the atmosphere?, 
    - and what were the conditions where it originated? 
7. Interpret the results;
8. Include the outcomes of your work in your report;

All steps you need to do have been shown earlier in weeks 3.7 and 4.2. 

## Day 3: Assess the temporal variation in the data

The first two days you looked at the data and performed a geochemical analysis on a selected sample. The task at hand for the third day is to check the temporal variation in the data set. As you well know, a year has four seasons, winter, spring, summer and autumn. As mentioned earlier, leachate production rates depend heavily on the season. In spring, after the winter with low evapo-transpiration, leachate production rates are highest, whereas in the autumn after summer with high evapo-transpiration leachate production rates tend to be lower. On this day you are provided with a data set with the measured cumulative leachate and leachate production rates.

The task at hand for you is to select some representative samples from the analyzed samples and repeat the analysis you did on the 2nd day. The samples should be selected in such a way that you are able to get an understanding of the seasonal variation in the data.

You should now have sufficient understanding how to code the analysis, that using copy-paste-edit you should be able to setup your analysis yourself. 

The steps you need to do on this day are:
1. Import and plot the data from the leachate production data-set;
2. Use this information to choose time periods from which you want to analyze the geochemistry of the leachate;
3. Select specific samples, please ensure that the samples have sufficient parameters. Ensure use the time series of the chemical parameters to make an educated guess for the missing values;
4. Run three types of pyOrchestra calculations to answer the three questions:
    - what is the initial state of the sample?, 
    - what happens if it is equilibrated with the atmosphere?, 
    - and what were the conditions where it originated? 
5. Consider putting the above steps in a single function which you can then call from a loop;
6. Interpret the results;
7. Include the outcomes of your work in your report;

## Day 4: Write a report

Every detailed analysis of a dataset needs to be reported in a consistent way. The aim of the report is to present your results, to motivate and document the strategy you applied in order to interpret the data and explain the assumptions you made while interpreting the data. In your report, you state the research questions and application challenges that need to solved. Finally you answer the questions using the results of your interpretation and your understanding of the underlying processes.

The abstract of your report is a concise summary of the above.

With this report you have concluded your group project. The report needs to be uploaded to Brightspace **before 18:00** on **4 June 2026** .

---


