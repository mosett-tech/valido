import reflex as rx
from typing import TypedDict, Literal, Optional
import datetime

ClaimStatus = Literal[
    "pending_review", "approved", "rejected", "in_progress", "completed"
]


class Claim(TypedDict):
    id: str
    warranty_id: str
    product_name: str
    customer_name: str
    submitted_date: str
    status: ClaimStatus
    description: str
    attachments: list[str]
    resolution_notes: Optional[str]


MOCK_CLAIMS: list[Claim] = [
    {
        "id": "claim-001",
        "warranty_id": "W-ABC-123",
        "product_name": "Super Blender 3000",
        "customer_name": "Alice Johnson",
        "submitted_date": "2024-07-30T14:00:00Z",
        "status": "pending_review",
        "description": "The blender motor stopped working. It makes a strange noise but the blades don't spin.",
        "attachments": ["receipt.pdf", "video_of_issue.mp4"],
        "resolution_notes": None,
    },
    {
        "id": "claim-002",
        "warranty_id": "W-DEF-456",
        "product_name": "Smart Watch Pro",
        "customer_name": "Bob Williams",
        "submitted_date": "2024-07-28T10:15:00Z",
        "status": "approved",
        "description": "The screen has dead pixels appearing in the top-right corner.",
        "attachments": ["photo_of_screen.jpg"],
        "resolution_notes": "Replacement unit shipped. Tracking: 1Z9999W99999999999",
    },
    {
        "id": "claim-003",
        "warranty_id": "W-GHI-789",
        "product_name": "Noise-Cancelling Headphones",
        "customer_name": "Charlie Brown",
        "submitted_date": "2024-07-25T09:00:00Z",
        "status": "rejected",
        "description": "Headphones don't turn on. I think the battery is dead.",
        "attachments": [],
        "resolution_notes": "Claim rejected due to evidence of water damage, not covered by warranty.",
    },
    {
        "id": "claim-004",
        "warranty_id": "W-JKL-101",
        "product_name": "4K Ultra HD TV",
        "customer_name": "Diana Miller",
        "submitted_date": "2024-07-31T11:00:00Z",
        "status": "in_progress",
        "description": "A vertical line has appeared on the left side of the screen.",
        "attachments": ["tv_screen_photo.png", "proof_of_purchase.pdf"],
        "resolution_notes": "Technician scheduled for home visit on 2024-08-05.",
    },
]


class ClaimsState(rx.State):
    claims: list[Claim] = MOCK_CLAIMS
    filter_status: str = "All"
    selected_claim: Optional[Claim] = None
    show_new_claim_modal: bool = False
    new_claim_description: str = ""
    new_claim_warranty_id: str = ""

    @rx.var
    def filtered_claims(self) -> list[Claim]:
        if self.filter_status == "All":
            return self.claims
        return [c for c in self.claims if c["status"] == self.filter_status]

    @rx.event
    def set_filter_status(self, status: str):
        self.filter_status = status

    @rx.event
    def select_claim(self, claim: Claim):
        self.selected_claim = claim

    @rx.event
    def deselect_claim(self):
        self.selected_claim = None

    @rx.event
    def toggle_new_claim_modal(self):
        self.show_new_claim_modal = not self.show_new_claim_modal
        self.new_claim_description = ""
        self.new_claim_warranty_id = ""

    @rx.event
    def submit_new_claim(self):
        new_claim: Claim = {
            "id": f"claim-{len(self.claims) + 1:03d}",
            "warranty_id": self.new_claim_warranty_id,
            "product_name": "Sample Product",
            "customer_name": "Current User",
            "submitted_date": datetime.datetime.now().isoformat() + "Z",
            "status": "pending_review",
            "description": self.new_claim_description,
            "attachments": [],
            "resolution_notes": None,
        }
        self.claims.insert(0, new_claim)
        self.toggle_new_claim_modal()