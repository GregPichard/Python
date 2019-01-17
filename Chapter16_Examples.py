import pandas as pd
from pandas import plotting

# Example 1 : FRED
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

ax = final[['GDP_growth', 'IP_growth', 'Unemp_rate']].plot(subplots=True)
fig = ax[0].get_figure()
fig.savefig('FRED_data_line_plot.pdf')

ax = pd.plotting.scatter_matrix(final[['GDP_growth', 'IP_growth', 'Unemp_rate']], diagonal = 'kde')
fig = ax[0, 0].get_figure()
fig.savefig('FRED_data_scatter_matrix.pdf')

# Example 2 : NSW (National Supported Work Demonstration)
import numpy as np
from scipy import stats
import seaborn as sns
sns.set()

NSW = pd.read_excel('NSW.xls', 'NSW')
print(NSW.describe())
NSW = NSW.rename(columns = {'Real income After ($)':'Income_after',
                            'Real income Before ($)':'Income_before',
                            'Education (years)':'Education'})
NSW['Minority'] = NSW['Black'] + NSW['Hispanic']

print(NSW.pivot_table(index = 'Treated'))
print(NSW.pivot_table(index = 'Minority'))
print(NSW.pivot_table(index = ['Minority', 'Married']))

ax = NSW[['Income_before', 'Income_after']].plot(kind = 'kde', subplots = True)
fig = ax[0].get_figure()
fig.savefig('NSW_density.pdf')

income_diff = NSW['Income_after'] - NSW['Income_before']
t = income_diff[NSW['Treated']==1]
nt = income_diff[NSW['Treated']==0]
tstat = (t.mean() - nt.mean())/np.sqrt(t.var()/t.count() - nt.var()/nt.count())
pval = 1 - stats.norm.cdf(tstat)
print('T-stat: {0:.2f}, P-val: {1:.3f}'.format(tstat, pval))
