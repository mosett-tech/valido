import reflex as rx
from app.states.vendor_performance_state import VendorPerformanceState, Vendor


def vendor_row(vendor: Vendor) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.img(src=vendor["logo_url"], class_name="h-8 w-8 rounded-full"),
            rx.el.span(vendor["name"], class_name="ml-3 font-semibold"),
            class_name="p-3 flex items-center",
        ),
        rx.el.td(f"{vendor['overall_score']}/100", class_name="p-3 font-bold"),
        rx.el.td(
            f"{vendor['metrics']['customer_satisfaction_rating_avg']:.1f} / 5.0",
            class_name="p-3",
        ),
        rx.el.td(
            f"{vendor['metrics']['claim_resolution_time_avg_days']:.1f} days",
            class_name="p-3",
        ),
        rx.el.td(
            f"{vendor['metrics']['warranty_fulfillment_rate'] * 100:.1f}%",
            class_name="p-3",
        ),
        class_name="border-b hover:bg-gray-50 cursor-pointer",
    )


def vendor_performance_dashboard() -> rx.Component:
    return rx.el.div(
        rx.el.h1(
            "Vendor Performance Analytics",
            class_name="text-2xl font-bold text-gray-800 mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Top Performers",
                    class_name="text-xl font-semibold text-gray-700 mb-4",
                ),
                rx.el.div(
                    rx.foreach(
                        VendorPerformanceState.top_performers,
                        lambda vendor: rx.el.div(
                            rx.el.img(
                                src=vendor["logo_url"],
                                class_name="h-10 w-10 rounded-full",
                            ),
                            rx.el.div(
                                rx.el.p(vendor["name"], class_name="font-semibold"),
                                rx.el.p(
                                    f"Score: {vendor['overall_score']}",
                                    class_name="text-sm text-green-600 font-bold",
                                ),
                            ),
                            class_name="flex items-center gap-3 p-3 bg-white rounded-lg border shadow-sm",
                        ),
                    ),
                    class_name="grid grid-cols-2 md:grid-cols-3 gap-4",
                ),
                class_name="p-6 bg-green-50 rounded-lg border border-green-200",
            ),
            rx.el.div(
                rx.el.h2(
                    "Needs Improvement",
                    class_name="text-xl font-semibold text-gray-700 mb-4",
                ),
                rx.el.div(
                    rx.foreach(
                        VendorPerformanceState.underperforming_vendors,
                        lambda vendor: rx.el.div(
                            rx.el.img(
                                src=vendor["logo_url"],
                                class_name="h-10 w-10 rounded-full",
                            ),
                            rx.el.div(
                                rx.el.p(vendor["name"], class_name="font-semibold"),
                                rx.el.p(
                                    f"Score: {vendor['overall_score']}",
                                    class_name="text-sm text-red-600 font-bold",
                                ),
                            ),
                            class_name="flex items-center gap-3 p-3 bg-white rounded-lg border shadow-sm",
                        ),
                    ),
                    class_name="grid grid-cols-2 md:grid-cols-3 gap-4",
                ),
                class_name="p-6 bg-red-50 rounded-lg border border-red-200",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8",
        ),
        rx.el.div(
            rx.el.h2(
                "All Vendors", class_name="text-xl font-semibold text-gray-700 mb-4"
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th("Vendor"),
                            rx.el.th("Overall Score"),
                            rx.el.th("Avg. Rating"),
                            rx.el.th("Avg. Resolution"),
                            rx.el.th("Fulfillment Rate"),
                            class_name="text-left text-xs font-medium text-gray-500 uppercase p-3 bg-gray-50",
                        )
                    ),
                    rx.el.tbody(
                        rx.foreach(VendorPerformanceState.sorted_vendors, vendor_row)
                    ),
                    class_name="min-w-full divide-y divide-gray-200",
                ),
                class_name="overflow-x-auto rounded-lg border shadow-sm",
            ),
        ),
        class_name="p-4 md:p-8",
    )