import ccxt
import requests

# Conectando à Bybit
bybit = ccxt.bybit({
    'enableRateLimit': True,
})

# Obter todos os pares de moedas na Bybit
bybit_markets = bybit.load_markets()
bybit_symbols = set(bybit_markets.keys())

# Função para obter moedas com maior volume de negociação no mercado em geral
def get_top_market_volumes():
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'usd',
        'order': 'volume_desc',
        'per_page': 100,  # Número de resultados desejados
    }
    response = requests.get(url, params=params)
    return response.json()

# Buscar criptomoedas com maior volume no mercado em geral
market_data = get_top_market_volumes()
top_market_symbols = {coin['symbol'].upper()+'/USDT' for coin in market_data if 'usdt' in coin['symbol'].lower()}

# Filtrar apenas as criptomoedas que estão listadas na Bybit
#top_symbols_on_bybit = top_market_symbols.intersection(bybit_symbols)

# Exibir as criptomoedas top que estão listadas na Bybit
print("Top moedas com maior volume de negociação no mercado, listadas na Bybit:")
#print("\n".join(top_symbols_on_bybit))
print("\n".join(top_market_symbols))
