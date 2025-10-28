import reflex as rx
from typing import TypedDict, Literal, Optional
import random
import string

Tier = Literal["Bronze", "Silver", "Gold", "Platinum"]


class LoyaltyTier(TypedDict):
    name: Tier
    points_required: int
    benefits: list[str]
    icon: str


class Reward(TypedDict):
    id: str
    name: str
    description: str
    points_cost: int
    icon: str


class UserLoyalty(TypedDict):
    user_id: str
    name: str
    points: int
    tier: Tier
    referral_code: str
    referrals: int


LOYALTY_TIERS: list[LoyaltyTier] = [
    {
        "name": "Bronze",
        "points_required": 0,
        "benefits": ["Basic support", "5% discount on select items"],
        "icon": "bronze-medal",
    },
    {
        "name": "Silver",
        "points_required": 500,
        "benefits": ["Priority support", "10% discount voucher"],
        "icon": "silver-medal",
    },
    {
        "name": "Gold",
        "points_required": 1500,
        "benefits": ["24/7 support", "Exclusive offers", "Early access to sales"],
        "icon": "gold-medal",
    },
    {
        "name": "Platinum",
        "points_required": 5000,
        "benefits": [
            "Dedicated account manager",
            "Free shipping",
            "Special event invites",
        ],
        "icon": "platinum-medal",
    },
]
REWARDS_CATALOG: list[Reward] = [
    {
        "id": "reward-01",
        "name": "10% Discount Voucher",
        "description": "Get 10% off your next purchase.",
        "points_cost": 250,
        "icon": "tag",
    },
    {
        "id": "reward-02",
        "name": "Free Shipping",
        "description": "Free shipping on your next order.",
        "points_cost": 500,
        "icon": "truck",
    },
    {
        "id": "reward-03",
        "name": "$20 Gift Card",
        "description": "A $20 gift card for any of our partner stores.",
        "points_cost": 1000,
        "icon": "gift",
    },
    {
        "id": "reward-04",
        "name": "Exclusive T-Shirt",
        "description": "A limited edition Valido branded t-shirt.",
        "points_cost": 1500,
        "icon": "shirt",
    },
]
MOCK_USER_LOYALTY_DATA: list[UserLoyalty] = [
    {
        "user_id": "user-01",
        "name": "Alice Johnson",
        "points": 1750,
        "tier": "Gold",
        "referral_code": "ALICE75",
        "referrals": 5,
    },
    {
        "user_id": "user-02",
        "name": "Bob Williams",
        "points": 300,
        "tier": "Bronze",
        "referral_code": "BOB22",
        "referrals": 1,
    },
    {
        "user_id": "user-03",
        "name": "Charlie Brown",
        "points": 6000,
        "tier": "Platinum",
        "referral_code": "CHARLIE44",
        "referrals": 12,
    },
    {
        "user_id": "user-04",
        "name": "Diana Miller",
        "points": 800,
        "tier": "Silver",
        "referral_code": "DIANA91",
        "referrals": 3,
    },
]


class LoyaltyState(rx.State):
    """Manages the state for the loyalty and rewards program."""

    tiers: list[LoyaltyTier] = LOYALTY_TIERS
    rewards: list[Reward] = REWARDS_CATALOG
    user_loyalty_data: list[UserLoyalty] = MOCK_USER_LOYALTY_DATA
    selected_user: Optional[UserLoyalty] = MOCK_USER_LOYALTY_DATA[0]
    show_redeem_confirm: bool = False
    selected_reward: Optional[Reward] = None

    @rx.var
    def current_user_name(self) -> str:
        return self.selected_user["name"] if self.selected_user else ""

    @rx.var
    def current_points(self) -> int:
        return self.selected_user["points"] if self.selected_user else 0

    @rx.var
    def current_tier(self) -> Optional[LoyaltyTier]:
        if not self.selected_user:
            return None
        for tier in self.tiers:
            if tier["name"] == self.selected_user["tier"]:
                return tier
        return None

    @rx.var
    def next_tier(self) -> Optional[LoyaltyTier]:
        if not self.current_tier:
            return None
        current_index = self.tiers.index(self.current_tier)
        if current_index + 1 < len(self.tiers):
            return self.tiers[current_index + 1]
        return None

    @rx.var
    def points_to_next_tier(self) -> int:
        if self.next_tier and self.selected_user:
            return self.next_tier["points_required"] - self.selected_user["points"]
        return 0

    @rx.var
    def tier_progress(self) -> float:
        if not self.selected_user or not self.current_tier or (not self.next_tier):
            return 100.0
        tier_range = (
            self.next_tier["points_required"] - self.current_tier["points_required"]
        )
        if tier_range == 0:
            return 100.0
        progress_in_tier = (
            self.selected_user["points"] - self.current_tier["points_required"]
        )
        return progress_in_tier / tier_range * 100

    @rx.event
    def select_reward_to_redeem(self, reward: Reward):
        self.selected_reward = reward
        self.show_redeem_confirm = True

    @rx.event
    def cancel_redeem(self):
        self.show_redeem_confirm = False
        self.selected_reward = None

    @rx.event
    def confirm_redeem(self):
        if self.selected_user and self.selected_reward:
            if self.selected_user["points"] >= self.selected_reward["points_cost"]:
                user_index = self.user_loyalty_data.index(self.selected_user)
                self.user_loyalty_data[user_index]["points"] -= self.selected_reward[
                    "points_cost"
                ]
        self.show_redeem_confirm = False
        self.selected_reward = None