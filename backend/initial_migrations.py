from app.models import Notification, UserNotifications
from sqlmodel import create_engine

engine = create_engine("sqlite:///./test.db")
Notification.metadata.create_all(bind=engine)
UserNotifications.metadata.create_all(bind=engine)

