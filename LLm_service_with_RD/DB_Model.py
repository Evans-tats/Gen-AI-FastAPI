from datetime import datetime, UTC, timedelta
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

def get_EAT_time():
    return datetime.now(UTC) + timedelta(hours=3)

class Base(DeclarativeBase):
    pass

class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    model_type: Mapped[str] = mapped_column(index=True)
    created_at: Mapped[datetime] = mapped_column(default=get_EAT_time)
    updated_at: Mapped[datetime] = mapped_column(default=get_EAT_time, onupdate=get_EAT_time)

    messages: Mapped[list["Message"]] = relationship(
        "Message", back_populates="conversation", cascade="all, delete-orphan"
    )

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    conversation_id = mapped_column(ForeignKey("conversations.id", ondelete="CASCADE"), index=True)
    prompt_content: Mapped[str] = mapped_column()
    response_content: Mapped[str] = mapped_column()
    prompt_token: Mapped[int | None] = mapped_column()
    response_token: Mapped[int | None] = mapped_column()
    is_success: Mapped[bool | None] = mapped_column()
    status_code: Mapped[int] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=get_EAT_time)
    updated_at: Mapped[datetime] = mapped_column(default=get_EAT_time, onupdate=get_EAT_time)

    conversation: Mapped["Conversation"] = relationship(
        "Conversation", back_populates="messages"
    )
