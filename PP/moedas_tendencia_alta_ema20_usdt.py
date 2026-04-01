import requests
import pandas as pd
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator

# Parâmetros
EMA_THRESHOLD_PERCENTAGE = 1  # Diferença percentual máxima entre o preço atual e a EMA20
MIN_MARKET_CAP = 100_000_000  # 100 milhões de dólares
INTERVAL = "15m"
LIMIT = 50  # Número de candles para análise
RSI_UPTREND_THRESHOLD = 50  # RSI acima de 50 indica tendência de alta
PAIR_SUFFIX = "USDT"  # Considerar apenas pares com USDT

# Função para obter informações de mercado de todas as moedas
def get_market_data():
    url = "https://api.binance.com/api/v3/ticker/24hr"
    response = requests.get(url)
    data = response.json()
    return [
        {"symbol": item["symbol"], "volume": float(item["quoteVolume"])}
        for item in data if item["symbol"].endswith(PAIR_SUFFIX)
    ]

# Função para verificar proximidade à EMA20 e tendência de alta
def is_uptrend_and_close_to_ema(symbol, interval=INTERVAL, limit=LIMIT):
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
    
    # Verificar proximidade ao preço atual
    close_price = df["close"].iloc[-1]
    ema20_value = df["ema20"].iloc[-1]
    difference_percentage = abs(close_price - ema20_value) / ema20_value * 100
    
    # Calcular RSI para verificar tendência de alta
    rsi_indicator = RSIIndicator(df["close"], window=14)
    rsi = rsi_indicator.rsi().iloc[-1]
    
    # Confirmar tendência de alta (RSI > 50) e proximidade à EMA20
    return difference_percentage <= EMA_THRESHOLD_PERCENTAGE and rsi > RSI_UPTREND_THRESHOLD

# Função para filtrar criptomoedas no par USDT com valor de mercado > 100 milhões e em tendência de alta
def filter_cryptos_by_ema_trend_and_market_cap():
    cryptos = get_market_data()
    selected_cryptos = []
    for crypto in cryptos:
        symbol = crypto["symbol"]
        market_cap = crypto["volume"]
        
        if market_cap >= MIN_MARKET_CAP:
            try:
                if is_uptrend_and_close_to_ema(symbol):
                    selected_cryptos.append({"symbol": symbol, "market_cap": market_cap})
            except Exception as e:
                print(f"Erro ao processar {symbol}: {e}")
                
    return selected_cryptos

# Exibir resultados
selected_cryptos = filter_cryptos_by_ema_trend_and_market_cap()
print("Criptomoedas no par USDT próximas à EMA20, em tendência de alta e com valor de mercado acima de 100 milhões:")
for crypto in selected_cryptos:
    print(f"Símbolo: {crypto['symbol']}, Market Cap: {crypto['market_cap']:.2f}")
