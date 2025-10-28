import reflex as rx
from app.states.recommendations_state import RecommendationsState, Product


def product_card(product: Product, is_wishlisted: rx.Var[bool]) -> rx.Component:
    return rx.el.div(
        rx.el.img(
            src=product["image_url"], class_name="w-full h-40 object-cover rounded-t-lg"
        ),
        rx.el.div(
            rx.el.h3(product["name"], class_name="font-semibold"),
            rx.el.p(f"${product['price']:.2f}", class_name="text-gray-700 font-bold"),
            rx.el.div(
                rx.icon("star", class_name="h-5 w-5 text-yellow-400"),
                rx.el.p(product["rating"].to_string()),
                class_name="flex items-center gap-1 text-sm",
            ),
            class_name="p-4 space-y-2",
        ),
        rx.el.button(
            rx.icon(
                "heart",
                fill=rx.cond(is_wishlisted, "red", "none"),
                color=rx.cond(is_wishlisted, "red", "currentColor"),
            ),
            on_click=rx.cond(
                is_wishlisted,
                RecommendationsState.remove_from_wishlist(product),
                RecommendationsState.add_to_wishlist(product),
            ),
            class_name="absolute top-2 right-2 bg-white p-1.5 rounded-full shadow",
        ),
        class_name="bg-white rounded-lg shadow-md border relative",
    )


def recommendations_dashboard() -> rx.Component:
    return rx.el.div(
        rx.el.h1(
            "AI Product Recommendations",
            class_name="text-2xl font-bold text-gray-800 mb-6",
        ),
        rx.el.div(
            rx.el.h2(
                "For You (Tech Enthusiast)",
                class_name="text-xl font-semibold text-gray-700 mb-4",
            ),
            rx.el.div(
                rx.foreach(
                    RecommendationsState.recommended_products,
                    lambda p: product_card(
                        p, RecommendationsState.wishlist.contains(p)
                    ),
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6",
            ),
            class_name="mb-8",
        ),
        rx.el.div(
            rx.el.h2(
                "Trending Products",
                class_name="text-xl font-semibold text-gray-700 mb-4",
            ),
            rx.el.div(
                rx.foreach(
                    RecommendationsState.trending_products,
                    lambda p: product_card(
                        p, RecommendationsState.wishlist.contains(p)
                    ),
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6",
            ),
        ),
        class_name="p-4 md:p-8",
    )