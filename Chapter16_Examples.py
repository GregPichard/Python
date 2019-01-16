import pandas as pd
from pandas import plotting
#import tables

codes = ['GDPC1', 'INDPRO', 'CPILFESL', 'UNRATE', 'GS10', 'GS1', 'BAA', 'AAA']
names = ['Real GDP', 'Industrial production', 'Core CPI', 'Unemployment rate', '10 Year Yield', '1 Year Yield', 'Baa Yield', 'Aaa Yield']
base_url = r'https://fred.stlouisfed.org/graph/fredgraph.csv?id={code}'

data = []
for code in codes:
    print(code)
    url = base_url.format(code=code)
    data.append(pd.read_csv(url))

time_series = {}
for code, d in zip(codes, data):
    d.index = d.DATE
    time_series[code] = d[code]
merged_data = pd.DataFrame(time_series)
print(merged_data)

term_premium = merged_data['GS10'] - merged_data['GS1']
term_premium.name = 'Term'
merged_data = merged_data.join(term_premium, how='outer')
default_premium = merged_data['BAA'] - merged_data['AAA']
default_premium.name = 'Default'
merged_data = merged_data.join(default_premium, how = 'outer')
merged_data = merged_data.drop(['AAA','BAA','GS10', 'GS1'], axis = 1)
print(merged_data.tail())

quarterly = merged_data.dropna()
print(quarterly.tail())

growth_rates_selector = ['GDPC1', 'INDPRO', 'CPILFESL']
growth_rates = 100 * quarterly[growth_rates_selector].pct_change()
final = quarterly.drop(growth_rates_selector, axis = 1).join(growth_rates)
new_names = {'GDPC1':'GDP_growth', 'INDPRO':'IP_growth', 'CPILFESL':'Core inflation', 'UNRATE':'Unemp_rate'}
final = final.rename(columns = new_names).dropna()
print(final)
final.to_hdf('FRED_data.h5', 'FRED', complevel = 6, complib = 'zlib')
final.to_excel('FRED_data.xlsx')

ax = final[['GDP_growth', 'Ind_prod_growth', 'Unemp_rate']].plot(subplots=True)
fig = ax[0].get_figure()
fig.savefig('FRED_data_line_plot.pdf')

ax = scatter_matrix(final[['GDP_growth', 'Ind_prod_growth', 'Unemp_rate']], diagonal = 'kde')
fig = ax[0, 0].get_figure()
fig.savefig('FRED_data_scatter_matrix.pdf')
