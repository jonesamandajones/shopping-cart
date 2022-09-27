from pydantic import BaseModel, Field


class ProductSchema(BaseModel):
    _id: int
    name: str = Field(max_length=100)
    description: str
    price: float
    image: str
     
