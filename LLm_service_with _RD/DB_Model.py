from datetime import datetime,UTC
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

class Base(DeclarativeBase):
    pass

class Conversation(Base):
    __tablename__ = "conversations"

    id : Mapped[int] = mapped_column(primary_key=True)
    title : Mapped[str] = mapped_column()
    model_type : Mapped[str] = mapped_column(index=True)
    created_at : Mapped[datetime] = mapped_column(default=datetime.now(UTC+3))
    updated_at :  Mapped[datetime] = mapped_column(
        default = datetime.now(UTC), onupdate = datetime.now(UTC)
    )
    messages : Mapped[list["Message"]]

class Message(Base):
    __tablename__ = "messages"

    id : Mapped[int] = mapped_column(primary_key=True)
    conversation_id = mapped_column(ForeignKey("conversations.id"), ondelete= "CASCADE", index=True)