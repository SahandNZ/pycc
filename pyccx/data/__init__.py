import itertools
import pandas as pd
from rich.progress import Progress
from typing import Dict, List, Tuple

from pyccx.constant.time_frame import TimeFrame
from pyccx.data.local import LocalData
from pyccx.defaults import BASE_TIME_FRAME
from pyccx.interface.exchange import Exchange
from pyccx.model.candle import Candle
from pyccx.utils import resample_time_frame

__EXCHANGE: Exchange = Exchange(exchange="binance", proxies=PROXIES)
__LOCAL_DATA: LocalData = LocalData(exchange=__EXCHANGE)


def load_dataframe(symbol: str, time_frame: TimeFrame, update: bool = False) -> pd.DataFrame:
    if update:
        candles = __LOCAL_DATA.download_candles(symbol=symbol, time_frame=BASE_TIME_FRAME)
        sdf = Candle.to_dataframe(candles=candles)
    else:
        sdf = __LOCAL_DATA.load_dataframe(symbol=symbol, time_frame=BASE_TIME_FRAME)

    df = resample_time_frame(tohlcv=sdf, source_timeframe=BASE_TIME_FRAME, destination_timeframe=time_frame)

    return df


def load_dataframes_dict(symbols: List[str], time_frames: List[TimeFrame], update: bool = False,
                         progress: Progress = None) -> Dict[Tuple[str, int], pd.DataFrame]:
    items = list(itertools.product(symbols, time_frames))

    if progress is not None:
        task = progress.add_task(description="Loading DataFrames", total=len(items))

    dfs_dict = {}
    for symbol, time_frame in items:
        df = load_dataframe(symbol=symbol, time_frame=time_frame, update=update)
        dfs_dict[symbol, time_frame] = df

        if progress is not None:
            progress.update(task, advance=1)

    return dfs_dict


def load_all_dataframes_dict(time_frames: List[TimeFrame], update: bool = False, progress: Progress = None) \
        -> Dict[Tuple[str, int], pd.DataFrame]:
    symbols_info = __EXCHANGE.future.market.get_symbols_info()
    symbols = [symbol_info.symbol for symbol_info in symbols_info]
    items = list(itertools.product(symbols, time_frames))

    dfs_dict = {}
    for symbol, time_frame in items:
        df = load_dataframe(symbol=symbol, time_frame=time_frame, update=update)
        dfs_dict[symbol, time_frame] = df

        if progress is not None:
            progress.update(task, advance=1)

    return dfs_dict
