import reflex as rx
import reflex_enterprise as rxe
from app.states.analytics_state import AnalyticsState
from reflex_enterprise.components.map.types import latlng


def chart_card(title: str, chart: rx.Component) -> rx.Component:
    return rx.el.div(
        rx.el.h3(title, class_name="font-semibold text-lg text-gray-800 mb-4"),
        chart,
        class_name="p-6 bg-white rounded-xl shadow-md",
    )


def analytics_dashboard() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Advanced Analytics Dashboard",
                class_name="text-2xl font-bold text-gray-800",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.label("Export Format:", class_name="text-sm font-medium"),
                    rx.el.select(
                        ["csv", "excel", "pdf"],
                        default_value="csv",
                        on_change=AnalyticsState.set_export_format,
                        class_name="rounded-md border-gray-300 ml-2",
                    ),
                    class_name="flex items-center",
                ),
                rx.el.button(
                    rx.icon("cloud_download", class_name="h-4 w-4 mr-2"),
                    "Export Data",
                    class_name="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 flex items-center",
                ),
                class_name="flex items-center gap-4",
            ),
            class_name="flex justify-between items-center mb-6",
        ),
        rx.el.div(
            chart_card(
                "90-Day Sales Trend",
                rx.recharts.line_chart(
                    rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
                    rx.recharts.x_axis(data_key="date"),
                    rx.recharts.y_axis(),
                    rx.recharts.tooltip(),
                    rx.recharts.line(
                        data_key="sales", stroke="#8884d8", type_="monotone"
                    ),
                    data=AnalyticsState.sales_data,
                    height=300,
                ),
            ),
            chart_card(
                "RFM Customer Segmentation",
                rx.recharts.bar_chart(
                    rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
                    rx.recharts.x_axis(data_key="segment"),
                    rx.recharts.y_axis(),
                    rx.recharts.tooltip(),
                    rx.recharts.bar(data_key="count", fill="#82ca9d"),
                    data=AnalyticsState.rfm_segments,
                    height=300,
                ),
            ),
            chart_card(
                "Warranty Claim Predictions",
                rx.recharts.area_chart(
                    rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
                    rx.recharts.x_axis(data_key="month"),
                    rx.recharts.y_axis(),
                    rx.recharts.tooltip(),
                    rx.recharts.area(
                        data_key="predicted_claims",
                        stroke="#ffc658",
                        fill="#ffc658",
                        type_="monotone",
                    ),
                    data=AnalyticsState.claim_predictions,
                    height=300,
                ),
            ),
            chart_card(
                "Validation Heat Map",
                rxe.map(
                    rxe.map.tile_layer(
                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
                        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                    ),
                    rx.el.div(),
                    id="heat-map",
                    center=latlng(lat=-1.286389, lng=36.817223),
                    zoom=6.0,
                    height="300px",
                    class_name="rounded-lg",
                ),
            ),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-6",
        ),
        class_name="p-4",
    )