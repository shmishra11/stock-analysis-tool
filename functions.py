import yfinance as yf
from datetime import datetime, timedelta
import statistics
import math
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# --------------------------------------------------
# VALID TICKER CHECKER
# --------------------------------------------------
def isValidTicker():
    ticker = input("Enter a Company Ticker: ")

    # Small date range used only to test whether the ticker returns data
    t1 = datetime.strptime("2026-01-01", "%Y-%m-%d")
    t2 = datetime.strptime("2026-01-03", "%Y-%m-%d")

    while True:
        # Try downloading a small amount of data for the ticker
        test = yf.download(ticker, start=t1, end=t2, progress=False)

        # If no data was returned, the ticker is probably invalid
        if test.empty:
            ticker = input("Ticker not found. Please try again: ")
        else:
            break
    return ticker

# --------------------------------------------------
# VALID DATE CHECKER
# --------------------------------------------------
def is_valid_date(ticker, message):
    date_format = "%Y-%m-%d"
    date_string = input(message)

    while True:
        try:
            # Try converting the user's input into a datetime object
            t = datetime.strptime(date_string, date_format)

            # Download data for just this date
            # End date is one day later because yfinance's end date is exclusive
            test = yf.download(ticker, start=t, end=t + timedelta(days=1), progress=False)

            # If there is no data, the stock market wasn't open that day
            if test.empty:
                date_string = input("Market was not open on that date. Try Again: ")
            else:
                break

        # Runs if the user entered something that isn't YYYY-MM-DD
        except ValueError:
            date_string = input("Unusable Date. Try Again (Formatting - YYYY-MM-DD): ")

    return t

# --------------------------------------------------
# USER INPUTS
# --------------------------------------------------
def userInputs():
    ticker = isValidTicker()

    # Get a valid starting date
    stdate = is_valid_date(ticker, "Enter a Start Date: ")
    # Get a valid ending date
    enddate = is_valid_date(ticker, "Enter an End Date: ")

    while stdate >= enddate:
        print("The Start Date must be before the End Date.")
        stdate = is_valid_date(ticker, "Enter a Start Date: ")
        enddate = is_valid_date(ticker, "Enter an End Date: ")


    return ticker, stdate, enddate


# --------------------------------------------------
# GET DATA
# --------------------------------------------------
def getData(ticker, stdate, enddate):
    return yf.download(ticker, start=stdate, end=enddate + timedelta(days=1), progress=False)


# --------------------------------------------------
# GRAPHING
# --------------------------------------------------
def graphing_prices(ticker, stdate, enddate, data):

    ind1 = data.index.get_loc(stdate)
    ind2 = data.index.get_loc(enddate)

    closing_prices = []
    dates = []
    while ind1 <= ind2:
        price = data["Close"].iloc[ind1][ticker]
        closing_prices.append(round(price, 3))
        dates.append(data.index[ind1])
        ind1 += 1

    plt.figure(figsize=(15, 6))
    plt.plot(dates, closing_prices, 'g--')

    plt.title(
        f'Closing Prices of {ticker} between '
        f'{stdate.strftime("%Y-%m-%d")} and {enddate.strftime("%Y-%m-%d")}'
    )

    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.grid(visible=True, which="both", axis="both")

    # Automatically choose how many dates to display
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())

    # Format the dates
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.xticks(rotation=45)

    plt.show()

# --------------------------------------------------
# DAILY RETURNS
# --------------------------------------------------
def dailyReturns(ticker, stdate, enddate, data):


    ind1 = data.index.get_loc(stdate)
    ind2 = data.index.get_loc(enddate)
    daily_returns = []

    # Compare each trading day's closing price
    # with the closing price of the following trading day
    while ind1 != ind2:

        p1 = data["Close"].iloc[ind1][ticker]
        p2 = data["Close"].iloc[ind1 + 1][ticker]

        daily_returns.append(float((p2 - p1) / p1))

        ind1 += 1

    return daily_returns

# --------------------------------------------------
# AVERAGE RETURNS
# --------------------------------------------------
def avgReturns(ticker, stdate, enddate, data):
    daily_returns = dailyReturns(ticker, stdate, enddate, data)
    return sum(daily_returns) / len(daily_returns)

# --------------------------------------------------
# MAXIMUM DRAWDOWN
# --------------------------------------------------

def maxDrawdown(ticker, stdate, enddate, data):


    ind1 = data.index.get_loc(stdate)
    ind2 = data.index.get_loc(enddate)

    max_price = float(data["Close"].iloc[ind1][ticker])
    max_drawdown = 0
    #  Find Max Drawdown
    for price in data["Close"].iloc[ind1:ind2 + 1][ticker]:

        if price > max_price:
            max_price = price

        # Calculate how far the current price has fallen
        # from the highest price seen so far
        drawdown = (price - max_price) / max_price

        # Drawdowns are negative, so a smaller value
        # means a larger loss
        if drawdown < max_drawdown:
            max_drawdown = drawdown


    return max_drawdown

# --------------------------------------------------
# DAILY VOLATILITY
# --------------------------------------------------
def dailyVolatility(ticker, stdate, enddate, data):
    daily_returns = dailyReturns(ticker, stdate, enddate, data)
    return statistics.stdev(daily_returns)

# --------------------------------------------------
# ANNUAL VOLATILITY
# --------------------------------------------------
def annualVolatility(ticker, stdate, enddate, data):
    daily_volatility = dailyVolatility(ticker, stdate, enddate, data)
    return math.sqrt(252) * daily_volatility

# --------------------------------------------------
# EVALUATE RISK
# --------------------------------------------------
def evaluateRisk(ticker, stdate, enddate, data):
    annvolatility = annualVolatility(ticker, stdate, enddate, data) * 100
    maxdrawdown = abs(maxDrawdown(ticker, stdate, enddate, data)) * 100
    volatility_score = min(annvolatility / 50 * 100, 100)
    drawdown_score = min(maxdrawdown / 50 * 100, 100)

    risk_score = volatility_score * 0.6 + drawdown_score * 0.4

    if risk_score < 33:
        risk_level = "LOW"
    elif risk_score < 66:
        risk_level = "MODERATE"
    else:
        risk_level = "HIGH"

    return risk_score, risk_level 

# --------------------------------------------------
# COMPARE
# --------------------------------------------------
def comparetwostocks(ticker, stdate, enddate, data, ticker2, data2):
    avgdreturn1 = avgReturns(ticker, stdate, enddate, data)
    avgdreturn2 = avgReturns(ticker2, stdate, enddate, data2)
    dvola1 = dailyVolatility(ticker, stdate, enddate, data)
    dvola2 = dailyVolatility(ticker2, stdate, enddate, data2)
    avola1 = annualVolatility(ticker, stdate, enddate, data)
    avola2 = annualVolatility(ticker2, stdate, enddate, data2)
    maxdraw1 = maxDrawdown(ticker, stdate, enddate, data)
    maxdraw2 = maxDrawdown(ticker2, stdate, enddate, data2)
    riskscore1, risklevel1 = evaluateRisk(ticker, stdate, enddate, data)
    riskscore2, risklevel2 = evaluateRisk(ticker2, stdate, enddate, data2)

    return avgdreturn1, avgdreturn2, dvola1, dvola2, avola1, avola2, maxdraw1, maxdraw2, riskscore1, risklevel1, riskscore2, risklevel2
# --------------------------------------------------
# PRINT MENU
# --------------------------------------------------
def printMenu():
    print("1. Print Average Daily Return as a Percentage.")
    print("2. Print Maximum Drawdown as a Percentage.")
    print("3. Print Daily Volatility as a Percentage.")
    print("4. Print Annual Volatility as a Percentage.")
    print("5. Graph Stock Prices.")
    print("6. New Stock Analysis.")
    print("7. Evaluate Historical Risk Based on Past Performance.")
    print("8. Compare with Another Stock.")
    print("9. Exit the Program.  \n")