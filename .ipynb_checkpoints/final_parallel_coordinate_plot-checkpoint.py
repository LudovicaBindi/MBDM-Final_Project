from ema_workbench.analysis import parcoords

import pandas as pd

# read the data
results = pd.read_csv('intermediate outputs/optimization output(5,[0-Copy1.1]).csv')

dike_model, planning_steps = get_model_for_problem_formulation(3)

# visualization in the parallel coordinate plots
data = results.loc[:, [o.name for o in dike_model.outcomes]] # we are keeping just the columns with the outcomes
limits = parcoords.get_limits(data) # creates a dataframe where for each outcome it gets the highest and lowest value
#limits.loc[0, ['utility', 'inertia', 'reliability', 'max_P']] = 0 # sets the lowerbound of each outcome to 0

paraxes = parcoords.ParallelAxes(limits) # creates the parallel axes
paraxes.plot(data) # put the data on the axes
#paraxes.invert_axis('max_P') # flip direction for a particular outcome
plt.show() # plots