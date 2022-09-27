import datetime
from decimal import Decimal
from typing import List
from pydantic import BaseModel, Field

from src.schemas.order_item import OrderItemSchema
from src.schemas.address import Address
from src.schemas.user import UserSchema


class OrderSchema(BaseModel):
    id: int
    user: UserSchema
    price: Decimal = Field(max_digits=10, decimal_places=2, default=0.00)
    paid: bool = Field(default=False)
    products: List[OrderItemSchema] = [] 
    create: datetime.datetime = Field(default=datetime.datetime.now())
    address: Address

