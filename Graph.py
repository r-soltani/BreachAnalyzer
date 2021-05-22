import matplotlib as mpl
mpl.use('MacOSX')
import matplotlib.pyplot as plt
import mplfinance as mpf
from pprint import pprint
from collections import Counter


def plot_stats_targets(values):
    print("Attempting to Draw Targets Diagram...")
    plot_stats_targets_helper(values)

def plot_stats_targets_helper(values):
    x = []
    y = []

    counter_values = Counter(values)
    selection = counter_values.most_common(5)
    pprint(selection)
    for item in selection:
        y.append(item[0])
        x.append(item[1])
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('equal')
    plt.title('Top 5 targets', fontsize=14)
    ax.pie(x, labels=y, autopct='%d%%')
    plt.show()


def plot_stats_breaches(values):
    print("Attempting to Draw Breaches Diagram...")
    plot_stats_breaches_helper(values)

def plot_stats_breaches_helper(values):
    x = []
    y = []
    for key in sorted(values.keys()):
       x.append(key)
       y.append(values[key])

    plt.plot(x, y, color='red', marker='o')
    plt.title('Breaches', fontsize=14)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Number of Breaches', fontsize=14)
    plt.grid(True)
    plt.show()


def plot_value(values, ticker, date_of_announcement = None, date_of_incident = None):
    print("Attempting to Draw Chart...")
    plot_values_helper(values, ticker,  date_of_announcement, date_of_incident)

def plot_values_helper(values, ticker, date_of_announcement, date_of_incident):

    plt.style.use('ggplot')

    # Extracting Data for plotting
    data = values
    ohlc = data.loc[:, ['Open', 'High', 'Low', 'Close', 'Volume']]  # get all rows and columns: open, high, low, close and volume
    ohlc.index.name = 'Date'


    # if incident and announcement dates are available, then draw them
    vline_dates = []
    if date_of_incident:
        transaction_line_incident = date_of_incident #data.index[0]  # specify the date the incident was discovered
        vline_dates.append(transaction_line_incident)
    if date_of_announcement:
        transaction_line_announcement = date_of_announcement #data.index[2]  # specify the date the incident was published
        vline_dates.append(transaction_line_announcement)

    # draw vlines at incident discovered date and published date
    transaction_line = []
    if vline_dates:
        transaction_line = dict(vlines = dict(vlines=vline_dates, linewidths=(2, 1), colors=('#000011','#000022')))





    # optional best line between discovered date and incident date
    #best_line = dict(tlines=[(transaction_line_date, transaction_line_date2)], colors = 'c', linewidths=40,  alpha=0.35)

    # Create a new style based on `yahoo` style
    s = mpf.make_mpf_style(base_mpf_style='yahoo', y_on_right=False, gridstyle=':', edgecolor='black', facecolor='#f9f9f9')

    # calculate MACD
    exp12 = ohlc['Close'].ewm(span=12, adjust=False).mean()     # exponential moving average = 12
    exp26 = ohlc['Close'].ewm(span=26, adjust=False).mean()     # exponential moving average = 26
    macd = exp12 - exp26
    signal = macd.ewm(span=9, adjust=False).mean()              # signal line: 9-day exponential moving average over macd
    histogram = macd - signal
    apds = [
            mpf.make_addplot(exp12, color='lime'),   # exponential moving average 12
            mpf.make_addplot(exp26, color='c'),      # exponential moving average 26

            mpf.make_addplot(histogram, type='bar', width=0.7, panel=2,   # volume
                             color='dimgray',  secondary_y=False),

            mpf.make_addplot(macd, panel=2, color='fuchsia', secondary_y=True),  # macd
            mpf.make_addplot(signal, panel=2, color='b', secondary_y=True, ylabel="MACD", y_on_right=True)  #signal line

            ]

    # plot the chart
    (fig, ax) = mpf.plot(ohlc,
             title=ticker.upper(),
             type='candle',  # can also be ohlc
             datetime_format=' %A, %d-%m-%Y',
             volume=True,
             figratio=(2,1),
             figscale=1.5,
             update_width_config=dict(line_width=1, candle_linewidth=1, candle_width=1),
             show_nontrading=True,
             tight_layout=False,
             xrotation=40,
             style=s,
             addplot=apds,
             returnfig=True,
             **transaction_line)


    # Add label to incident and announcement lines
    highest_y = max(ohlc['High'])
    if transaction_line_incident:
        ax[0].text(transaction_line_incident, highest_y, 'Breach Date',
                horizontalalignment='right',
                verticalalignment='top',
                rotation='vertical')

    if transaction_line_announcement:
        ax[0].text(transaction_line_announcement, highest_y, 'Publish Date',
                   horizontalalignment='right',
                   verticalalignment='top',
                   rotation='vertical')

    mpf.show()



