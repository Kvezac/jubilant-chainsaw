from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.app.config import settings
from src.app.infrastructure.database.database import Base


class Categories(Base):
    __tablename__ = 'Categories'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str]


class Deliveries(Base):
    __tablename__ = 'Deliveries'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str]
    weight: Mapped[Decimal]
    type_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=False)
    user_session: Mapped[str] = mapped_column(nullable=False)
    content_value: Mapped[Decimal] = mapped_column(default='0')
    shipping_cost: Mapped[str] = mapped_column(default='Не рассчитано')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=settings.time_zone),
                                                 server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(settings.time_zone), onupdate=func.now())

    type = relationship("Categories")
