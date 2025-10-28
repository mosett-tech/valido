import reflex as rx
from typing import TypedDict, Literal
import datetime

NotificationStatus = Literal["read", "unread"]
NotificationType = Literal["expiry_reminder", "fraud_alert", "system_update"]


class Notification(TypedDict):
    id: str
    type: NotificationType
    message: str
    timestamp: str
    status: NotificationStatus


class NotificationPreferences(TypedDict):
    email: bool
    sms: bool
    in_app: bool


MOCK_NOTIFICATIONS: list[Notification] = [
    {
        "id": "notif-001",
        "type": "expiry_reminder",
        "message": "Your warranty for 'Product X' is expiring in 30 days.",
        "timestamp": (
            datetime.datetime.now() - datetime.timedelta(hours=2)
        ).isoformat(),
        "status": "unread",
    },
    {
        "id": "notif-002",
        "type": "fraud_alert",
        "message": "A new critical fraud alert has been detected.",
        "timestamp": (datetime.datetime.now() - datetime.timedelta(days=1)).isoformat(),
        "status": "unread",
    },
    {
        "id": "notif-003",
        "type": "system_update",
        "message": "The system will be down for maintenance on Sunday at 2 AM.",
        "timestamp": (datetime.datetime.now() - datetime.timedelta(days=2)).isoformat(),
        "status": "read",
    },
]


class NotificationState(rx.State):
    notifications: list[Notification] = MOCK_NOTIFICATIONS
    preferences: NotificationPreferences = {"email": True, "sms": False, "in_app": True}
    show_notification_center: bool = False
    filter_status: str = "All"

    @rx.var
    def unread_count(self) -> int:
        return sum((1 for n in self.notifications if n["status"] == "unread"))

    @rx.var
    def filtered_notifications(self) -> list[Notification]:
        if self.filter_status == "All":
            return self.notifications
        return [n for n in self.notifications if n["status"] == self.filter_status]

    @rx.event
    def toggle_notification_center(self):
        self.show_notification_center = not self.show_notification_center

    @rx.event
    def mark_as_read(self, notification_id: str):
        for i, notif in enumerate(self.notifications):
            if notif["id"] == notification_id:
                self.notifications[i]["status"] = "read"
                break

    @rx.event
    def mark_all_as_read(self):
        for i in range(len(self.notifications)):
            self.notifications[i]["status"] = "read"

    @rx.event
    def toggle_preference(self, medium: str):
        current_value = self.preferences.get(medium, False)
        self.preferences[medium] = not current_value