from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order, Trade, Symbol
import pandas as pd
import numpy as np
import statistics as stat
import math


"""
Params:
    Takes in your predicted price and the best current market price.
    Also capped by max possible volume for this transaction.
Returns:
    Number/volume of units to perform for the transaction.
"""
def volume_function(predicted, best_price, max_possible_volume):
    
    percent = min(0.5, abs(predicted - best_price) / predicted)
    
    return percent * max_possible_volume


"""
Params:
    Takes in history of pearl trades since the last 'refresh'
Returns:
    Predicted price/value of a pearl.
"""
def pearl_predictor(pearl_history: List[Trade]):
    runningAverage = 0
    totalVolume = 0

    for trade in pearl_history:
        runningAverage += trade.price * trade.quantity
        totalVolume += trade.quantity

    return runningAverage / totalVolume


"""
Params:
    Takes in history of banana trades since the last 'refresh'
Returns:
    Predicted price/value of a banana.
"""
def banana_predictor(banana_history: List[Trade]):
    runningAverage = 0
    totalVolume = 0

    for trade in banana_history:
        runningAverage += trade.price * trade.quantity
        totalVolume += trade.quantity

    return runningAverage / totalVolume


ALL_PRODUCTS = [
    "PEARLS",
    "BANANAS"
]

PREDICTORS = {
    "PEARLS" : pearl_predictor,
    "BANANAS" : banana_predictor
}


class Trader:

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        """
        Only method required. It takes all buy and sell orders for all symbols as an input,
        and outputs a list of orders to be sent
        """

        result = {}

        # Iterate over all the keys (the available products) contained in the order depths
        for product in state.order_depths.keys():

            # Forced skip if there is no data or insufficient data
            if product not in state.market_trades or len(state.market_trades[product]) < 2:
                continue

            market_data = state.market_trades[product]

            order_depth: OrderDepth = state.order_depths[product]

            orders: list[Order] = []
            

            predictor = PREDICTORS[product]
            acceptable_price = predictor(market_data)

            """
            Logic:
                Buy when we think market value is lower than real value.
                Sell when we think market value is higher than real value.
            """
            if len(order_depth.sell_orders) > 0:

                asks = [k for k in order_depth.sell_orders.keys() if k < acceptable_price]
                
                # Check if the lowest ask (sell order) is lower than the defined acceptable value
                if asks:
                    for ask_price in asks:
                        ask_price_volume = abs(order_depth.sell_orders[ask_price])
                        volume = volume_function(acceptable_price, ask_price, ask_price_volume)
                        
                        # Then we buy
                        orders.append(Order(
                            product, ask_price, volume
                        ))

            if len(order_depth.buy_orders) > 0:

                asks = [k for k in order_depth.buy_orders.keys() if k > acceptable_price]

                # Check if the highest bid (buy order) is higher than the defined acceptable value
                if asks:
                    for bid_price in asks:
                        bid_price_volume = order_depth.buy_orders[bid_price]
                        volume = volume_function(acceptable_price, bid_price, bid_price_volume)
                        
                        # Then we sell
                        orders.append(Order(
                            product, ask_price, -volume
                        ))

            # Add all the above orders to the result dict
            result[product] = orders

        return result

