# Room for the River: An Analysis of Integrated Water Basin Management Strategies for the Province of Overijsssel in the Netherlands



Released by: EPA1361 Group 23

|           Name           | Student Number |
|:------------------------:|:---------------|
|       Yaren Aslan        | 5257514        | 
|      Ludovica Bindi      | 5469856        |
|     Alexandre Curley     | 5500125        | 
|        Imam Masud        | 5276993        | 
|   Aspasia Panagiotidou   | 5631211        |
|     Dorukhan Yesilli     | 5539501        |


---

## Introduction
This repository contains our analysis to address the case study of the upper branch of the IJssel River, which aimed at developing a flood risk management plan for the Province of Overijsssel.

We conducted a Multi-Scenario Many Objective Robust Decision Making (MS-MORDM) (Bartholomew & Kwakkel, 2020) using the model developed by Kwakkel (2021).

## How to Use

The repository contains both the provided model files (Kwakkel, 2021) and scripts and notebooks created to carry out our analysis (all the files that start with final_step).

To perform the policy, run the the analysis folder in order according to the step number. The results of one step are saved via <code>csv</code> or <code>pickle</code> file and opened in the next file.

To plot the pictures:
* the results of the re-evaluations of the optimal policies (steps 2 and 6) are analyzed and plotted in the <code>final_parallel_coordinate_plot.ipynb</code>
* the plots of the results of the robustness metrics computation (step 3 and 7) are created in their corresponding notebook files (<code>final_step2_reevaluate_policies.ipynb</code> and <code>final_step7_compute_robustness_second_optimization.ipynb</code>)
* the plots for the scenario discovery (step 4) can also be found in the corresponding notebook file (<code>final_step4_scenario_discovery.ipynb</code>)

## Files

EPA1352-G03-A3
│   |   README.md                       # this markdown document 
│   |   

└───report
│   │   report.pdf                  # report of our analysis
│
└───data                            # contains datasets used by the model functions
│   
└───intermediate outputs            # contains datasets to pass results from one step to the followings
|   └───step5 - multi scenario optimization results # contains the results of step 5
|   └───bin                         # older versions of the results
└───output pictures                 # contains the pictures created for the analysis
│   
└───bin                             # contains older versions of the final files and temporary files

## Reference
Bartholomew, E., & Kwakkel, J. H. (2020). On considering robustness in the search phase of Robust Decision Making: A comparison of Many-Objective Robust Decision Making, multi-scenario Many-Objective Robust Decision Making, and Many Objective Robust Optimization. In Environmental Modelling & Software (Vol. 127, p. 104699). Elsevier BV. https://doi.org/10.1016/j.envsoft.2020.104699
Kwakkel, J. H. (2021). Epa1361_open, final assignment. Retrieved from https://github.com/quaquel/epa1361_open