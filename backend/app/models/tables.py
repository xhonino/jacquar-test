from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, UniqueConstraint
from .models import NotificationType


class UserNotifications(SQLModel, table=True):
    __tablename__ = "user_notifications"
    user_id: str = Field(primary_key=True)
    notification_id: str = Field(foreign_key="notifications.id", primary_key=True)
    is_read: bool = Field(default=False)

    __table_args__ = (
        UniqueConstraint("user_id", "notification_id", name="uix_user_notification"),
    )


class Notification(SQLModel, table=True):
    __tablename__ = "notifications"

    id: Optional[int] = Field(default=None, primary_key=True)
    actor_id: str
    actor_name: Optional[str]
    actor_avatar: Optional[str]
    date: datetime = Field(default=datetime.utcnow, index=True)
    type: NotificationType
    actors_count: int
    comment: Optional[str]
    previous_actor_id: Optional[str]
    previous_actor_name: Optional[str]
    previous_actor_avatar: Optional[str]
    previous_date: Optional[datetime] = Field(default=None, index=True)
    previous_comment: Optional[str]
    third_actor_name: Optional[str]
    post_id: str = Field(index=True)
    post_title: str

    __table_args__ = (
        UniqueConstraint("post_id", "type", name="uix_user_notification"),
    )
