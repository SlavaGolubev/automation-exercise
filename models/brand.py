from pydantic import BaseModel


class Brand(BaseModel):
    id: int
    brand: str
