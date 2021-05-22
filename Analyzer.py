
from datetime import timedelta
import datetime
import math
import collections
from pandas.tseries.offsets import BDay

from Utility import Cache, Util
from Graph import *
import Constants
from ApiClients import ApiClients


def stats_analyze(input, quantity):
    if input:
        records = Util.read_input(input, quantity)
        if records is None:
            return

        print("\n Analyzing {} valid records from the given input file..".format(len(records)))
    # iterate and analyze

        num_of_records = {}
        total_count = {}
        total_count_name = {}

    for i, item in enumerate(records):
        # input CSV has the this format:
        (date, name, city, state, type_of_breach, type_of_org, total_records, description, source, URL_source, year, lattitude, longitude, *others) = item

        if year:
            year = int(year)

        # analytics A: capture breach count per year
        if total_count != 0:
            if year in total_count:
                total_count[year] = total_count[year] + 1
            else:
                total_count[year] = 1

        # capture total number of breaches per target
        if total_count_name != 0:
            if name in total_count_name:
                total_count_name[name] = total_count_name[name] + 1
            else:
                total_count_name[name] = 1


    collections.OrderedDict(sorted(total_count.items()), reverse=True)
    plot_stats_breaches(total_count)
    plot_stats_targets(total_count_name)


def ticker_analyze(ticker, date_of_announcement = None, date_of_incident = None):
    '''
    Analyze a single ticker at the given announcement and/or incident date
    '''
    # get stock value
    if ticker is None:
        print("Oops! Ticker can't be empty")
    else:
        if date_of_announcement is None and date_of_incident is None:
            print("Oops! no valid date given")
        else:
            if date_of_announcement:
                date_of_announcement = datetime.datetime.strptime(date_of_announcement, '%m/%d/%Y')
                print("Given announcement date: {}".format(date_of_announcement.date()))

            if date_of_incident:
                date_of_incident = datetime.datetime.strptime(date_of_incident, '%m/%d/%Y')
                print("Given incident date: {}".format(date_of_incident.date()))

            # get stock values
            values = get_stock_value(ticker, date_of_announcement, Constants.STOCK_PRICE_TARGET_DAYS_DELTA_BEFORE, Constants.STOCK_PRICE_TARGET_DAYS_DELTA_AFTER, date_of_incident)

            # plot value
            if not values is None:
                plot_value(values, ticker, date_of_announcement, date_of_incident)


def file_analyze(input, quantity = None, selected_ticker = None):
    '''
    Anaylze Data
    CSV Format: Ticker, Company Name, Date incident made public, Date Incident Occurred, Type of Incident, Number of Records Affected, Location, Source
    '''
    if input:
        records = Util.read_input(input, quantity)
        if records is None:
            return

        print("\nFound {} valid records in file...".format(len(records)))

        # iterate and analyze
        for i, item in enumerate(records):

            ''' Current input structure: '''
            '''         Date Made Public, Company, City, State, Type of breach,
                        Type of organization, Total
                        Records, Description of incident, Information
                        Source, Source URL, Year of Breach, Latitude, Longitude
            '''

            # input CSV has the this format:
            (date, name, city, state, type_of_breach, type_of_org, total_records, description, source, URL_source, year, lattitude, longitude, *others) = item

            print("-------")

            ticker = None
            occurance_date = None
            if others[0]:   # ticker symbol (optional)
                ticker = others[0]
            if others[1]:   # occurance date (optional)
                occurance_date = others[1]


            if ticker == "-":
                print("Skipping record in row {}".format(i + 1))  # skip records with "-" as symbol name
                continue

            # if ticket value exist
            if ticker is None:
                if name:
                    ticker = get_ticker(name)
                else:
                    print("Oops!  Skipping record. No name or symbol found for record in row {} and values {}".format(i+1, item))
                    continue

            if ticker == None:
                print("Skipping record. No symbol found for record in row {} and values {}".format(i + 1, item))
                continue


            if date:
                date_of_announcement = datetime.datetime.strptime(date, '%m/%d/%Y')

            date_of_incident = None
            if occurance_date:
                date_of_incident = datetime.datetime.strptime(occurance_date, '%m/%d/%Y')


            if not date and not occurance_date:
                print("Oops!  Skipping record. No date given for the record in row  {} and values {}".format(i+1, item))
                continue



            # get stock value
            values = get_stock_value(ticker, date_of_announcement, Constants.STOCK_PRICE_TARGET_DAYS_DELTA_BEFORE, Constants.STOCK_PRICE_TARGET_DAYS_DELTA_AFTER, date_of_incident)

            if values is None:
                continue


            # graph stock if it matches the given ticker
            if selected_ticker is not None and selected_ticker.upper() == ticker.upper():
                plot_value(values, ticker, date_of_announcement, date_of_incident)


    else:
        print("Oops!  given CSV filename is invalid")


def get_date_or_find_closest_after(target_date, list):
    if not target_date in list:
        target_date = (target_date + timedelta(days=1))
        if not target_date in list:
            target_date = (target_date + timedelta(days=2))
            if not target_date in list:
                print("Oops! Can't find given date {} or closest days in the result".format(target_date))
                return None
    return target_date

def print_values(ticker, values,  date_of_announcement = None, delta_before_const = None, delta_before_value = None,  delta_after_const = None, delta_after_value = None, date_of_incident = None):
    '''
    Print the values
    '''



    # check date is in result
    date_of_announcement_string  = get_date_or_find_closest_after(date_of_announcement, values.index).strftime("%Y-%m-%d")

    ohlc_announcement = values.loc[date_of_announcement_string, ['Open', 'High', 'Low', 'Close', 'Volume']]
    ohlc_before = values.loc[delta_before_value, ['Open', 'High', 'Low', 'Close', 'Volume']]
    ohlc_after = values.loc[delta_after_value, ['Open', 'High', 'Low', 'Close', 'Volume']]


    # get all rows and columns: open, high, low, close and volume
    print("\nStock Price:")
    print("---------------")

    if date_of_incident:
        date_of_incident_string = get_date_or_find_closest_after(date_of_incident, values.index).strftime("%Y-%m-%d")

        ohlc_incident = values.loc[date_of_incident_string, ['Open', 'High', 'Low', 'Close',
                                                 'Volume']]  # get all rows and columns: open, high, low, close and volume
        print("On the day of incident: {}.. Open: {}, Close: {}, High: {}, Low: {}, Volume: {}  ".format(date_of_incident_string, round(ohlc_incident['Open'], 4),
                                                                                                         round(ohlc_incident['Close'],4),
                                                                                                         round(ohlc_incident['High'],4),
                                                                                                         round(ohlc_incident['Low'],4),
                                                                                                         int(ohlc_incident['Volume'])))

        print("{} days before the incident: {}.. Open: {}, Close: {}, High: {}, Low: {}, Volume: {}  ".format(
            delta_before_const, delta_before_value, round(ohlc_before['Open'],4), round(ohlc_before['Close'],4), round(ohlc_before['High'],4), round(ohlc_before['Low'],4),
            int(ohlc_before['Volume'])))
    else:
        print("{} days before the announcement: {}.. Open: {}, Close: {}, High: {}, Low: {}, Volume: {}  ".format(
            delta_before_const, delta_before_value, round(ohlc_before['Open'],4), round(ohlc_before['Close'],4), round(ohlc_before['High'],4), round(ohlc_before['Low'],4),
            int(ohlc_before['Volume'])))

    print("On the day of announcement: {}.. Open: {}, Close: {}, High: {}, Low: {}, Volume: {}  ".format(date_of_announcement_string, round(ohlc_announcement['Open'],4), round(ohlc_announcement['Close'],4), round(ohlc_announcement['High'],4), round(ohlc_announcement['Low'],4), int(ohlc_announcement['Volume'])))

    print("{} days after the announcement: {}.. Open: {}, Close: {}, High: {}, Low: {}, Volume: {}  ".format(
        delta_after_const, delta_after_value, round(ohlc_after['Open'],4), round(ohlc_after['Close'],4), round(ohlc_after['High'],4), round(ohlc_after['Low'],4),
        int(ohlc_after['Volume'])))

    print("\nSummary of Change:")
    print("---------------")
    print(
        "Percentage change from announcement date of {} to {} ({} days after) is {}".format(date_of_announcement_string,
                                                                                            delta_after_value,
                                                                                            delta_after_const,
                                                                                            calculate_percentage_change(
                                                                                                ohlc_announcement[
                                                                                                    'Close'],
                                                                                                ohlc_after['Close'])))
    print(
        "Percentage change based on Nasdaq Index from announcement date of {} to {} ({} days after) is {}".format(
            date_of_announcement_string, delta_after_value, delta_after_const,
            calculate_change_based_on_NASDAQ(date_of_announcement, delta_after_const, ohlc_announcement['Close'],
                                             ohlc_after['Close'])))




    print("\nDaily Prices:")
    print("---------------")

    # iterate through rows based on delta interval
    for i in range(1, len(values)-1, Constants.STOCK_PRICE_TARGET_DAYS_DELTA_INTERVAL):
        #if i == 0:
        #    continue

        # 0-> Open, 1-> High, 2-> Low, 3-> Close, 4-> Adj Close, 5-> Volume
        print("Record {} for date {}:  Open: {}, Close: {}, High: {}, Low: {}, Volume: {}, Change: {}, Change (Nasdaq): {}  ".format(
            i, values.index[i].strftime("%Y-%m-%d"), round(values.iloc[i, 0], 4) , round(values.iloc[i, 1],4) , round(values.iloc[i, 2], 4),
            round(values.iloc[i, 3], 4),
            int(values.iloc[i, 5]),
            calculate_percentage_change(ohlc_announcement['Close'], values.iloc[i, 2]),
            calculate_change_based_on_NASDAQ(date_of_announcement, i, ohlc_announcement['Close'],  values.iloc[i, 2])))



    #print("---")



def calculate_percentage_change(first, second):
    '''
    Calculate percentage change between two given decimal values
    '''
    return round(((second - first) / first) * 100, 2)



def calculate_log_change(first, second):
    '''
    Calculate percentage change between two given decimal values based on logs
    '''
    #return (second / first) - 1
    return math.log(second) - math.log(first)



def calculate_change_based_on_NASDAQ(announcement_date, delta_after, price_before_announcement, price_after_announcement):
    '''
    Calculate percentage change between two given decimal values with respect to NASDAQ composite index
    '''
    # get NAsDAQ price for breach date, and after
    nasdaq_prices = get_stock_value(Constants.NASDAQ_TICKER, announcement_date, 0, delta_after, date_of_incident=None, print_result = False)
    if nasdaq_prices is not None and not nasdaq_prices.empty:
        date_of_announcement_string = get_date_or_find_closest_after(announcement_date, nasdaq_prices.index).strftime("%Y-%m-%d")
        nasdaq_before_announcement = nasdaq_prices.loc[date_of_announcement_string,['Open', 'High', 'Low', 'Close',
                                                 'Volume']]
        nasdaq_after_announcement = nasdaq_prices.loc[nasdaq_prices.index[-1], ['Open', 'High', 'Low', 'Close',
                                                 'Volume']] #get last date whatever it is

        return round(((((price_after_announcement / price_before_announcement) - 1) * 100) - (((nasdaq_after_announcement['Close']/nasdaq_before_announcement['Close'])-1)*100)), 2)
    else:
        None




# date format: YYYY-MM-DD
def get_stock_value(ticker_name, date_of_announcement, delta_before_const, delta_after_const, date_of_incident = None, print_result = True, verbose = False):
    '''
    Return stock value for a given start and end time
    '''

    if print_result:
        print("\n Organization's Stock Symbol: {} ".format(ticker_name.upper()))

    # get data for (incident date (or announcement date) - delta_before) to (date of announcement + delta_after)
    # if date of incident is available then use it, otherwise use date of announcement
    if date_of_incident:
        #date_of_event_and_delta_before = date_of_incident - timedelta(days=delta_before_const)
        date_of_event_and_delta_before = date_of_incident - BDay(delta_before_const)
    else:
        #date_of_event_and_delta_before = date_of_announcement - timedelta(days=delta_before_const)
        date_of_event_and_delta_before = date_of_announcement - BDay(delta_before_const)

    #date_of_event_and_delta_after = date_of_announcement + timedelta(days=delta_after_const)
    date_of_event_and_delta_after = date_of_announcement + BDay(delta_after_const)

    date_of_event_and_delta_before_string = date_of_event_and_delta_before.strftime("%Y-%m-%d")
    date_of_event_and_delta_after_string = date_of_event_and_delta_after.strftime("%Y-%m-%d")
    if verbose:
        print("Getting stock price for " + ticker_name + " From " + date_of_event_and_delta_before_string + "  to " + date_of_event_and_delta_after_string)


    # add an extra day to capture last day
    date_of_event_and_delta_after_adjusted = date_of_event_and_delta_after + timedelta(days=1)

    # check our cache first
    cache = Cache.check(ticker_name, date_of_event_and_delta_before, date_of_event_and_delta_after)
    if cache is not None:
        response = cache
    else:
        response = ApiClients.get_ticker_value(ticker_name, start=date_of_event_and_delta_before_string, end=date_of_event_and_delta_after_adjusted, progress=verbose)
        Cache.update(ticker_name, response)

    if response.empty:
        print("Oops!  Unable to retrieve data for the given ticker {} and time range of {} to {}".format(ticker_name,date_of_event_and_delta_before_string, date_of_event_and_delta_after_adjusted ))
        return None
    else:
        if print_result:
            print_values(ticker_name, response, date_of_announcement, delta_before_const, date_of_event_and_delta_before_string, delta_after_const, date_of_event_and_delta_after_string, date_of_incident=date_of_incident)
        return response




def get_ticker(name):
    '''
    Return the stock ticker symbol of a given company name
    '''
    return ApiClients.get_ticker(name)








