from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Dict, Tuple
from app.models import (
    Notification,
    UserNotifications,
    InputNotificationsList,
    OutputNotificationList,
    OutputNotification,
)


def aggregate_notifications(
    feed: "InputNotificationsList",
) -> Dict[Tuple[str, str], Dict]:
    """
    Aggregate the notification feed by (post_id, type) before writing to the database.
    This reduces the number of DB operations required to create/update the notifications.

    Returns a dictionary of aggregated notifications keyed by (post_id, type).
    """
    aggregated: Dict[Tuple[str, str], Dict] = {}

    for input_notification in feed.feed:
        post_id = input_notification.post.id
        notification_type = input_notification.type
        key = (post_id, notification_type)

        if key not in aggregated:
            aggregated[key] = {
                "post_id": post_id,
                "post_title": input_notification.post.title,
                "type": notification_type,
                "entries": [],
            }

        entry = {
            "actor": {
                "id": input_notification.user.id,
                "name": input_notification.user.name,
                "avatar": getattr(input_notification.user, "avatar", None),
            },
            "comment": (
                input_notification.comment.commentText
                if input_notification.comment
                else None
            ),
        }
        aggregated[key]["entries"].append(entry)

    return aggregated


def input_notifications(feed: "InputNotificationsList", session: Session):
    """
    Processes and validates a notification feed before updating the database.
    We first aggregate the feed using `aggregate_notifications`, then update the DB.
    """
    aggregated = aggregate_notifications(feed)

    for (post_id, notification_type), data in aggregated.items():
        # Each aggregated group may contain multiple entries.
        for entry in data["entries"]:
            comment_text = entry["comment"]
            actor_id = entry["actor"]["id"]
            actor_name = entry["actor"]["name"]
            actor_avatar = entry["actor"]["avatar"]
            post_title = data["post_title"]

            # Check if the notification exists in the database
            notification = (
                session.query(Notification)
                .filter(
                    Notification.post_id == post_id,
                    Notification.type == notification_type,
                )
                .one_or_none()
            )

            if not notification:
                notification = Notification(
                    actor_id=actor_id,
                    actor_name=actor_name,
                    actor_avatar=actor_avatar,
                    date=datetime.now(timezone.utc),
                    type=notification_type,
                    actors_count=1,
                    comment=comment_text,
                    post_id=post_id,
                    post_title=post_title,
                )
                session.add(notification)
                session.flush()
            else:
                if notification.actor_id != actor_id:
                    notification.actors_count += 1
                    # Keep track of previous actor and comment details
                    notification.third_actor_name = notification.previous_actor_name
                    notification.previous_actor_id = notification.actor_id
                    notification.previous_actor_name = notification.actor_name
                    notification.previous_actor_avatar = notification.actor_avatar
                    notification.previous_date = notification.date
                    notification.previous_comment = notification.comment

                # Update with the latest actor/comment
                notification.actor_id = actor_id
                notification.actor_name = actor_name
                notification.actor_avatar = actor_avatar
                notification.date = datetime.now(timezone.utc)
                notification.comment = comment_text
                if post_title != notification.post_title:
                    session.query(Notification).filter(
                        Notification.post_id == post_id
                    ).update({"post_title": post_title})

            # Ensure UserNotifications is updated
            user_notification = session.query(UserNotifications).get(
                (actor_id, notification.id)
            )
            if not user_notification:
                user_notification = UserNotifications(
                    user_id=actor_id,
                    notification_id=notification.id,
                    is_read=False,
                )
                session.add(user_notification)

    session.commit()


def output_notifications(
    actor_id: str,
    skip: int,
    limit: int,
    session: Session,
) -> OutputNotificationList:
    """
    Retrieve a list of notifications for a specific user.

    Args:
        actor_id (str): ID of the user to retrieve notifications for.
        skip (int): Number of notifications to skip.
        limit (int: Maximum number of notifications to return.
        session (Session): Database connection session.

    Returns:
        OutputNotificationList: A list of notifications.
    """

    query = text(
        """
        SELECT DISTINCT n.post_id,
            CASE
                WHEN n.actor_id = '{actor_id}' THEN n.previous_actor_id
                ELSE n.actor_id
            END AS actor_id,
            CASE
                WHEN n.actor_id = '{actor_id}' THEN n.previous_actor_name
                ELSE n.actor_name
            END AS actor_name,
            CASE
                WHEN n.actor_id = '{actor_id}' THEN n.previous_actor_avatar
                ELSE n.actor_avatar
            END AS actor_avatar,
            CASE
                WHEN n.actor_id = '{actor_id}' THEN n.previous_date
                ELSE n.date
            END AS notification_date,
            CASE
                WHEN n.actor_id = '{actor_id}' THEN n.third_actor_name
                ELSE n.previous_actor_name
            END AS previous_actor_name,
            CASE
                WHEN n.actor_id = '{actor_id}' THEN n.actors_count - 1
                ELSE n.actors_count
            END AS actors_count,
            n.type,
            n.comment,
            n.post_title,
            un.is_read,
            n.id AS id
        FROM user_notifications un
        JOIN notifications n
            ON un.notification_id = n.id
        WHERE NOT (n.actor_id = '{actor_id}' AND n.actors_count = 1)
        ORDER BY notification_date DESC
        LIMIT {limit} OFFSET {skip}
    """.format(
            actor_id=actor_id,
            limit=limit,
            skip=skip,
        )
    )
    result = session.execute(query).fetchall()
    rows_as_dicts = [row._mapping for row in result]
    result = [OutputNotification(**row) for row in rows_as_dicts]
    return OutputNotificationList(feed=result)
