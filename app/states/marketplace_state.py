import reflex as rx
from typing import TypedDict, Literal, Optional
import logging

ListingStatus = Literal["active", "sold", "expired"]
OfferStatus = Literal["pending", "accepted", "rejected"]


class WarrantyListing(TypedDict):
    id: str
    product_name: str
    seller_name: str
    price: float
    condition: str
    expiry_date: str
    image_url: str
    status: ListingStatus
    category: str


class Offer(TypedDict):
    id: str
    listing_id: str
    buyer_name: str
    offer_price: float
    status: OfferStatus


MOCK_LISTINGS: list[WarrantyListing] = [
    {
        "id": "list-001",
        "product_name": "Super Blender 3000",
        "seller_name": "Alice Johnson",
        "price": 45.0,
        "condition": "Like New",
        "expiry_date": "2025-08-15",
        "image_url": "/placeholder.svg",
        "status": "active",
        "category": "Electronics",
    },
    {
        "id": "list-002",
        "product_name": "Smart Watch Pro",
        "seller_name": "Bob Williams",
        "price": 120.0,
        "condition": "Used",
        "expiry_date": "2026-01-20",
        "image_url": "/placeholder.svg",
        "status": "active",
        "category": "Wearables",
    },
    {
        "id": "list-003",
        "product_name": "4K Ultra HD TV",
        "seller_name": "Diana Miller",
        "price": 350.0,
        "condition": "Open Box",
        "expiry_date": "2025-11-30",
        "image_url": "/placeholder.svg",
        "status": "sold",
        "category": "Electronics",
    },
]


class MarketplaceState(rx.State):
    listings: list[WarrantyListing] = MOCK_LISTINGS
    offers: list[Offer] = []
    selected_listing: Optional[WarrantyListing] = None
    show_offer_modal: bool = False
    offer_amount: float = 0.0
    filter_category: str = "All"
    search_query: str = ""

    @rx.var
    def filtered_listings(self) -> list[WarrantyListing]:
        return [
            listing
            for listing in self.listings
            if (
                self.filter_category == "All"
                or listing["category"] == self.filter_category
            )
            and (
                self.search_query.lower() in listing["product_name"].lower()
                or self.search_query.lower() in listing["seller_name"].lower()
            )
        ]

    @rx.event
    def set_filter_category(self, category: str):
        self.filter_category = category

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query

    @rx.event
    def select_listing(self, listing: WarrantyListing):
        self.selected_listing = listing
        self.show_offer_modal = True
        self.offer_amount = 0.0

    @rx.event
    def deselect_listing(self):
        self.selected_listing = None
        self.show_offer_modal = False

    @rx.event
    def set_offer_amount(self, amount: str):
        try:
            self.offer_amount = float(amount)
        except ValueError as e:
            logging.exception(f"Error converting offer amount to float: {e}")
            self.offer_amount = 0.0

    @rx.event
    def submit_offer(self):
        if self.selected_listing and self.offer_amount > 0:
            new_offer: Offer = {
                "id": f"offer-{len(self.offers) + 1:03d}",
                "listing_id": self.selected_listing["id"],
                "buyer_name": "Current User",
                "offer_price": self.offer_amount,
                "status": "pending",
            }
            self.offers.append(new_offer)
            self.deselect_listing()