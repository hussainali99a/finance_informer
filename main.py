from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()

    # Extract parameters from Dialogflow
    unit_currency = req['queryResult']['parameters'].get('unit-currency', {})
    amount = unit_currency.get('amount')
    source = unit_currency.get('currency')
    target = req['queryResult']['parameters'].get('currency-name')

    if not all([amount, source, target]):
        return jsonify({"fulfillmentText": "Please provide both source and target currencies along with amount."})

    # API Call to ExchangeRate-API or similar
    api_key = os.getenv('f24830c12b1367507d428884')  # set in environment or hardcode temporarily
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{source}/{target}/{amount}"
    
    res = requests.get(url).json()
    if res['result'] != 'success':
        return jsonify({"fulfillmentText": "Failed to retrieve exchange rate. Please try again later."})

    converted = res['conversion_result']
    reply = f"{amount} {source} is approximately {converted} {target}"

    return jsonify({
        "fulfillmentText": reply
    })

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
