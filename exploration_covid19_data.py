import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('us-states.csv', index_col=0)

states = list(set(data['state'].values))
print(states)
state_dict = {}
for state in states:
    state_dict[state] = data[data['state'] == state]
    state_dict[state]['velocity_cases'] = state_dict[state]['cases'].diff()
    state_dict[state]['acceleration_cases'] = state_dict[state]['velocity_cases'].diff()

print(state_dict['Alabama'])