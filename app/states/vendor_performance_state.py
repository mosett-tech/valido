import reflex as rx
from typing import TypedDict, Optional


class VendorPerformanceMetrics(TypedDict):
    claim_resolution_time_avg_days: float
    customer_satisfaction_rating_avg: float
    warranty_fulfillment_rate: float
    fraud_incident_rate: float


class Vendor(TypedDict):
    id: str
    name: str
    logo_url: str
    overall_score: int
    metrics: VendorPerformanceMetrics


MOCK_VENDORS: list[Vendor] = [
    {
        "id": "vendor-01",
        "name": "Super Electronics",
        "logo_url": "/placeholder.svg",
        "overall_score": 92,
        "metrics": {
            "claim_resolution_time_avg_days": 2.5,
            "customer_satisfaction_rating_avg": 4.8,
            "warranty_fulfillment_rate": 0.98,
            "fraud_incident_rate": 0.01,
        },
    },
    {
        "id": "vendor-02",
        "name": "Home Goods Inc.",
        "logo_url": "/placeholder.svg",
        "overall_score": 78,
        "metrics": {
            "claim_resolution_time_avg_days": 5.1,
            "customer_satisfaction_rating_avg": 4.2,
            "warranty_fulfillment_rate": 0.95,
            "fraud_incident_rate": 0.03,
        },
    },
    {
        "id": "vendor-03",
        "name": "Gadget World",
        "logo_url": "/placeholder.svg",
        "overall_score": 95,
        "metrics": {
            "claim_resolution_time_avg_days": 1.8,
            "customer_satisfaction_rating_avg": 4.9,
            "warranty_fulfillment_rate": 0.99,
            "fraud_incident_rate": 0.005,
        },
    },
]


class VendorPerformanceState(rx.State):
    vendors: list[Vendor] = MOCK_VENDORS
    selected_vendor: Optional[Vendor] = None
    sort_by: str = "-overall_score"

    @rx.var
    def sorted_vendors(self) -> list[Vendor]:
        reverse = self.sort_by.startswith("-")
        sort_key = self.sort_by.lstrip("-")
        return sorted(self.vendors, key=lambda v: v[sort_key], reverse=reverse)

    @rx.var
    def top_performers(self) -> list[Vendor]:
        return [v for v in self.sorted_vendors if v["overall_score"] >= 90]

    @rx.var
    def underperforming_vendors(self) -> list[Vendor]:
        return [v for v in self.sorted_vendors if v["overall_score"] < 80]

    @rx.event
    def select_vendor(self, vendor: Vendor):
        self.selected_vendor = vendor

    @rx.event
    def deselect_vendor(self):
        self.selected_vendor = None

    @rx.event
    def set_sort_by(self, sort_key: str):
        self.sort_by = sort_key