import reflex as rx
from app.states.marketplace_state import MarketplaceState, WarrantyListing


def offer_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.content(
            rx.radix.primitives.dialog.title("Make an Offer"),
            rx.cond(
                MarketplaceState.selected_listing,
                rx.el.div(
                    rx.el.p(
                        f"You are making an offer for: {MarketplaceState.selected_listing['product_name']}"
                    ),
                    rx.el.p(
                        f"Seller: {MarketplaceState.selected_listing['seller_name']}"
                    ),
                    rx.el.p(
                        f"Asking Price: ${MarketplaceState.selected_listing['price']:.2f}"
                    ),
                    rx.el.input(
                        placeholder="Enter your offer amount",
                        type="number",
                        on_change=MarketplaceState.set_offer_amount,
                        class_name="w-full p-2 border rounded-md mt-4",
                    ),
                    class_name="space-y-2",
                ),
                rx.el.p("No listing selected."),
            ),
            rx.el.div(
                rx.el.button(
                    "Cancel",
                    on_click=MarketplaceState.deselect_listing,
                    class_name="mr-2 bg-gray-200 text-gray-800 px-4 py-2 rounded-md",
                ),
                rx.el.button(
                    "Submit Offer",
                    on_click=MarketplaceState.submit_offer,
                    class_name="bg-blue-600 text-white px-4 py-2 rounded-md",
                ),
                class_name="flex justify-end mt-4",
            ),
        ),
        open=MarketplaceState.show_offer_modal,
        on_open_change=lambda open: rx.cond(
            open, rx.noop(), MarketplaceState.deselect_listing
        ),
    )


def listing_card(listing: WarrantyListing) -> rx.Component:
    return rx.el.div(
        rx.el.img(
            src=listing["image_url"], class_name="w-full h-48 object-cover rounded-t-lg"
        ),
        rx.el.div(
            rx.el.h3(listing["product_name"], class_name="font-bold text-lg"),
            rx.el.p(
                f"Seller: {listing['seller_name']}", class_name="text-sm text-gray-600"
            ),
            rx.el.p(f"Condition: {listing['condition']}", class_name="text-sm"),
            rx.el.p(f"Expires: {listing['expiry_date']}", class_name="text-sm"),
            rx.el.div(
                rx.el.p(
                    f"${listing['price']:.2f}",
                    class_name="text-xl font-bold text-blue-600",
                ),
                rx.el.button(
                    "Make Offer",
                    on_click=lambda: MarketplaceState.select_listing(listing),
                    class_name="bg-blue-500 text-white px-3 py-1 rounded-md text-sm",
                ),
                class_name="flex justify-between items-center mt-4",
            ),
            class_name="p-4",
        ),
        class_name="bg-white rounded-lg shadow-md overflow-hidden border",
    )


def marketplace_dashboard() -> rx.Component:
    return rx.el.div(
        rx.el.h1(
            "Warranty Marketplace", class_name="text-2xl font-bold text-gray-800 mb-6"
        ),
        rx.el.div(
            rx.el.input(
                placeholder="Search for products or sellers...",
                on_change=MarketplaceState.set_search_query,
                class_name="w-full md:w-1/2 p-2 border rounded-md",
            ),
            rx.el.select(
                ["All", "Electronics", "Wearables", "Home"],
                on_change=MarketplaceState.set_filter_category,
                default_value="All",
                class_name="p-2 border rounded-md",
            ),
            class_name="flex flex-col md:flex-row gap-4 mb-6",
        ),
        rx.el.div(
            rx.foreach(MarketplaceState.filtered_listings, listing_card),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
        ),
        offer_modal(),
        class_name="p-4 md:p-8",
    )