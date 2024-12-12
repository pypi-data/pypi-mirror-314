from pydantic import BaseModel
from typing import Any, List, Optional
from datetime import datetime

from pydantic import BaseModel, Field, schema, validator

class ExtraAttribute(BaseModel):
    name: str
    description: Optional[str]

class ExternalProductModel(BaseModel):
    external_id: str

    category: Optional[List[str]]
    category_name: Optional[List[str]]
    name: str
    description: Optional[str]
    price: Optional[float]
    final_price: Optional[float]
    currency: Optional[str]
    stock_qty: int
    orders_qty: int = Field(0, hidden_field=True)
    created: datetime = Field(default=datetime.now, hidden_field=True)
    updated: datetime = Field(default=datetime.now, hidden_field=True)
    preview_url: List[str] = []
    extra_attributes: List[ExtraAttribute] = []

class ProductModel(BaseModel):
    id: Optional[str]
    external_id: Optional[str]
    category: Optional[List[int]]
    category_name: Optional[List[str]]
    name: str
    description: Optional[str]
    price: Optional[float]
    final_price: Optional[int]
    currency: Optional[str]
    stock_qty: int
    orders_qty: int = Field(0, hidden_field=True)
    created: datetime = Field(default=datetime.now, hidden_field=True)
    updated: datetime = Field(default=datetime.now, hidden_field=True)
    preview_url: List[str] = []
    extra_attributes: List[ExtraAttribute] = []
