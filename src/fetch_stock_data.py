from alpha_vantage.timeseries import TimeSeries
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the Alpha Vantage API key
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')





# Initialize the TimeSeries class from alpha_vantage
def get_stock_data(symbol):
    ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY, output_format='pandas')

    # Get intraday data (you can change the interval, here it's set to 1min)
    data, meta_data = ts.get_intraday(symbol=symbol, interval='1min', outputsize='full')

    # You can also use get_daily(), get_weekly(), or get_monthly() for other timeframes
    return data


# Example usage:
if __name__ == '__main__':
    symbol = 'AAPL'  # Apple stock symbol
    data = get_stock_data(symbol)
    print(data.head())
