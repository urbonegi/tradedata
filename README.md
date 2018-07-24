# Trade Proccessing Application

Python 2.7 flask application for trade data proccessing, transformation and representation.

Requires flask 1.0.2 and pandas 0.23.3.

# Getting started

## Install dependencies

Install application requirements in python virtual environment.

```bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

## Run flask application

After sourcing application virtual environment, run app webserver. Sepcify <trade_data_files_dir>, <webserver hostname>, <webserver port> optionally or use default. Default values: <trade_data_files_dir> - <app_code_root_dir>/common, <webserver hostname> - 127.0.0.1, <webserver port> - 5000.

```bash
cd <app_code_root_dir>
python trade_app_run.py --dir <trade_data_files_dir> --host <webserver hostname> --port <webserver port>
```

Note: app load all trading data into memory and process trade data on startup, therefore starting might take couple of seconds depending on data size and gear.

## Run tests

TBC

# Client API Documentation

## Get all trades data

## Filter trades by trade_reference

## Export all trades to .csv file

## Get Instrument daily Statistics

## Filter Instrument daily Statistrics by date or by instrument

## Export all instrument statistics to .csv file

## Get Daily Market Statistics

## Export aily Market Statistics to .csv file

## Filter Total Trading Statistrics by date

# Task description

You need to process, in Python 2.7, a set of client-provided trades that they will be providing in CSV format. Each trade will consist of an instrument, a price, a quantity and a timestamp - together with a number of optional columns such as the trade reference, instrument type, underlying asset, client reference. They may provide one or more files, each consisting of zero or more trades, into a common directory.
 
Assume we need to store the trades somewhere for further processing as well provide an in-memory representation to work with them. Specifically we want to enrich the in-memory representation with the following derived information:
+ For each trade we need the market value, i.e. the price multiplied by the quantity
+ For each instrument we need the total market value, the closing value, and average price per day
+ For each trade reference we need the constituent trades
+ For each day we need to the total traded value, closing value, and the closing position
 
# Assumptions

+ Data loaded on application startup and pandas dataframe initialized. The same dataframe objects instance is used for application lifetime. In case new data needs to be uploaded application should be restarted with dir path to a trade data dir.
+ Trade data can consist multiple day trades and multiple client data. Trade data is in CSV format without column titles. Trading data files have '.csv' file ending. Child directories, if there are any, with .csv files they are ignored.
+ The data columns order is as follows (order can be changed by changing enumeration in trade_data_conf.json; also new client data columns can be defined there.):
    - Mandatory data columns:
        - instrument (any string),
        - date (date in format: yyyymmdd, i.e. 20110623),
        - time_in_milsec (time in miliseconds, integer, i.e. 37200003),
        - quantity (traded quantity, interger),
        - price (instrument price, float);
    - Optional data columns:
        - trade_ref (trade reference, any string value categorizing trades),
        - instrument_type (instrument type, any string value categorizing instruments),
        - client_ref (client reference, any string value categorizing clients),
        - underlying_asset (underlying asset, any string value categorizing assets).
+ Example data downloaded from [NASDAQ](http://www.nasdaqdod.com/Samples.aspx) at "NASDAQMassDownload: Trades". The data was manipulated to have couple of days trade data, similar data to client, trade reference and instrument type.
+ Instrument daily total market value is a sum of all intrument daily trade values.
+ Instrument closing value is the last daily traded price.
+ Instrument average price per day is sum of intrument daily traded values divided by traded quantity.
+ Total daily market traded value is sum of all daily trades markets values.
+ Daily market closing value and closing position definitions are unclear - can be added later when clarified.
