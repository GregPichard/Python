# Exercise 1
import numpy as np
import matplotlib as mpl
from matplotlib import pylab
import seaborn as sns
sns.set()
import pandas as pd
import datetime as dt
import calendar
SP500 = pd.read_csv('C:/Users/gpichard/Desktop/PythonTuto/GSPC.csv', parse_dates=['Date'])

mpl.pyplot.plot_date(SP500.loc[:,"Date"], SP500.loc[:,"Close"],'-r', label = 'S&P 500 Close')
mpl.pyplot.autoscale(tight='x')
mpl.pyplot.tight_layout()
mpl.pyplot.legend()
mpl.pyplot.title('S&P 500 Index History')

# Exercise 2
SP500.loc[:,'Date'] = pd.to_datetime(SP500.loc[:,'Date'])
SP500 = SP500.assign(Weekday = pd.Series(SP500["Date"]).values)
for d in SP500["Date"].index:
    SP500.loc[d, "Weekday"] = dt.datetime.weekday(SP500.loc[d, "Date"])
    SP500.loc[d, "WeekdayName"] = calendar.day_name[SP500.loc[d,  "Weekday"]]
SP500_Fri = SP500[SP500["Weekday"]==4]
SP500_Fri = SP500_Fri.assign(LogClose = pd.Series(np.log(SP500_Fri["Close"])))
SP500_Fri = SP500_Fri.assign(DLogClose = pd.Series(SP500_Fri["LogClose"]).values)
SP500_Fri["DLogClose"] = SP500_Fri["LogClose"].diff()

    
SP500_Fri.loc[min(SP500_Fri["DLogClose"].index), "DLogClose"] = 0.0
sns.set()
fig = mpl.pyplot.figure()
i = 1
for b in np.array(['auto', 'sturges', 'doane', 'sqrt', 'scott', 'rice']):
    ax = fig.add_subplot(3, 2, i)
    mpl.pyplot.hist(SP500_Fri["DLogClose"], bins = b)
    ax.set_title(b)
    i+=1
mpl.pyplot.autoscale(tight='x')
mpl.pyplot.tight_layout()
mpl.pyplot.draw()

# Exercise 3
boundaries = [-0.02, 0, 0.02, 10]
sample_elements = np.zeros(len(boundaries))
for d in SP500_Fri.index:
    for i, b in enumerate(boundaries):
        if SP500_Fri.loc[d,"DLogClose"] <= b:
            sample_elements[i] += 1
            break
sample_elements
percentages = sample_elements/np.sum(sample_elements)
percentages
colors = sns.light_palette("red", 6 , reverse=False)
labels = ['r < 2%','-2% < r <= 0%','0% < r <= 2%','r > 2%']
mpl.pyplot.pie(percentages, colors = colors, labels = labels, autopct = '%2.0f')
mpl.pyplot.autoscale(tight='x')
mpl.pyplot.tight_layout()

# Exercise 4
FTSE = pd.read_csv('C:/Users/gpichard/Desktop/PythonTuto/FTSE.csv', parse_dates=['Timestamp'], skiprows = 1,  usecols=['Timestamp', 'Close Price'])
FTSE = FTSE.assign(Date = pd.to_datetime(FTSE['Timestamp']))
FTSE['Date'] = [dt.datetime.date(d) for d in FTSE['Timestamp']]# extracting date from timestamp

mpl.pyplot.plot_date(FTSE.loc[:,"Date"], FTSE.loc[:,"Close Price"],'-r', label = 'FTSE 100 Close')
mpl.pyplot.autoscale(tight='x')
mpl.pyplot.tight_layout()
mpl.pyplot.legend()
mpl.pyplot.title('FTSE 100 Index History')

FTSE = FTSE.assign(Weekday = pd.Series(FTSE["Timestamp"]).values)
for d in FTSE["Date"].index:
    FTSE.loc[d, "Weekday"] = dt.datetime.weekday(FTSE.loc[d, "Date"])
    FTSE.loc[d, "WeekdayName"] = calendar.day_name[FTSE.loc[d,  "Weekday"]]
FTSE_Fri = FTSE[FTSE["Weekday"]==4]
FTSE_Fri = FTSE_Fri.assign(LogClose = pd.Series(np.log(FTSE_Fri["Close Price"])))
FTSE_Fri = FTSE_Fri.assign(DLogClose = pd.Series(FTSE_Fri["LogClose"]).values)
FTSE_Fri["DLogClose"] = FTSE_Fri["LogClose"].diff()
FTSE_Fri.loc[min(FTSE_Fri["DLogClose"].index), "DLogClose"] = 0.0

CommonDates, FTSE_ind, SP500_ind = np.intersect1d(mpl.dates.date2num(FTSE_Fri['Date']),mpl.dates.date2num(SP500_Fri['Date']), return_indices=True)
CommonDates = mpl.dates.num2date(CommonDates, tz=None)
CommonDates = [CommonDates[i].replace(tzinfo=None) for i,d in enumerate(CommonDates)]

mpl.pyplot.scatter(SP500_Fri['DLogClose'].iloc[SP500_ind], FTSE_Fri['DLogClose'].iloc[FTSE_ind] )
mpl.pyplot.autoscale(tight='x')
mpl.pyplot.tight_layout()

# Exercise 5 - Linear fit
SP500_CommonWRet = SP500_Fri['DLogClose'].iloc[SP500_ind]
SP500_CommonWRet.name = 'S&P 500 Weekly returns'
FTSE_CommonWRet = FTSE_Fri['DLogClose'].iloc[FTSE_ind]
FTSE_CommonWRet.name = 'FTSE 100 Weekly returns'

ax = sns.regplot(SP500_CommonWRet, FTSE_CommonWRet, ci = None,  line_kws={"color": "red"})

# Exercise 6 - EWMA
lambda_ = 0.97
    