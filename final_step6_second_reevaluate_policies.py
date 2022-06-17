# import needed libraries

# ema_workbench components needed
from ema_workbench import Policy, MultiprocessingEvaluator
from ema_workbench import ema_logging

# model functions needed
from problem_formulation import get_model_for_problem_formulation

# other libraries needed
import numpy as np # to carry out selection of policies
import pandas as pd # to read csv and manipulated dataframes
import time # to keep track of the runtime
import pickle # to save dictionaries

'''
    After having optimized based on the worst-case scenarios, we continue with the re-evaluation of the policies. We proceed
    in the same way as we did in step 2: we sample 100 scenarios and we evaluate the policies under these scenarios. The
    results are saved in csv file for further analysis.
'''

if __name__ == '__main__':
    # read the results of the optimization (step5)
    results = []
    for i in range(3):
        read_results = pd.read_csv("intermediate outputs/step5 - multi scenario optimization results/step5 - " + str(i) + " optimization results.csv")
        results.append(read_results)

    # concatenate the results in a Dataframe
    tpm = pd.concat([results[0], results[1]])
    tpm = pd.concat([tpm, results[2]])

    # to reduce the policies, we define a threshold and keep only the ones that satisfy such threshold. The threshold was defined through
    # trial and error so that we were to reduce the policies significantly
    logical = (tpm['A.4_Expected Number of Deaths'] < 0.01) &  (tpm['A.5_Expected Number of Deaths'] < 0.01) &  (tpm['Other.Dikes_Expected Number of Deaths'] < 0.01)
    selected = tpm[logical]

    # since we saw that the policies were still too many, to further reduce the number of policies we introduce an additional threshold
    # we use percentiles to reduce the policies
    selected['Dike 4 & 5 - Total deaths'] = selected["A.4_Expected Number of Deaths"] + selected["A.5_Expected Number of Deaths"] # we sum up the values so that
    # not to have to choose of the dike to work with it first
    perc = np.percentile(selected['Dike 4 & 5 - Total deaths'], 25)

    # keep the final policies after the reduction
    final_results = []
    for result in results:
        result['Dike 4 & 5 - Total deaths'] = result["A.4_Expected Number of Deaths"] + result["A.5_Expected Number of Deaths"]
        logical = (result['Dike 4 & 5 - Total deaths'] < perc) & (result['Other.Dikes_Expected Number of Deaths'] < 0.01)
        final_results.append(result[logical])

    # create the dike_model
    problem_formulation = 6 # WARNING: use the same PF as the ones that you used to create the results csv file!
    dike_model, planning_steps = get_model_for_problem_formulation(problem_formulation)

    # get the policies from the optimization results and convert them in ema_workbench.Policy to be used to perform the experiments
    policies = []
    to_drop = []
    for i, result in enumerate(final_results):
        # from the result dataframe keep only the levers
        for column in final_results[i].columns:
                to_drop.append(column)
        for o in dike_model.levers:
                to_drop.remove(o.name)

        result = result.drop([column for column in to_drop], axis=1);
        for j, row in result.iterrows():
                policy = Policy(f'scenario {i} option {j}', **row.to_dict())
                policies.append(policy)

    # perform the re-evaluation

    # print information of starting time on the console
    start_time = time.time()
    print('Runtime started')

    ema_logging.log_to_stderr(ema_logging.INFO)

    # run the re-evaluation algorithm
    with MultiprocessingEvaluator(dike_model) as evaluator:
        experiments,outcomes = evaluator.perform_experiments(100, policies=policies)

    # print information of ending time on the console
    end_time = time.time()
    print('Runtime ended with duration of', str(end_time - start_time))

    #save the results
    experiments.to_csv("intermediate outputs/step6 - second re-evaluation - experiments description.csv")

    # save the outcomes to a pickle file (outcomes is a dictionary)
    a_file = open("intermediate outputs/step6 - second re-evaluation - outcomes description.pkl", "wb")
    pickle.dump(outcomes, a_file)
    a_file.close()



