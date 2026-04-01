import requests
import pandas as pd
from ta.momentum import RSIIndicator

# Definir parâmetros
RSI_THRESHOLD = 30
MIN_MARKET_CAP = 100_000_000  # 100 milhões de dólares
INTERVAL = "5m"
LIMIT = 100  # Número de candles para análise de RSI

# Função para obter informações de mercado de todas as moedas
def get_market_data():
    url = "https://api.binance.com/api/v3/ticker/24hr"
    response = requests.get(url)
    data = response.json()
    return [
        {"symbol": item["symbol"], "volume": float(item["quoteVolume"])}
        for item in data
    ]

# Função para calcular o RSI a partir do preço histórico
def get_rsi(symbol, interval=INTERVAL, limit=LIMIT):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume", "num_trades", "taker_buy_base", "taker_buy_quote", "ignore"])
    df["close"] = df["close"].astype(float)
    
    # Calcular o RSI
    rsi_indicator = RSIIndicator(df["close"], window=14)
    rsi = rsi_indicator.rsi().iloc[-1]
    return rsi

# Função para filtrar criptomoedas com RSI < 30 e valor de mercado > 100 milhões
def filter_cryptos_by_rsi_and_market_cap():
    cryptos = get_market_data()
    selected_cryptos = []
    for crypto in cryptos:
        symbol = crypto["symbol"]
        market_cap = crypto["volume"]
        
        if market_cap >= MIN_MARKET_CAP:
            rsi = get_rsi(symbol)
            if rsi < RSI_THRESHOLD:
                selected_cryptos.append({"symbol": symbol, "rsi": rsi, "market_cap": market_cap})
                
    return selected_cryptos

# Exibir resultados
selected_cryptos = filter_cryptos_by_rsi_and_market_cap()
print("Criptomoedas com RSI abaixo de 30 e valor de mercado acima de 100 milhões:")
for crypto in selected_cryptos:
    print(f"Símbolo: {crypto['symbol']}, RSI: {crypto['rsi']:.2f}, Market Cap: {crypto['market_cap']:.2f}")
