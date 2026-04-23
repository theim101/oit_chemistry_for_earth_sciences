# Week 4.2: Aqueous Chemistry Applications, Buffers and Real Data

**Reference:** Appelo & Postma (2012) – *Geochemistry, Groundwater and Pollution*  
<https://doi-org.tudelft.idm.oclc.org/10.1201/9781439833544>  
*Chapters:* 4 and 5  

**Reference:** Lorah, M.M. & Herman J.S. (1988) – *The chemical evolution of a tervertine-depositing stream: Geochemical processes and mass transfer reactions*  
<https://doi-org.tudelft.idm.oclc.org/10.1029/WR024i009p01541>  

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

## 🧠 Lecture 4.2.1 Chemical Buffer Systems

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
In natural waters, chemical buffers are very important. A constant pH is essential for live and many processes buffer the pH. Geochemical modelling using large databases with thermodynamic equilibrium data provide us a tool with whcih we can analyse these complex systems.

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
4. Add text to the jupyter notebook where you explain what you have done and how you interpret the results. Please note, you can later use your notebook as reference material during the exam


**Self-study Before Lecture 1**
- Read Appelo and Postma (2012): Ch. 1.  
- Write equilibrium expressions for 3 given reactions.  
- Watch short video: *Activities vs Concentrations*.  
- Prepare one discussion question.

**Self-study After Lecture 1**
- Read Ch. 4 (4.1–4.5).  
- Write equilibrium expressions for 3 given reactions.  
- Watch short video: *Activities vs Concentrations*.  
- Prepare one discussion question.

---

## ✍️ Tutorial 1: Equilibrium Practice

**Goals**
- Reinforce equilibrium expressions and constants.  
- Practice calculating Q and K.  

**Activities**
1. Dissolution/precipitation examples (calcite, gypsum).  
2. Determine direction of reaction from Q vs K.  
3. Group balancing exercises.  
4. 10-minute conceptual quiz.

---

## 🌍 Lecture 2 (Thursday): Speciation & Natural Waters

**Objectives**
- Extend equilibria to multiple reactions and species.  
- Introduce acid-base, complexation, and redox reactions.  
- Interpret carbonate speciation diagrams.  
- Discuss environmental implications (buffering, pH control).

**Outline**
1. Review key equilibrium concepts.  
2. Overview of reaction types.  
3. Carbonate system (CO₂–H₂CO₃–HCO₃⁻–CO₃²⁻).  
4. Speciation and pH dependence.  
5. Applications in natural waters.  
6. Intro to modeling (PHREEQC, Visual MINTEQ).

**Self-study After Lecture 2**
- Read Ch. 5 completely.  
- Practice carbonate speciation problems.  
- Complete online self-test.  
- Reflection: *How do chemical reactions control groundwater chemistry?*

---

## 🧩 Tutorial 2: Speciation Integration

**Goals**
- Connect Chapters 4 & 5 concepts.  
- Apply equilibrium and speciation ideas.  
- Foster conceptual understanding through teamwork.

**Activities**
1. Carbonate equilibrium exercises (log K, pH, species fractions).  
2. Group discussion: effects of CO₂ and temperature.  
3. Optional PHREEQC demo.  
4. Recap quiz + feedback.

---

## 📚 Student Workload Summary

| Task | Timing | Hours |
|------|---------|-------|
| Lecture review | Mon–Thu | 1 |
| Reading (Ch. 4 & 5) | Throughout week | 2–3 |
| Homework problems | Between tutorials | 2 |
| Online quiz/reflection | Weekend | 1 |

---

## 🧭 Instructor Notes

- Keep lectures conceptual and visual.  
- Use simple examples linking to natural processes (e.g., rainwater pH).  
- Emphasize “why” behind equilibria, not just calculations.  
- Use visuals: diagrams, flowcharts, and sketches.  
- Tutorials should consolidate intuition before quantitative rigor.
