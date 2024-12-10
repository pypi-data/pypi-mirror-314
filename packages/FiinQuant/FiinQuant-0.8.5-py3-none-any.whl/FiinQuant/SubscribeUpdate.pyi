import pandas as pd
from typing import Union
from datetime import datetime
class SubscribeUpdate:
    def __init__(self,
                 realtime: bool,
                 tickers: list, 
                 fields:list, 
                 adjusted: bool, 
                 period: Union[int, None] = None,
                 by: str = '1M',
                 from_date: Union[str, datetime, None] = None,
                 to_date: Union[str, datetime, None] = None,
                 callback: callable = None,
                 wait_for_full_timeFrame: bool = False) -> None:
            self._stop: bool
       
    def get_data(self) -> pd.DataFrame: ...
    def stop(self) -> None: ...

        
  