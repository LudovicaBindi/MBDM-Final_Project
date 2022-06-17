
# Re-evalute the policies after the optimization of the worst-case scenarios

import numpy as np
if __name__ == '__main__':
    import pandas as pd

'''
    After having optimized based on the worst-case scenarios we continue with the re-evaluation of the policies.
'''

# read the results of the optimization(step5)
results = []
for i in range(3):
    read_results= pd.read_csv("intermediate outputs/step5 - multi scenario optimization results/step5 - " + str(i) + " optimization results.csv")
    results.append(read_results)


# concatenate the results in a Dataframe
tpm = pd.concat([results[0], results[1]])
tpm = pd.concat([tpm, results[2]])
#tpm



logical = (tpm['A.4_Expected Number of Deaths'] < 0.01) &  (tpm['A.5_Expected Number of Deaths'] < 0.01) &  (tpm['Other.Dikes_Expected Number of Deaths'] < 0.01)
res = np.sum(logical) / len(tpm)
print(res * 100)
print(np.sum(logical))


# to reduce the policies keep only the ones that satisfy the defined thresholds
selected = tpm[logical]


# to further reduce the number of policies we introduce an additional threshold
selected['Dike 4 & 5 - Total deaths'] = selected["A.4_Expected Number of Deaths"] + selected["A.5_Expected Number of Deaths"]

for q in [25, 50, 75]:
    logical = selected['Dike 4 & 5 - Total deaths'] < np.percentile(selected['Dike 4 & 5 - Total deaths'], q)
    print(f'Policies kept: {np.sum(logical)}')
    print(f'% Policies kept: {np.sum(logical)/len(results) * 100}')
    print()


logical = selected['Dike 4 & 5 - Total deaths'] < np.percentile(selected['Dike 4 & 5 - Total deaths'], q)

#perc = np.percentile(selected['Dike 4 & 5 - Total deaths'], 25)
#perc


# count the number of policies that satisfy the defined thresholds
count = 0
for result in results:
    result['Dike 4 & 5 - Total deaths'] = result["A.4_Expected Number of Deaths"] + result["A.5_Expected Number of Deaths"]
    logical = (result['Dike 4 & 5 - Total deaths'] < perc) &  (result['Other.Dikes_Expected Number of Deaths'] < 0.01)
    count += np.sum(logical)
print(count)


# keep the final policies after the reduction
final_results=[]
for result in results:
    result['Dike 4 & 5 - Total deaths'] = result["A.4_Expected Number of Deaths"] + result["A.5_Expected Number of Deaths"]
    logical = (result['Dike 4 & 5 - Total deaths'] < perc) &  (result['Other.Dikes_Expected Number of Deaths'] < 0.01)
    final_results.append(result[logical])



#len(final_results[0]) + len(final_results[2]) + len(final_results[1])



from ema_workbench import Policy, MultiprocessingEvaluator
from problem_formulation import get_model_for_problem_formulation

# create the dike_model
problem_formulation = 6 # WARNING: use the same PF as the ones that you used to create the results csv file!
dike_model, planning_steps = get_model_for_problem_formulation(problem_formulation)


policies = []
to_drop = []

for i, result in enumerate(final_results):
    for column in final_results[i].columns:  #keep only the levers
            to_drop.append(column)
    for o in dike_model.levers:
            to_drop.remove(o.name)

    result = result.drop([column for column in to_drop], axis=1);
    for j, row in result.iterrows():
            policy = Policy(f'scenario {i} option {j}', **row.to_dict())
            policies.append(policy)



#len(policies)


#perform the re-evaluation
import time, pickle
## print information of starting time on the console
start_time = time.time()
print('Runtime started')

from ema_workbench import ema_logging
ema_logging.log_to_stderr(ema_logging.INFO)
#run the re-evaluation algorithm
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



