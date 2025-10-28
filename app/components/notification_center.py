import reflex as rx
from app.states.notification_state import NotificationState, Notification


def notification_item(notification: Notification) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(tag="bell", class_name="w-4 h-4 text-gray-500"),
            class_name="flex-shrink-0",
        ),
        rx.el.div(
            rx.el.p(
                notification["message"], class_name="text-sm font-medium text-gray-800"
            ),
            rx.el.p(notification["timestamp"], class_name="text-xs text-gray-500"),
        ),
        rx.cond(
            notification["status"] == "unread",
            rx.el.div(
                on_click=lambda: NotificationState.mark_as_read(notification["id"])
            ),
            None,
        ),
        class_name="flex items-start gap-3 p-3 hover:bg-gray-50 rounded-lg cursor-pointer",
    )


def notification_center() -> rx.Component:
    return rx.el.div(
        rx.el.button(
            rx.icon("bell", class_name="h-5 w-5"),
            rx.cond(
                NotificationState.unread_count > 0,
                rx.el.span(
                    NotificationState.unread_count.to_string(),
                    class_name="absolute -top-1 -right-1 flex h-4 w-4 items-center justify-center rounded-full bg-red-500 text-xs font-bold text-white",
                ),
                None,
            ),
            on_click=NotificationState.toggle_notification_center,
            class_name="relative rounded-full p-2 text-gray-500 hover:bg-gray-100 hover:text-gray-700",
        ),
        rx.cond(
            NotificationState.show_notification_center,
            rx.el.div(
                rx.el.div(
                    rx.el.h3("Notifications", class_name="font-semibold text-gray-900"),
                    rx.el.button(
                        "Mark all as read",
                        on_click=NotificationState.mark_all_as_read,
                        class_name="text-xs text-blue-600 hover:underline",
                    ),
                    class_name="flex justify-between items-center p-4 border-b",
                ),
                rx.el.div(
                    rx.foreach(
                        NotificationState.filtered_notifications, notification_item
                    ),
                    class_name="overflow-y-auto max-h-96 p-2 space-y-1",
                ),
                rx.el.div(
                    rx.el.a(
                        "View all notifications",
                        href="/notifications",
                        class_name="w-full block text-center py-2 text-sm font-medium text-blue-600 hover:bg-gray-50",
                    ),
                    class_name="border-t",
                ),
                class_name="absolute right-0 mt-2 w-80 origin-top-right rounded-xl bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none z-20",
            ),
            None,
        ),
        class_name="relative",
    )