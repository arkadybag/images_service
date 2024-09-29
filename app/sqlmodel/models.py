from uuid import UUID as _UUID
from uuid import uuid4

from sqlalchemy import UUID, Float, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.sqlmodel.db import Base


class Image(Base):
    __tablename__ = "images"

    id: Mapped[_UUID] = mapped_column(UUID(), primary_key=True, default=uuid4, index=True)


class Frame(Base):
    __tablename__ = "frames"

    id: Mapped[_UUID] = mapped_column(UUID(), primary_key=True, default=uuid4, index=True)
    image_id: Mapped[_UUID] = mapped_column(ForeignKey("images.id"))
    depth: Mapped[float] = mapped_column(Float(), index=True)
    points: Mapped[list[int]] = mapped_column(ARRAY(Integer))
