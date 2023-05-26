
from typing import Optional, Union
from pydantic import BaseModel

class BaseSqlBasket(BaseModel):
    id: Optional[int]
    InvoiceNo: Optional[str]
    StockCode: Optional[str]
    Description: Optional[str]
    Quantity: Optional[int]
    InvoiceDate: Optional[str]
    UnitPrice: Optional[float]
    CustomerID: Optional[float]
    Country: Optional[str]
