from typing import List
from ...interface import IData
from ..market.ohlc_data import OHLCData
from ...packer.chart.ohlc_value_list_data_packer import OHLCValueListDataPacker


class OHLCValueListData(IData):
    def __init__(self, ohlc_value_list: List[OHLCData]):
        super().__init__(OHLCValueListDataPacker(self))
        self._OHLCList: List[OHLCData] = ohlc_value_list

    @property
    def OHLCList(self):
        return self._OHLCList

    @OHLCList.setter
    def OHLCList(self, value: List[OHLCData]):
        self._OHLCList = value
