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

We conducted a Multi-Scenario Many Objective Robust Decision Making (MS-MORDM) (Bartholomew & Kwakkel, 2020) using the model developed by Kwakkel (2021). This analysis is performed thanks
to the functionalities developed in the <code>ema_workbench</code> Python package developed by Kwakkel (2022a).

## How to Use

The repository contains both the provided model files (Kwakkel, 2021b) and scripts and notebooks created to carry out our analysis (all the files that start with final_step).

To perform the policy, run the the analysis folder in order according to the step number. The results of one step are saved via <code>csv</code> or <code>pickle</code> file and opened in the next file.

To plot the pictures:
* the results of the re-evaluations of the optimal policies (steps 2 and 6) are analyzed and plotted in the <code>final_parallel_coordinate_plot.ipynb</code>
* the plots of the results of the robustness metrics computation (step 3 and 7) are created in their corresponding notebook files (<code>final_step2_reevaluate_policies.ipynb</code> and <code>final_step7_compute_robustness_second_optimization.ipynb</code>)
* the plots for the scenario discovery (step 4) can also be found in the corresponding notebook file (<code>final_step4_scenario_discovery.ipynb</code>)

## Files

<b>MBDM-Final_Project</b>
* _README.md_: this markdown document 
* _dike_model_function.py_: contains the model creation functions
* _funs_dikes.py_: contains functions for the dike physics sub-model
* _funs_economy.py: contains functions for the costs sub-model
* _funs_generate_network.py_: contains functions for generating a network of the dike rings
* _funs_hydrostat.py_: contains functions for the waves sub-model
* _problem_formulation.py_: contains a function to attach the model to the <code>ema_workbench</code>
* _final_parallel_coordinate_plot.ipynb_: used to plot <code>Parallel Coordinate Plots</code> for the re-evaluation results
* _final_step1_optimization.py_: optimization under reference scenario
* _final_step2_reevaluate_policies.py_: re-evaluation of the optimal policies under sampled scenarios
* _final_step3_compute_robustness.ipynb_: computation of robustness for the optimal policies
* _final_step4_scenario_discovery.ipynb_: scenario discovery based on the optimal policies performances
* _final_step5_multi_scenario_optimization.py_: optimization under scenarios found via scenario discovery
* _final_step6_second_reevaluate_policies.py_: re-evaluation of the new optimal policies
* _final_step7:compute_robustness_second_optimization.ipynb_: computation of robustness for the new optimal policies
* <b>report</b>
    * _report.pdf_: report of our analysis
* <b>data</b>: contains datasets used by the model functions
* <b>intermediate outputs</b>: contains datasets to pass results from one step to the followings
    * <b>step5 - multi scenario optimization results</b>: contains the results of step 5
    * <b>bin</b>: older versions of the results
* <b>output pictures</b>: contains the pictures created for the analysis
* <b>bin</b>: contains older versions of the final files and temporary files

## Reference
Bartholomew, E., & Kwakkel, J. H. (2020). On considering robustness in the search phase of Robust Decision Making: A comparison of Many-Objective Robust Decision Making, multi-scenario Many-Objective Robust Decision Making, and Many Objective Robust Optimization. In Environmental Modelling & Software (Vol. 127, p. 104699). Elsevier BV. https://doi.org/10.1016/j.envsoft.2020.104699
Kwakkel, J. H. (2022a). ema_workbench - Docs - A High Level Overview. Retrieved from https://emaworkbench.readthedocs.io/en/latest/overview.html
Kwakkel, J. H. (2022b). Epa1361_open, final assignment. Retrieved from https://github.com/quaquel/epa1361_open