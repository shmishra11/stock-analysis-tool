# Stock Analysis Tool

A Python-based stock analysis tool that uses historical market data to calculate returns, volatility, maximum drawdown, and historical risk. The program also allows users to graph stock prices and compare two stocks over the same time period.

## Features
- Validate stock tickers
- Validate trading dates
- Calculate average daily return
- Calculate daily volatility
- Calculate annualized volatility
- Calculate maximum drawdown
- Generate a historical risk score (0–100)
- Graph historical closing prices
- Compare two stocks using performance and risk metrics
- Terminal-based interactive menu

## Technologies
- Python
- yfinance
- Matplotlib

## Project Structure
- `main.py` — Runs the program and handles the terminal menu
- `functions.py` — Contains the stock validation, analysis, comparison, and graphing functions
- `requirements.txt` — Lists the required Python libraries

## How It Works
The program retrieves historical stock data using yFinance based on a user-selected ticker and date range.
It calculates several performance and risk metrics, including average daily return, daily volatility, annualized volatility, and maximum drawdown.
The historical risk score is a custom 0–100 metric that combines annualized volatility and maximum drawdown to provide a simplified measure of historical risk.
The program can also compare two stocks using the same metrics and display their historical closing prices graphically.

## Installation
Clone the repository and install the required libraries:
```bash
pip install -r requirements.txt
```

## Usage
Run the program with:
```bash
python main.py
```

## Disclaimer
This project is for educational purposes only and is not financial advice.
The risk score is a custom metric based on historical stock performance and should not be interpreted as a prediction of future performance.
