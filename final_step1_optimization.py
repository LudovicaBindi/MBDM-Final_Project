# import needed libraries

# ema_workbench components needed
from ema_workbench import (MultiprocessingEvaluator, Scenario, ema_logging)

# model functions needed
from problem_formulation import get_model_for_problem_formulation

# other libraries needed
import time  # to keep track of the runtime
import warnings
warnings.filterwarnings("ignore")

'''
    In this script we use the e-NSGA2 algorithm to find policies that are optimal for the reference scenario
    that we define here (mainly we take the mean of the range of the uncertainties to create this scenario).
    The solutions found by the algorithm are saved in a csv file for further processing in other scripts
    and notebooks.
'''

_logger = ema_logging.create_module_logger(__name__)

if __name__ == '__main__':
    ema_logging.log_to_stderr((ema_logging.INFO))

    # parameters needed for this optimization
    problem_formulation = 6 # our own problem formulation
    nfe_selection = 100000 # nfe the algorithm will use
    epsilon_selection = [0.1] # epsilon value the algorithm will use

    # we set up the initial reference scenario by using average for the uncertainties
    ref_scenario_description = {}
    for i in [0, 1, 2]:
        ref_scenario_description['discount rate ' + str(i)] = 2.5
    ref_scenario_description['A.0_ID flood wave shape'] = 5 # chosen in ad-hoc manner
    for dike_ring in ['A.1', 'A.2', 'A.3', 'A.4', 'A.5']:
        ref_scenario_description[dike_ring + "_Bmax"] = 190
        ref_scenario_description[dike_ring + "_pfail"] = 0.5
        ref_scenario_description[dike_ring + "_Brate"] = 1.5

    # create the model using this pre-defined and given function
    dike_model, planning_steps = get_model_for_problem_formulation(problem_formulation)

    # print information of starting time on the console
    start_time = time.time()
    _logger.info('Runtime started')

    # run the optimization algorithm
    with MultiprocessingEvaluator(dike_model) as evaluator:
        results = evaluator.optimize(nfe=nfe_selection,
                                     reference=Scenario(**ref_scenario_description),
                                     searchover='levers',
                                     epsilons=epsilon_selection * len(dike_model.outcomes))

    # print information of ending time on the console
    end_time = time.time()
    _logger.info(f'Runtime ended with duration of {end_time - start_time}')

    # save the results on a csv file
    results.to_csv("intermediate outputs/step1 - first optimization output(" +
                   str(nfe_selection) + "," + str(epsilon_selection) + ").csv")
