import requests

headers = {
    "app_version": "8.10.0",
    "device_id": "64a8c630-acc2-11ef-aa5e-9f6ee3baa1a5",
    "lang": "ru-RU",
    "platformid": "30",
    "sign": "5679FBAAF1D0A199E6B0975616B44807220C5FC8824D41F0DE21D2261F2D8E18",
    "timestamp": "1733496004073",
    "traceid": "8557cddbfe574e07b36c3014b5773358",
}

params = {
    "coinName": "USDT",
    "tradeCoinName": "USD",
    "type": "1",
    "amount": "500",
}

response = requests.get("https://api-app.qq-os.com/api/fiat/v1/rapid-buy-integration", params=params, headers=headers)

print([i.get("paymentMethod")["name"] for i in response.json()["data"]["matchOptimalAdvertListVo"]["optimals"]])
