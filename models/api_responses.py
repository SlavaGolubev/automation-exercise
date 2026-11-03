from typing import Optional

from pydantic import BaseModel
from models.brand import Brand
from models.product import Product
from models.user import RegistrationData


class APIResponse(BaseModel):
    responseCode: int


class APIError(APIResponse):
    message: str

class APIMessage(APIResponse):
    message: str

class ProductsResponse(APIResponse):
    products: list[Product]


class BrandsResponse(APIResponse):
    brands: list[Brand]

class UserDetail(BaseModel):
    """Описывает ТОЛЬКО те поля, которые реально приходят в объекте 'user' от сервера"""
    id: int
    name: str
    email: str
    title: str
    birth_day: str
    birth_month: str
    birth_year: str
    first_name: str
    last_name: str
    company: str
    address1: str
    address2: Optional[str] = None  # Может прийти как пустая строка или отсутствовать
    country: str
    state: str
    city: str
    zipcode: str
    # Обрати внимание: password, newsletter, mobile_number здесь НЕТ.
    # И это правильно, Pydantic не будет требовать их наличия.

class UserDetailsResponse(APIResponse):
    """Финальная модель ответа эндпоинта getUserDetailByEmail"""
    user: UserDetail