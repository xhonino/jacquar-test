from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_session
from sqlalchemy.orm import Session
from app.models import (
    UserNotifications,
    OutputNotificationList,
    InputNotificationsList,
)
from app.operations import input_notifications, output_notifications
from pydantic import ValidationError

router = APIRouter(
    tags=["notifications"],
    prefix="/notifications",
)


@router.get("", response_model=OutputNotificationList)
def list_notifications(
    user_id: str,  # This will come from the JWT token in a real-world application
    skip: int = 0,
    limit: int = 5,
    session: Session = Depends(get_session),
):
    """Retrieve a list of notifications for a specific user."""
    return output_notifications(user_id, skip, limit, session)


@router.post(
    "/read",
    status_code=status.HTTP_200_OK,
)
def mark_notifications_as_read(
    notification_ids: list[int], session: Session = Depends(get_session)
):
    """
    Mark notifications as read. Updates the 'read' status of notifications specified by their IDs.
    Note: This function does not check if the notifications exist before updating.
    """
    session.query(UserNotifications).filter(
        UserNotifications.notification_id.in_(notification_ids)
    ).update({"is_read": True}, synchronize_session=False)
    session.commit()
    return {
        "message": "Notifications marked as read",
        "status_code": status.HTTP_200_OK,
    }


@router.post("/consume")
def consume_notification_feed(
    feed: InputNotificationsList, session: Session = Depends(get_session)
):
    """Consume a notification feed and update the database."""
    try:
        input_notifications(feed, session)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"An error occurred: {str(e)}",
        )
    return {
        "message": "Notification feed processed successfully",
        "status_code": status.HTTP_200_OK,
    }
