#!/usr/bin/env python
# coding: utf-8
# %% [markdown]
#
# Scenario Discovery

# %%
import pickle
# read the outcomes of the previous policy re-evaluation (step2)

outcomes_file = open("intermediate outputs/step2 - first re-evaluation - outcomes description.pkl", "rb")

outcomes = pickle.load(outcomes_file) # outcomes is a dictionary

# %%
# read the experiments' results from the previous policy re-evaluation (step2)
import pandas as pd

experiments = pd.read_csv('intermediate outputs/step2 - first re-evaluation - experiments description.csv')

# %%
from ema_workbench.analysis import prim
from ema_workbench import MultiprocessingEvaluator, ema_logging

ema_logging.log_to_stderr(ema_logging.INFO)


# %%
outcomes_prim = []
for i in range(len(outcomes['A.4_Expected Number of Deaths'])):
    if outcomes['A.4_Expected Number of Deaths'][i] > 0.001 and outcomes['A.5_Expected Number of Deaths'][i] > 0.001 :
        outcomes_prim.append(True)
    else:
        outcomes_prim.append(False)
outcomes_prim

# %%
count = 0
for i in outcomes_prim:
    if i is True:
        count =+ 1
        
print((count/len(outcomes_prim)*100))

# %%
import numpy as np
outcomes_prim = np.asarray(outcomes_prim) #convert into an array

# %%
# run the PRIM algorithm
x = experiments.drop(columns=['0_RfR 0', '0_RfR 1', '0_RfR 2',
       '1_RfR 0', '1_RfR 1', '1_RfR 2', '2_RfR 0', '2_RfR 1', '2_RfR 2',
       '3_RfR 0', '3_RfR 1', '3_RfR 2', '4_RfR 0', '4_RfR 1', '4_RfR 2',
       'EWS_DaysToThreat', 'A.1_DikeIncrease 0', 'A.1_DikeIncrease 1',
       'A.1_DikeIncrease 2', 'A.2_DikeIncrease 0', 'A.2_DikeIncrease 1',
       'A.2_DikeIncrease 2', 'A.3_DikeIncrease 0', 'A.3_DikeIncrease 1',
       'A.3_DikeIncrease 2', 'A.4_DikeIncrease 0', 'A.4_DikeIncrease 1',
       'A.4_DikeIncrease 2', 'A.5_DikeIncrease 0', 'A.5_DikeIncrease 1',
       'A.5_DikeIncrease 2','policy'])
y = outcomes_prim 
prim_alg = prim.Prim(x,y, threshold=0.5) 
                                         
box = prim_alg.find_box()


# %%
x

# %%
#plot density vs coverage
import matplotlib.pyplot as plt
 
box.show_tradeoff()
plt.show()


# %%
box.peeling_trajectory #investigating the coverage and density values for all boxes

# %%
#explore the characteristics of the chosen box
box.inspect(36) 
box.select(36)
box.inspect(style='graph')
plt.show()


# %%
#Save the results
scens_in_box = experiments.iloc[box.yi]
outcomes_in_box = {k:v[box.yi] for k,v in outcomes.items()}


# %%
#save the results
scens_in_box.to_csv('intermediate outputs/step4 - prim results - scens in box.csv')
a_file = open("intermediate outputs/step4 - prim results - outcomes in box.pkl", "wb")
pickle.dump(outcomes_in_box, a_file)
a_file.close()


# %%
#identify the worst-case scenario

from ema_workbench.analysis import parcoords


data = pd.DataFrame({k:v[y] for k,v in outcomes.items()})
all_data = pd.DataFrame({k:v for k,v in outcomes.items()})

selected_data = all_data[['A.4_Expected Number of Deaths','A.5_Expected Number of Deaths','Other.Dikes_Expected Number of Deaths']]

limits = parcoords.get_limits(selected_data)
plt.rcParams["figure.figsize"] = (15,7)
axes = parcoords.ParallelAxes(limits)
axes.plot(all_data, color='lightgrey')
axes.plot(data, color='blue')

plt.show()

# %%
# print the indices of the scenarios in which the death numbers of dikes 4 and 5 as well as of the rest dikes are the maximum
# and the minimum respectively
print(selected_data.idxmax())
print(selected_data.idxmin())

# %%
# keep only the uncertainty columns
selected = experiments.loc[[887,2476,863], ['A.0_ID flood wave shape', 'A.1_Bmax', 'A.1_Brate',
       'A.1_pfail', 'A.2_Bmax', 'A.2_Brate', 'A.2_pfail', 'A.3_Bmax',
       'A.3_Brate', 'A.3_pfail', 'A.4_Bmax', 'A.4_Brate', 'A.4_pfail',
       'A.5_Bmax', 'A.5_Brate', 'A.5_pfail', 'discount rate 0',
       'discount rate 1', 'discount rate 2']]
selected

# %%
# save the results 
selected.to_csv('intermediate outputs/step4 - prim results - worst case scenarios.csv')
