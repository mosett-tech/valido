import reflex as rx
from app.states.audit_state import AuditState, AuditLog


def audit_log_entry(log: AuditLog, index: int) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.cond(
                log["previous_hash"]
                == rx.cond(
                    index > 0, AuditState.current_trail[index - 1]["hash"], "0" * 64
                ),
                rx.icon("square_check", class_name="h-5 w-5 text-green-500"),
                rx.icon("circle_x", class_name="h-5 w-5 text-red-500"),
            ),
            class_name="absolute -left-2.5 mt-1.5 h-5 w-5 rounded-full border border-white bg-gray-100 flex items-center justify-center",
        ),
        rx.el.time(
            log["timestamp"],
            class_name="mb-1 text-xs font-normal leading-none text-gray-400",
        ),
        rx.el.h3(log["event"], class_name="text-md font-semibold text-gray-900"),
        rx.el.p(
            f"User: {log['user']} - {log['details']}",
            class_name="mb-2 text-sm font-normal text-gray-500",
        ),
        rx.el.div(
            rx.el.p("Hash:", class_name="font-semibold text-xs"),
            rx.el.p(log["hash"], class_name="truncate font-mono text-xs"),
            class_name="bg-gray-50 p-2 rounded-md border text-gray-600",
        ),
        rx.el.div(
            rx.icon("arrow-down", class_name="h-4 w-4 text-gray-400 mx-auto my-1")
        ),
        rx.el.div(
            rx.el.p("Previous Hash:", class_name="font-semibold text-xs"),
            rx.el.p(log["previous_hash"], class_name="truncate font-mono text-xs"),
            class_name="bg-gray-50 p-2 rounded-md border text-gray-600",
        ),
        class_name="relative border-l border-gray-200 pl-8 pb-8",
    )


def audit_trail_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.content(
            rx.radix.primitives.dialog.title(
                f"Audit Trail for {AuditState.current_trail_id}"
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            rx.cond(
                                AuditState.is_chain_valid,
                                "shield-check",
                                "shield-alert",
                            ),
                            class_name="h-5 w-5",
                        ),
                        rx.el.span(
                            rx.cond(
                                AuditState.is_chain_valid,
                                "Chain Valid",
                                "Chain Invalid",
                            )
                        ),
                        class_name=rx.cond(
                            AuditState.is_chain_valid,
                            "flex items-center gap-2 text-sm font-medium px-3 py-1 rounded-full bg-green-100 text-green-800 w-fit",
                            "flex items-center gap-2 text-sm font-medium px-3 py-1 rounded-full bg-red-100 text-red-800 w-fit",
                        ),
                    )
                ),
                class_name="my-4",
            ),
            rx.el.div(rx.foreach(AuditState.current_trail, audit_log_entry)),
            rx.el.div(
                rx.el.button(
                    "Close",
                    on_click=AuditState.close_audit_trail,
                    class_name="mt-4 w-full bg-gray-200 text-gray-800 py-2 rounded-md",
                ),
                class_name="mt-4 flex justify-end",
            ),
            class_name="max-h-[80vh] overflow-y-auto",
        ),
        open=AuditState.show_audit_trail,
        on_open_change=lambda is_open: rx.cond(
            is_open, rx.noop(), AuditState.close_audit_trail
        ),
    )