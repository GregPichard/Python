import numpy as np
import pandas as pd
# Exercise 1
data = pd.read_excel('exercise3.xlsx', 'table (5)')
data = data.values

dates = data[:,0]
SP500 = np.array(data[:,2])
XOM = np.array(data[:,3])
neg_SP500 = sum(SP500 < 0)
neg_XOM = sum(XOM < 0)
print('SP500:', neg_SP500)
print('XOM:', neg_XOM)

# Exercise 2
std_SP500 = np.std(SP500)
std_XOM = np.std(XOM)

SP500_minus2sigma = SP500 < -2*std_SP500
SP500_plus2sigma = SP500 > 2*std_SP500
XOM_minus2sigma = XOM < -2*std_XOM
XOM_plus2sigma = XOM > 2*std_XOM
print(np.mean(SP500[SP500_minus2sigma]))
print(np.mean(SP500[SP500_plus2sigma]))
print(np.mean(XOM[XOM_minus2sigma]))
print(np.mean(XOM[XOM_plus2sigma]))

# Exercise 3
neg_both = np.logical_and(SP500 < 0,XOM < 0)
#returns = np.vstack((SP500, XOM)).T
#corr_neg_both = np.corrcoef(returns[neg_both, :])
#print(corr_neg_both)
#print(np.corrcoef(SP500, XOM, rowvar=False))
print(np.shape(SP500))
print(np.shape(XOM))
print(np.corrcoef(SP500.T,XOM.T))
