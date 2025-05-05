from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Replace this with your preferred exchange rate API
EXCHANGE_API_URL = "f24830c12b1367507d428884"

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    intent = req.get("queryResult").get("intent").get("displayName")

    if intent == "CurrencyConversion":
        return handle_currency_conversion(req)
    else:
        return jsonify({"fulfillmentText": "Intent not supported."})

def handle_currency_conversion(req):
    parameters = req["queryResult"]["parameters"]
    amount = parameters.get("amount")
    from_currency = parameters.get("from-currency")
    to_currency = parameters.get("to-currency")

    # Call exchange rate API
    response = requests.get(EXCHANGE_API_URL + from_currency.upper())
    data = response.json()

    if "rates" in data and to_currency.upper() in data["rates"]:
        rate = data["rates"][to_currency.upper()]
        converted_amount = round(amount * rate, 2)
        result_text = f"{amount} {from_currency.upper()} is approximately {converted_amount} {to_currency.upper()}."
    else:
        result_text = "Sorry, I couldn't fetch the conversion rate at the moment."

    return jsonify({"fulfillmentText": result_text})

if __name__ == '__main__':
    app.run(debug=True)
