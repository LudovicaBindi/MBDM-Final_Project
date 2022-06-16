# import libraries
from ema_workbench import MultiprocessingEvaluator, ema_logging
from ema_workbench import Scenario

from problem_formulation import get_model_for_problem_formulation

import pandas as pd
if __name__ == '__main__':
    # reading the scenarios
    selected = pd.read_csv("intermediate outputs/step4 - prim results - worst case scenarios.csv")
    scenarios = [Scenario(f"{index}", **row) for index, row in selected.iterrows()]

    # create the model
    dike_model, planning_steps = get_model_for_problem_formulation(6)

    ema_logging.log_to_stderr(ema_logging.INFO)

    def optimize(scenario, nfe, model, epsilons):

        with MultiprocessingEvaluator(model) as evaluator:
            results = evaluator.optimize(nfe=nfe, searchover='levers',
                                         epsilons=epsilons,
                                         reference=scenario)
        return results


    results = []
    for scenario in scenarios:

        epsilons = [0.1, ] * len(dike_model.outcomes)

        res = optimize(scenario, 100000, dike_model, epsilons)

        res.to_csv("intermediate outputs/step5 - multi scenario optimization results/" + str(scenario.name) + " optimization results.csv")

        results.append(res)
