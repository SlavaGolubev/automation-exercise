from enum import Enum

from typing_extensions import TypedDict
from pydantic import BaseModel, Field


class UserType(str, Enum):
    WOMEN = "Women"
    MEN = "Men"
    KIDS = "Kids"


class UserTypeDict(TypedDict):
    usertype: UserType


class CategoryDict(TypedDict):
    usertype: UserTypeDict
    category: str


class Product(BaseModel):
    id: int
    name: str
    price: str = Field(pattern=r"^Rs\. \d+$")
    brand: str
    category: CategoryDict

# product = Product.model_validate(inm)
# print(product.model_dump_json())
