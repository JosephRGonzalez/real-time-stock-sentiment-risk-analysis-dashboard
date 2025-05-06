import requests
import tweepy
import streamlit as st
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time
import tweepy
import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

@st.cache_data(ttl=3600)
def fetch_news(query, api_key):
    url = f'https://newsapi.org/v2/everything?q={query}&apiKey={api_key}'
    response = requests.get(url)

    if response.status_code != 200:
        st.error(f"Error fetching news data: {response.status_code}")
        return []

    news_data = response.json()

    if 'articles' not in news_data:
        st.error(f"Error: 'articles' not found in the news API response.")
        st.json(news_data)
        return []

    return news_data['articles']


# Function to authenticate to the X API
def authenticate_x_api():
    bearer_token = os.getenv('X_API_BEARER_TOKEN')  # Set your Bearer Token in .env
    client = tweepy.Client(bearer_token=bearer_token)
    return client





# Function to authenticate to the X API (formerly Twitter API)
def authenticate_x_api():
    bearer_token = os.getenv('X_API_BEARER_TOKEN')  # Set your Bearer Token in .env
    client = tweepy.Client(bearer_token=bearer_token)
    return client


# Fetch tweets related to a stock symbol with backoff logic for rate limits
@st.cache_data(ttl=3600)  # Cache for 1 hour (3600 seconds)
def fetch_tweets(symbol, count=100):
    client = authenticate_x_api()

    query = f'{symbol} -is:retweet'  # Remove cashtag operator if needed
    try:
        tweets = client.search_recent_tweets(query=query, tweet_fields=["created_at", "text"], max_results=count)
        return tweets.data
    except tweepy.errors.TooManyRequests as e:
        # Wait for the rate limit reset time (15 minutes)
        reset_time = e.response.headers.get('x-rate-limit-reset')
        if reset_time:
            reset_timestamp = int(reset_time)
            wait_time = reset_timestamp - int(time.time())  # Calculate wait time
            st.warning(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)  # Wait until rate limit is reset
        return fetch_tweets(symbol, count)  # Retry after waiting
    except Exception as e:
        st.error(f"Error fetching tweets: {e}")
        return []


# Analyze sentiment of tweets using VADER
def analyze_tweet_sentiment_vader(tweets):
    analyzer = SentimentIntensityAnalyzer()
    sentiments = []

    for tweet in tweets:
        sentiment_score = analyzer.polarity_scores(tweet['text'])
        sentiment = sentiment_score['compound']  # Compound score (ranges from -1 to 1)
        sentiments.append(sentiment)

    return sentiments
