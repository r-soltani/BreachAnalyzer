import webbrowser
import sys
import csv

import Constants



class Util:
    def open_url(url):
        webbrowser.open(url, new=2)

    def open_yahoo_finance(ticker):
        '''
        display information about a given ticker on Yahoo Finance
        '''
        Util.open_url("https://finance.yahoo.com/quote/{}/".format(ticker))

    def read_input(filename, quantity):
        '''
        Read input CSV file
        Format: Date incident made public,
        '''
        print("Reading {} items from input file: {}".format(quantity, filename))
        result = []
        i = 0
        try:
            with open(filename, 'r') as file:
                file.readline()  # skip header row
                reader = csv.reader(file, delimiter=',')
                try:
                    for row in reader:
                        if i >= quantity and quantity > -1:
                            break
                        if Constants.VERBOSE:
                            print(row)
                        i += 1
                        rowArray = list(row)
                        result.append(rowArray)  # get date of publication, get target name
                except csv.Error as e:
                    print("Oops!  Couldn't read the entire CSV file")
                    sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))
        except OSError:
            print("Oops!  File not found")
            return None
        except ValueError:
            print("Oops!  Couldn't open the given CSV file")
            return None

        return result

'''
Check local cache for stock values
'''
class Cache(object):

    _cache = dict()

    @staticmethod
    def update(ticker, data):
        Cache._cache[ticker] = data

    @staticmethod
    def check(ticker, date_of_event_and_delta_before, date_of_announcement_and_delta_after):

        if ticker in Cache._cache:
            data = Cache._cache[ticker]

            # check if any date later than or equal to 'date_of_event_and_delta_before'  exist in data.index
            if any(date_of_announcement_and_delta_after <= date_item for date_item in data.index):
                if any(date_of_event_and_delta_before >= date_item for date_item in data.index):
                        return data


        return None

