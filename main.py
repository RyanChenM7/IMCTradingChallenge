from datamodel import Listing, OrderDepth, Trade, TradingState
from trader import Trader
timestamp = 1000

listings = {
	"PEARLS": Listing(
		symbol="PEARLS", 
		product="PEARLS", 
		denomination= "SEASHELLS"
	),
	"BANANAS": Listing(
		symbol="BANANAS", 
		product="BANANAS", 
		denomination= "SEASHELLS"
	),
}

p1 = OrderDepth()
p1.buy_orders = {10: 7, 9: 5}
p2 = OrderDepth()
p2.sell_orders = {11: -4, 12: -8}

order_depths = {
	"PEARLS": p1,
	"BANANAS": p2
}

own_trades = {
	"PEARLS": [],
	"BANANAS": []
}

market_trades = {
	"PEARLS": [
		Trade(
			symbol="PEARLS",
			price=11,
			quantity=4,
			buyer="",
			seller="",
			timestamp=900
		)
	],
	"BANANAS": []
}

position = {
	"PEARLS": 3,
	"BANANAS": -5
}

observations = {}

state = TradingState(
	timestamp=timestamp,
    listings=listings,
	order_depths=order_depths,
	own_trades=own_trades,
	market_trades=market_trades,
    position=position,
    observations=observations
)


t = Trader()

res = t.run(state)

for item in res.items():
    print(item)
