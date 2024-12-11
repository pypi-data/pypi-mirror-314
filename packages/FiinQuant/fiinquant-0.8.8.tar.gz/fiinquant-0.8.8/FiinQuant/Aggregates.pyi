import pandas as pd
from typing import Union
from datetime import datetime


class BarData:
    def __init__(self, data) -> None:
        self.__private_attribute: pd.DataFrame = data
        self.Timestamp: Union[str, datetime]
        self.Open: float
        self.High: float
        self.Low: float
        self.Close: float
        self.Volume: int
        self.Ticker: str
        self.BU: int
        self.SD: int
        self.FB: float
        self.FS: float
        self.FN: float
        
    def to_dataFrame(self) -> pd.DataFrame: ...

class BarDataUpdate:
    def __init__(self, data) -> None:
        self.__private_attribute: pd.DataFrame
        self.Timestamp: Union[str, datetime]
        self.Open: float
        self.High: float
        self.Low: float
        self.Close: float
        self.Volume: int
        self.Ticker: str 
        self.BU: int
        self.SD: int
        self.FB: float
        self.FS: float
        self.FN: float
    def to_dataFrame(self) -> pd.DataFrame: ...


class GetBarData:
    def __init__(self, 
                 tickers: Union[str, list],
                 by: str, 
                 from_date: Union[str, datetime, None], 
                 to_date: Union[str, datetime, None],
                 adjusted: bool, 
                 fields: list, 
                 period: int) -> None: ...
    
    def get(self) -> BarData: ...

