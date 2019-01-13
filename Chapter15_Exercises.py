# Exercise 1
import numpy as np
import matplotlib as mpl
from matplotlib import pylab
import pandas as pd
SP500 = pd.read_csv('^GSPC.csv')


mpl.pylab.plot_date(SP500['Date'], SP500['Close'])
