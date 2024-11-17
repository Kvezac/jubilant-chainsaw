from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict


class DeliverySchema(BaseModel):
    id: int
    name: str = Field(max_length=255)
    weight: Decimal = Field(gt=0)
    type_id: int
    user_session: str
    content_cost: Decimal = Field(gt=0)
    shipping_cost: str

    model_config = ConfigDict(from_attributes=True)


class DeliveryCreateSchema(BaseModel):
    name: str = Field(max_length=255)
    weight: Decimal = Field(gt=0)
    type_id: int = Field(ge=1, le=3)
    content_cost: Decimal = Field(gt=0)

    model_config = ConfigDict(from_attributes=True)


class CategoriesSchema(BaseModel):
    id: int
    name: str = Field(max_length=255)

    model_config = ConfigDict(from_attributes=True)
