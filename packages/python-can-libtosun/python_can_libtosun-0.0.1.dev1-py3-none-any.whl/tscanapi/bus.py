'''
Author: seven 865762826@qq.com
Date: 2023-06-11 14:14:06
LastEditors: notmmao@gmail.com
LastEditTime: 2024-12-10 11:46:49
'''
import typing

from can.message import Message
import can
from typing import List, Optional, Tuple, Union, Deque, Any
from can.bus import LOG
from .TSMasterDevice import *


class TsBus(can.BusABC):
    def __init__(self, channel: Any = None, *,
                configs: typing.List[dict],
                is_include_tx=False,
                can_filters: Optional[can.typechecking.CanFilters] = None,
                hwserial: bytes = b"",
                dbc:str = '',
                filters = [],
                 **kwargs: object):
        super().__init__(channel, can_filters, **kwargs)
        self.device = TSMasterDevice(configs=configs, hwserial=hwserial,is_include_tx=is_include_tx,
        dbc=dbc,filters = filters)

    def send(self, msg: can.Message, timeout: Optional[float] = 0.1, sync: bool = False,
            is_cyclic: bool = False) -> None:
        self.device.send_msg(msg, timeout, sync, is_cyclic)

    def recv(self, timeout:float = 0.1, channel=0) -> Optional[Message]:
        msg = self._recv_internal(channel = channel, timeout=timeout)[0]
        return msg
    
    def _recv_internal(self, timeout: float = 0.1, channel=0) -> Tuple[Optional[can.Message], bool] or Tuple[None,bool]:
        return self.device.recv(channel=channel,timeout = timeout), False

    def shutdown(self) -> None:
        LOG.debug('TSMaster - shutdown.')
        self.device.shut_down()
        super().shutdown()
