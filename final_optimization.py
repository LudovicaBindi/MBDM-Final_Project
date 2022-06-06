# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('white')
import platypus

from ema_workbench import (Model, RealParameter, TimeSeriesOutcome,
                           perform_experiments, ema_logging,Policy,MultiprocessingEvaluator,SequentialEvaluator)
from ema_workbench.em_framework.evaluators import BaseEvaluator

from ema_workbench.em_framework.evaluators import Samplers
from ema_workbench.em_framework.points import Scenario

from ema_workbench.analysis import feature_scoring
from ema_workbench.analysis.scenario_discovery_util import RuleInductionType
from ema_workbench.em_framework.salib_samplers import get_SALib_problem


from problem_formulation import get_model_for_problem_formulation


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    
    ema_logging.log_to_stderr(ema_logging.INFO)

    dike_model, planning_steps = get_model_for_problem_formulation(3)
    
    lower_bound_ref_sce = {}
    for uncertainty in dike_model.uncertainties:
        lower_bound_ref_sce[uncertainty.name] = uncertainty.lower_bound
    
    with SequentialEvaluator(dike_model) as evaluator:
        results1 = evaluator.optimize(nfe=5, reference=Scenario(**lower_bound_ref_sce),
                                      searchover='levers',
                                      epsilons=[0.1]*len(dike_model.outcomes))
    
