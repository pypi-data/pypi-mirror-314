import threading
from .tsocket import TSocket

from .handle.findata_handle import FinDataHandle
from .handle.base_handle import BaseHandle


class FinDataClient(object):
    __TSocket = None
    __FinDataHandle = None
    __BaseHandle = None
    __instance_lock = threading.Lock()

    def __init__(self):
        self.__TSocket = TSocket()
        self.__FinDataHandle = FinDataHandle(self.__TSocket)
        self.__BaseHandle = BaseHandle(self.__TSocket)

    def __del__(self):
        self.__TSocket.close()
        del self.__FinDataHandle
        del self.__BaseHandle
        del self.__TSocket

    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            with cls.__instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = FinDataClient()
        return cls._instance

    def base_handle(self):
        return self.__BaseHandle

    def findata_handle(self):
        return self.__FinDataHandle

    def connect(self, host: str = None, port: int = None, timeout: int = 30000):
        return self.__TSocket.connect(host, port, timeout)

    def is_connected(self):
        return self.__TSocket.is_connected()

    def close(self):
        self.__TSocket.close()
