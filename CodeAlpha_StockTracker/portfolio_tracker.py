import csv
import os

STOCK_PRICES = {
    "AAPL": 185.50,
    "TSLA": 245.20,
    "GOOGL": 142.80,
    "MSFT": 415.30,
    "AMZN": 178.90,
    "NVDA": 890.40,
    "META": 485.10
}


def display_menu():
    print("\n" + "=" * 45)
    print("      CODEALPHA PYTHON INTERNSHIP        ")
    print("      TASK 2: STOCK PORTFOLIO TRACKER    ")
    print("=" * 45)
    print("1. View Market Prices")
    print("2. View Current Portfolio & Total Value")
    print("3. Add / Update Stock Position")
    print("4. Remove Stock Position")
    print("5. Export Portfolio Report (CSV)")
    print("6. Exit Program")
    print("=" * 45)


def view_market_prices():
    print("\n--- Live Market Price Board ---")
    print(f"{'Ticker':<10} | {'Price ($)':<10}")
    print("-" * 25)
    for ticker, price in STOCK_PRICES.items():
        print(f"{ticker:<10} | ${price:<10.2f}")


def view_portfolio(portfolio):
    if not portfolio:
        print("\n📭 Your portfolio is currently empty.")
        return 0.0

    print("\n---------------------------------------------")
    print(f"{'Ticker':<8} | {'Qty':<6} | {'Price ($)':<10} | {'Total ($)':<10}")
    print("-" * 45)

    total_portfolio_value = 0.0
    for ticker, quantity in portfolio.items():
        price = STOCK_PRICES[ticker]
        item_value = price * quantity
        total_portfolio_value += item_value
        print(f"{ticker:<8} | {quantity:<6} | ${price:<9.2f} | ${item_value:<9.2f}")

    print("-" * 45)
    print(f"💰 Total Portfolio Value: ${total_portfolio_value:.2f}")
    print("---------------------------------------------")
    return total_portfolio_value


def add_stock(portfolio):
    view_market_prices()
    ticker = input("\nEnter stock ticker to add/update: ").upper().strip()

    if ticker not in STOCK_PRICES:
        print(f"❌ Error: '{ticker}' is not available in the market database.")
        return

    while True:
        try:
            quantity = int(input(f"Enter quantity of shares for {ticker}: "))
            if quantity < 0:
                print("❌ Quantity cannot be negative.")
                continue
            elif quantity == 0:
                if ticker in portfolio:
                    del portfolio[ticker]
                    print(f"🗑️ Removed {ticker} from portfolio (quantity set to 0).")
                else:
                    print("⚠️ Quantity is 0. No stock added.")
                return
            break
        except ValueError:
            print("❌ Invalid input. Please enter a valid integer for shares.")

    portfolio[ticker] = portfolio.get(ticker, 0) + quantity if ticker in portfolio else quantity
    print(f"✅ Successfully updated {ticker}: Now holding {portfolio[ticker]} shares.")


def remove_stock(portfolio):
    if not portfolio:
        print("\n📭 Your portfolio is empty. Nothing to remove.")
        return

    view_portfolio(portfolio)
    ticker = input("\nEnter the ticker symbol you want to remove: ").upper().strip()

    if ticker in portfolio:
        del portfolio[ticker]
        print(f"🗑️ Successfully removed {ticker} from your portfolio.")
    else:
        print(f"❌ Error: {ticker} is not present in your portfolio holdings.")


def export_portfolio(portfolio):
    if not portfolio:
        print("\n❌ Cannot export an empty portfolio.")
        return

    filename = "portfolio_report.csv"
    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Ticker", "Shares Owned", "Current Price ($)", "Total Value ($)"])

            total_value = 0.0
            for ticker, qty in portfolio.items():
                price = STOCK_PRICES[ticker]
                val = price * qty
                total_value += val
                writer.writerow([ticker, qty, f"{price:.2f}", f"{val:.2f}"])

            writer.writerow([])
            writer.writerow(["Net Portfolio Value", "", "", f"{total_value:.2f}"])

        print(f"📁 Portfolio successfully exported to '{os.path.abspath(filename)}'")
    except IOError:
        print("❌ Error writing file to local disk.")


def main():
    portfolio = {}

    while True:
        display_menu()
        choice = input("Select an option (1-6): ").strip()

        if choice == '1':
            view_market_prices()
        elif choice == '2':
            view_portfolio(portfolio)
        elif choice == '3':
            add_stock(portfolio)
        elif choice == '4':
            remove_stock(portfolio)
        elif choice == '5':
            export_portfolio(portfolio)
        elif choice == '6':
            print("\nThank you for using the CodeAlpha Stock Portfolio Tracker. Exiting...")
            break
        else:
            print("❌ Invalid selection. Please choose an option between 1 and 6.")


if __name__ == "__main__":
    main()