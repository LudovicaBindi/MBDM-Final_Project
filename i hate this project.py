from ema_workbench import (Model, RealParameter, TimeSeriesOutcome,
                           perform_experiments, ema_logging,Policy,MultiprocessingEvaluator,SequentialEvaluator)
from ema_workbench.em_framework.points import Scenario

from problem_formulation import get_model_for_problem_formulation

# setting up the model as usual
if __name__ == '__main__':

    dike_model, planning_steps = get_model_for_problem_formulation(3)

    lower_bound_ref_sce = {}
    for uncertainty in dike_model.uncertainties:
        lower_bound_ref_sce[uncertainty.name] = uncertainty.lower_bound

    ema_logging.log_to_stderr(ema_logging.INFO)

    with MultiprocessingEvaluator(dike_model) as evaluator:
        results1 = evaluator.optimize(nfe=5, reference=Scenario(**lower_bound_ref_sce),
                                      searchover='levers',
                                      epsilons=[0.1,]*len(dike_model.outcomes))