from ema_workbench.analysis import parcoords

from problem_formulation import get_model_for_problem_formulation

import pandas as pd
import matplotlib.pyplot as plt

# read the data
results = pd.read_csv('intermediate outputs/optimization output(5000,[0.1]).csv')

dike_model, planning_steps = get_model_for_problem_formulation(6)

# visualization in the parallel coordinate plots

# we are keeping just the columns with the outcomes or a part of these outcomes
#data = results.loc[:, [o.name for o in dike_model.outcomes]] # all the outcomes
data = results.loc[:, [o for o in ["A.1 Total Costs", "A.2 Total Costs", "A.3 Total Costs"]]]
limits = parcoords.get_limits(data) # creates a dataframe where for each outcome it gets the highest and lowest value
#limits.loc[0, ['utility', 'inertia', 'reliability', 'max_P']] = 0 # sets the lowerbound of each outcome to 0

paraxes = parcoords.ParallelAxes(limits) # creates the parallel axes
paraxes.plot(data) # put the data on the axes
#paraxes.invert_axis('max_P') # flip direction for a particular outcome

# save figure

# if you wanna play with the size of the picture
#figure = plt.gcf()
#figure.set_size_inches(15, 25)

plt.savefig("sample.png", dpi=100) # dpi is the resolution

plt.savefig('output pictures/results first optimization - prova.png')

plt.show() # plots

