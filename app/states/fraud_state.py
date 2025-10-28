import reflex as rx
from typing import TypedDict, Literal, Optional
import datetime

Severity = Literal["Low", "Medium", "High", "Critical"]


class FraudAlert(TypedDict):
    id: str
    timestamp: str
    type: str
    description: str
    severity: Severity
    risk_score: int
    details: dict
    status: str


MOCK_ALERTS: list[FraudAlert] = [
    {
        "id": "alert-001",
        "timestamp": "2024-07-29T10:30:00Z",
        "type": "Duplicate QR Code",
        "description": "QR Code scanned multiple times in different locations within a short period.",
        "severity": "High",
        "risk_score": 85,
        "details": {
            "qr_code_id": "QR-XYZ-123",
            "locations": ["Nairobi", "Mombasa"],
            "count": 5,
        },
        "status": "new",
    },
    {
        "id": "alert-002",
        "timestamp": "2024-07-29T11:05:00Z",
        "type": "Rapid Validation",
        "description": "Unusually high number of validations from a single IP address.",
        "severity": "Medium",
        "risk_score": 62,
        "details": {"ip_address": "192.168.1.100", "validation_count": 150},
        "status": "new",
    },
    {
        "id": "alert-003",
        "timestamp": "2024-07-28T23:00:00Z",
        "type": "Off-Hours Validation",
        "description": "Warranty validation occurred outside of typical business hours.",
        "severity": "Low",
        "risk_score": 30,
        "details": {"product_id": "PROD-ABC-456", "validation_time": "23:00"},
        "status": "reviewed",
    },
    {
        "id": "alert-004",
        "timestamp": "2024-07-27T14:15:00Z",
        "type": "High-Value Item Flag",
        "description": "Multiple validations for a high-value item from different users.",
        "severity": "Critical",
        "risk_score": 95,
        "details": {"item_serial": "SN-987654321", "user_count": 4},
        "status": "resolved",
    },
]


class FraudState(rx.State):
    alerts: list[FraudAlert] = MOCK_ALERTS
    filter_severity: str = "All"
    filter_status: str = "All"
    sort_by: str = "-risk_score"
    selected_alert: Optional[FraudAlert] = None

    @rx.var
    def filtered_and_sorted_alerts(self) -> list[FraudAlert]:
        alerts = self.alerts
        if self.filter_severity != "All":
            alerts = [a for a in alerts if a["severity"] == self.filter_severity]
        if self.filter_status != "All":
            alerts = [a for a in alerts if a["status"] == self.filter_status]
        sort_key = self.sort_by.replace("-", "")
        reverse = self.sort_by.startswith("-")
        alerts.sort(key=lambda x: x.get(sort_key, 0), reverse=reverse)
        return alerts

    @rx.event
    def select_alert(self, alert: FraudAlert):
        self.selected_alert = alert

    @rx.event
    def deselect_alert(self):
        self.selected_alert = None

    @rx.event
    def update_alert_status(self, alert_id: str, new_status: str):
        for i, alert in enumerate(self.alerts):
            if alert["id"] == alert_id:
                self.alerts[i]["status"] = new_status
                break
        self.deselect_alert()

    @rx.event
    async def view_audit_trail(self, alert: FraudAlert):
        from app.states.audit_state import AuditState

        audit_state = await self.get_state(AuditState)
        return audit_state.load_audit_trail(alert["id"])