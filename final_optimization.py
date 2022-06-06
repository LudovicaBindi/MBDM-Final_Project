# This is a sample Python script.

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('white')
import platypus

from ema_workbench import (Model, RealParameter, TimeSeriesOutcome,
                           perform_experiments, Policy,
                           MultiprocessingEvaluator)
from ema_workbench.em_framework.evaluators import BaseEvaluator

from ema_workbench.em_framework.evaluators import Samplers
from ema_workbench.em_framework.points import Scenario

from ema_workbench.analysis import feature_scoring
from ema_workbench.analysis.scenario_discovery_util import RuleInductionType
from ema_workbench.em_framework.salib_samplers import get_SALib_problem

from problem_formulation import get_model_for_problem_formulation

# other libraries needed
import pandas as pd
import time  # to keep track of the runtime

if __name__ == '__main__':

    start_time = time.time()
    print('Runtime started')

    problem_formulation = 6
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
