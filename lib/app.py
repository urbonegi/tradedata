import json

from flask import Flask, make_response, request, jsonify, Response
from flasgger import Swagger
import pandas

from trades import TradesData

app = Flask(__name__)
swagger = Swagger(app)


def activate_job(dir):
    print('Processing trade data from directory: {}'.format(dir))
    trades = TradesData()
    trades.process_trade_data(dir=dir)


@app.route("/daily")
def daily_summary():
    """Get Daily Market Statistics
    Daily trade market statistics contain: total traded value and number
    of daily trades.
    ---
    responses:
      200:
        description: Daily Market trade summary Dataframe html page
      400:
        description: Trade data not loaded
    """
    trade_data = TradesData()
    data = trade_data.get_daily_summary()
    if isinstance(data, pandas.DataFrame):
        return data.to_html()
    return Response(data, status=400)


@app.route("/trades")
def trades_data():
    """Get trades data
    Trade data contains trade instrument, trade date, time in miliseconds,
    instrument price, trade quantity and trade reference.
    ---
    parameters:
        - in: query
          name: ref
          schema:
            type: string
          description: trade_reference
    responses:
      200:
        description: Daily Market trades Dataframe html page
      400:
        description: Trade data not loaded
    """
    reference = request.args.get('ref', None)
    trade_data = TradesData()
    data = trade_data.get_trade_data(reference=reference)
    if isinstance(data, pandas.DataFrame):
        return data.to_html()
    return Response(data, status=400)


@app.route("/instruments")
def instrument_summary():
    """Get Instrument daily Statistics
    Instrument stats data contains: instrument, date, instrument closing value,
    instrument average price and instrument daily market value.
    ---
    parameters:
        - in: query
          name: inst
          schema:
            type: string
          description: instrument
    responses:
      200:
        description: Daily Market trade summary Dataframe html page
      400:
        description: Trade data not loaded
    """
    instrument = request.args.get('inst', None)
    trade_data = TradesData()
    data = trade_data.get_instrument_summary(instrument=instrument)
    if isinstance(data, pandas.DataFrame):
        return data.to_html()
    return Response(data, status=400)


@app.route("/tradesexport")
def export_trades():
    """Export trades data to .csv file
    Export processed all trades data to CSV file for download.
    ---
    responses:
      200:
        description: Download all trades CSV file
      400:
        description: Trade data not loaded
    """
    trade_data = TradesData()
    df = trade_data.get_trade_data()
    if isinstance(df, pandas.DataFrame):
        resp = make_response(df.to_csv())
        resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp
    return Response(df, status=400)


@app.route("/instrumentsexport")
def export_instruments():
    """Export instrument data to .csv file
    Export processed instrument statistics data to CSV file for download.
    ---
    responses:
      200:
        description: Download instrument statistics CSV file
      400:
        description: Trade data not loaded
    """
    trade_data = TradesData()
    df = trade_data.get_instrument_summary()
    if isinstance(df, pandas.DataFrame):
        resp = make_response(df.to_csv())
        resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp
    return Response(df, status=400)


@app.route("/dailyexport")
def export_daily_summary():
    """Export daily trade statistics to .csv file
    Export processed daily trade statistics data to CSV file for download.
    ---
    responses:
      200:
        description: Download daily trade statistics CSV file
      400:
        description: Trade data not loaded
    """
    trade_data = TradesData()
    df = trade_data.get_daily_summary()
    if isinstance(df, pandas.DataFrame):
        resp = make_response(df.to_csv())
        resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp
    return Response(df, status=400)
