# Below are the 'imports' used to run the API and the strategy.
import base64
import datetime
import json
from typing import Any, Dict, Optional
import uuid
import requests
import time
from cryptography.hazmat.primitives.asymmetric import ed25519

#Below is the 'main' Python Code for the strategy
def main():


    """
    This 'TRADING STRATEGY' bot code is designed to take advantage of the
    Robinhood Crypto Trading API (1.0.0) sample Python script.

    The bot follows a simple tading strategy that relies an market fluctuation.
    to generate gain. The bot maintans a 50% to 50% balace value ratio
    between your Robinhood Account's [Buying Power] and [ETH-USD Holdings Value].
    * As your [ETH-USD Holdings Value] increases the bot will spill over profit into
      your [Buying Power].
    * As your [ETH-USD Holdings Value] decreases the bot will use funds from your
      [Buying Power] to purchase ETH-USD at the lower price.
    * You can set Buy and Sell Thresholds to prevent the bot from trading before a
      reasonable Market change in value occurs. 
    * By adjusting the variables, you can also control how many times the code Loops,
      the Wait Time in secconds befor the next Loop.
    
    Adjust the settings to fit your needs. Happy trading!
    """


# VARIABLES for TRADING
    # Set the number of times the Loop will iterate
    num_iterations = 10000
    # Specify sleep_time in seconds to wait befor next trade attempt.
    sleep_time = (5 * 60)

    # Specify Buy and Sell Trading Thresholds Exampe: 5.00
    threshold_buy = 5.00
    threshold_sell = 5.00

    # Specify if ACTUAL REAL LIVE Buy/Sell ("YES")
    live_buy = "YES"
    live_sell = "YES"

#Begin the Loops    
    for i in range(num_iterations):
        

# Get the Account Information
        api_trading_client = CryptoAPITrading()
        account_data = api_trading_client.get_account()
        # Extract (buying_power) and convert to float
        buying_power = float(account_data['buying_power'])
        print("")
        print("Buying Power:", buying_power)
    

# Get the ETH holding info
        eth_holdings = api_trading_client.get_holdings('ETH')
        # Extract (total_quantity) and convert to float
        # Extract (quantity_available_for_trading) and convert to float
        eth_holding = eth_holdings['results'][0] 
        total_quantity = eth_holding['total_quantity']
        eth_available_for_trading = eth_holding['quantity_available_for_trading']
        print(f"Total ETH Coin Holdings : {total_quantity}")
        print(f"ETH Coin Available trade: {eth_available_for_trading}")
    

# Get the ETH best Bid and Ask Prices
        eth_bid_askings = api_trading_client.get_best_bid_ask('ETH-USD')
        # Extract (ask_inclusive_of_buy_spread) and convert to float
        # Extract (price) and convert to float
        # Extract (bid_inclusive_of_buy_spread) and convert to float
        eth_data = eth_bid_askings['results'][0]
        try:
          eth_ask = float(eth_data['ask_inclusive_of_buy_spread'])
        #  eth_ask = (5276.15) # uncomment to inject fake price eth_ask = (3716.0185916)
          eth_price = float(eth_data['price'])
        #  eth_price = (5276.15) # uncomment to inject fake price eth_price = (3699.3992958)
          eth_bid = float(eth_data['bid_inclusive_of_sell_spread'])
        #  eth_bid = (5276.15) # uncomment to inject fake price eth_bid = (3682.78)
        except ValueError:
          print("Price values are not numbers")  # Handle non-numeric values
        print(f"Ask Price: {eth_ask}")
        print(f"Price    : {eth_price}")
        print(f"Bid Price: {eth_bid}")

        eth_usd_val_ask = float(eth_ask) * float(total_quantity)
        print("USD Ask Value of ETH: ", eth_usd_val_ask)
        eth_usd_val = float(eth_price) * float(total_quantity)
        print("USD Value of ETH    : ", eth_usd_val)
        eth_usd_val_bid = float(eth_bid) * float(total_quantity)
        print("USD Bid Value of ETH: ", eth_usd_val_bid)


# Check for Buy/Sell Opportunities using retrieved data

# Buy Action
        buy_amount = (buying_power - eth_usd_val_ask) * 0.5   # Calculate 50% of the difference
        print("Checking Opportunities to Buy....")
        if buy_amount > threshold_buy:
            print(f"I need to Buy: ${buy_amount:.2f}")
            eth_to_buy = float(buy_amount) / float(eth_price)

            # Ensure the calculated quantity doesn't exceed available buying power (adjusted for potential fees)
            # Assuming a 0.1% fee
            fee_rate = 0.001
            max_buy_power = float(buying_power) * (1 - fee_rate)
            eth_to_buy = min(float(eth_to_buy), float(max_buy_power) / float(eth_price))  # Clamp to available buying power

            # Place the order with the calculated asset_quantity
            formatted_quantity = f"{eth_to_buy:.6f}"

            if live_buy == "YES":
                print("LIVE BUY TRADING")
                order = api_trading_client.place_order(
                    str(uuid.uuid4()),
                    "buy",
                    "market",
                    "ETH-USD",
                    {"asset_quantity": formatted_quantity}  # Convert to string for the API
                )
            else:
                print("SIMULATED BUY TRADING")

            # Print confirmation message with the amount of ETH bought
            print(f"Bought {eth_to_buy:.6f} ETH for approximately ${buy_amount:.2f}")


# Sell Action
        sell_amount = (eth_usd_val_bid - buying_power) * 0.5  # Calculate 50% of the difference
        print("Checking Opportunities to Sell...")
        if sell_amount > threshold_sell:
            print(f"I need to Sell: ${sell_amount:.2f}")
    
            # Calculate the number of ETH units to sell based on sell_amount and current price
            eth_to_sell = float(sell_amount) / float(eth_price)

            # Ensure the calculated quantity doesn't exceed available ETH
            eth_to_sell = min(float(eth_to_sell), float(total_quantity))  # Clamp to available quantity

            # Place the order with the calculated asset_quantity
            
            formatted_quantity = f"{eth_to_sell:.6f}"

            if live_sell == "YES":
                print("LIVE SELL TRADING")
                order = api_trading_client.place_order(
                    str(uuid.uuid4()),
                    "sell",
                    "market",
                    "ETH-USD",
                    {"asset_quantity": formatted_quantity}  # Convert to string for the API
                )
            else:
                print("SIMULATED SELL TRADING")

            print(str(eth_to_sell))
            print(f"Sold {eth_to_sell:.6f} ETH for approximately ${sell_amount:.2f}")
        print(f"Iteration {i+1} compleated.")
        print("")

# Sleep for the specified time before each iteration (except the last iteration).
        if i < num_iterations - 1:  # Check if not the last iteration
            print(f"Waiting for {sleep_time / 60} minutes before next Iteration...")
            time.sleep(sleep_time)  # Sleep
# Do this after all iterations have compleated.
        else:
            print("All iterations completed. Ending session.")
            print("")


if __name__ == "__main__":
    main()
