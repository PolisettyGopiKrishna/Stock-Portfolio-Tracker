import requests
import pandas as pd
from datetime import datetime

# Define API key and base URL
API_KEY = "<YOUR_API_KEY>"
BASE_URL = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol="

# User data
portfolio = {}

# Function to get real-time stock data
def get_stock_data(symbol):
    url = f"{BASE_URL}{symbol}&apikey={API_KEY}"
    response = requests.get(url)
    response.raise_for_status()

    try:
        data = response.json()["Global Quote"]
    except requests.exceptions.JSONDecodeError:
        print(f"Error decoding data for {symbol}:")
        print(f"Response content:\n{response.content}")
        print(f"Response headers:\n{response.headers}")
        print("Please check your API key or symbol.")
        return None

    return data

# Function to add a stock to the portfolio
def add_stock(symbol, quantity):
    if symbol in portfolio:
        print(f"Stock {symbol} already exists in your portfolio.")
    else:
        stock_data = get_stock_data(symbol)
        if stock_data:
            portfolio[symbol] = {
                "quantity": quantity,
                "price": float(stock_data["05. price"]),
                "total_cost": quantity * float(stock_data["05. price"])
            }
            print(f"Stock {symbol} added successfully to your portfolio.")
        else:
            print(f"Invalid stock symbol: {symbol}")

# Function to remove a stock from the portfolio
def remove_stock(symbol):
    if symbol in portfolio:
        del portfolio[symbol]
        print(f"Stock {symbol} removed successfully from your portfolio.")
    else:
        print(f"Stock {symbol} does not exist in your portfolio.")

# Function to calculate total portfolio value
def get_portfolio_value():
    total_value = 0
    for symbol, data in portfolio.items():
        stock_data = get_stock_data(symbol)
        latest_price = float(stock_data["05. price"])
        total_value += data["quantity"] * latest_price
    return total_value

# Function to show portfolio details
def show_portfolio():
    if portfolio:
        print("-" * 50)
        print("Portfolio Details:")
        print("-" * 50)
        print("| Symbol | Quantity | Price | Total Cost | Current Value |")
        print("|---|---|---|---|---|")
        for symbol, data in portfolio.items():
            stock_data = get_stock_data(symbol)
            latest_price = float(stock_data["05. price"])
            current_value = data["quantity"] * latest_price
            print(f"| {symbol} | {data['quantity']} | ${data['price']:.2f} | ${data['total_cost']:.2f} | ${current_value:.2f} |")
        total_value = get_portfolio_value()
        print("-" * 50)
        print(f"Total Portfolio Value: ${total_value:.2f}")
        print("-" * 50)
    else:
        print("Your portfolio is empty.")

# Main program loop
while True:
    print("-" * 50)
    print("1. Add Stock")
    print("2. Remove Stock")
    print("3. Show Portfolio")
    print("4. Exit")
    print("-" * 50)

    choice = input("Enter your choice: ")

    try:
        choice = int(choice)
    except ValueError:
        print("Invalid option. Please enter a number.")
        continue

    if choice == 1:
        symbol = input("Enter stock symbol: ").upper()
        quantity = int(input("Enter quantity: "))
        add_stock(symbol, quantity)
    elif choice == 2:
        symbol = input("Enter stock symbol: ").upper()
        remove_stock(symbol)
    elif choice == 3:
        show_portfolio()
    elif choice == 4:
        print("Thank you for using the stock portfolio tracker!")
        break
