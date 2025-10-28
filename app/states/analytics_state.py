import reflex as rx
from typing import TypedDict
import datetime
import random


class SalesData(TypedDict):
    date: str
    sales: int


class RFMSegment(TypedDict):
    segment: str
    count: int
    recency: float
    frequency: float
    monetary: float


class ClaimPrediction(TypedDict):
    month: str
    predicted_claims: int


class LocationData(TypedDict):
    lat: float
    lng: float
    intensity: int


def generate_sales_data() -> list[SalesData]:
    data = []
    today = datetime.date.today()
    for i in range(90):
        date = today - datetime.timedelta(days=i)
        sales = random.randint(50, 200) + (90 - i)
        data.append({"date": date.strftime("%Y-%m-%d"), "sales": sales})
    return data[::-1]


def generate_rfm_data() -> list[RFMSegment]:
    return [
        {
            "segment": "Champions",
            "count": 150,
            "recency": 10,
            "frequency": 12,
            "monetary": 2500,
        },
        {
            "segment": "Loyal Customers",
            "count": 300,
            "recency": 30,
            "frequency": 8,
            "monetary": 1500,
        },
        {
            "segment": "At-Risk",
            "count": 120,
            "recency": 80,
            "frequency": 3,
            "monetary": 700,
        },
        {
            "segment": "New Customers",
            "count": 200,
            "recency": 15,
            "frequency": 1.5,
            "monetary": 400,
        },
        {
            "segment": "Hibernating",
            "count": 250,
            "recency": 150,
            "frequency": 1.1,
            "monetary": 250,
        },
    ]


def generate_claim_predictions() -> list[ClaimPrediction]:
    predictions = []
    today = datetime.date.today()
    for i in range(6):
        month = (today + datetime.timedelta(days=i * 30)).strftime("%b %Y")
        claims = random.randint(20, 50) + i * 5
        predictions.append({"month": month, "predicted_claims": claims})
    return predictions


def generate_location_data() -> list[LocationData]:
    locations = []
    for _ in range(50):
        locations.append(
            {
                "lat": -1.286389 + random.uniform(-0.05, 0.05),
                "lng": 36.817223 + random.uniform(-0.05, 0.05),
                "intensity": random.randint(5, 10),
            }
        )
    for _ in range(30):
        locations.append(
            {
                "lat": -4.043477 + random.uniform(-0.04, 0.04),
                "lng": 39.668205 + random.uniform(-0.04, 0.04),
                "intensity": random.randint(3, 8),
            }
        )
    for _ in range(20):
        locations.append(
            {"lat": 0.5142, "lng": 35.2691, "intensity": random.randint(1, 4)}
        )
    return locations


class AnalyticsState(rx.State):
    """Manages the state for the advanced analytics dashboard."""

    sales_data: list[SalesData] = generate_sales_data()
    rfm_segments: list[RFMSegment] = generate_rfm_data()
    claim_predictions: list[ClaimPrediction] = generate_claim_predictions()
    location_data: list[LocationData] = generate_location_data()
    export_format: str = "csv"
    is_exporting: bool = False

    @rx.event
    def set_export_format(self, fmt: str):
        self.export_format = fmt