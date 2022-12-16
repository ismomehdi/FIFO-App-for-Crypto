from flask import request, session

def create_tx_dict(type: str):
    tx_data = {}

    if type == 'sell':
        amount = f"-{request.form['amount']}"
    else:
        amount = request.form['amount']

    tx_data['amount'] = amount
    tx_data['portfolio_id'] = session['portfolio']
    tx_data['datetime'] = request.form['datetime']
    tx_data['ticker'] = request.form['ticker']
    tx_data['price'] = request.form['price']
    tx_data['note'] = request.form['note']

    return tx_data
