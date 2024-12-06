from enum import Enum
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, validator


class NotificationType(str, Enum):
    LIKE = "Like"
    COMMENT = "Comment"


class OutputNotification(BaseModel):
    id: int
    actor_id: str
    actor_name: str
    actor_avatar: str
    notification_date: datetime
    previous_actor_name: Optional[str] = None
    type: str
    actors_count: int
    comment: Optional[str] = None
    post_id: str
    post_title: str
    is_read: int


class OutputNotificationList(BaseModel):
    feed: Optional[List[OutputNotification]] = []


class InputPostModel(BaseModel):
    id: str
    title: str


class InputUserModel(BaseModel):
    id: str
    name: Optional[str] = None
    avatar: Optional[str] = None


class InputCommentModel(BaseModel):
    id: str
    commentText: str


class InputNotificationModel(BaseModel):
    type: NotificationType
    post: InputPostModel
    user: InputUserModel
    comment: Optional[InputCommentModel] = None

    @validator("comment", pre=True, always=True)
    def validate_comment(cls, v, values):
        if v is None and values["type"] == NotificationType.COMMENT:
            raise ValueError("Comment is required for comment notifications")
        return v


class InputNotificationsList(BaseModel):
    feed: Optional[List[InputNotificationModel]] = None
