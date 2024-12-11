import aiohttp
import json
from typing import TYPE_CHECKING, Callable, Dict, List, Optional, Union
from datetime import datetime

from AsyncYoomoney import (
    Account,
    History,
    OperationDetails,
)


class Client:
    def __init__(self,
                 token: str = None,
                 base_url: str = None,
                 session: aiohttp.ClientSession = None
                 ):

        if base_url is None:
            self.base_url = "https://yoomoney.ru/api/"

        if token is not None:
            self.token = token

        self.session = session



    async def account_info(self):
        method = "account-info"
        return await Account.create(base_url=self.base_url,
                                    token=self.token,
                                    method=method,
                                    session=self.session
                                    )

    async def operation_history(self,
                          type: str = None,
                          label: str = None,
                          from_date: datetime = None,
                          till_date: datetime = None,
                          start_record: str = None,
                          records: int = None,
                          details: bool = None,
                          ):
        method = "operation-history"
        return await History.create(base_url=self.base_url,
                                    token=self.token,
                                    method=method,
                                    type=type,
                                    label=label,
                                    from_date=from_date,
                                    till_date=till_date,
                                    start_record=start_record,
                                    records=records,
                                    details=details,
                                    session=self.session
                                    )

    async def operation_details(self,
                          operation_id: str
                          ):
        method = "operation-details"
        return await OperationDetails.create(base_url=self.base_url,
                                       token=self.token,
                                       method=method,
                                       operation_id=operation_id,
                                       session=self.session
                                       )