import functions

ticker, stdate, enddate = functions.userInputs()
data = functions.getData(ticker, stdate, enddate)

# --------------------------------------------------
# OUTPUT
# --------------------------------------------------
print(f"\n\n---------- {ticker} Stock Analysis ----------  \n")
print("Please type the number of the respective function you want executed.\n")
functions.printMenu()

userdemand = input("Enter a command: ")
possiblecommands = "123456789"

while True:
    if userdemand not in possiblecommands or len(userdemand) != 1:
        print("Unable to understand command. Please type number only.")
    else:
        if userdemand == "1":
            avgreturn = functions.avgReturns(ticker, stdate, enddate, data)
            print(f"The average daily returns of {ticker} per day from {stdate.strftime('%d/%m/%Y')} to {enddate.strftime('%d/%m/%Y')} is: {round(avgreturn * 100, 2) }%.\n")

        elif userdemand == "2":
            maxdrawdown = functions.maxDrawdown(ticker, stdate, enddate, data)
            print(f"The maximum drawdown of {ticker} from {stdate.strftime('%d/%m/%Y')} to {enddate.strftime('%d/%m/%Y')} is: {round(maxdrawdown * 100, 2) }%\n")

        elif userdemand == "3":
            dailyvolatility = functions.dailyVolatility(ticker, stdate, enddate, data)
            print(f"The daily volatility of {ticker} from {stdate.strftime('%d/%m/%Y')} to {enddate.strftime('%d/%m/%Y')} is: {round(dailyvolatility * 100, 2) }%\n")

        elif userdemand == "4":
            annvolatility = functions.annualVolatility(ticker, stdate, enddate, data)
            print(f"The annual volatility of {ticker} based on dates from {stdate.strftime('%d/%m/%Y')} to {enddate.strftime('%d/%m/%Y')} is: {round(annvolatility * 100, 2) }%\n")

        elif userdemand == "5":
            functions.graphing_prices(ticker,stdate, enddate, data)
            print("\n")

        elif userdemand == "6":
            print("Please input new data to be analyzed.")
            ticker, stdate, enddate = functions.userInputs()
            data = functions.getData(ticker, stdate, enddate)
            print("Data has been updated. Future command will utilize updated data. \n")

        elif userdemand == "7":
            risk_score, risk_level = functions.evaluateRisk(ticker, stdate, enddate, data)
            print(f"Historical Risk Score: {round(risk_score, 0)}/100")
            print(f"Historical Risk Level: {risk_level} \n")

        elif userdemand == "8":
            ticker2 = functions.isValidTicker()
            data2 = functions.getData(ticker2, stdate, enddate)
            avgdreturn1, avgdreturn2, dvola1, dvola2, avola1, avola2, maxdraw1, maxdraw2, rs1, rl1, rs2, rl2 = functions.comparetwostocks(ticker,stdate,enddate,data,ticker2,data2)

            print("\n---------- Stock Comparison ----------")
            print(f"{'Metric':<20}{ticker:<15}{ticker2:<15}")
            print(f"{'Average':<20}{f'{avgdreturn1 * 100:.2f}%':<15}{f'{avgdreturn2 * 100:.2f}%':<15}")
            print(f"{'Daily Vol.':<20}{f'{dvola1 * 100:.2f}%':<15}{f'{dvola2 * 100:.2f}%':<15}")
            print(f"{'Annual Vol.':<20}{f'{avola1 * 100:.2f}%':<15}{f'{avola2 * 100:.2f}%':<15}")
            print(f"{'Max Drawdown':<20}{f'{maxdraw1 * 100:.2f}%':<15}{f'{maxdraw2 * 100:.2f}%':<15}")
            print(f"{'Risk Score':<20}{f'{rs1:.0f}/100':<15}{f'{rs2:.0f}/100':<15}")
            print(f"{'Risk Level':<20}{rl1:<15}{rl2:<15} \n")

        elif userdemand == "9":
            print("Thank you for using this program.")
            break

        print("Command processed. What other function would you like executed.")
        functions.printMenu()

    userdemand = input("Enter a command: ")

        

    
    