from decimal import Decimal

from pydantic import BaseModel, field_validator, Field


class DeliverySchema(BaseModel):
    id: int
    name: str
    name: str = Field(max_length=255)
    weight: Decimal = Field(gt=0)
    type_id: int
    user_session: str
    content_cost: Decimal
    shipping_cost: Decimal | str


class DeliveryCreateSchema(BaseModel):
    name: str = Field(max_length=255)
    weight: Decimal = Field(gt=0)
    type_id: int = Field(ge=1, le=3)
    user_session: str
    content_cost: Decimal = Field(gt=0)


class CategoriesSchema(BaseModel):
    id: int
    name: str = Field(max_length=255)
