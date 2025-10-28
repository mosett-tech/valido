import reflex as rx
import reflex_enterprise as rxe
from app.components.fraud_dashboard import fraud_dashboard
from app.components.analytics_dashboard import analytics_dashboard
from app.components.loyalty_dashboard import loyalty_dashboard
from app.components.navigation import navigation
from app.components.notification_preferences import notification_preferences
from app.states.notification_state import NotificationState, Notification


def index() -> rx.Component:
    return rx.el.div(
        navigation(),
        rx.el.main(fraud_dashboard(), class_name="p-4 md:p-8"),
        class_name="font-['Inter'] bg-gray-50 min-h-screen",
    )


def analytics() -> rx.Component:
    return rx.el.div(
        navigation(),
        rx.el.main(analytics_dashboard(), class_name="p-4 md:p-8"),
        class_name="font-['Inter'] bg-gray-50 min-h-screen",
    )


def full_notification_item(notification: Notification) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                rx.cond(
                    notification["type"] == "expiry_reminder",
                    "clock",
                    rx.cond(
                        notification["type"] == "fraud_alert", "shield-alert", "info"
                    ),
                ),
                class_name="h-5 w-5 text-gray-500 mr-4",
            ),
            rx.el.div(
                rx.el.p(
                    notification["message"],
                    class_name="text-sm font-medium text-gray-900",
                ),
                rx.el.p(notification["timestamp"], class_name="text-xs text-gray-500"),
            ),
        ),
        rx.el.span(
            notification["status"].capitalize(),
            class_name=rx.cond(
                notification["status"] == "unread",
                "text-xs font-semibold px-2 py-1 rounded-full bg-blue-100 text-blue-800",
                "text-xs font-semibold px-2 py-1 rounded-full bg-gray-100 text-gray-800",
            ),
        ),
        class_name="flex items-center justify-between p-4 border-b hover:bg-gray-50",
    )


def notifications() -> rx.Component:
    return rx.el.div(
        navigation(),
        rx.el.main(
            rx.el.h1(
                "Notifications", class_name="text-2xl font-bold text-gray-800 mb-6"
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "History", class_name="text-xl font-bold text-gray-800 mb-4"
                    ),
                    rx.el.div(
                        rx.foreach(
                            NotificationState.notifications, full_notification_item
                        ),
                        class_name="bg-white rounded-xl shadow-md divide-y",
                    ),
                    class_name="flex-grow",
                ),
                rx.el.div(
                    notification_preferences(),
                    class_name="w-full lg:w-96 lg:ml-8 mt-8 lg:mt-0",
                ),
                class_name="lg:flex",
            ),
            class_name="p-4 md:p-8",
        ),
        class_name="font-['Inter'] bg-gray-50 min-h-screen",
    )


def loyalty() -> rx.Component:
    return rx.el.div(
        navigation(),
        rx.el.main(loyalty_dashboard(), class_name="p-4 md:p-8"),
        class_name="font-['Inter'] bg-gray-50 min-h-screen",
    )


app = rxe.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
        rx.el.link(
            rel="stylesheet",
            href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css",
            integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=",
            cross_origin="",
        ),
    ],
)
app.add_page(index)
app.add_page(analytics, route="/analytics")
app.add_page(notifications, route="/notifications")
from app.components.claims_dashboard import claims_dashboard
from app.components.marketplace import marketplace_dashboard
from app.components.recommendations_dashboard import recommendations_dashboard
from app.components.reports_hub import reports_hub
from app.components.vendor_performance import vendor_performance_dashboard


def claims() -> rx.Component:
    return rx.el.div(
        navigation(),
        rx.el.main(claims_dashboard(), class_name="p-4 md:p-8"),
        class_name="font-['Inter'] bg-gray-50 min-h-screen",
    )


def marketplace() -> rx.Component:
    return rx.el.div(
        navigation(),
        rx.el.main(marketplace_dashboard(), class_name="p-4 md:p-8"),
        class_name="font-['Inter'] bg-gray-50 min-h-screen",
    )


def recommendations() -> rx.Component:
    return rx.el.div(
        navigation(),
        rx.el.main(recommendations_dashboard(), class_name="p-4 md:p-8"),
        class_name="font-['Inter'] bg-gray-50 min-h-screen",
    )


def reports() -> rx.Component:
    return rx.el.div(
        navigation(),
        rx.el.main(reports_hub(), class_name="p-4 md:p-8"),
        class_name="font-['Inter'] bg-gray-50 min-h-screen",
    )


def vendor_performance() -> rx.Component:
    return rx.el.div(
        navigation(),
        rx.el.main(vendor_performance_dashboard(), class_name="p-4 md:p-8"),
        class_name="font-['Inter'] bg-gray-50 min-h-screen",
    )


app.add_page(loyalty, route="/loyalty")
app.add_page(claims, route="/claims")
app.add_page(marketplace, route="/marketplace")
app.add_page(recommendations, route="/recommendations")
app.add_page(reports, route="/reports")
app.add_page(vendor_performance, route="/vendor-performance")