import reflex as rx
from typing import TypedDict
import asyncio


class Product(TypedDict):
    id: str
    name: str
    category: str
    price: float
    image_url: str
    rating: float


MOCK_PRODUCTS: list[Product] = [
    {
        "id": "prod-01",
        "name": "Wireless Charging Pad",
        "category": "Accessories",
        "price": 35.0,
        "image_url": "/placeholder.svg",
        "rating": 4.8,
    },
    {
        "id": "prod-02",
        "name": "Portable Power Bank",
        "category": "Accessories",
        "price": 55.0,
        "image_url": "/placeholder.svg",
        "rating": 4.7,
    },
    {
        "id": "prod-03",
        "name": "Ergonomic Office Chair",
        "category": "Furniture",
        "price": 250.0,
        "image_url": "/placeholder.svg",
        "rating": 4.9,
    },
    {
        "id": "prod-04",
        "name": "Bluetooth Speaker",
        "category": "Electronics",
        "price": 89.99,
        "image_url": "/placeholder.svg",
        "rating": 4.6,
    },
]


class RecommendationsState(rx.State):
    recommended_products: list[Product] = MOCK_PRODUCTS
    trending_products: list[Product] = MOCK_PRODUCTS[::-1]
    seasonal_offers: list[Product] = []
    wishlist: list[Product] = []
    customer_segment: str = "Tech Enthusiast"
    is_loading: bool = False

    @rx.event(background=True)
    async def refresh_recommendations(self):
        async with self:
            self.is_loading = True
        await asyncio.sleep(1)
        async with self:
            self.recommended_products = self.recommended_products[1:] + [
                self.recommended_products[0]
            ]
            self.is_loading = False

    @rx.event
    def add_to_wishlist(self, product: Product):
        if product not in self.wishlist:
            self.wishlist.append(product)

    @rx.event
    def remove_from_wishlist(self, product: Product):
        self.wishlist = [p for p in self.wishlist if p["id"] != product["id"]]