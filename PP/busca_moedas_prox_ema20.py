import requests
import pandas as pd
from ta.trend import EMAIndicator

# Parâmetros
EMA_THRESHOLD_PERCENTAGE = 1  # Diferença percentual máxima entre o preço atual e a EMA20
MIN_MARKET_CAP = 100_000_000  # 100 milhões de dólares
INTERVAL = "5m"
LIMIT = 50  # Número de candles para cálculo da EMA

# Função para obter informações de mercado de todas as moedas
def get_market_data():
    url = "https://api.binance.com/api/v3/ticker/24hr"
    response = requests.get(url)
    data = response.json()
    return [
        {"symbol": item["symbol"], "volume": float(item["quoteVolume"])}
        for item in data
    ]

# Função para calcular a EMA20 e verificar a proximidade
def is_close_to_ema(symbol, interval=INTERVAL, limit=LIMIT):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    data = response.json()
    
    # Verificar se o retorno contém dados suficientes
    if len(data) < limit:
        return False
    
    # Criar DataFrame com os dados
    df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume", "num_trades", "taker_buy_base", "taker_buy_quote", "ignore"])
    df["close"] = df["close"].astype(float)
    
    # Calcular a EMA20
    ema_indicator = EMAIndicator(df["close"], window=20)
    df["ema20"] = ema_indicator.ema_indicator()
    
    # Verificar a proximidade ao preço atual
    close_price = df["close"].iloc[-1]
    ema20_value = df["ema20"].iloc[-1]
    difference_percentage = abs(close_price - ema20_value) / ema20_value * 100
    
    return difference_percentage <= EMA_THRESHOLD_PERCENTAGE

# Função para filtrar criptomoedas com valor de mercado > 100 milhões e perto da EMA20
def filter_cryptos_by_ema_and_market_cap():
    cryptos = get_market_data()
    selected_cryptos = []
    for crypto in cryptos:
        symbol = crypto["symbol"]
        market_cap = crypto["volume"]
        
        if market_cap >= MIN_MARKET_CAP:
            try:
                if is_close_to_ema(symbol):
                    selected_cryptos.append({"symbol": symbol, "market_cap": market_cap})
            except Exception as e:
                print(f"Erro ao processar {symbol}: {e}")
                
    return selected_cryptos

# Exibir resultados
selected_cryptos = filter_cryptos_by_ema_and_market_cap()
print("Criptomoedas próximas à EMA20 e com valor de mercado acima de 100 milhões:")
for crypto in selected_cryptos:
    print(f"Símbolo: {crypto['symbol']}, Market Cap: {crypto['market_cap']:.2f}")
