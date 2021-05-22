import Constants

import yfinance as yf
from alpha_vantage.timeseries import TimeSeries

class ApiClients:

    def get_ticker_value(ticker_name, start, end, progress):
        '''
        Use Yahoo Finance API to obtain stock value of a given ticker
        '''
        try:
            response = yf.download(ticker_name, start=start,
                               end=end,
                               progress=progress)  # TODO: Is the response an aggregation or from a particular exchange?
        except ConnectionError:
            print("Oops! There is a connection Error. Unable to pull stock data")

        return response


    def get_ticker(name):
        '''
        Use Alpha Advantage to return the stock ticker symbol of a given company name
        '''
        # Note: There are limitations with this API
        print("Getting symbol name for organization {} using the API...".format(name))
        if not Constants.ALPHA_ADVANTAGE_API_KEY:
            print("Oops! You need a valid AlphaAdvantage API KEY to retrieve stock symbols!")
            return None
        else:
            ts = TimeSeries(key=Constants.ALPHA_ADVANTAGE_API_KEY)
        # Get json object with the intraday data and another with  the call's metadata
        try:
            data, meta_data = ts.get_symbol_search(name)
        except ValueError:
            print("Oops! You may have exceeded your API quota")
            return None


        response = None
        if data is not None and data:
            response = data[0]['1. symbol']
            print("Found ticker {}...".format(response))
        else:
            print("Oops! No symbol found for '{}' using the API".format(name))
        return response  # return the first item from the list of results