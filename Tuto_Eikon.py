import numpy
import pandas
import eikon
eikon.set_app_key('638fa3bbb90349d5a97dc60c1c0cc4b0b5646846')
eikon.get_news_headlines('R:LHAG.DE', date_from='2018-01-01T00:00:00', date_to='2018-12-13T18:00:00')

#df = eikon.get_timeseries("SPY",
 #       ['TR.IndexConstituentRIC',
  #          'TR.IndexConstituentName',
   #         'TR.IndexConstituentWeightPercent'],


data_grid, err = eikon.get_data("SPY",
	['TR.IndexConstituentRIC',
	{'TR.IndexConstituentWeightPercent':{'sort_dir':'desc'}}],
	{'SDate':'2018-12-14'}
	)
print(data_grid)
weight = data_grid.loc[:, "Weight percent"]
weight

import matplotlib.pyplot as plt
fig1, ax1 = plt.subplots()

ax1.pie(weight, shadow = True)
ax1.axis('equal')
plt.show()

NESN = eikon.get_timeseries(["NESN.S"], start_date="2014-01-06",
                                 end_date="2018-12-20", interval="daily")
plt.plot(NESN.loc[:, "CLOSE"])

## Tutorial code from  https://pythonprogramming.net/custom-legends-matplotlib-tutorial/?completed=/multi-y-axis-twinx-matplotlib-tutorial/

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import mpl_finance
from matplotlib import style

import numpy as np
import datetime as dt

style.use('seaborn-dark')
print(plt.style.available)

print(plt.__file__)

MA1 = 10
MA2 = 30

def moving_average(values, window):
    weights = np.repeat(1.0, window)/window
    smas = np.convolve(values, weights, 'valid')
    return smas

def high_minus_low(highs, lows):
    return highs-lows


def bytespdate2num(fmt, encoding='utf-8'):
    strconverter = mdates.strpdate2num(fmt)
    def bytesconverter(b):
        s = b.decode(encoding)
        return strconverter(s)
    return bytesconverter
    

def graph_data(stock):

    fig = plt.figure(facecolor='#f0f0f0')
    ax1 = plt.subplot2grid((6,1), (0,0), rowspan=1, colspan=1)
    plt.title(stock)
    plt.ylabel('H-L')
    ax2 = plt.subplot2grid((6,1), (1,0), rowspan=4, colspan=1, sharex=ax1)
    plt.ylabel('Price')
    ax2v = ax2.twinx()
    
    ax3 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
    plt.ylabel('MAvgs')

    

    GoogleHist = eikon.get_timeseries(["GOOGL.O"], start_date="2017-01-06", end_date="2018-12-20", interval="daily")
    date = mdates.date2num(GoogleHist.index.to_pydatetime())
    closep = GoogleHist.loc[:, "CLOSE"]
    highp = GoogleHist.loc[:, "HIGH"]
    lowp = GoogleHist.loc[:, "LOW"]
    openp = GoogleHist.loc[:, "OPEN"]
    volume = GoogleHist.loc[:, "VOLUME"]

    x = 0
    y = len(date)
    ohlc = []

    while x < y:
        append_me = date[x], openp[x], highp[x], lowp[x], closep[x], volume[x]
        ohlc.append(append_me)
        x+=1

    ma1 = moving_average(closep,MA1)
    ma2 = moving_average(closep,MA2)
    start = len(date[MA2-1:])

    h_l = list(map(high_minus_low, highp, lowp))
    

    ax1.plot_date(date[-start:],h_l[-start:],'-', label='H-L')
    ax1.yaxis.set_major_locator(mticker.MaxNLocator(nbins=4, prune='lower'))


    mpl_finance.candlestick_ohlc(ax2, ohlc, width=0.4, colorup='#77d879', colordown='#db3f3f')

    ax2.yaxis.set_major_locator(mticker.MaxNLocator(nbins=7, prune='upper'))
    ax2.grid(True)
    
    bbox_props = dict(boxstyle='round',fc='w', ec='k',lw=1)
    
    ax2.annotate(str(closep[-1]), (date[-1], closep[-1]),
                 xytext = (date[-1]+4, closep[-1]), bbox=bbox_props)

##    # Annotation example with arrow
##    ax2.annotate('Bad News!',(date[11],highp[11]),
##                 xytext=(0.8, 0.9), textcoords='axes fraction',
##                 arrowprops = dict(facecolor='grey',color='grey'))
##
##    
##    # Font dict example
##    font_dict = {'family':'serif',
##                 'color':'darkred',
##                 'size':15}
##    # Hard coded text 
##    ax2.text(date[10], closep[1],'Text Example', fontdict=font_dict)

    ax2v.plot([],[], color='#0079a3', alpha=0.4, label='Volume')
    ax2v.fill_between(date[-start:],0, volume[-start:], facecolor='#0079a3', alpha=0.4)
    ax2v.axes.yaxis.set_ticklabels([])
    ax2v.grid(False)
    ax2v.set_ylim(0, 3*volume.max())



    ax3.plot(date[-start:], ma1[-start:], linewidth=1, label=(str(MA1)+'MA'))
    ax3.plot(date[-start:], ma2[-start:], linewidth=1, label=(str(MA2)+'MA'))
    
    ax3.fill_between(date[-start:], ma2[-start:], ma1[-start:],
                     where=(ma1[-start:] < ma2[-start:]),
                     facecolor='r', edgecolor='r', alpha=0.5)

    ax3.fill_between(date[-start:], ma2[-start:], ma1[-start:],
                     where=(ma1[-start:] > ma2[-start:]),
                     facecolor='g', edgecolor='g', alpha=0.5)
    
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax3.xaxis.set_major_locator(mticker.MaxNLocator(10))
    ax3.yaxis.set_major_locator(mticker.MaxNLocator(nbins=4, prune='upper'))

    for label in ax3.xaxis.get_ticklabels():
        label.set_rotation(45)



    plt.setp(ax1.get_xticklabels(), visible=False)
    plt.setp(ax2.get_xticklabels(), visible=False)
    plt.subplots_adjust(left=0.11, bottom=0.24, right=0.90, top=0.90, wspace=0.2, hspace=0)

    ax1.legend()
    leg = ax1.legend(loc=9, ncol=2,prop={'size':11})
    leg.get_frame().set_alpha(0.4)
    
    ax2v.legend()
    leg = ax2v.legend(loc=9, ncol=2,prop={'size':11})
    leg.get_frame().set_alpha(0.4)
    
    ax3.legend()
    leg = ax3.legend(loc=9, ncol=2,prop={'size':11})
    leg.get_frame().set_alpha(0.4)
    
    plt.show()
    fig.savefig('google.png', facecolor=fig.get_facecolor())


graph_data('GOOGL')

