def main():

    """
    The sample code below can be inserted into Robinhoods sample trading code. 
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
# Sell Action
    #Set a Buy/Sell threshold
        threshold = 25.00
        sell_amount = (eth_usd_val_bid - buying_power) * 0.5  # Calculate 50% of the difference
        print("Checking Opportunities to Sell...")
        if sell_amount > threshold:
            print(f"I need to Sell: ${sell_amount:.2f}")
            # Assuming you have already retrieved the ETH price (eth_price) and total ETH quantity (total_quantity)

            # Calculate the number of ETH units to sell based on sell_amount and current price
            eth_to_sell = float(sell_amount) / float(eth_price)

            # Ensure the calculated quantity doesn't exceed available ETH
            eth_to_sell = min(float(eth_to_sell), float(total_quantity))  # Clamp to available quantity

            # Place the order with the calculated asset_quantity
            
            formatted_quantity = f"{eth_to_sell:.6f}"

            # !!! THIS STEP BELOW DOES THE ACTUAL SELL - REMOVE """ TO FUNCTION !!!
            """
            order = api_trading_client.place_order(
                str(uuid.uuid4()),
                "sell",
                "market",
                "ETH-USD",
                {"asset_quantity": formatted_quantity}  # Convert to string for the API
            )
            """
            # !!! THIS STEP ABOVE DOES THE ACTUAL SELL - REMOVE """ TO FUNCTION !!!

            print(str(eth_to_sell))
            print(f"Sold {eth_to_sell:.6f} ETH for approximately ${sell_amount:.2f}")
# Buy Action
        buy_amount = (buying_power - eth_usd_val_ask) * 0.5   # Calculate 50% of the difference
        print("Checking Opportunities to Buy....")
        if buy_amount > threshold:
            print(f"I need to Buy: ${buy_amount:.2f}")
            eth_to_buy = float(buy_amount) / float(eth_price)

            # Ensure the calculated quantity doesn't exceed available buying power (adjusted for potential fees)
            # Assuming a 0.1% fee
            fee_rate = 0.001
            max_buy_power = float(buying_power) * (1 - fee_rate)
            eth_to_buy = min(float(eth_to_buy), float(max_buy_power) / float(eth_price))  # Clamp to available buying power

            # Place the order with the calculated asset_quantity
            formatted_quantity = f"{eth_to_buy:.6f}"

            # !!! THIS STEP BELOW DOES THE ACTUAL BUY - REMOVE """ TO FUNCTION !!!
            """
            order = api_trading_client.place_order(
                str(uuid.uuid4()),
                "buy",
                "market",
                "ETH-USD",
                {"asset_quantity": formatted_quantity}  # Convert to string for the API
            )
            """
            # !!! THIS STEP ABOVE DOES THE ACTUAL BUY - REMOVE """ TO FUNCTION !!!

            # Print confirmation message with the amount of ETH bought
            print(f"Bought {eth_to_buy:.6f} ETH for approximately ${buy_amount:.2f}")
        print(f"Iteration {i+1} compleated.")

# Sleep for 5 minutes before each iteration (except the last)
        if i < num_iterations - 1:  # Check if not the last iteration
            print("Waiting for 5 minutes before next Iteration...")
            time.sleep(5 * 60)  # Sleep for 5 minutes (adjust units if needed)
        else:
            print("Loop completed. Ending session.")
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
