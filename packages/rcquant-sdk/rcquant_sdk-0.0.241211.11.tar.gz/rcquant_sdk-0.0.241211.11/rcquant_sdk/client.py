import threading
from .tsocket import TSocket
from .listener import IListener

from .handle.chart_handle import ChartHandle
from .handle.base_handle import BaseHandle
from .handle.trade_handle import TradeHandle
from .handle.market_handle import MarketHandle


class FinClient(object):
    __TSocket = None
    __ChartHandle = None
    __BaseHandle = None
    __MarketHandle = None
    __TradeHandle = None
    __instance_lock = threading.Lock()

    def __init__(self):
        self.__TSocket = TSocket()
        self.__ChartHandle = ChartHandle(self.__TSocket)
        self.__BaseHandle = BaseHandle(self.__TSocket)
        self.__MarketHandle = MarketHandle(self.__TSocket)
        self.__TradeHandle = TradeHandle(self.__TSocket)

    def __del__(self):
        self.__TSocket.close()
        del self.__TradeHandle
        del self.__MarketHandle
        del self.__ChartHandle
        del self.__BaseHandle
        del self.__TSocket

    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            with cls.__instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = FinClient()
        return cls._instance

    def set_callback(self, **kwargs):
        if kwargs is None:
            return
        for key in kwargs:
            if key == "on_tick":
                self.__MarketHandle.set_callback(on_tick=kwargs[key])
            elif key == "on_ohlc":
                self.__MarketHandle.set_callback(on_ohlc=kwargs[key])
            elif key == "on_order_update":
                self.__TradeHandle.set_callback(on_order_update=kwargs[key])
            elif key == "on_tradeorder_update":
                self.__TradeHandle.set_callback(on_tradeorder_update=kwargs[key])
            elif key == "on_select_rect":
                self.__ChartHandle.set_callback(on_select_rect=kwargs[key])

    def set_listener(self, listener: IListener):
        self.__MarketHandle.set_listener(listener)
        self.__TradeHandle.set_listener(listener)

    def base_handle(self):
        return self.__BaseHandle

    def chart_handle(self):
        return self.__ChartHandle

    def market_handle(self):
        return self.__MarketHandle

    def trade_handle(self):
        return self.__TradeHandle

    def connect(self, host: str = None, port: int = None, timeout: int = 30000):
        return self.__TSocket.connect(host, port, timeout)

    def is_connected(self):
        return self.__TSocket.is_connected()

    def close(self):
        self.__TSocket.close()
