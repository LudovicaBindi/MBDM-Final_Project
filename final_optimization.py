# This is a sample Python script.
# other libraries needed
import time  # to keep track of the runtime
import warnings

warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd

# ema_workbench components needed
from ema_workbench import (MultiprocessingEvaluator, Scenario, ema_logging)

# model functions needed
from problem_formulation import get_model_for_problem_formulation


_logger = ema_logging.create_module_logger(__name__)

if __name__ == '__main__':
    ema_logging.log_to_stderr((ema_logging.INFO))

    problem_formulation = 6
    nfe_selection = 100000
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

    start_time = time.time()
    _logger.info('Runtime started')
    with MultiprocessingEvaluator(dike_model) as evaluator:
        results = evaluator.optimize(nfe=nfe_selection,
                                     reference=Scenario(**ref_scenario_description),
                                     searchover='levers',
                                     epsilons=epsilon_selection * len(dike_model.outcomes))

    end_time = time.time()
    _logger.info(f'Runtime ended with duration of {end_time - start_time}')

    results.to_csv("intermediate outputs/optimization output(" +
                   str(nfe_selection) + "," + str(epsilon_selection) + ") - lUDO.csv")
