from datetime import datetime

from pyccx.constant.order_side import OrderSide
from pyccx.constant.order_type import OrderType
from pyccx.constant.time_frame import TimeFrame
from pyccx.interface.exchange import Exchange


def future_market_examples(exchange: Exchange, symbol: str, time_frame: TimeFrame):
    print("\t- Future Market")

    # get market server time
    # server_time = exchange.future.market.get_server_time()
    # print("\t\t- {:<40} {}".format("Server time", server_time))
    #
    # # get market ping in milli-seconds
    # ping = exchange.future.market.get_ping()
    # print("\t\t- {:<40} {}".format("Ping", ping))

    # # get market info
    # symbols_info = exchange.future.market.get_symbols_info()

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

    # # post hedge_mode
    # mode = exchange.future.trade.post_hedge_mode(hedge_mode=HedgeMode.ONE_WAY)
    # print("\t\t- Post Hedge mode")
    # print("\t\t\t- {:<36} {}".format("Mode", mode))

    # get balance
    # balance = exchange.future.trade.get_balance()
    # print("\t\t- Get balance")
    # print("\t\t\t- {:<36} {}".format("Available", balance.available))

    # # get long leverage
    # long = exchange.future.trade.get_leverage(symbol=symbol, side=PositionSide.LONG)
    # short = exchange.future.trade.get_leverage(symbol=symbol, side=PositionSide.SHORT)
    # print("\t\t- Get leverage")
    # print("\t\t\t- {:<36} {}".format(f"Long leverage of {symbol}", long))
    # print("\t\t\t- {:<36} {}".format(f"Short leverage of {symbol}", short))

    # # post long leverage
    leverage = 20
    long = exchange.future.trade.set_leverage(symbol=symbol, leverage=leverage)
    print("\t\t- Post leverage")
    print("\t\t\t- {:<36} {}".format(f"leverage of {symbol}", long))

    # # post market order
    # order_id = exchange.future.trade.post_order(symbol=symbol, side=OrderSide.BUY, order_type=OrderType.MARKET,
    #                                             volume=0.001)
    # print("\t\t- Post Market order")
    # print("\t\t\t- {:<36} {}".format("Buy market order", order_id))

    # post limit order
    # order_id = exchange.future.trade.post_order(symbol=symbol, side=OrderSide.BUY, type=OrderType.LIMIT,
    #                                             volume=10, price=0.155)
    # print("\t\t- Post Limit order")
    # print("\t\t\t- {:<36} {}".format("order id", order_id))

    # # get orders
    # orders = exchange.future.trade.get_open_orders()
    # print("\t\t- Get open orders")
    # print("\t\t\t- {:<36} {}".format("orders count", len(orders)))

    # # 5 seconds delay
    # time.sleep(5)

    # # delete limit order
    # order_id = exchange.future.trade.delete_order(order_id=order_id)
    # print("\t\t- Delete Limit order")
    # print("\t\t\t- {:<36} {}".format("order id", order_id))

    # get position
    position = exchange.future.trade.get_open_position(symbol=symbol)
    print("\t\t- Get position")
    print("\t\t\t- {:<36} {}".format("side", position.side))
    print("\t\t\t- {:<36} {}".format("volume", position.volume))


def future_examples(exchange: Exchange, symbol: str, time_frame: TimeFrame):
    future_market_examples(exchange, symbol, time_frame)
    future_trade_examples(exchange, symbol)
