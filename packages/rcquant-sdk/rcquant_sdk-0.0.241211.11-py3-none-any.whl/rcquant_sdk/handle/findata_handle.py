from typing import Tuple
import msgpack
import lzma
import zlib
import pickle
import pandas as pd
import numpy as np


from .req_rsp import ReqRspDict, ReqRsp
from ..interface import IData, MsgID
from ..tsocket import TSocket
from ..data.message_data import MessageData


from ..data.market.tick_data import TickData
from ..data.market.ohlc_data import OHLCData
from ..data.market.history_ohlc_param_data import HistoryOHLCParamData
from ..data.market.fin_persist_filed_data import FinPersistFiledData
from ..data.market.fin_persist_save_param_data import FinPersistSaveParamData
from ..data.market.fin_persist_read_param_data import FinPersistReadParamData
from ..data.market.fin_persist_delete_param_data import FinPersistDeleteParamData
from ..data.trade.read_exc_product_param_data import ReadExcProductParamData
from ..data.trade.read_instrument_param_data import ReadInstrumentParamData
from ..data.trade.save_instrument_param_data import SaveInstrumentParamData


class FinDataHandle():
    def __init__(self, tsocket: TSocket):
        self.__TSocket = tsocket
        self.__TSocket.set_findata_callback(self.__recv_msg)
        self.__ReqID = 0
        self.__ReqRspDict = ReqRspDict()
        self.__ExcProduct_Columns_Types = {"ExchangeID": str, "ProductID": str, "ProductName": str,
                                           "VolumeMultiple": np.float32, "PriceTick": np.float32,
                                           "MaxMarketOrderVolume": np.int32, "MaxLimitOrderVolume": np.int32,
                                           "Times": {}}
        self.__ExcProductTime_Columns_Types = {"StartTime": str, "EndTime": str, "AddDay": np.int32, "InstrumentStatusKind": np.int32}
        self.__DB_Columns_Types = {"Day": int, "Mark": str, "Offset": int, "Buffer": bytes}
        self.__Tick_Columns_Types = {"ExchangeID": str, "InstrumentID": str, "TradingDay": str, "ActionDay": str,
                                     "ActionTime": str, "ActionMSec": str, "LastPrice": np.float32,
                                     "LastVolume": np.int32, "BidPrice": np.float32, "BidVolume": np.int32,
                                     "AskPrice": np.float32, "AskVolume": np.int32, "TotalTurnover": np.float64,
                                     "TotalVolume": np.int32, "OpenInterest": np.int32}
        self.__OHLC_Columns_Types = {
            "ExchangeID": str, "InstrumentID": str, "TradingDay": str, "ActionDay": str, "ActionTime": str,
            "Period": np.int32, "OpenPrice": np.float32, "HighestPrice": np.float32, "LowestPrice": np.float32,
            "ClosePrice": np.float32, "CloseVolume": np.int32, "CloseBidPrice": np.float32,
            "CloseAskPrice": np.float32, "CloseBidVolume": np.int32, "CloseAskVolume": np.int32,
            "TotalTurnover": np.float64, "TotalVolume": np.int32, "OpenInterest": np.int32}

        self.__Day_Columns_Types = {
            "ExchangeID": str, "InstrumentID": str, "TradingDay": str,
            "OpenPrice": np.float32, "HighestPrice": np.float32, "LowestPrice": np.float32, "ClosePrice": np.float32,
            "UpperLimitPrice": np.float32, "LowerLimitPrice": np.float32, "SettlementPrice": np.float32,
            "TotalTurnover": np.float64, "TotalVolume": np.int32, "OpenInterest": np.int32}

        self.__Instrument_Columns_Types = {
            "InstrumentID": str, "ExchangeID": str, "InstrumentName": str, "UniCode": str, "ProductID": str,
            "ProductType": np.int32, "DeliveryYear": str, "DeliveryMonth": str, "CreateDate": str, "OpenDate": str,
            "ExpireDate": str, "StartDelivDate": str, "EndDelivDate": str, "MaxMarketOrderVolume": np.int64,
            "MinMarketOrderVolume": np.int64, "MaxLimitOrderVolume": np.int64, "MinLimitOrderVolume": np.int64,
            "VolumeMultiple": np.int32, "PriceTick": np.float32, "PricePrecision": np.int64, "IsTrading": bool,
            "MaxMarginSideAlgorithm": bool, "ProductGroupID": str, "StrikePrice": np.float64, "OptionsType": np.int32,
            "UnderlyingInstrID": str, "UnderlyingMultiple": np.float64, "CombinationType": np.int32, "StrikeModeType": np.int32,
            "ObjectPrice": np.float64, "ObjectMarginRatioByMoney": np.float64, "ObjectMarginRatioByVolume": np.float64,
            "EnsureRatio1": np.float64, "EnsureRatio2": np.float64, "IsCloseToday": bool, "Times": str
        }

    def set_callback(self, **kwargs):
        if kwargs is None:
            return
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def get_ohlc_column_types(self):
        return self.__OHLC_Columns_Types

    def get_tick_column_types(self):
        return self.__Tick_Columns_Types

    def get_day_column_types(self):
        return self.__Day_Columns_Types

    def get_instrument_columns_types(self):
        return self.__Instrument_Columns_Types

    def get_db_columns_types(self):
        return self.__DB_Columns_Types

    def fin_save_day_list(self, instrument_id: str, df, period: str, **kwargs) -> Tuple[bool, str]:
        if len(period) == 0:
            period = "day"
        return self.__fin_save_list(int(MsgID.FinData_FinSaveDayList.value), self.__Day_Columns_Types.keys(),
                                    instrument_id, df, period, "TradingDay", **kwargs)

    def fin_read_day_list(self, params: FinPersistReadParamData) -> Tuple[bool, str, pd.DataFrame]:
        return self.__fin_read_list(int(MsgID.FinData_FinReadDayList.value), "day",
                                    self.__Day_Columns_Types.keys(), params)

    def fin_save_ohlc_list(self, instrument_id: str, df, period: str, **kwargs) -> Tuple[bool, str]:
        return self.__fin_save_list(int(MsgID.FinData_FinSaveOHLCList.value), self.__OHLC_Columns_Types.keys(),
                                    instrument_id, df, period, "ActionDay", **kwargs)

    def fin_read_ohlc_list(self, params: FinPersistReadParamData) -> Tuple[bool, str, pd.DataFrame]:
        return self.__fin_read_list(int(MsgID.FinData_FinReadOHLCList.value), "ohlc",
                                    self.__OHLC_Columns_Types.keys(), params)

    def fin_save_tick_list(self, instrument_id, df, period: str, **kwargs) -> Tuple[bool, str]:
        if len(period) == 0:
            period = "tick"
        return self.__fin_save_list(int(MsgID.FinData_FinSaveTickList.value), self.__Tick_Columns_Types.keys(),
                                    instrument_id, df, period, "ActionDay", **kwargs)

    def fin_read_tick_list(self, params: FinPersistReadParamData) -> Tuple[bool, str, pd.DataFrame]:
        return self.__fin_read_list(int(MsgID.FinData_FinReadTickList.value), "tick",
                                    self.__Tick_Columns_Types.keys(), params)

    def fin_read_db_list(self, params: FinPersistReadParamData) -> Tuple[bool, str, pd.DataFrame]:
        return self.__fin_read_db_list(int(MsgID.FinData_FinReadDBList.value), period_name='',
                                       col_keys=self.__DB_Columns_Types.keys(), params=params)

    def fin_delete_list(self, params: FinPersistDeleteParamData) -> Tuple[bool, str]:
        return self.__wait_send_msg(int(MsgID.FinData_FinDeleteList.value), params)

    def fin_read_exc_products(self, params: ReadExcProductParamData):
        return self.wait_read_datas(int(MsgID.FinData_ReadExcProducts.value), params, '', self.__unpack_excproduct_list)

    def fin_read_instruments(self, params: ReadInstrumentParamData):
        return self.wait_read_datas(int(MsgID.FinData_FinReadInstrument.value), params, "", self.__unpack_instrument_list)

    def fin_save_instruments(self, df, base_path: str = ''):
        if df.columns.to_list() != list(self.__Instrument_Columns_Types.keys()):
            return [False, "df 数据列名称不匹配,当前:%s 应为:%s" % (df.columns.to_list(), self.__Instrument_Columns_Types.keys())]

        params: SaveInstrumentParamData = SaveInstrumentParamData()
        params.DataList = df.values.tolist()
        params.BasePath = base_path

        return self.__wait_send_msg(int(MsgID.FinData_FinSaveInstrument.value), params)

    def __unpack_excproduct_list(self, reqrsp: ReqRsp):
        os = list()
        rsp_list = reqrsp.get_rsp_list()
        for r in rsp_list:
            if len(r.UData) > 0:
                rspparams = ReadExcProductParamData()
                rspparams.un_pack(r.UData)
                for ot in rspparams.DataList:
                    if len(ot) >= 7 and isinstance(ot[7], list):
                        df_pts = pd.DataFrame(ot[7], columns=list(self.__ExcProductTime_Columns_Types.keys()))
                        ot[7] = df_pts
                    os.append(ot)
        df = pd.DataFrame(os, columns=self.__ExcProduct_Columns_Types.keys())
        return df

    def __unpack_instrument_list(self, reqrsp: ReqRsp):
        os = list()
        rsp_list = reqrsp.get_rsp_list()
        for r in rsp_list:
            if len(r.UData) > 0:
                rspparams = ReadInstrumentParamData()
                rspparams.un_pack(r.UData)
                for ot in rspparams.DataList:
                    os.append(ot)
        df = pd.DataFrame(os, columns=self.__Instrument_Columns_Types.keys())
        return df

    def wait_read_datas(self, mid, params: IData, fun_name: str, unpack_func):
        self.__ReqID = self.__ReqID + 1
        msg = MessageData(mid=mid, request_id=self.__ReqID)
        if params is not None:
            msg.UData = params.pack()

        key = '%s_%s' % (mid, self.__ReqID)
        req_rsp = self.__ReqRspDict.new_reqrsp(key, msg)
        if self.__TSocket.send_message(msg) is False:
            self.__ReqRspDict.remove(key)
            return [False, '发送%s失败' % fun_name, None]

        rsp = req_rsp.wait_last_rsp(10)
        if rsp is None:
            self.__ReqRspDict.remove(key)
            return [False, '获取%s数据超时' % fun_name, None]

        return [True, '%s读取成功' % fun_name, unpack_func(req_rsp)]

    def __fin_save_list(self, mid: int, col_keys, instrument_id, df, period: str, groupby_key: str, **kwargs) -> Tuple[bool, str]:
        if not isinstance(df, pd.DataFrame):
            return [False, "df 数据类型格式不是 DataFrame"]

        if df.columns.to_list() != list(col_keys):
            return [False, "df 数据列名称不匹配,当前:%s 应为:%s" % (df.columns.to_list(), col_keys)]

        b, m, params = self.__create_fin_persists_save_param_data(instrument_id, df, period, groupby_key, **kwargs)
        if b == False:
            return [b, m]

        return self.__wait_send_msg(int(mid), params)

    def __fin_read_db_list(self, mid: int, period_name: str, col_keys, params: FinPersistReadParamData) -> Tuple[bool, str, pd.DataFrame]:
        self.__ReqID = self.__ReqID + 1
        msg = MessageData(mid=mid, request_id=self.__ReqID)
        if params is not None:
            msg.UData = params.pack()

        key = '%s_%s' % (mid, self.__ReqID)
        req_rsp = self.__ReqRspDict.new_reqrsp(key, msg)
        if self.__TSocket.send_message(msg) is False:
            self.__ReqRspDict.remove(key)
            return [False, '发送命令失败', None]

        rsp = req_rsp.wait_last_rsp(60)
        if rsp is None:
            self.__ReqRspDict.remove(key)
            return [False, ('获取%s数据超时' % period_name), None]

        dflist = []
        rsp_list = req_rsp.get_rsp_list()
        for r in rsp_list:
            if len(r.UData) <= 0:
                continue

            rspparams = FinPersistReadParamData()
            rspparams.un_pack(r.UData)
            for d in rspparams.DataFileds:
                dflist.append(d.obj_to_tuple())
        df = pd.DataFrame(dflist, columns=col_keys)
        ret = [rsp.RspSuccess, rsp.RspMsg, df]

        self.__ReqRspDict.remove(key)
        return ret

    def __fin_read_list(self, mid: int, period_name: str, col_keys, params: FinPersistReadParamData) -> Tuple[bool, str, pd.DataFrame]:
        self.__ReqID = self.__ReqID + 1
        msg = MessageData(mid=mid, request_id=self.__ReqID)
        if params is not None:
            msg.UData = params.pack()

        key = '%s_%s' % (mid, self.__ReqID)
        req_rsp = self.__ReqRspDict.new_reqrsp(key, msg)
        if self.__TSocket.send_message(msg) is False:
            self.__ReqRspDict.remove(key)
            return [False, '发送命令失败', None]

        rsp = req_rsp.wait_last_rsp(60)
        if rsp is None:
            self.__ReqRspDict.remove(key)
            return [False, ('获取%s数据超时' % period_name), None]

        ret = [rsp.RspSuccess, rsp.RspMsg, self.__unpack_fin_persist_read_param_data_to_df(req_rsp, list(col_keys))]

        self.__ReqRspDict.remove(key)
        return ret

    def __unpack_fin_persist_read_param_data_to_df(self, reqrsp: ReqRsp, columns):
        olist = self.__unpack_decompress_buffers(reqrsp, columns)
        if len(olist) == 0:
            return pd.DataFrame(columns=columns)
        return pd.concat(olist, ignore_index=True)

    def __unpack_stream_buffer(self, buffer, columns):
        o_list = []
        sz = int.from_bytes(buffer[:4], byteorder='little')
        while len(buffer) >= sz + 4 and sz > 0:
            o_list.extend(msgpack.unpackb(buffer[4:sz + 4], raw=False))
            buffer = buffer[sz + 4:]
            sz = int.from_bytes(buffer[:4], byteorder='little')
        return pd.DataFrame(o_list, columns=columns)

    def __unpack_decompress_buffers(self, req_rsp: ReqRsp, columns):
        rsp_list = req_rsp.get_rsp_list()
        dflist = []
        for r in rsp_list:
            if len(r.UData) <= 0:
                continue
            rspparams = FinPersistReadParamData()
            rspparams.un_pack(r.UData)
            for df in rspparams.DataFileds:
                marks = df.Mark.split(",")
                if len(marks) != 3:
                    continue

                decombytes = b''
                if marks[0] == 'zip':
                    decombytes = zlib.decompress(df.Buffer)
                elif marks[0] == 'xz':
                    decombytes = lzma.decompress(df.Buffer)
                elif marks[0] == 'qtzip':
                    decombytes = zlib.decompress(df.Buffer[4:])
                elif marks[0] == '0':
                    dflist.append(self.__unpack_stream_buffer(df.Buffer, columns))
                    continue

                if len(decombytes) == 0:
                    continue

                if marks[2] == 'pickle':
                    dflist.append(pickle.loads(decombytes))
                else:
                    dflist.append(pd.DataFrame(msgpack.unpackb(decombytes, raw=False), columns=columns))

        return dflist

    def __create_fin_persists_save_param_data(self, instrument_id: str, df, period: str, groupby_key: str, **kwargs):
        if not isinstance(df, pd.DataFrame):
            return [False, "df 数据类型格式不是 DataFrame", {}]
        if len(period) == 0:
            return [False, "period不能为空"]

        compress = 'zip' if 'compress' not in kwargs.keys() else kwargs.get('compress')
        level = -1 if 'level' not in kwargs.keys() else kwargs.get('level')
        pack = 'msgpack' if 'pack' not in kwargs.keys() else kwargs.get('pack')
        vacuum = True if 'vacuum' not in kwargs.keys() else kwargs.get('vacuum')
        base_path = '' if 'base_path' not in kwargs.keys()else kwargs.get('base_path')

        params: FinPersistSaveParamData = FinPersistSaveParamData()
        params.Append = False
        params.Period = period
        params.InstrumentID = instrument_id
        params.Vacuum = bool(vacuum)
        params.BasePath = base_path
        groups = df.groupby(groupby_key)
        buffer_sz = 0
        for day, day_list in groups:
            filed = FinPersistFiledData()
            filed.Day = int(day)
            filed.Mark = '%s,%s,%s' % (compress, level, pack)
            pack_buffer = b''

            if pack == 'pickle':
                pack_buffer = pickle.dumps(day_list)
            else:
                pack_buffer = msgpack.packb(day_list.values.tolist(), use_bin_type=True)

            if compress == 'zip':
                filed.Buffer = zlib.compress(pack_buffer, level=level)
            else:
                filed.Buffer = lzma.compress(pack_buffer)

            buffer_sz = buffer_sz + len(filed.Buffer)
            params.Fileds.append(filed)
        return [True, "", params]

    def __recv_msg(self, msg: MessageData):
        key = '%s_%s' % (msg.MID, msg.RequestID)
        reqrsp: ReqRsp = self.__ReqRspDict.get_reqrsp(key)
        if reqrsp is not None:
            reqrsp.append_rsp(msg)

    def __wait_send_msg(self, mid, params: IData):
        self.__ReqID = self.__ReqID + 1
        msg = MessageData(mid=mid, request_id=self.__ReqID)
        if params is not None:
            msg.UData = params.pack()

        key = '%s_%s' % (mid, self.__ReqID)

        req_rsp = self.__ReqRspDict.new_reqrsp(key, msg)
        if self.__TSocket.send_message(msg) is False:
            self.__ReqRspDict.remove(key)
            return [False, '发送命令失败']

        rsp = req_rsp.wait_last_rsp(60)
        if rsp is None:
            self.__ReqRspDict.remove(key)
            return [False, '发送命令超时']

        ret = [rsp.RspSuccess, rsp.RspMsg]
        self.__ReqRspDict.remove(key)
        return ret
