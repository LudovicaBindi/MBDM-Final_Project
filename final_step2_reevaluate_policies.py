import pandas as pd


import pickle
import time  # to keep track of the runtime

from ema_workbench import Policy, MultiprocessingEvaluator

# model functions needed
from problem_formulation import get_model_for_problem_formulation

if __name__ == '__main__':
    # read the data
    results = pd.read_csv('intermediate outputs/step1 - first optimization output(100000,[0.1]).csv')
    results = results.drop(columns=['Unnamed: 0'])  # cleaning

    # create the dike_model
    problem_formulation = 6 # WARNING: use the same PF as the ones that you used to create the results csv file!
    dike_model, planning_steps = get_model_for_problem_formulation(problem_formulation)

    # select the columns to keep (the ones with the levers)
    to_drop = []
    for column in results.columns:
        to_drop.append(column)
    for o in dike_model.levers:
        to_drop.remove(o.name)

    # select some policies
    # logical = results['A.1_DikeIncrease 1'] < 4
    # policies = results[logical]
    policies = results  # keep everything
    policies = policies.drop([column for column in to_drop], axis=1);

    # prepare the policies for the experiments
    policies_to_evaluate = []
    for i, policy in policies.iterrows():
        policies_to_evaluate.append(Policy(str(i), **policy.to_dict()))

    start_time = time.time()
    print('Runtime started')

    # run the experiments
    n_scenarios = 100
    with MultiprocessingEvaluator(dike_model) as evaluator:
        experiments, outcomes = evaluator.perform_experiments(n_scenarios,
                                                policies_to_evaluate)

    end_time = time.time()
    print('Runtime ended with duration of', str(end_time - start_time))

    # save the experiments as a csv file
    experiments.to_csv("intermediate outputs/step2 - first re-evaluation - experiments description.csv")

    # save the outcomes to a pickle file (outcomes is a dictionary)
    a_file = open("intermediate outputs/step2 - first re-evaluation - outcomes description.pkl", "wb")
    pickle.dump(outcomes, a_file)
    a_file.close()
    # to read back our dictionary: https://www.adamsmith.haus/python/answers/how-to-save-a-dictionary-to-a-file-in-python
