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


# print(state_dict['Illinois'])

# for state in states:
#     plt.plot(state_dict[state]['acceleration_cases'][datetime(2020, 3, 1):], label = state)
# plt.xticks(rotation = 45)
# plt.legend()
# plt.show()

county_data = pd.read_csv('co-est2019-alldata.csv', encoding='latin-1')
county_data = county_data.filter(['SUMLEV', 'REGION', 'DIVISION', 'STATE', 'COUNTY', 'STNAME', 'CTYNAME', 'POPESTIMATE2019'])

state_data = county_data.filter(['STNAME', 'CTYNAME', 'POPESTIMATE2019'])
state_population_df = state_data[state_data['CTYNAME'] == state_data['STNAME']].drop('CTYNAME', axis = 1).drop_duplicates(keep = 'first')

state_filter = county_data.filter(['STATE', 'STNAME'])
state_code_dict = {row['STNAME']:row['STATE'] for index, row in state_filter.iterrows()}

keys_not_in_state_code_dict = [key for key in state_dict.keys() if key not in state_code_dict.keys()]

state_population_df.rename(columns = {"STNAME":"state", 'POPESTIMATE2019':'population_estimate_2019'}, inplace = True)
state_population_df.set_index('state', inplace = True)

state_analysis_df = pd.DataFrame(data.groupby('state')['cases', 'deaths'].max())
state_analysis_df.drop(keys_not_in_state_code_dict, inplace = True)


analysis_df = pd.concat([state_analysis_df, state_population_df], axis = 1 )

analysis_df['pct_of_state_population'] = analysis_df['cases'] / analysis_df['population_estimate_2019']
analysis_df['pct_of_total_population'] = analysis_df['population_estimate_2019'] / analysis_df['population_estimate_2019'].sum()
# analysis_df['above_average_pct'] = [1.0 if x > analysis_df['pct_of_state_population'].mean() else 0.0 for x in analysis_df['pct_of_state_population'].values]
# analysis_df['above_average_pop'] = [1.0 if x > analysis_df['population_estimate_2019'].mean() else 0.0 for x in analysis_df['population_estimate_2019'].values]
analysis_df['deaths_percentage_of_state_cases'] = analysis_df['deaths'] / analysis_df['cases']
analysis_df['state_deaths_percentage_of_total_deaths'] = analysis_df['deaths'] / analysis_df['deaths'].sum()
print(analysis_df['deaths'].sum())