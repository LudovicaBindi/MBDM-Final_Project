# This is a sample Python script.
# other libraries needed
import time  # to keep track of the runtime
import warnings

warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd

# ema_workbench components needed
from ema_workbench import (MultiprocessingEvaluator, Scenario, ema_logging)
from ema_workbench.em_framework.optimization import (HyperVolume,
                                                     EpsilonProgress)

# model functions needed
from problem_formulation import get_model_for_problem_formulation


_logger = ema_logging.create_module_logger(__name__)

if __name__ == '__main__':
    ema_logging.log_to_stderr((ema_logging.INFO))

    problem_formulation = 6
    nfe_selection = 3
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

    convergence_metrics = [HyperVolume.from_outcomes(dike_model.outcomes),
                           EpsilonProgress()]

    start_time = time.time()
    _logger.info('Runtime started')

    with MultiprocessingEvaluator(dike_model) as evaluator:
        results, convergence = evaluator.optimize(nfe=nfe_selection, searchover='levers',
                                                  reference=Scenario(**ref_scenario_description),
                                                  epsilons=[0.125, 0.05, 0.01, 0.01],
                                                  convergence=convergence_metrics)

    end_time = time.time()
    _logger.info(f'Runtime ended with duration of {end_time - start_time}')

    print(type(results))
    print(type(convergence))

    results.to_csv("intermediate outputs/optimization + convergence - results.csv")
    convergence.to_csv("intermediate outputs/optimization + convergence - convergence res.csv")
