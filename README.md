# 📈 Real-Time Stock Sentiment & Risk Analysis Dashboard

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An interactive web dashboard built with **Streamlit**, **Plotly**, and **Python** to fetch real-time stock data, perform sentiment analysis on news articles, and calculate risk metrics.

 <!-- ![Dashboard Screenshot](insert-screenshot-here)  (Optional: you can add a screenshot later) -->

---

## 🚀 Features

- 🔍 **Real-time Stock Data** (price history, metrics, financials)
- 📰 **Latest News Articles** related to the stock
- 😊 **Sentiment Analysis** (Positive / Negative / Neutral)
- 📊 **Risk Analysis** (Sharpe Ratio, Historical Volatility)
- 🎨 **Responsive UI** with stylish column layouts
- ⚡ **Fast & Lightweight** with caching and efficient APIs

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name
```

### 2. (Optional) Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate    # On Windows use: venv\Scripts\activate
```

### 3. Install Required Packages

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root of the project:

```bash
# .env file
NEWS_API_KEY=your_newsapi_key_here
```

> 🔑 **Note:** You’ll need a [NewsAPI](https://newsapi.org/) key to fetch news headlines.

### 5. Run the App

```bash
streamlit run dashboard.py
```

---

## 🧩 Project Structure

```
├── data
├── notebooks
├── dashboard.py
├── requirements.txt
├── .env               # (you create this manually)
├── src/
│   ├── fetch_stock_data.py
│   ├── news_api.py
│   ├── risk_analysis.py
│   └── sentiment_analysis.py
├── LICENSE
└── README.md

```

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).