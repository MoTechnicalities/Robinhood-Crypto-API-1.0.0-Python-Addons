def main():

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
    """
    The example code below can be inserted into Robinhoods saple trading code. 
    """

    for i in range(3):
        print(f"\nIteration {i+1}:")
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
          eth_price = float(eth_data['price'])
          eth_bid = float(eth_data['bid_inclusive_of_sell_spread'])
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

        threshold=0
        sell_amount = (eth_usd_val_bid - buying_power) * 0.5  # Calculate 50% of the difference
        print("Checking Sell Ops")
        if sell_amount > threshold:
            print(f"I need to Sell: ${sell_amount:.2f}")
            # Assuming you have already retrieved the ETH price (eth_price) and total ETH quantity (total_quantity)

            # Calculate the number of ETH units to sell based on sell_amount and current price
            eth_to_sell = float(sell_amount) / float(eth_price)

            # Ensure the calculated quantity doesn't exceed available ETH
            eth_to_sell = min(float(eth_to_sell), float(total_quantity))  # Clamp to available quantity

            # Place the order with the calculated asset_quantity
            """
            order = api_trading_client.place_order(
                str(uuid.uuid4()),
                "sell",
                "market",
                "ETH-USD",
                {"asset_quantity": str(eth_to_sell)}  # Convert to string for the API
            )
            """
            print(str(eth_to_sell))
            print(f"Sold {eth_to_sell:.6f} ETH for approximately ${sell_amount:.2f}")

        buy_amount = (buying_power - eth_usd_val_ask) * 0.5   # Calculate 50% of the difference
        print("Checking Buy Ops")
        if buy_amount > threshold:
           print(f"I need to Buy: ${buy_amount:.2f}")


    

        # Wait for 5 minutes before next iteration
        print(f"Waiting for 5 minutes before next check (Iteration {i+1})...")
        time.sleep(5 * 60)  # Sleep for 5 minutes (adjust units if needed)







if __name__ == "__main__":
    main()
