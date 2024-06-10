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
    This is 'TRADING STRATEGY' code is designed to be inserted into the
    Robinhood Crypto Trading API (1.0.0) sample Python code.

    This tading strategy maintans a 50/50 value ratio between your Account's
    [Buying Power] and [ETH-USD Holdings Value]. You can specify how many times the
    code Loops, the Wait Time in secconds befor the next Loop, and The Buy and Sell
    Threshold. Adjust the setting to fit your needs.
    """
# SET ITERATIONS
    num_iterations = 4
    for i in range(num_iterations):
        
# Check for Buy/Sell Opportunities using retrieved data

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
          #eth_ask = (3276.15) # uncomment to inject fake price eth_ask = (3716.0185916)
          eth_price = float(eth_data['price'])
          #eth_price = (3276.15) # uncomment to inject fake price eth_price = (3699.3992958)
          eth_bid = float(eth_data['bid_inclusive_of_sell_spread'])
          #eth_bid = (3276.15) # uncomment to inject fake price eth_bid = (3682.78)
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


# Check for Buy/Sell Opportunities Using the Retrieved Data

# Specify Buy and Sell Thresholds
        threshold_buy = 5.00
        threshold_sell = 5.00
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

            # !!! THE BELOW STEP DOES THE ACTUAL BUY - REMOVE """ TO FUNCTION !!!
            """
            order = api_trading_client.place_order(
                str(uuid.uuid4()),
                "buy",
                "market",
                "ETH-USD",
                {"asset_quantity": formatted_quantity}  # Convert to string for the API
            )
            """
            # !!! THE ABOVE STEP DOES THE ACTUAL BUY - REMOVE """ TO FUNCTION !!!

            # Print confirmation message with the amount of ETH bought
            print(f"Bought {eth_to_buy:.6f} ETH for approximately ${buy_amount:.2f}")


# Sell Action
    #Set a Buy/Sell threshold
        sell_amount = (eth_usd_val_bid - buying_power) * 0.5  # Calculate 50% of the difference
        print("Checking Opportunities to Sell...")
        if sell_amount > threshold_sell:
            print(f"I need to Sell: ${sell_amount:.2f}")
            # Assuming you have already retrieved the ETH price (eth_price) and total ETH quantity (total_quantity)

            # Calculate the number of ETH units to sell based on sell_amount and current price
            eth_to_sell = float(sell_amount) / float(eth_price)

            # Ensure the calculated quantity doesn't exceed available ETH
            eth_to_sell = min(float(eth_to_sell), float(total_quantity))  # Clamp to available quantity

            # Place the order with the calculated asset_quantity
            
            formatted_quantity = f"{eth_to_sell:.6f}"

            # !!! THE BELOW STEP DOES THE ACTUAL SELL - REMOVE """ TO FUNCTION !!!
            """
            order = api_trading_client.place_order(
                str(uuid.uuid4()),
                "sell",
                "market",
                "ETH-USD",
                {"asset_quantity": formatted_quantity}  # Convert to string for the API
            )
            """
            # !!! THE ABOVE STEP DOES THE ACTUAL SELL - REMOVE """ TO FUNCTION !!!

            print(str(eth_to_sell))
            print(f"Sold {eth_to_sell:.6f} ETH for approximately ${sell_amount:.2f}")
        print(f"Iteration {i+1} compleated.")
        print("")

# Sleep for the specified time before each iteration (except the last iteration).
        if i < num_iterations - 1:  # Check if not the last iteration
            sleep_time = (5 * 60)   # Specify sleep_time in seconds.
            print(f"Waiting for {sleep_time / 60} minutes before next Iteration...")
            time.sleep(sleep_time)  # Sleep
# Do this after all iterations have compleated.
        else:
            print("All loop completed. Ending session.")
            print("")


        """
        BUILD YOUR TRADING STRATEGY HERE

        order = api_trading_client.place_order(
            str(uuid.uuid4()),
            "buy",
            "market",
            "BTC-USD",
            {"asset_quantity": "0.0001"}
        )
        """


if __name__ == "__main__":
    main()
