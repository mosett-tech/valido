import reflex as rx
from typing import TypedDict, Optional
import datetime
import hashlib


class AuditLog(TypedDict):
    timestamp: str
    event: str
    user: str
    details: str
    hash: str
    previous_hash: str


MOCK_AUDIT_TRAILS: dict[str, list[AuditLog]] = {
    "alert-001": [
        {
            "timestamp": "2024-07-29T10:30:00Z",
            "event": "Alert Created",
            "user": "System",
            "details": "Severity: High, Risk Score: 85",
            "hash": hashlib.sha256(b"alert-001-0").hexdigest(),
            "previous_hash": "0" * 64,
        },
        {
            "timestamp": "2024-07-29T12:00:00Z",
            "event": "Status Changed",
            "user": "admin@valido.com",
            "details": "Status changed from new to reviewed",
            "hash": hashlib.sha256(b"alert-001-1").hexdigest(),
            "previous_hash": hashlib.sha256(b"alert-001-0").hexdigest(),
        },
    ],
    "alert-002": [
        {
            "timestamp": "2024-07-29T11:05:00Z",
            "event": "Alert Created",
            "user": "System",
            "details": "Severity: Medium, Risk Score: 62",
            "hash": hashlib.sha256(b"alert-002-0").hexdigest(),
            "previous_hash": "0" * 64,
        }
    ],
}


class AuditState(rx.State):
    show_audit_trail: bool = False
    current_trail: list[AuditLog] = []
    current_trail_id: str = ""

    @rx.event
    def load_audit_trail(self, item_id: str):
        self.current_trail_id = item_id
        self.current_trail = MOCK_AUDIT_TRAILS.get(item_id, [])
        self.show_audit_trail = True

    @rx.event
    def close_audit_trail(self):
        self.show_audit_trail = False
        self.current_trail = []
        self.current_trail_id = ""

    @rx.var
    def is_chain_valid(self) -> bool:
        for i, log in enumerate(self.current_trail):
            if i == 0:
                if log["previous_hash"] != "0" * 64:
                    return False
            elif log["previous_hash"] != self.current_trail[i - 1]["hash"]:
                return False
        return True