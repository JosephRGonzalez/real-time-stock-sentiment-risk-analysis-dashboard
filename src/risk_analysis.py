def calculate_sharpe_ratio(stock_data):
    stock_data['Returns'] = stock_data['Close'].pct_change()
    mean_return = stock_data['Returns'].mean()
    std_dev = stock_data['Returns'].std()
    return mean_return / std_dev
