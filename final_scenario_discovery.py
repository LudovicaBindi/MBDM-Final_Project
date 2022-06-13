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


# %% [markdown]
# #use a threshold of 0.1 for number of deaths

# %%
y = []
for i in range(len(outcomes['A.4_Expected Number of Deaths'])):
    if outcomes['A.4_Expected Number of Deaths'][i] < 0.1 and outcomes['A.5_Expected Number of Deaths'][i] < 0.1 :
        y.append(True)
    else:
        y.append(False)
y

# %%
x = experiments.drop(columns=['scenario','policy','model'])
for
y = outcomes['A.4_Expected Number of Deaths'] < 0.1 and outcomes['A.5_Expected Number of Deaths'] < 0.1# the code is taken from exercise 8, instead of 'utility' we should use the outcome that is
                                # on our interest and also instead of 0.35 we should define the threshold that suits our case.

prim_alg = prim.Prim(x,y, threshold=0.5) # x is the dataframe with the independent variables, y is the dependent variable,
                                         # and threshold is the density that a box needs to meet 
box = prim_alg.find_box()


# %%
#plot density vs coverage
import matplotlib.pyplot as plt
 
box1.show_tradeoff()
plt.show()


# %%
box.inspect_tradeoff()


# %%
box.inspect(42) # the code is taken from assignment 8, the number in the parenthesis is the number of the box we choose
                # this choice has to made by us
box.select(42)
box.inspect(style='graph')
plt.show()


# %%


#--- Save scenarios and outcomes of the box  #the following code is from last year's report about saving the results
scens_in_box = experiments.iloc[box.yi]
outcomes_in_box = {k:v[box.yi] for k,v in outcomes.items()}


# %%
from ema_workbench import save_results

save_results((scens_in_box, outcomes_in_box), 'mordm_42.tar.gz')

