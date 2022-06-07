# This is a sample Python script.

import warnings

warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('white')

# ema_workbench components needed
from ema_workbench import (MultiprocessingEvaluator)
from ema_workbench.em_framework.points import Scenario
from ema_workbench.analysis import parcoords

# model functions needed
from problem_formulation import get_model_for_problem_formulation

# other libraries needed
import time  # to keep track of the runtime

if __name__ == '__main__':

    start_time = time.time()
    print('Runtime started')

    problem_formulation = 3
    nfe_selection = 5
    epsilon_selection = [0.1]

    # our way to set the initial reference scenario: using average
    ref_scenario_description = {}
    for i in [0, 1, 2]:
        ref_scenario_description['discount rate ' + str(i)] = 2.5
    ref_scenario_description['A.0_ID flood wave shape'] = 5
    for dike_ring in ['A.1', 'A.2', 'A.3', 'A.4', 'A.5']:
        ref_scenario_description[dike_ring + "_Bmax"] = 190
        ref_scenario_description[dike_ring + "_pfail"] = 0.5
        ref_scenario_description[dike_ring + "_Brate"] = 1.5

    dike_model, planning_steps = get_model_for_problem_formulation(problem_formulation)

    with MultiprocessingEvaluator(dike_model) as evaluator:
        results = evaluator.optimize(nfe=nfe_selection,
                                     reference=Scenario(**ref_scenario_description),
                                     searchover='levers',
                                     epsilons=epsilon_selection * len(dike_model.outcomes))

    end_time = time.time()
    print('Runtime ended with duration of', str(end_time - start_time))

    results.to_csv("intermediate outputs/optimization output(" +
                   str(nfe_selection) + "," + str(epsilon_selection) + ").csv")

    # visualization in the parallel coordinate plots
    data = results.loc[:, [o.name for o in dike_model.outcomes]] # we are keeping just the columns with the outcomes
    limits = parcoords.get_limits(data) # creates a dataframe where for each outcome it gets the highest and lowest value
    #limits.loc[0, ['utility', 'inertia', 'reliability', 'max_P']] = 0 # sets the lowerbound of each outcome to 0

    paraxes = parcoords.ParallelAxes(limits) # creates the parallel axes
    paraxes.plot(data) # put the data on the axes
    #paraxes.invert_axis('max_P') # flip direction for a particular outcome
    plt.show() # plots
