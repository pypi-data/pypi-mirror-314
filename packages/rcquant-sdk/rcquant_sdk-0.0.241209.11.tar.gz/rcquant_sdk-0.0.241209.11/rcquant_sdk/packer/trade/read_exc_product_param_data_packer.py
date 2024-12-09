from ...interface import IPacker


class ReadExcProductParamDataPacker(IPacker):
    def __init__(self, obj) -> None:
        super().__init__(obj)

    def obj_to_tuple(self):
        return [list(self._obj.ExchangeID), list(self._obj.ProductID), list(self._obj.DataList)]

    def tuple_to_obj(self, t):
        if len(t) >= 3:
            self._obj.ExchangeID = t[0]
            self._obj.ProductID = t[1]
            self._obj.DataList = t[2]

            return True
        return False
