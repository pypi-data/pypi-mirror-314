from .Aggregates import GetBarData

from .Trading_Data_Stream import Trading_Data_Stream
from .Fetch_Trading_Data import Fetch_Trading_Data
from datetime import datetime
from .FiinIndicator import _FiinIndicator
from typing import Union

class FiinSession:
    def __init__(self, username: str, password: str):...

    def login(self) -> FiinSession: ...
        
   
    def FiinIndicator(self) -> _FiinIndicator: ...
    
    # def SubscribeDerivativeEvents(self,
    #                         tickers: list, 
    #                         callback: callable) -> SubscribeDerivativeEvents: ...
    # def SubscribeCoveredWarrantEvents(self,
    #                         tickers: list, 
    #                         callback: callable) -> SubscribeCoveredWarrantEvents: ...
    # def SubscribeTickerEvents(self,
    #                         tickers: list, 
    #                         callback: callable) -> SubscribeTickerEvents: ...
    # def SubscribeIndexEvents(self,
    #                         tickers: list, 
    #                         callback: callable) -> SubscribeIndexEvents: ...
    # def SubscribeTickerUpdate(self,
    #                         tickers: list, 
    #                         callback: callable,
    #                         by: str,
    #                         from_date: str,
    #                         wait_for_full_timeFrame: bool) -> SubscribeTickerUpdate: ...
    
    def Trading_Data_Stream(self, 
                        tickers: list, 
                        callback: callable) -> Trading_Data_Stream: ...
    
    def Fetch_Trading_Data(self,
                 realtime: bool,
                 tickers: list, 
                 fields:list, 
                 adjusted: bool, 
                 period:Union[int, None] = None, 
                 by:str = '1M',
                 from_date: Union[str, datetime, None] = None,
                 to_date: Union[str, datetime, None] = None,
                 callback: callable = None,
                 wait_for_full_timeFrame: bool = False) -> Fetch_Trading_Data: ...

    # def GetBarData(self, tickers: Union [str, list], by: str, 
    #             from_date: Union [str, datetime, None] = None, 
    #             to_date: Union [str, datetime, None] = None, 
    #             adjusted: bool = True,
    #             fields: list = [],
    #             period: int = 0) -> GetBarData: ...
