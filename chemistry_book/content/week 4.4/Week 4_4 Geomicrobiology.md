# Week 4.4 Redox chemistry in practice: Geomicrobiology and element cycling

**Schedule:**
-   11 May 2026 0945 - 1245: lecture (1h) followed by guided exercise
-   11 May 2026 1545 - 1745: demonstration cloud chamber (Ajit)
-   18 May 2026 0945 - 1245: lecture (1h) followed by guided exercise

**Reading material:**
-   Microbiology for Earth Scientists chapter 4 and 8 
    -   Extra: chapter 2, par 5.1, par 9.1, par. 12.1
-   Tro: sections on redox chemistry (see week 3.4 and 3.8)

**Extra background reading:**
-   [The Biomass Distribution on Earth](https://www.pnas.org/doi/10.1073/pnas.1711842115),  Bar-On et al. 2018
-   [The biomass and biodiversity of the continental subsurface](https://www.nature.com/articles/s41561-018-0221-6), Magnabosco et al. 2018
-   [A global comparison of surface and subsurface microbiomes reveals large-scale biodiversity gradients, and a marine-terrestrial divide](https://www.science.org/doi/10.1126/sciadv.adq0645), Ruff et al. 2024


This 'week' (spread over two weeks) will link what you learned about redox chemistry in weeks 3.4 and 3.8 to the role of microbial activity in the cycling of elements such as carbon. In week 3.4 you learned how the transfer of electrons in electrochemical cell can be used for power generation. This is also how life, big and small, obtains its energy, and one of the main ways in which microbes mediate the cycling of elements between different redox states. In this section of the course you will learn to:

1.  Explain the role of microorganisms in global element cycling
2.  Apply the principles of redox chemistry to calculate the biological (designated with " ' ")cell potential (E<sup>0'</sup><sub>cell</sub>) and Gibbs free energy (𝚫G<sup>0'</sup> ) of microbial metabolic reactions.  

## Biomass in the biosphere

In the course on Earth & Climate Systems you learned about the biosphere and its influence on the climate (see the lectureslides from prof. Susan Steele-Dunne). Plants are an obvious part of the biosphere, accounting for ~82 % of biomass on Earth, as are animals, although these account for only 0.4 % of total biomass, see figure 1 ([Our world in Data - Life on Earth](https://ourworldindata.org/life-on-earth)). The rest is stored in microbial cells (14.3 %) and fungi (2.2 %). 

:::{figure} images/OWiD_Global_Biomass.png
:name: Global Biomass distribution, Our world in data
:align: center
:width: 50%
Global Biomass distribution, Our world in data
:::


Where do we then find this biomass? With plants, you will probably think of the Earth surface. But what about the oceans, and the Earth beneath our feet? As you can see in figure 2 from the paper by Bar-On et al. (link above), biomass is spread over terrestrial, marine, and deep subsurface (>8 m) environments, holding 85 %, 1 % and 14 % of biomass, respectively.

:::{figure} images/Bar_on_figure2.png
:name: Bar-On et al. 2018 figure 2
:align: center
:width: 50%
Bar-On et al. 2018 figure 2
:::

Biomass is composed of a range of elements, of which carbon, hydrogen, oxygen, nitrogen, sulfur and phosphorus are the main ones. Biomass therefore is one of the pools in which these elements are stored. Let's take carbon as an example, consider the global carbon pools summarised in table 1:  

:::{figure} images/Table_2_1_Geomicrobiology.png
:name: Table 2.1 Falkowski, 2012
:align: center
:width: 50%
Table 2.1 Falkowski, 2012
:::

We can make a distinction between inorganic (no C-H bonds) and organic (C-H bonds) carbon. Organic carbon pools originate from biomass. Next to the biosphere this includes kerogens and fossil fuels, together accounting for up to 20 % of global carbon (note that while the carbonate reservoir is inorganic, microbes can contribute to carbonate mineralization, see 12.1.1 in Microbiology for Earth Scientists). If we then consider the mean carbon fluxes between these different reservoirs (table 2) as they were before the industrial age, given in Tmol C yr<sup>-1</sup>, we see that the burial of organic carbon (biomass!) accounts for ~57 % of the annual flux to carbon sinks. 

:::{figure} images/Table_3_4_top_Geobiology.png
:name: Table 3_4 Walmann, 2012
:align: center
:width: 50%
Table 3.4 Walmann, 2012
:::

Note that this data from [The Global Carbon Cycle: Geological Processes](https://onlinelibrary.wiley.com/doi/10.1002/9781118280874.ch3) by Walmann et al. (2012) reflects their mean over the past million years. For more detail on the impact of industrial activity on the carbon cycle, revisit the lectures from the Earth & Climate Systems course. 

### Microbial biomass
We will focus on microorganisms, single-celled organisms too small to see with the naked eye. We distinguish between two groups: bacteria and archaea. While they can look similar under the microscope, there are important differences, for example how their cells are structured. We will not go into that in detail, but if you are interested, read chapter 2 (p. 11 - 16) in Microbiology for Earth Scientists. 

You already saw in figure 2 above that microbial cells account for 14.3 % of total biomass on Earth. Note that 90 % of this is found in the deep subsurface (!). The remaining 10 % of microbial biomass is stored in terrestrial and marine environments. 

If we now go back to our carbon example: of all carbon stored in global biomass, about 80 % is stored in plants, and 20 % in microbes. 

:::{figure} images/Brock_biomass_carbon.png
:name: Figure 2: Percentage of total organic Carbon, Nitrogen, Phosphorus per biomass type
:align: center
:width: 50%
Figure 2, Brock et al. 
:::

Note that for nitrogen and phosphorus this is the opposite: ~80 % of N and P stored in biomass is found in microbial biomass. 


## Redox chemistry, microbial metabolism and element cycling
The section above shows how microbial biomass acts as a reservoir for elements like carbon, nitrogen, phosphorous and sulfur, making it an important part of the cycling of these elements. 

To produce biomass life needs energy, and their mode of obtaining this energy is another main route through which life impacts element cycling. Microbes can obtain this energy from light (photosynthesis, like plants) or by **catalyzing exergonic redox reactions** that do not occur spontaneously, or at significantly lower rates under the environmental conditions at which the microbial cells grow. These redox reactions are **thermodynamically favorable**, but **kinetically hindered**. Microbes (and all life, for that matter) can overcome these kinetic barriers with specialized enzymes that lower the activation energy for specific reactions. This is a key principle underpinning life, see e.g. paragraph 9.1 in Microbiology for Earth Scientists. 

**Wnat to know more?** If you want to know more about how energy from redox reactions is harvested by microbial cells, read section 4.4 of Microbiology for Earth Scientists. For our purposes here it suffices to consider microbial cells as **'catalysts'** of redox reactions.  

### Example: The microbial carbon cycle
Sticking with carbon, how does microbial energy metabolism impact the cycling of carbon? Figure 3 (Figure 5.1 in Microbiology for Earth Scientists) shows the main microbial processes mediating conversion between inorganic (CO<sub>2</sub> and CH<sub>4</sub>) and organic carbon (C<sub>org</sub>). Here, we will look at a microbially catalyzed redox reaction that involves CO<sub>2</sub> and CH<sub>4</sub>.

:::{figure} images/Carbon_cycle.png
:name: Figure 3: Main reactions in the biological carbon cycle
:align: center
:width: 50%
Figure 3, Carbon Cycle (Kirk, 2022) 
:::


## Exercises 
*Applying your knowledge:*

A.  Let's use some of the concepts you learned in week 3.4 to take a look at redox reactions involving CO<sub>2</sub> and CH<sub>4</sub>: 
1.   Would CO<sub>2</sub> be an electron donor or acceptor? And CH<sub>4</sub>? What are the oxidation states of both molecules? 
2.   What is the half reaction relating CO<sub>2</sub> and CH<sub>4</sub>? 
3.   What is the standard electrochemical potential of this half reaction?
4.   In the environment, a neutral pH is more realistic than pH 0 (standard conditions). How does this impact the electrochemical potential of the half reaction you formulated above? The concentrations of the other reactants remain 1 M (including electrons, although these don't exist freely in solution). 
5.   If hydrogen oxidation/proton reduction is the accompanying half reaction to the half reaction described in (3), what is the overall redox reaction? 
6.   What is the electrode potential for H<sub>2</sub> oxidation at pH 7?
7.   What is the electrode potential of the overall redox reaction formulated in (5) at pH 7?
8.   And the Gibbs free energy?  


B.  Now with hydrogenotrophic sulfate reduction
1.  What is the half reaction for the reduction of sulfate (SO<sub>4</sub><sup>2-</sup>) to hydrogen sulfide (H<sub>2</sub>S)? 
2.  What are the oxidation states of S in both molecules?
3.  What are the standard Gibbs free energy change (𝚫G<sup>0</sup>) and standard electrochemical potential (E<sup>0</sup>) of this half reaction? Use 𝚫G<sub>f</sub> of SO₄²⁻(aq): -744.5 kJ/mol; H₂S(aq): -27.9 kJ/mol
4.  And the biological electrochemical potential (E<sup>0'</sup>)? 
5.  What is the overall redox reaction for sulfate reduction coupled to H<sub>2</sub> oxidation?
6.  What is the biological standard electrochemical potential (E<sup>0'</sup>) of the overall redox reaction?
7.  And the standard biological Gibbs free energy (𝚫G<sup>0'</sup>)? 
8.  Compare the impact of pH on hydrogenotrophic CO<sub>2</sub> reduction and hydrogenotrophic sulfate reduction


## Take Aways
After this week you are now able to:
1.  Explain the role of microorganisms in global element cycling
2.  Apply the principles of redox chemistry to calculate the biological (designated with " ' ")cell potential (E<sup>0'</sup><sub>cell</sub>) and Gibbs free energy (𝚫G<sup>0'</sup> ) of microbial metabolic reactions. 

As you have seen, microorganisms play an important role in global element cycling both as **element reservoirs**. Of all carbon stored in biomass, microbes harbor ~14 % of biomass carbon. For Phosphorus and Nitrogne this is ~80 %. They furthermore are important **catalysts** of redox reactions that are **thermodynamically favorable** but **kinetically hindered**. Without microbes, many environmental redox reactions would not occur.

In the exercises with hydrogenotrophic CO<sub>2</sub> and SO<sub>4</sub><sup>2-</sup> reduction you have seen how you can apply the principles of redox chemistry you learned in week 3.4 to calculate the Gibbs free energy change of redox reactions at pH 7, the **biological standard condition**.
