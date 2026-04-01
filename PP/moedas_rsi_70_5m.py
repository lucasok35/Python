import ccxt
import pandas as pd
import time

def calculate_rsi(data, period=14):
    delta = data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def get_crypto_pairs_with_rsi_near_70(exchange, limit=100):
    rsi_threshold = 70
    pairs_near_rsi = []

    markets = exchange.load_markets()
    for symbol in markets:
        try:
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe='5m', limit=limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['rsi'] = calculate_rsi(df)

            if df['rsi'].iloc[-1] >= rsi_threshold - 1 and df['rsi'].iloc[-1] <= rsi_threshold + 1:
                pairs_near_rsi.append(symbol)
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            continue

    return pairs_near_rsi

def main():
    exchange = ccxt.binance()
    pairs_near_rsi = get_crypto_pairs_with_rsi_near_70(exchange)
    print(f"Crypto pairs with RSI near 70 on 5-minute chart: {pairs_near_rsi}")

if __name__ == "__main__":
    main()
