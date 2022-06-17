# import needed libraries

# ema_workbench components needed
from ema_workbench import Policy, MultiprocessingEvaluator

# model functions needed
from problem_formulation import get_model_for_problem_formulation

# other libraries needed
import pandas as pd # to deal with csv files
import pickle # to save dictionaries
import time  # to keep track of the runtime

'''
    In this script we re-evaluate the policies found in the previous step (optimization under the reference scenario).
    We sample 100 scenarios and we evaluate the policies under each of these scenarios. The results are saved in a
    csv file for further analysis.
'''

if __name__ == '__main__':

    # read the policies found via the first optimization
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

    # select some policies. In our case we saw that the policies we got our a small enough number and cause low enough
    # number of deaths in our reference scenario that are in line with our client's values
    # logical = results['A.4_Expected Number of Deaths'] < 0.0012
    # policies = results[logical]
    policies = results  # keep everything
    policies = policies.drop([column for column in to_drop], axis=1);

    # prepare the policies for the experiments
    policies_to_evaluate = []
    for i, policy in policies.iterrows():
        policies_to_evaluate.append(Policy(str(i), **policy.to_dict()))

    # print information of starting time on the console
    start_time = time.time()
    print('Runtime started')

    # run the experiments: each policy will be evaluated in all the sampled scenarios
    n_scenarios = 100 # number of scenarios that will be sampled
    with MultiprocessingEvaluator(dike_model) as evaluator:
        experiments, outcomes = evaluator.perform_experiments(n_scenarios,
                                                policies_to_evaluate)

    # print information of ending time on the console
    end_time = time.time()
    print('Runtime ended with duration of', str(end_time - start_time))

    # save the experiments as a csv file
    experiments.to_csv("intermediate outputs/step2 - first re-evaluation - experiments description.csv")

    # save the outcomes to a pickle file (outcomes is a dictionary)
    a_file = open("intermediate outputs/step2 - first re-evaluation - outcomes description.pkl", "wb")
    pickle.dump(outcomes, a_file)
    a_file.close()
    # to read back our dictionary: https://www.adamsmith.haus/python/answers/how-to-save-a-dictionary-to-a-file-in-python
