import requests
import tweepy
import praw

# Function to fetch trending coins from CoinGecko
def get_top_trending_coins():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {'vs_currency': 'usd', 'order': 'volume_desc', 'per_page': 10, 'page': 1}
    response = requests.get(url, params=params)
    return response.json()

# Function to fetch trending tweets from Twitter
def search_trending_tweets(query, count=10):
    tweets = tweepy.Cursor(api.search_tweets, q=query, lang='en').items(count)
    tweet_list = [tweet.text for tweet in tweets]
    return tweet_list

# Reddit mentions function
def get_reddit_mentions(subreddit="cryptocurrency", keyword="memecoin"):
    posts = reddit.subreddit(subreddit).search(keyword, limit=10)
    return [submission.title for submission in posts]

# Combine all sources to look for potential memecoin
def check_memecoin_potential():
    trending_coins = get_top_trending_coins()
    for coin in trending_coins:
        coin_name = coin['name'].lower()
        tweets = search_trending_tweets(coin_name, count=10)
        reddit_posts = get_reddit_mentions(keyword=coin_name)
        
        if len(tweets) > 5 or len(reddit_posts) > 3:
            print(f"Potential Memecoin: {coin['name']}")
            print(f"Price: {coin['current_price']} USD")
            print(f"24h Change: {coin['price_change_percentage_24h']}%")
            print(f"Tweets: {len(tweets)} mentions")
            print(f"Reddit: {len(reddit_posts)} mentions\n")

check_memecoin_potential()
