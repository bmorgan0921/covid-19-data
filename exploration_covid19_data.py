import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

data = pd.read_csv('us-states.csv', index_col=0)
data.index = pd.to_datetime(data.index)

states = list(set(data['state'].values))
state_dict = {}
for state in states:
    state_dict[state] = data[data['state'] == state]
    state_dict[state]['velocity_cases'] = state_dict[state]['cases'].diff()
    state_dict[state]['acceleration_cases'] = state_dict[state]['velocity_cases'].diff()


print(state_dict['Illinois'])

# for state in states:
#     plt.plot(state_dict[state]['acceleration_cases'][datetime(2020, 3, 1):], label = state)
# plt.xticks(rotation = 45)
# plt.legend()
# plt.show()