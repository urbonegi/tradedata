import json

from flask import Flask, make_response, request

from trades import TradesData

app = Flask(__name__)


def activate_job(dir):
    print('Processing trade data from directory: {}'.format(dir))
    trades = TradesData()
    trades.process_trade_data(dir=dir)


@app.route("/daily")
def daily_summary():
    trade_data = TradesData()
    return trade_data.get_daily_summary().to_html()


@app.route("/trades")
def trades_data():
    reference = request.args.get('ref', None)
    trade_data = TradesData()
    return trade_data.get_trade_data(reference=reference).to_html()


@app.route("/instruments")
def instrument_summary():
    instrument = request.args.get('inst', None)
    trade_data = TradesData()
    return trade_data.get_instrument_summary(instrument=instrument).to_html()


@app.route("/tradesexport")
def export_trades():
    trade_data = TradesData()
    df = trade_data.get_trade_data()
    resp = make_response(df.to_csv())
    resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp


@app.route("/instrumentsexport")
def export_instruments():
    trade_data = TradesData()
    df = trade_data.get_instrument_summary()
    resp = make_response(df.to_csv())
    resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp


@app.route("/dailyexport")
def export_daily_summary():
    trade_data = TradesData()
    df = trade_data.get_daily_summary()
    resp = make_response(df.to_csv())
    resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp
