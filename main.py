from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    
    unit_currency = req['queryResult']['parameters'].get('unit-currency', {})
    amount = unit_currency.get('amount')
    source = unit_currency.get('currency')
    target = req['queryResult']['parameters'].get('currency-name')

    if not all([amount, source, target]):
        return jsonify({"fulfillmentText": "Please provide amount and currencies."})

    api_key = os.getenv("f24830c12b1367507d428884")  # or paste directly
    url = f"https://v6.exchangerate-api.com/v6/{'f24830c12b1367507d428884'}/pair/{source}/{target}/{amount}"

    res = requests.get(url).json()

    if res.get('result') != 'success':
        return jsonify({"fulfillmentText": "Error fetching conversion rate."})

    converted = res.get('conversion_result')
    reply = f"{amount} {source} = {converted:.2f} {target}"

    return jsonify({"fulfillmentText": reply})

if __name__ == "__main__":
    app.run(port=5000)
