import random
import time

from pyccx.constant.order_side import OrderSide
from pyccx.constant.time_frame import TimeFrame
from pyccx.interface.exchange import Exchange


def future_market_examples(exchange: Exchange, symbol: str, time_frame: TimeFrame):
    print("\t- Future Market")

    # get market server time
    server_time = exchange.future.market.get_server_time()
    print("\t\t- {:<40} {}".format("Server time", server_time))

    # get market ping in milli-seconds
    ping = exchange.future.market.get_ping()
    print("\t\t- {:<40} {}".format("Ping", ping))

    # get market info
    symbols_info = exchange.future.market.get_symbols_info()
    symbol_info = symbols_info[0]
    print("\t\t- {:<40}".format("Symbols info"))
    print("\t\t\t- {:<40} {}".format(symbol_info.symbol + " Price precision", symbol_info.price_precision))

    # get candles
    candles = exchange.future.market.get_candles(symbol=symbol, time_frame=time_frame)
    print("\t\t- {:<40} {}".format("Last candle open price", candles[-1].open))

    # # get historical candles
    # current_timestamp = datetime.now().timestamp() // time_frame * time_frame
    # start_timestamp = current_timestamp - 120 * TimeFrame.DAY1
    # stop_timestamp = start_timestamp + 100 * time_frame
    # candles = exchange.future.market.get_historical_candles(symbol=symbol, time_frame=time_frame,
    #                                                         start_timestamp=start_timestamp,
    #                                                         stop_timestamp=stop_timestamp)
    # print("\t\t- {:<40} {}".format("Last candle open price", candles[-1].open))


def future_trade_examples(exchange: Exchange, symbol: str):
    print("\t- Future Trade")

    # get balance
    balance = exchange.future.trade.get_balance()
    print("\t\t- Get balance")
    print("\t\t\t- {:<36} {}".format("Available", balance.available))

    # get long leverage
    leverage = exchange.future.trade.get_leverage(symbol=symbol)
    print("\t\t- Get leverage")
    print("\t\t\t- {:<36} {}".format(f"leverage of {symbol}", leverage))

    # post long leverage
    leverage = random.randint(15, 20)
    exchange.future.trade.set_leverage(symbol=symbol, leverage=leverage)
    print("\t\t- Post leverage")
    print("\t\t\t- {:<36} {}".format(f"leverage of {symbol}", leverage))

    # post limit order
    order_id = exchange.future.trade.set_limit_order(symbol=symbol, side=OrderSide.BUY, volume=0.001, price=20000)
    print("\t\t- Post Limit order")
    print("\t\t\t- {:<36} {}".format("order id", order_id))

    # post limit order again
    order_id = exchange.future.trade.set_limit_order(symbol=symbol, side=OrderSide.BUY, volume=0.001, price=21000)
    print("\t\t- Post Limit order")
    print("\t\t\t- {:<36} {}".format("order id", order_id))

    # get orders
    orders = exchange.future.trade.get_open_orders(symbol=symbol)
    print("\t\t- Get open orders")
    print("\t\t\t- {:<36} {}".format("orders count", len(orders)))

    # 5 seconds delay
    time.sleep(5)

    # cancel limit order
    order_id = exchange.future.trade.cancel_order(symbol=symbol, order_id=order_id)
    print("\t\t- Cancel last limit order")
    print("\t\t\t- {:<36} {}".format("order id", order_id))

    # cancel all order
    order_id = exchange.future.trade.cancel_all_orders(symbol=symbol)
    print("\t\t- Cancel all orders")
    print("\t\t\t- {:<36} {}".format("order id", order_id))

    # post market order to open long position
    order_id = exchange.future.trade.set_market_order(symbol=symbol, side=OrderSide.BUY, volume=0.001)
    print("\t\t- Post Market order")
    print("\t\t\t- {:<36} {}".format("Buy market order", order_id))

    # get position
    position = exchange.future.trade.get_open_position(symbol=symbol)
    print("\t\t- Get position")
    print("\t\t\t- {:<36} {}".format("symbol", position.symbol))
    print("\t\t\t- {:<36} {}".format("side", position.side))
    print("\t\t\t- {:<36} {}".format("volume", position.volume))
    print("\t\t\t- {:<36} {}".format("Entry price", position.entry_price))
    print("\t\t\t- {:<36} {}".format("Liquidation price", position.leverage))
    print("\t\t\t- {:<36} {}".format("Liquidation price", position.liquidation_price))

    # post market order to close long position
    order_id = exchange.future.trade.set_market_order(symbol=symbol, side=OrderSide.SELL, volume=position.volume)
    print("\t\t- Post Market order")
    print("\t\t\t- {:<36} {}".format("Buy market order", order_id))

    # get position
    position = exchange.future.trade.get_open_position(symbol=symbol)
    print("\t\t- Get position")
    print("\t\t\t- {:<36} {}".format("symbol", position.symbol))
    print("\t\t\t- {:<36} {}".format("side", position.side))
    print("\t\t\t- {:<36} {}".format("volume", position.volume))
    print("\t\t\t- {:<36} {}".format("Entry price", position.entry_price))
    print("\t\t\t- {:<36} {}".format("Liquidation price", position.leverage))
    print("\t\t\t- {:<36} {}".format("Liquidation price", position.liquidation_price))


def future_examples(exchange: Exchange, symbol: str, time_frame: TimeFrame):
    future_market_examples(exchange, symbol, time_frame)
    future_trade_examples(exchange, symbol)
