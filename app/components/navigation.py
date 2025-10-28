import reflex as rx
from app.states.navigation_state import NavigationState
from app.components.notification_center import notification_center


def nav_button(text: str, href: str) -> rx.Component:
    return rx.el.a(
        text,
        href=href,
        class_name=rx.cond(
            NavigationState.current_page == href,
            "px-4 py-2 rounded-md text-sm font-medium bg-blue-100 text-blue-700",
            "px-3 py-2 rounded-md text-sm font-medium text-gray-500 hover:bg-gray-100 hover:text-gray-700",
        ),
    )


def navigation() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("shield-check", class_name="h-6 w-6 text-blue-600"),
                rx.el.h1("Valido", class_name="text-xl font-bold text-gray-900"),
                class_name="flex items-center gap-3",
            ),
            rx.el.div(
                nav_button("Home", "/landing"),
                nav_button("Fraud Dashboard", "/"),
                nav_button("Analytics", "/analytics"),
                nav_button("Loyalty", "/loyalty"),
                nav_button("Claims", "/claims"),
                nav_button("Marketplace", "/marketplace"),
                nav_button("Recommendations", "/recommendations"),
                nav_button("Reports", "/reports"),
                nav_button("Vendors", "/vendor-performance"),
                class_name="flex items-center space-x-1",
            ),
            rx.el.div(notification_center(), class_name="flex items-center gap-4"),
            class_name="flex items-center justify-between p-4 border-b",
        ),
        class_name="bg-white shadow-sm sticky top-0 z-10",
    )