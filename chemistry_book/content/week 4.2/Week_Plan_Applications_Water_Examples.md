# Week 4.2: Aqueous Chemistry Applications, Buffers and Real Data

**Reference:** Appelo & Postma (2012) – *Geochemistry, Groundwater and Pollution*  
<https://doi-org.tudelft.idm.oclc.org/10.1201/9781439833544>  (#appelo&postma)
*Chapters:* 4 and 5  

**Reference:** Lorah, M.M. & Herman J.S. (1988) – *The chemical evolution of a travertine-depositing stream: Geochemical processes and mass transfer reactions*  
<https://doi-org.tudelft.idm.oclc.org/10.1029/WR024i009p01541> (#lorah&herman)

**Format:**  
- 2 lectures (Wed & Thu) – 1 hrs each  
- 2 tutorials (Mon & Thu) – 3 hrs each  
- 6 hrs self-study  

---

## 🎯 Learning Goals

By the end of the week, students should:

1. Understand how to, and be able to setup a chemical equilibrium problem using ORCHESTRA.  
2. Understand how to, and be able to develop a scenario to run and experiment with ORCHESTRA using a template notebook.  
3. Understand how to, and be able to evaluate the simulation results and process the results to create graphs.  
4. Apply all of the above to carbonate reactions in a heterogeneous gas, liquid and solid system.
---

## 🗓 Weekly Overview

| Component | Duration | Focus | Method |
|------------|-----------|--------|--------|
| **Self-study** | 3 hrs | Preparation for week 4.2 + reflection | Study, Practice & Review earlier content |
| **Lecture 1 (Wed)** | 1 hrs | Mass-action law and buffered systems| Lecture + examples |
| **Tutorial 1** | 2 hrs | Practice with template and Orchestra | Guided group exercises + discussion |
| **Self-study (Wed)** | 1 hrs | Study paper by Lorah & Herman| Reading & problems |
| **Lecture 2 (Thu)** | 1 hrs | Real world examples, precipitation of travertine | Interactive lecture |
| **Tutorial 2** | 2 hrs | Assignments & weekly test | Group Exercises + discussion, online formative test |
| **Self-study** | 3 hrs | Preparation for week 4.3 + reflection | Study, Practice & Review |

---

## 🧠 Practical 4.2.1 Chemical Buffer Systems

**Introduction**
A chemical buffer is a solution in which more or less equal amounts of a weak acid and its conjugate base are present. Buffers are essential systems for the living nature as buffers resist pH change. We will work on three examples, two related to carbonate which for example control the pH in the oceans and in our blood. A third which is used in industrial processes (such as food and beverage preservation), the sulfurous acid buffer.

For a chemical buffer system we can derive the following relationship from the mass-action law:
$$
pH = - \log K + \log(\frac{\text{A}^-}{\text{HA}})
$$
where $\text{HA}$ is the weak acid and $\text{A}^-$ is its conjugate base.

*Selfstudy question*
Are you able to derive the above equation from the mass-action law?

A buffer system is created by dissolving more or less equal amounts of the weak acid and its conjugate base. 

*Selfstudy question* What is the pH if the amount of weak acid is exactly equal to the conjugate base?

**Using Orchestra to analyse chemical buffer systems**
In natural waters, chemical buffers are very important. A constant pH is essential for live and many processes buffer the pH. Geochemical modelling using large databases with thermodynamic equilibrium data provide us a tool with which we can analyse these complex systems.

In order to be able to run an geochemical solver you need to apply the following concepts and steps:
1. The solver needs to know the total amounts of all Master Species in the system;
2. You as a user need to define the Master Species and what the totals are;
3. The solver solves the non-linear chemical equilibrium problem by calculating the activities of all possible species present in the database which can be derived from the set of master species;
4. The solver ensures that the mass-balance of all master species is achieved;
5. The solver ensures that the charge-balance is achieved;
6. You as a user have different options to allow the solver to achieve charge balance:
    - do not change, only calculate;
    - adjust the pH to achieve charge balance;
    - adjust ions like $\text{Na}^+$ and $\text{Cl}^-$ to achieve charge balance.
7. You as a user need to think how you want to implement a model scenario. This scenario consists of a sequence of Geochemical solver calculations which provide you with the information you are interested in.

**Implementing the carbonate buffer system in Orchestra**
We will use pyOrchestra to calculate the pH change for a non-buffered and a buffered carbonate system. 
1. *Model set-up* We first to set-up the model by defining the variables that we use to obtain data from pyOrchestra;

2. *Scenario calculations* Each simulation scenario consists of steps where we repeat a number of steps:
    1. Define the initial mass of the master species for the current step;
    2. Run the simulation for this step. For the buffer system we will simulate a titration using a strong acid ($\text{HCl}$). We achieve this by incrementally adding small amounts of acid to our solution and then recalculating the chemical equilibrium. During the simulation, we capture all relevant output from pyOrchestra in order to process data afterwards;
    3. Process the output. In this case we mainly generate plots to see how the pH of the system changes as a function of adding the acid.

**Different scenarios**
In order to get you started, *Tutorial 1_Carbonate_Buffer_system.ipynb* provides you with a script with an implementation of a scenario for a non-buffered carbonate system. Your task is to expand this script with two additional scenarios: 
1. a buffered bicarbonate / carbonate system; 
2. a buffered carbonic acid / bicarbonate system;

In order to create the scenarios you need to consider the following:
1. how should you change the initial conditions so that you implement the buffer. I suggest you explicitly write down on a piece of paper what the chemical composition is of your buffer system. Use this information to calculate the total amounts of the master species present in your scenario.
2. think through how you would like to present the results of your scenario and then find a way how you can program this.
3. the provided script, has one plot for the results. Many different plots are possible, try to implement three additional plots that give more insight in to your results;
4. Add text to the jupyter notebook where you explain what you have done and how you interpret the results. Please note, you can later use your notebook as reference material during the exam.

The final analysis you need to carry out is very similar to the carbonate scenarios you have implemented. You need to assess a buffer system based on sulfurous acid. You need to carry out the same steps as above.

**Checking input parameters for ORCHESTRA**
The input files controlling the Orchestra calculations have been predefined for these assignments. Once you are able to carry out the assignments with pyOrchestra, we suggest that you also have a closer look at the ORCHESTRA GUI which you can start by clicking on the *orchestra2026.jar*. In the GUI you will be able to adjust settings which are then written to the input files.

For the adventurous of heart, we suggest to copy the contents from one of the tutorial folders to a new folder. See if you can modify the system to work for another buffer system. One of the most used buffer systems in microbiology is the so-called phosphate buffer. Lots of information can be found using an online search.


## ✍️ Practical 4.2.2: Deposition of travertine from a stream
**Discussion results practical 4.2.1**
At the start of this practical, we will briefly revisit the outcomes for practical 4.2.1.

**Introduction to practical**
This practical is aims to show how you can redo the analysis presented in an academic paper. The application is a realworld example of how geochemistry is used to get a better understanding of natural processes.

In the paper by Lorah and Herman (1988), samples have been taken from a stream and analysed in the laboratory. The chemical results have been analysed with one of the first geochemical solvers. The analysis shown in the paper gives a good insight of carbonate chemistry and how we can use equilibrium solvers to interpret systems which are not necessarily in equilibrium. In this case, the degassing of $\text{CO}_2\text{[g]}$ from the water in the stream is a relatively slow process. Most of the degassing takes place in the turbulence of a water fall in the stream.

**Implementing the chemical system in Orchestra**
Again we have provided you with a template with the model set-up and an example scenario. In the template two of the samples are passed to pyOrchestra. You need to figure out a way to pass all samples in an efficient manner so that you can create a table of the amounts of master-species for the different calculations. For this you need to translate the values from mg/l to mol/l. To do this you need to use some basic Python coding.

In the initial calculations of our scenario, we will not allow the minerals to precipitate. The output of pyOrchestra will provide us information about the saturation state in the sample (*.si) values. Supersaturation is indicated by SI values > 0.

In our scenario we will allow minerals to precipitate, either completely or partially using a parameter called *deltaSICalcite*, with which we can force pyOrchestra to allow Calcite to precipitate to a fixed SI-value not necessarily equal to 0.

The sequence of steps you need to perform are :
1. Initial calculation: Calculate the equilibrium conditions and corresponding SI-values for the minerals for all water samples. This is done using the measurements from the laboratory which you translate to the initial mass of all master species in each sample;
2. Run the simulations you want to carry out. An example of a simulation is to use pyOrchestra to calculate how much Calcite needs to precipitate in order to achieve a specific downstream SI-value. At the same time we can evaluate to what extent the concentration of dissolved in the stream are changing due to the precipitation of calcite and if other processes need to be taken in to account;
3. Process the output so that you can convey your results in the best way.

**Exam level question**
At the end of the practical we will provide you with an exam-level question which is similar to the ones used in the final exam.

---


