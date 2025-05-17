from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Your Dhan credentials
DHAN_ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzUwMDE0NDE3LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiaHR0cHM6Ly9hcGkuZGhhbi5jbyIsImRoYW5DbGllbnRJZCI6IjExMDI4MjM0ODUifQ.wa8v47rQy5nX1m9GG2pHIcvmSuzqkiOJDkd8j9QVhC6ouXMsX_4m8qpD1HS-7j850lrso6yciHNWKBiHcr43xg"
CLIENT_ID = "1102823485"

def place_order(symbol, side, qty):
    headers = {
        'access-token': DHAN_ACCESS_TOKEN,
        'client-id': CLIENT_ID,
        'Content-Type': 'application/json'
    }

    payload = {
        "exchangeSegment": "MCX_COMM",                   # Corrected
        "productType": "INTRADAY",
        "orderType": "MARKET",
        "transactionType": "BUY" if side == "BUY" else "SELL",  # Correct values
        "orderSide": side,                               # Still required
        "instrumentId": symbol,
        "quantity": qty,
        "price": 0,
        "triggerPrice": 0,
        "afterMarketOrder": False,
        "amoTime": "OPEN",
        "disclosedQuantity": 0,
        "validity": "DAY"
    }

    res = requests.post("https://api.dhan.co/orders", headers=headers, json=payload)
    return res.status_code, res.json()

@app.route('/', methods=['POST'])
def webhook():
    data = request.json
    signal = data.get('signal')
    symbol = data.get('symbol')
    qty = int(data.get('qty', 1))

    if signal == "buy":
        status, res = place_order(symbol, "BUY", qty)
    elif signal == "sell":
        status, res = place_order(symbol, "SELL", qty)
    else:
        return "Invalid signal", 400

    return {"status": status, "response": res}

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
