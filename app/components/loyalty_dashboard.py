import reflex as rx
from app.states.loyalty_state import LoyaltyState, Reward


def tier_card(tier: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(tier["icon"], class_name="h-8 w-8"),
            rx.el.h3(tier["name"], class_name="text-xl font-bold"),
            class_name="flex items-center gap-3",
        ),
        rx.el.p(
            f"{tier['points_required']} Points", class_name="text-sm font-semibold"
        ),
        rx.el.ul(
            rx.foreach(
                tier["benefits"],
                lambda benefit: rx.el.li(
                    rx.icon("square_check", class_name="h-4 w-4 text-green-500"),
                    rx.el.span(benefit),
                    class_name="flex items-center gap-2 text-sm",
                ),
            ),
            class_name="mt-2 space-y-1",
        ),
        class_name=rx.cond(
            LoyaltyState.current_tier["name"] == tier["name"],
            "p-6 rounded-xl border-2 border-blue-500 bg-blue-50 shadow-lg scale-105",
            "p-6 bg-white rounded-xl border shadow-sm",
        ),
    )


def reward_card(reward: Reward) -> rx.Component:
    can_redeem = LoyaltyState.current_points >= reward["points_cost"]
    return rx.el.div(
        rx.el.div(
            rx.icon(reward["icon"], class_name="h-10 w-10 text-blue-600"),
            class_name="p-3 bg-blue-100 rounded-lg w-fit",
        ),
        rx.el.h4(reward["name"], class_name="mt-4 font-semibold text-gray-800"),
        rx.el.p(reward["description"], class_name="text-sm text-gray-500 mt-1"),
        rx.el.div(
            rx.el.div(
                rx.icon("star", class_name="h-5 w-5 text-yellow-500"),
                rx.el.span(
                    f"{reward['points_cost']} Points",
                    class_name="font-bold text-blue-700",
                ),
                class_name="flex items-center gap-1",
            ),
            rx.el.button(
                "Redeem",
                on_click=lambda: LoyaltyState.select_reward_to_redeem(reward),
                disabled=~can_redeem,
                class_name="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed",
            ),
            class_name="flex justify-between items-center mt-4",
        ),
        class_name="p-5 bg-white rounded-xl border shadow-sm flex flex-col justify-between",
    )


def redeem_confirmation_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.content(
            rx.radix.primitives.dialog.title("Confirm Redemption"),
            rx.radix.primitives.dialog.description(
                "Are you sure you want to redeem this reward?"
            ),
            rx.el.div(
                rx.cond(
                    LoyaltyState.selected_reward,
                    rx.el.div(
                        rx.el.h3(
                            LoyaltyState.selected_reward["name"],
                            class_name="font-bold text-lg",
                        ),
                        rx.el.p(
                            f"This will cost {LoyaltyState.selected_reward['points_cost']} points."
                        ),
                        class_name="my-4 p-4 bg-gray-100 rounded-lg",
                    ),
                    rx.el.div(),
                )
            ),
            rx.el.div(
                rx.el.button(
                    "Cancel",
                    on_click=LoyaltyState.cancel_redeem,
                    class_name="mr-2 bg-gray-200 text-gray-800 px-4 py-2 rounded-md",
                ),
                rx.el.button(
                    "Confirm",
                    on_click=LoyaltyState.confirm_redeem,
                    class_name="bg-blue-600 text-white px-4 py-2 rounded-md",
                ),
                class_name="flex justify-end mt-4",
            ),
        ),
        open=LoyaltyState.show_redeem_confirm,
        on_open_change=lambda is_open: rx.cond(
            is_open, rx.noop(), LoyaltyState.cancel_redeem
        ),
    )


def loyalty_dashboard() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    f"Welcome, {LoyaltyState.current_user_name}!",
                    class_name="text-2xl font-bold text-gray-800",
                ),
                rx.el.p(
                    "Here is your loyalty and rewards overview.",
                    class_name="text-gray-600",
                ),
            ),
            rx.el.div(
                rx.icon("star", class_name="h-6 w-6 text-yellow-400"),
                rx.el.span(
                    LoyaltyState.current_points, class_name="text-2xl font-bold"
                ),
                rx.el.span("Points", class_name="text-gray-600"),
                class_name="flex items-center gap-2 p-4 bg-white rounded-xl shadow-sm",
            ),
            class_name="flex justify-between items-start mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.h3(
                                "Your Tier Progress", class_name="font-semibold text-lg"
                            ),
                            rx.cond(
                                LoyaltyState.next_tier,
                                rx.el.p(
                                    f"{LoyaltyState.points_to_next_tier} points to {LoyaltyState.next_tier['name']}",
                                    class_name="text-sm text-gray-500",
                                ),
                                rx.el.p(
                                    "You are at the highest tier!",
                                    class_name="text-sm text-blue-600 font-semibold",
                                ),
                            ),
                            class_name="flex justify-between items-center",
                        ),
                        rx.el.div(
                            rx.el.div(
                                style={
                                    "width": LoyaltyState.tier_progress.to_string()
                                    + "%"
                                },
                                class_name="bg-blue-500 h-2 rounded-full",
                            ),
                            class_name="w-full bg-gray-200 rounded-full h-2 mt-2",
                        ),
                    ),
                    class_name="p-6 bg-white rounded-xl shadow-md mb-6",
                ),
                rx.el.div(
                    rx.el.h3(
                        "Rewards Catalog", class_name="font-semibold text-lg mb-4"
                    ),
                    rx.el.div(
                        rx.foreach(LoyaltyState.rewards, reward_card),
                        class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
                    ),
                ),
                class_name="flex-grow",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Referral Program", class_name="font-semibold text-lg mb-2"
                    ),
                    rx.el.p(
                        "Share your code and earn 100 points for each friend who signs up!",
                        class_name="text-sm text-gray-600 mb-4",
                    ),
                    rx.el.div(
                        rx.el.p("Your Referral Code:", class_name="text-sm"),
                        rx.el.div(
                            rx.el.p(
                                LoyaltyState.selected_user["referral_code"],
                                class_name="font-mono text-lg font-bold text-blue-700",
                            ),
                            rx.el.button(
                                rx.icon("copy", class_name="h-4 w-4"),
                                on_click=rx.set_clipboard(
                                    LoyaltyState.selected_user["referral_code"]
                                ),
                                class_name="p-2 hover:bg-gray-200 rounded-md",
                            ),
                            class_name="flex items-center justify-between p-2 bg-blue-50 border border-blue-200 rounded-lg",
                        ),
                    ),
                    class_name="p-6 bg-white rounded-xl shadow-md mb-6",
                ),
                rx.el.div(
                    rx.el.h3("Loyalty Tiers", class_name="font-semibold text-lg mb-4"),
                    rx.el.div(
                        rx.foreach(LoyaltyState.tiers, tier_card),
                        class_name="space-y-4",
                    ),
                    class_name="p-6 bg-white rounded-xl shadow-md",
                ),
                class_name="w-full lg:w-96 lg:ml-8 mt-8 lg:mt-0",
            ),
            class_name="lg:flex",
        ),
        redeem_confirmation_modal(),
        class_name="p-4 md:p-8",
    )