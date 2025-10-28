import reflex as rx
from app.states.claims_state import ClaimsState, Claim


def _status_badge(status: str) -> rx.Component:
    color_map = {
        "pending_review": "bg-yellow-100 text-yellow-800",
        "approved": "bg-blue-100 text-blue-800",
        "in_progress": "bg-indigo-100 text-indigo-800",
        "completed": "bg-green-100 text-green-800",
        "rejected": "bg-red-100 text-red-800",
    }
    return rx.el.span(
        status.replace("_", " ").title(),
        class_name=f"px-2 py-1 text-xs font-semibold rounded-full w-fit {color_map.get(status, 'bg-gray-100 text-gray-800')}",
    )


def claim_details_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.content(
            rx.radix.primitives.dialog.title(
                rx.cond(
                    ClaimsState.selected_claim,
                    f"Claim Details: {ClaimsState.selected_claim['id']}",
                    "Claim Details",
                )
            ),
            rx.el.div(
                rx.cond(
                    ClaimsState.selected_claim,
                    rx.el.div(
                        rx.el.div(
                            rx.el.h3("Product", class_name="font-semibold"),
                            rx.el.p(ClaimsState.selected_claim["product_name"]),
                            class_name="text-sm",
                        ),
                        rx.el.div(
                            rx.el.h3("Submitted", class_name="font-semibold mt-2"),
                            rx.el.p(ClaimsState.selected_claim["submitted_date"]),
                            class_name="text-sm",
                        ),
                        rx.el.div(
                            rx.el.h3("Description", class_name="font-semibold mt-2"),
                            rx.el.p(
                                ClaimsState.selected_claim["description"],
                                class_name="p-2 bg-gray-50 rounded-md",
                            ),
                        ),
                        rx.el.div(
                            rx.el.h3("Attachments", class_name="font-semibold mt-2"),
                            rx.el.ul(
                                rx.foreach(
                                    ClaimsState.selected_claim["attachments"],
                                    lambda attachment: rx.el.li(
                                        rx.el.a(
                                            attachment,
                                            href="#",
                                            class_name="text-blue-500 underline",
                                        )
                                    ),
                                ),
                                class_name="list-disc list-inside",
                            ),
                        ),
                        rx.el.div(
                            rx.el.h3(
                                "Resolution Notes", class_name="font-semibold mt-2"
                            ),
                            rx.el.p(
                                ClaimsState.selected_claim[
                                    "resolution_notes"
                                ].to_string(),
                                class_name="p-2 bg-gray-50 rounded-md",
                            ),
                        ),
                    ),
                    rx.el.p("No claim selected."),
                ),
                class_name="mt-4 space-y-2",
            ),
            rx.el.div(
                rx.el.button(
                    "Close",
                    on_click=ClaimsState.deselect_claim,
                    class_name="mt-4 w-full bg-gray-200 text-gray-800 py-2 rounded-md",
                ),
                class_name="mt-4 flex justify-end",
            ),
            class_name="max-h-[80vh] overflow-y-auto",
        ),
        open=ClaimsState.selected_claim.is_not_none(),
        on_open_change=lambda is_open: rx.cond(
            is_open, rx.noop(), ClaimsState.deselect_claim
        ),
    )


def new_claim_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.content(
            rx.radix.primitives.dialog.title("Submit New Warranty Claim"),
            rx.el.div(
                rx.el.label("Warranty ID", class_name="font-medium text-sm"),
                rx.el.input(
                    placeholder="Enter your warranty ID (e.g., W-ABC-123)",
                    on_change=ClaimsState.set_new_claim_warranty_id,
                    class_name="w-full p-2 border rounded-md mt-1",
                ),
                rx.el.label(
                    "Problem Description", class_name="font-medium text-sm mt-4"
                ),
                rx.el.textarea(
                    placeholder="Describe the issue with your product in detail...",
                    on_change=ClaimsState.set_new_claim_description,
                    class_name="w-full p-2 border rounded-md mt-1 h-32",
                ),
                rx.el.div(
                    rx.icon("paperclip", class_name="h-4 w-4 mr-2"),
                    rx.el.p("Attach Photos/Videos (optional)"),
                    class_name="flex items-center mt-4 text-sm text-gray-600 p-4 border-2 border-dashed rounded-md cursor-pointer hover:bg-gray-50",
                ),
                class_name="mt-4",
            ),
            rx.el.div(
                rx.el.button(
                    "Cancel",
                    on_click=ClaimsState.toggle_new_claim_modal,
                    class_name="mr-2 bg-gray-200 text-gray-800 px-4 py-2 rounded-md",
                ),
                rx.el.button(
                    "Submit Claim",
                    on_click=ClaimsState.submit_new_claim,
                    class_name="bg-blue-600 text-white px-4 py-2 rounded-md",
                ),
                class_name="flex justify-end mt-6",
            ),
        ),
        open=ClaimsState.show_new_claim_modal,
        on_open_change=lambda is_open: rx.cond(
            is_open, rx.noop(), ClaimsState.toggle_new_claim_modal
        ),
    )


def claim_row(claim: Claim) -> rx.Component:
    return rx.el.tr(
        rx.el.td(claim["id"], class_name="p-3 font-mono text-xs"),
        rx.el.td(claim["product_name"], class_name="p-3"),
        rx.el.td(claim["customer_name"], class_name="p-3"),
        rx.el.td(claim["submitted_date"], class_name="p-3"),
        rx.el.td(_status_badge(claim["status"]), class_name="p-3"),
        rx.el.td(
            rx.el.button(
                rx.icon("eye", class_name="h-4 w-4 mr-1"),
                "View",
                on_click=lambda: ClaimsState.select_claim(claim),
                class_name="text-xs bg-blue-500 text-white px-2 py-1 rounded-md flex items-center hover:bg-blue-600",
            ),
            class_name="p-3",
        ),
        class_name="border-b hover:bg-gray-50",
    )


def claims_dashboard() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Warranty Claims Portal", class_name="text-2xl font-bold text-gray-800"
            ),
            rx.el.button(
                rx.icon("circle_plus", class_name="h-4 w-4 mr-2"),
                "File a New Claim",
                on_click=ClaimsState.toggle_new_claim_modal,
                class_name="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 flex items-center",
            ),
            class_name="flex justify-between items-center mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Filter by Status:", class_name="text-sm font-medium text-gray-600"
                ),
                rx.el.select(
                    [
                        "All",
                        "pending_review",
                        "approved",
                        "rejected",
                        "in_progress",
                        "completed",
                    ],
                    default_value="All",
                    on_change=ClaimsState.set_filter_status,
                    class_name="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md",
                ),
                class_name="flex-1 max-w-xs",
            ),
            class_name="flex gap-4 mb-4",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Claim ID",
                            class_name="p-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Product",
                            class_name="p-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Customer",
                            class_name="p-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Date Submitted",
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
                rx.el.tbody(rx.foreach(ClaimsState.filtered_claims, claim_row)),
                class_name="min-w-full divide-y divide-gray-200",
            ),
            class_name="overflow-x-auto rounded-lg border shadow-sm",
        ),
        claim_details_modal(),
        new_claim_modal(),
        class_name="p-6 bg-white rounded-xl shadow-md",
    )