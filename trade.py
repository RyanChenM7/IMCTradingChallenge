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
    return max_possible_volume


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

                best_ask = min(order_depth.sell_orders.keys())
                best_ask_volume = order_depth.sell_orders[best_ask]

                # Check if the lowest ask (sell order) is lower than the defined acceptable value
                if best_ask < acceptable_price:
                    volume = volume_function(acceptable_price, best_ask, best_ask_volume)
                    
                    # Then we buy
                    orders.append(Order(
                        product, best_ask, volume
                    ))

            if len(order_depth.buy_orders) > 0:

                best_bid = max(order_depth.buy_orders.keys())
                best_bid_volume = order_depth.buy_orders[best_bid]

                # Check if the highest bid (buy order) is higher than the defined acceptable value
                if best_bid > acceptable_price:
                    volume = volume_function(acceptable_price, best_bid, best_bid_volume)

                    # Then we sell
                    orders.append(Order(
                        product, best_bid, -volume
                    ))

            # Add all the above orders to the result dict
            result[product] = orders

        return result

