from ema_workbench import (Model, RealParameter, TimeSeriesOutcome,
                           perform_experiments, ema_logging,Policy,MultiprocessingEvaluator,SequentialEvaluator)

from problem_formulation import get_model_for_problem_formulation

# setting up the model as usual
ema_logging.log_to_stderr(ema_logging.INFO)

model, planning_steps = get_model_for_problem_formulation(2)

with SequentialEvaluator(model) as evaluator:
    results1 = evaluator.optimize(nfe=2, searchover='levers',
                                 epsilons=[0.1,]*len(model.outcomes))