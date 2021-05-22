
import argparse
import Analyzer
from Utility import Util

APP_NAME = "Data BreachAnalyzer"
VERSION = "1.0.0"
COPYRIGHT = "Copyright 2021 Reza Soltani"


def visualize(input):
    pass

if __name__ == "__main__":

    print("\n" + APP_NAME + " v" + VERSION)

    # Initialize parser
    parser = argparse.ArgumentParser(description=APP_NAME + " v"+ VERSION + " " + COPYRIGHT)


    # Adding optional argument
    parser.add_argument("-r", "--read", dest='FILENAME', help="Read CSV input file")   # parent argument

    parser.add_argument("-ad", "--adate", dest='ADATE', help="The day of breach announcement")
    parser.add_argument("-id", "--idate", dest='IDATE', help="The actual day of the breach")

    parser.add_argument("-a", "--analyze", action="store_true", help="Analyze the input CSV file")  # parent argument

    parser.add_argument("-l", "--limit", dest='LIMIT', type=int,  help="Limit number of rows to read. Default is all rows")

    parser.add_argument("-t", "--ticker", dest='TICKER', help="Select a specific ticker to analyze. If an input file is provided then the ticker is searched in the file, otherwise atleast an adate or idate must be provided. ")

    parser.add_argument("-s", "--stats", action="store_true", help="Produce high-level analytics on breach instances based in the given CSV input file")
    parser.add_argument("-w", "--web", action="store_true", help="Display details about the given Ticker on Yahoo Finance")


    args = parser.parse_args()




    count = -1  # cover all entries by default

    # if a single entry is provided along with a date
    if args.TICKER and (args.ADATE or args.IDATE):
        ticker = args.TICKER
        adate = args.ADATE
        idate = args.IDATE
        Analyzer.ticker_analyze(ticker, adate, idate)

    # if a file is provided
    elif args.FILENAME:
        ticker = None
        # if selecting a specific ticker
        if args.TICKER:
            ticker = args.TICKER
            if args.web:  # show details of a specific ticker on web
                Util.open_yahoo_finance(ticker)

        if args.LIMIT: # limit input if limit value is provided
            count = args.LIMIT

        if args.analyze:  # analyze input file row by row
            Analyzer.file_analyze(args.FILENAME, count, ticker)

        # show high-level stats on given records
        if args.stats:
            Analyzer.stats_analyze(args.FILENAME, count)



    else:
        parser.print_help()


    print("End.")
