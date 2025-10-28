import reflex as rx
from app.states.notification_state import NotificationState


def preference_toggle(
    label: str, medium: str, is_checked: rx.Var[bool]
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="font-medium text-gray-700"),
        rx.el.button(
            rx.el.span(
                class_name=rx.cond(is_checked, "translate-x-5", "translate-x-0")
                + " pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition-transform duration-200 ease-in-out"
            ),
            on_click=lambda: NotificationState.toggle_preference(medium),
            class_name=rx.cond(is_checked, "bg-blue-600", "bg-gray-200")
            + " relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2",
        ),
        class_name="flex items-center justify-between py-4 border-b",
    )


def notification_preferences() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Notification Preferences",
            class_name="text-xl font-bold text-gray-800 mb-4",
        ),
        rx.el.div(
            rx.el.p(
                "Manage how you receive notifications from Valido.",
                class_name="text-sm text-gray-600 mb-6",
            ),
            preference_toggle(
                "Email Notifications", "email", NotificationState.preferences["email"]
            ),
            preference_toggle(
                "SMS Alerts", "sms", NotificationState.preferences["sms"]
            ),
            preference_toggle(
                "In-App Notifications",
                "in_app",
                NotificationState.preferences["in_app"],
            ),
            class_name="max-w-2xl",
        ),
        class_name="p-6 bg-white rounded-xl shadow-md",
    )