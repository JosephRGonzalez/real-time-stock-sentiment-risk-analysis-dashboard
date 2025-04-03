import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up your API key
API_KEY = os.getenv('NEWS_API_KEY')  # Environment variables for security

# Function to fetch news articles
def get_news(query):
    url = f'https://newsapi.org/v2/everything?q={query}&apiKey={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['articles']
    else:
        return None

# Example usage:
if __name__ == '__main__':
    query = 'Apple stock'  # You can adjust this for any stock
    news = get_news(query)
    if news:
        for article in news[:5]:  # Display first 5 articles
            print(f"Title: {article['title']}")
            print(f"Source: {article['source']['name']}")
            print(f"Description: {article['description']}")
            print(f"URL: {article['url']}\n")
