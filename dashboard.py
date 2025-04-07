import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import time
import os
from dotenv import load_dotenv
import traceback
import plotly.express as px

from src.fetch_stock_data import fetch_stock_data
from src.news_api import fetch_news
from src.sentiment_analysis import analyze_sentiment_vader
from src.risk_analysis import calculate_sharpe_ratio

load_dotenv()

st.set_page_config(page_title='Stock Sentiment & Risk Analysis', layout='wide')

# Sidebar - User Inputs
st.sidebar.header('Stock Analysis Settings')
symbol = st.sidebar.text_input('Enter Stock Symbol', 'AAPL').upper()
period = st.sidebar.selectbox('Select Time Period', ['1d', '5d', '30d', '1mo', '6mo', '1y'])
interval = st.sidebar.selectbox('Select Interval', ['1m', '5m', '15m', '30m', '1h', '1d'])
sentiment_filter = st.sidebar.selectbox("Filter by Sentiment", ["All", "Positive", "Negative", "Neutral"])
refresh = st.sidebar.slider('Auto-refresh Interval (sec)', 10, 300, 60)

# Initialize session state
if 'visible_articles' not in st.session_state:
    st.session_state.visible_articles = 5

# Caching logic to avoid redundant API calls
@st.cache_data(ttl=refresh)
def get_data(symbol, period, interval):
    return fetch_stock_data(symbol, period, interval)

@st.cache_data(ttl=refresh)
def get_news_sentiment(symbol, api_key):
    news = fetch_news(symbol, api_key)
    sentiments = [analyze_sentiment_vader(article['title']) for article in news]
    return news, sentiments

# Fetch Stock Data
try:
    data = get_data(symbol, period, interval)

    if data is not None and isinstance(data, pd.DataFrame) and not data.empty and len(data) >= 2:
        current_price = float(data['Close'].iloc[-1])
        previous_price = float(data['Close'].iloc[-2])
        price_change = current_price - previous_price
        price_change_pct = (price_change / previous_price) * 100
        change_sign = "+" if price_change > 0 else ""

        st.markdown("### 📈 Stock Overview")
        st.metric(
            label=f"{symbol} - Current Price",
            value=f"${current_price:.2f}",
            delta=f"{change_sign}{price_change:.2f} ({change_sign}{price_change_pct:.2f}%)"
        )

        st.write(f"Displaying {symbol} Stock Data:")
        st.dataframe(data)
    else:
        st.warning("Insufficient stock data to calculate current price.")

except Exception as e:
    st.error(f"Error fetching stock data: {e}")
    st.text(traceback.format_exc())

# Line chart for stock price
chart_data = pd.DataFrame(data['Close'])
st.subheader(f"{symbol} Closing Price Over Time")
st.line_chart(chart_data)

# News Sentiment Section
api_key = os.getenv('NEWS_API_KEY')
if api_key:
    try:
        news, sentiments = get_news_sentiment(symbol, api_key)

        filtered_articles = [
            (article, sentiment)
            for article, sentiment in zip(news, sentiments)
            if sentiment_filter == "All" or sentiment == sentiment_filter
        ]
        filtered_articles.sort(key=lambda x: x[0]['publishedAt'], reverse=True)

        with st.container():
            st.markdown("## 🧠 Sentiment Analysis")

            if filtered_articles:
                latest_sentiment = filtered_articles[0][1]
                sentiment_display = f"Current Sentiment: {latest_sentiment}"
                sentiment_text_color = {"Positive": "green", "Negative": "red", "Neutral": "orange"}

                st.markdown(f'<h1 style="color: {sentiment_text_color[latest_sentiment]};">{sentiment_display}</h1>',
                            unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                sentiment_counts = pd.Series(sentiments).value_counts()
                sentiment_labels = sentiment_counts.index.tolist()
                sentiment_values = sentiment_counts.values.tolist()

                pie_chart = go.Figure(data=[go.Pie(
                    labels=sentiment_labels,
                    values=sentiment_values,
                    hole=0.3,
                    textinfo="percent+label",
                    marker=dict(colors=['orange', 'green', 'red'])
                )])

                pie_chart.update_layout(
                    title=f"Sentiment Distribution for {symbol}",
                    title_x=0.5
                )

                st.plotly_chart(pie_chart, use_container_width=True)

            with col2:
                sentiment_dates = [article['publishedAt'][:10] for article in news]
                sentiment_trend_data = {
                    'date': sentiment_dates,
                    'sentiment': sentiments
                }
                sentiment_trend_df = pd.DataFrame(sentiment_trend_data)
                sentiment_trend_df['date'] = pd.to_datetime(sentiment_trend_df['date'])
                sentiment_trend_df_grouped = sentiment_trend_df.groupby(
                    [sentiment_trend_df['date'], 'sentiment']).size().unstack(fill_value=0)

                sentiment_trend_figure = go.Figure()
                for sentiment in sentiment_trend_df_grouped.columns:
                    sentiment_trend_figure.add_trace(
                        go.Scatter(
                            x=sentiment_trend_df_grouped.index,
                            y=sentiment_trend_df_grouped[sentiment],
                            mode='lines',
                            name=sentiment
                        )
                    )

                sentiment_trend_figure.update_layout(
                    title=f"Sentiment Trend for {symbol}",
                    xaxis_title='Date',
                    yaxis_title='Frequency',
                    showlegend=True
                )

                st.plotly_chart(sentiment_trend_figure, use_container_width=True)

            st.markdown("### 📰 Related News Articles")

            if filtered_articles:
                st.write(f"Showing {min(st.session_state.visible_articles, len(filtered_articles))} articles.")
                col1, col2 = st.columns(2)
                for i, (article, sentiment) in enumerate(filtered_articles[:st.session_state.visible_articles]):
                    timestamp = article.get('publishedAt', 'Unknown Time')
                    sentiment_text_color = {"Positive": "green", "Negative": "red", "Neutral": "orange"}

                    with (col1 if i % 2 == 0 else col2):
                        with st.container():
                            st.markdown(f"""
                            <div style="
                                border-radius: 15px; 
                                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                                padding: 20px;
                                background-color: #f9f9f9;
                                margin-bottom: 20px;
                                transition: transform 0.3s ease-in-out;
                                cursor: pointer;
                            " onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'">
                                <h4 style="margin-bottom: 10px; font-size: 1.2em;">
                                    <a href="{article['url']}" target="_blank" style="text-decoration: none; color: #2c3e50;">
                                        {article['title']}
                                    </a>
                                </h4>
                                <p style="margin: 0 0 5px 0;">
                                    <strong>Sentiment:</strong> 
                                    <span style="font-weight: bold; color: {sentiment_text_color[sentiment]};">
                                        {sentiment}
                                    </span>
                                </p>
                                <p style="font-size: 0.9em; color: #888;">🕒 {timestamp}</p>
                            </div>
                            """, unsafe_allow_html=True)

                if st.session_state.visible_articles < len(filtered_articles):
                    if st.button("🔽 View More"):
                        st.session_state.visible_articles += 5

            else:
                st.warning("No articles found with the selected sentiment filter.")

    except Exception as e:
        st.error(f"Error fetching or analyzing news: {e}")

else:
    st.error("Missing NEWS_API_KEY in environment.")

# Sharpe Ratio
if st.sidebar.button('Calculate Sharpe Ratio'):
    try:
        ratio = calculate_sharpe_ratio(data)
        st.metric(label=f'Sharpe Ratio for {symbol}', value=round(ratio, 4))
    except Exception as e:
        st.error(f"Error calculating Sharpe Ratio: {e}")

# Auto Refresh Notice (handled above via cache ttl)
st.markdown(f"<p style='color:gray; font-size:0.9em;'>Auto-refreshing every {refresh} seconds.</p>", unsafe_allow_html=True)
