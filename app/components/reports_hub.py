import reflex as rx
from app.states.reports_state import ReportsState, Report


def report_row(report: Report) -> rx.Component:
    return rx.el.tr(
        rx.el.td(report["id"], class_name="p-3 font-mono text-xs"),
        rx.el.td(report["type"], class_name="p-3"),
        rx.el.td(report["date_range"], class_name="p-3"),
        rx.el.td(report["generated_at"], class_name="p-3"),
        rx.el.td(report["format"], class_name="p-3"),
        rx.el.td(
            rx.el.span(
                report["status"],
                class_name=rx.match(
                    report["status"],
                    (
                        "Completed",
                        "bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs",
                    ),
                    (
                        "Processing",
                        "bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full text-xs",
                    ),
                    (
                        "Failed",
                        "bg-red-100 text-red-800 px-2 py-1 rounded-full text-xs",
                    ),
                    "bg-gray-100 text-gray-800 px-2 py-1 rounded-full text-xs",
                ),
            ),
            class_name="p-3",
        ),
        rx.el.td(
            rx.cond(
                report["status"] == "Completed",
                rx.el.a(
                    rx.icon("download", class_name="h-4 w-4 mr-1"),
                    "Download",
                    href=report["download_url"],
                    class_name="text-blue-600 hover:underline flex items-center text-sm",
                ),
                rx.el.span("-", class_name="text-gray-500"),
            ),
            class_name="p-3",
        ),
        class_name="border-b hover:bg-gray-50",
    )


def reports_hub() -> rx.Component:
    return rx.el.div(
        rx.el.h1(
            "Advanced Reports Hub", class_name="text-2xl font-bold text-gray-800 mb-6"
        ),
        rx.el.div(
            rx.el.h2(
                "Generate New Report",
                class_name="text-xl font-semibold text-gray-700 mb-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.label("Report Type", class_name="text-sm font-medium"),
                    rx.el.select(
                        ReportsState.report_types,
                        on_change=ReportsState.set_selected_report_type,
                        class_name="w-full p-2 border rounded-md mt-1",
                    ),
                ),
                rx.el.div(
                    rx.el.label("Format", class_name="text-sm font-medium"),
                    rx.el.select(
                        ReportsState.report_formats,
                        on_change=ReportsState.set_selected_format,
                        class_name="w-full p-2 border rounded-md mt-1",
                    ),
                ),
                rx.el.div(
                    rx.el.label("Start Date", class_name="text-sm font-medium"),
                    rx.el.input(
                        type="date",
                        on_change=ReportsState.set_start_date,
                        default_value=ReportsState.start_date,
                        class_name="w-full p-2 border rounded-md mt-1",
                    ),
                ),
                rx.el.div(
                    rx.el.label("End Date", class_name="text-sm font-medium"),
                    rx.el.input(
                        type="date",
                        on_change=ReportsState.set_end_date,
                        default_value=ReportsState.end_date,
                        class_name="w-full p-2 border rounded-md mt-1",
                    ),
                ),
                rx.el.button(
                    rx.cond(
                        ReportsState.is_generating,
                        rx.fragment(
                            rx.spinner(class_name="h-4 w-4 mr-2"), "Generating..."
                        ),
                        rx.fragment(
                            rx.icon("play", class_name="h-4 w-4 mr-2"),
                            "Generate Report",
                        ),
                    ),
                    on_click=ReportsState.generate_report,
                    disabled=ReportsState.is_generating,
                    class_name="bg-blue-600 text-white px-4 py-2 rounded-md flex items-center justify-center col-span-2 md:col-span-1 self-end",
                ),
                class_name="grid grid-cols-2 md:grid-cols-5 gap-4 items-end",
            ),
            class_name="p-6 bg-white rounded-lg shadow-md border mb-8",
        ),
        rx.el.div(
            rx.el.h2(
                "Report History", class_name="text-xl font-semibold text-gray-700 mb-4"
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th("ID"),
                            rx.el.th("Type"),
                            rx.el.th("Date Range"),
                            rx.el.th("Generated At"),
                            rx.el.th("Format"),
                            rx.el.th("Status"),
                            rx.el.th("Action"),
                            class_name="text-left text-xs font-medium text-gray-500 uppercase p-3 bg-gray-50",
                        )
                    ),
                    rx.el.tbody(rx.foreach(ReportsState.report_history, report_row)),
                    class_name="min-w-full divide-y divide-gray-200",
                ),
                class_name="overflow-x-auto rounded-lg border shadow-sm",
            ),
        ),
        class_name="p-4 md:p-8",
    )