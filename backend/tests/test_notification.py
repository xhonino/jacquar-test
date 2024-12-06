import unittest
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from app.models import (
    InputUserModel,
    InputPostModel,
    InputNotificationModel,
    NotificationType,
    InputNotificationsList,
    Notification,
    UserNotifications,
)
from app.operations import (
    aggregate_notifications,
    input_notifications,
    output_notifications,
)


class TestNotifications(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a new database in memory
        cls.engine = create_engine("sqlite:///:memory:", echo=False, future=True)
        # Create all tables
        SQLModel.metadata.create_all(bind=cls.engine)
        cls.SessionLocal = sessionmaker(
            bind=cls.engine, autocommit=False, autoflush=False
        )

    def setUp(self):
        # Each test gets a fresh session
        self.session = self.SessionLocal()

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def test_aggregate_notifications_like(self):
        # Prepare test notifications
        input_feed = InputNotificationsList(
            feed=[
                InputNotificationModel(
                    type=NotificationType.LIKE,
                    post=InputPostModel(id="post_1", title="Post Title One"),
                    user=InputUserModel(
                        id="user_1", name="User One", avatar="avatar1.png"
                    ),
                ),
                InputNotificationModel(
                    type=NotificationType.LIKE,
                    post=InputPostModel(id="post_1", title="Post Title One"),
                    user=InputUserModel(id="user_2", name="User Two"),
                ),
            ]
        )

        aggregated = aggregate_notifications(input_feed)

        self.assertIn(("post_1", NotificationType.LIKE), aggregated)
        data = aggregated[("post_1", NotificationType.LIKE)]
        self.assertEqual(data["post_id"], "post_1")
        self.assertEqual(data["post_title"], "Post Title One")
        self.assertEqual(data["type"], NotificationType.LIKE)
        self.assertEqual(len(data["entries"]), 2)
        self.assertEqual(data["entries"][0]["actor"]["name"], "User One")
        self.assertEqual(data["entries"][1]["actor"]["name"], "User Two")

    def test_aggregate_notifications_comment_requires_comment(self):
        """Test that a comment notification requires a comment"""
        with self.assertRaises(ValueError):
            InputNotificationsList(
                feed=[
                    InputNotificationModel(
                        type=NotificationType.COMMENT,
                        post=InputPostModel(id="post_2", title="Post Title Two"),
                        user=InputUserModel(id="user_1", name="User One"),
                    )
                ]
            )

    def test_input_notifications_insert_new(self):
        """Test inserting new notifications into the database"""
        input_feed = InputNotificationsList(
            feed=[
                InputNotificationModel(
                    type=NotificationType.LIKE,
                    post=InputPostModel(id="post_1", title="Post Title One"),
                    user=InputUserModel(
                        id="user_1", name="User One", avatar="avatar1.png"
                    ),
                )
            ]
        )

        input_notifications(input_feed, self.session)

        # Check that notification is inserted
        notif = (
            self.session.query(Notification)
            .filter_by(post_id="post_1", type=NotificationType.LIKE)
            .one_or_none()
        )
        self.assertIsNotNone(notif)
        self.assertEqual(notif.actor_id, "user_1")
        self.assertEqual(notif.post_title, "Post Title One")
        self.assertEqual(notif.actors_count, 1)
        self.assertEqual(notif.comment, None)

        # Check that user_notifications is inserted
        user_notif = (
            self.session.query(UserNotifications)
            .filter_by(user_id="user_1", notification_id=notif.id)
            .one_or_none()
        )
        self.assertIsNotNone(user_notif)
        self.assertFalse(user_notif.is_read)

    def test_input_notifications_update_existing(self):
        # Insert a notification first
        notif = Notification(
            actor_id="user_1",
            actor_name="User One",
            actor_avatar="avatar1.png",
            date=datetime.now(timezone.utc),
            type=NotificationType.LIKE,
            actors_count=1,
            comment=None,
            post_id="post_3",
            post_title="Old Title",
        )
        self.session.add(notif)
        self.session.commit()

        # Add user_notifications entry
        user_notif = UserNotifications(
            user_id="user_1", notification_id=notif.id, is_read=False
        )
        self.session.add(user_notif)
        self.session.commit()

        # Now send a second notification for the same post & type but with a different actor
        input_feed = InputNotificationsList(
            feed=[
                InputNotificationModel(
                    type=NotificationType.LIKE,
                    post=InputPostModel(id="post_3", title="New Post Title"),
                    user=InputUserModel(
                        id="user_2", name="User Two", avatar="avatar2.png"
                    ),
                )
            ]
        )

        input_notifications(input_feed, self.session)

        # Check that notification is updated
        updated_notif = (
            self.session.query(Notification)
            .filter_by(post_id="post_3", type=NotificationType.LIKE)
            .one()
        )
        self.assertEqual(
            updated_notif.actors_count, 2
        )  # incremented since a new actor appeared
        self.assertEqual(updated_notif.actor_id, "user_2")
        self.assertEqual(updated_notif.actor_name, "User Two")
        self.assertEqual(updated_notif.post_title, "New Post Title")  # Title updated
        self.assertIsNotNone(updated_notif.previous_actor_id)
        self.assertEqual(updated_notif.previous_actor_id, "user_1")

        # Check user_notifications for the new actor
        new_user_notif = (
            self.session.query(UserNotifications)
            .filter_by(user_id="user_2", notification_id=updated_notif.id)
            .one_or_none()
        )
        self.assertIsNotNone(new_user_notif)
        self.assertFalse(new_user_notif.is_read)

    def test_output_notifications(self):
        output = output_notifications(self.session, 0, 5, session=self.session)
        self.assertEqual(len(output.feed), 2)


if __name__ == "__main__":
    unittest.main()
