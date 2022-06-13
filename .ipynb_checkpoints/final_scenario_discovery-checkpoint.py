#!/usr/bin/env python
# coding: utf-8
# %% [markdown]
#
# #### Perform Scenario Discovery
# ### By performing Scenario Discovery we basically assess the uncertain conditions under which our policies perform poorly.
# ### For that we are going to use the PRIM algorithm.

# %%
import pickle

# %%
outcomes_file = open("intermediate outputs/first evaluation - outcomes description.pkl", "rb")
outcomes = pickle.load(outcomes_file)

# %%
outcomes

# %%
outcomes['A.4_Expected Number of Deaths']

# %%
outcomes.keys()

# %%
#import csv
#with open('intermediate outputs/first evaluation - experiments description.csv', 'r') as file:
#    reader = csv.reader(file)

# %%
import pandas as pd
experiments = pd.read_csv('intermediate outputs/first evaluation - experiments description.csv')

# %%
experiments.head()

# %%
experiments.columns

# %%
from ema_workbench.analysis import prim
from ema_workbench import MultiprocessingEvaluator, ema_logging
ema_logging.log_to_stderr(ema_logging.INFO)


# %% [markdown]
# #use a threshold of 0.1 for number of deaths

# %%
outcomes_prim = []
for i in range(len(outcomes['A.4_Expected Number of Deaths'])):
    if outcomes['A.4_Expected Number of Deaths'][i] > 0.001 and outcomes['A.5_Expected Number of Deaths'][i] > 0.001 :
        outcomes_prim.append(True)
    else:
        outcomes_prim.append(False)
outcomes_prim

# %%
import numpy as np
outcomes_prim = np.asarray(outcomes_prim)

# %%
x = experiments.drop(columns=['0_RfR 0', '0_RfR 1', '0_RfR 2',
       '1_RfR 0', '1_RfR 1', '1_RfR 2', '2_RfR 0', '2_RfR 1', '2_RfR 2',
       '3_RfR 0', '3_RfR 1', '3_RfR 2', '4_RfR 0', '4_RfR 1', '4_RfR 2',
       'EWS_DaysToThreat', 'A.1_DikeIncrease 0', 'A.1_DikeIncrease 1',
       'A.1_DikeIncrease 2', 'A.2_DikeIncrease 0', 'A.2_DikeIncrease 1',
       'A.2_DikeIncrease 2', 'A.3_DikeIncrease 0', 'A.3_DikeIncrease 1',
       'A.3_DikeIncrease 2', 'A.4_DikeIncrease 0', 'A.4_DikeIncrease 1',
       'A.4_DikeIncrease 2', 'A.5_DikeIncrease 0', 'A.5_DikeIncrease 1',
       'A.5_DikeIncrease 2','policy'])
y = outcomes_prim # the code is taken from exercise 8, instead of 'utility' we should use the outcome that is
#y =  outcomes['A.4_Expected Number of Deaths'] > 0.1                               # on our interest and also instead of 0.35 we should define the threshold that suits our case.

prim_alg = prim.Prim(x,y, threshold=0.5) # x is the dataframe with the independent variables, y is the dependent variable,
                                         # and threshold is the density that a box needs to meet 
box = prim_alg.find_box()


# %%
#plot density vs coverage
import matplotlib.pyplot as plt
 
box.show_tradeoff()
plt.show()


# %%
box.inspect_tradeoff()


# %%
box.peeling_trajectory

# %%
box.inspect(36) # the code is taken from assignment 8, the number in the parenthesis is the number of the box we choose
                # this choice has to made by us
box.select(36)
box.inspect(style='graph')
plt.show()


# %%
#--- Save scenarios and outcomes of the box  #the following code is from last year's report about saving the results
scens_in_box = experiments.iloc[box.yi]
outcomes_in_box = {k:v[box.yi] for k,v in outcomes.items()}


# %%
scens_in_box

# %%
outcomes_in_box.items()

# %%
type( outcomes_in_box)

# %%
#save the results
scens_in_box.to_csv('intermediate outputs/prim results - scens in box.csv')
a_file = open("intermediate outputs/prim results - outcomes in box.pkl", "wb")
pickle.dump(outcomes_in_box, a_file)
a_file.close()

