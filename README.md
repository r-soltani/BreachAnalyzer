## BreachAnalyzer
The objective of this project is to build the preliminary basis for an open-source application that enables automated data retrieval, analysis, and visualization of breach and stock data through an intuitive and simple-to-use user interface. Its future iterations are expected to provide a richer layer of data analytics, an interactive web GUI, and more extensive API integration.

### Major Features

The current version of the BreachAnalyzer can perform a number of useful tasks:

**Single Symbol Analysis and Visualization - Price change analysis and visualization of a single stock symbol based on the breach publication date and optionally the breach occurrence date.** Given the stock symbol name of a target organization, and the breach publication date (and optionally the breach occurrence date), the app can perform analysis on the change in the stock price from 7 days prior to the breach publication date (or occurrence date) and up to 14 days after. All parameters are configurable.The app will output the values as text and as a candlestick chart.

**Multiple Symbol Analysis - Price change analysis on a list of stock symbols along with their breach publication date and optionally their occurrence dates.** Given a CSV file that includes a list of the symbol names, breach publication date, and optionally the occurrence date, the app is able to retrieve the stock price of the target organization and perform price change analysis one row at a time. If a stock symbol is not given, the application will attempt to identify the stock symbol based on the organization's name.

**Statistical Analysis - Statistical analysis on a list of stock symbols file.** Given a CSV file with symbol names, the breach publication dates, and optionally the occurrence date, the app is able to identify patterns, trends and relations among the data records.

The objective of this project is to build the preliminary basis for an open-source application that enables automated data retrieval, analysis, and visualization of breach and stock data through an intuitive and simple-to-use user interface. Its future iterations are expected to provide a richer layer of data analytics, an interactive web GUI, and more extensive API integration.
The current version supports a command-line interface. To get the complete list of program argument simply run 'python Main.py' as shown below:

    python Main.py
    usage: Main.py [-h] [-r FILENAME] [-ad ADATE] [-id IDATE] [-a] [-l LIMIT]
                 [-t TICKER] [-s] [-w]
    Data Breach Analyzer v1.0.0 Copyright 2021 Reza Soltani
    optional arguments:
      -h, --help            show this help message and exit
      -r FILENAME, --read FILENAME      Read CSV input file
      -ad ADATE, --adate ADATE      The day of breach announcement
      -id IDATE, --idate IDATE        The actual day of the breach
      -a, --analyze         Analyze the input CSV file
      -l LIMIT, --limit LIMIT        Limit number of rows to read. Default is all rows
      -t TICKER, --ticker TICKER          Select a specific ticker to analyze. If an input file   is provided then the ticker is searched in the file, otherwise atleast an adate or idate must be provided.
      -s, --stats           Produce high-level analytics on breach instances based from the given CSV input file
      -w, --web             Display details about the given Ticker on Yahoo  Finance


### Walk-through
For more details explaination visit www.zeroknowledgeproof.com or https://medium.com/@zeroknowledgeproof
