import requests
import streamlit as st

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
