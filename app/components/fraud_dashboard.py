import reflex as rx
from app.states.fraud_state import FraudState, FraudAlert
from app.components.audit_trail import audit_trail_modal


def _severity_badge(severity: str) -> rx.Component:
    color_map = {
        "Low": "bg-blue-100 text-blue-800",
        "Medium": "bg-yellow-100 text-yellow-800",
        "High": "bg-orange-100 text-orange-800",
        "Critical": "bg-red-100 text-red-800",
    }
    return rx.el.span(
        severity,
        class_name=f"px-2 py-1 text-xs font-medium rounded-full w-fit {color_map.get(severity, 'bg-gray-100 text-gray-800')}",
    )


def _status_badge(status: str) -> rx.Component:
    color_map = {
        "new": "bg-green-100 text-green-800",
        "reviewed": "bg-purple-100 text-purple-800",
        "resolved": "bg-gray-200 text-gray-600",
    }
    return rx.el.span(
        status.capitalize(),
        class_name=f"px-2 py-1 text-xs font-semibold rounded-full w-fit {color_map.get(status, 'bg-gray-100 text-gray-800')}",
    )


def _alert_details_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.content(
            rx.radix.primitives.dialog.title(
                rx.cond(
                    FraudState.selected_alert,
                    FraudState.selected_alert["type"],
                    "Alert Details",
                )
            ),
            rx.radix.primitives.dialog.description(
                rx.cond(
                    FraudState.selected_alert,
                    FraudState.selected_alert["description"],
                    "No alert selected.",
                )
            ),
            rx.el.div(
                rx.foreach(
                    rx.cond(
                        FraudState.selected_alert,
                        FraudState.selected_alert["details"].keys(),
                        [],
                    ),
                    lambda key: rx.el.div(
                        rx.el.span(
                            key.to_string().capitalize(), class_name="font-semibold"
                        ),
                        rx.el.span(
                            FraudState.selected_alert["details"]
                            .get(key, "")
                            .to_string()
                        ),
                        class_name="flex justify-between text-sm py-1 border-b",
                    ),
                ),
                class_name="mt-4 space-y-1",
            ),
            rx.el.div(
                rx.el.button(
                    "Close",
                    on_click=FraudState.deselect_alert,
                    class_name="mt-4 w-full bg-gray-200 text-gray-800 py-2 rounded-md",
                ),
                class_name="mt-4 flex justify-end",
            ),
        ),
        open=FraudState.selected_alert.is_not_none(),
        on_open_change=lambda is_open: rx.cond(
            is_open, rx.noop(), FraudState.deselect_alert
        ),
    )


def alert_row(alert: FraudAlert) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(alert["timestamp"], class_name="font-mono text-xs"),
            class_name="p-3",
        ),
        rx.el.td(alert["type"], class_name="p-3"),
        rx.el.td(
            rx.el.div(
                alert["description"],
                class_name="text-sm text-gray-600 truncate max-w-xs",
            ),
            class_name="p-3",
        ),
        rx.el.td(_severity_badge(alert["severity"]), class_name="p-3"),
        rx.el.td(f"{alert['risk_score']}/100", class_name="p-3 font-semibold"),
        rx.el.td(_status_badge(alert["status"]), class_name="p-3"),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon("eye", class_name="h-4 w-4 mr-1"),
                    "View",
                    on_click=lambda: FraudState.select_alert(alert),
                    class_name="text-xs bg-blue-500 text-white px-2 py-1 rounded-md flex items-center hover:bg-blue-600",
                ),
                rx.el.button(
                    rx.icon("history", class_name="h-4 w-4 mr-1"),
                    "Audit",
                    on_click=lambda: FraudState.view_audit_trail(alert),
                    class_name="text-xs bg-gray-500 text-white px-2 py-1 rounded-md flex items-center hover:bg-gray-600",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="p-3",
        ),
        class_name="border-b hover:bg-gray-50",
    )


def fraud_dashboard() -> rx.Component:
    return rx.el.div(
        rx.el.h1(
            "Fraud Detection Dashboard",
            class_name="text-2xl font-bold mb-6 text-gray-800",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.label(
                        "Filter by Severity:",
                        class_name="text-sm font-medium text-gray-600",
                    ),
                    rx.el.select(
                        ["All", "Low", "Medium", "High", "Critical"],
                        default_value="All",
                        on_change=FraudState.set_filter_severity,
                        class_name="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md",
                    ),
                    class_name="flex-1",
                ),
                rx.el.div(
                    rx.el.label(
                        "Filter by Status:",
                        class_name="text-sm font-medium text-gray-600",
                    ),
                    rx.el.select(
                        ["All", "new", "reviewed", "resolved"],
                        default_value="All",
                        on_change=FraudState.set_filter_status,
                        class_name="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md",
                    ),
                    class_name="flex-1",
                ),
                class_name="flex gap-4 mb-4",
            )
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Timestamp",
                            class_name="p-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Type",
                            class_name="p-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Description",
                            class_name="p-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Severity",
                            class_name="p-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Risk Score",
                            class_name="p-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Status",
                            class_name="p-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Actions",
                            class_name="p-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        class_name="bg-gray-50",
                    )
                ),
                rx.el.tbody(
                    rx.foreach(FraudState.filtered_and_sorted_alerts, alert_row)
                ),
                class_name="min-w-full divide-y divide-gray-200",
            ),
            class_name="overflow-x-auto rounded-lg border shadow-sm",
        ),
        _alert_details_modal(),
        audit_trail_modal(),
        class_name="p-6 bg-white rounded-xl shadow-md",
    )