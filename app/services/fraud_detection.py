from datetime import datetime, timedelta


def calculate_risk_score(validation_event: dict) -> int:
    """Calculates a fraud risk score (0-100) for a validation event."""
    score = 0
    validation_time = datetime.fromisoformat(
        validation_event["timestamp"].replace("Z", "+00:00")
    )
    if not 7 <= validation_time.hour < 22:
        score += 25
    if validation_event.get("source_velocity", 0) > 10:
        score += 30
    if validation_event.get("geo_inconsistent", False):
        score += 40
    if validation_event.get("duplicate_count", 0) > 1:
        score += 50 * (validation_event["duplicate_count"] - 1)
    return min(100, score)


def analyze_validation_patterns(events: list[dict]) -> list[dict]:
    """Analyzes a batch of validation events to detect suspicious patterns."""
    alerts = []
    ip_counts = {}
    for event in events:
        ip = event.get("ip_address")
        if ip:
            ip_counts[ip] = ip_counts.get(ip, 0) + 1
    for ip, count in ip_counts.items():
        if count > 100:
            alerts.append(
                {
                    "type": "Rapid Validation",
                    "description": f"{count} validations from IP {ip} in a short period.",
                    "severity": "Medium",
                    "details": {"ip_address": ip, "count": count},
                }
            )
    return alerts


def get_severity(risk_score: int) -> str:
    if risk_score > 90:
        return "Critical"
    if risk_score > 75:
        return "High"
    if risk_score > 50:
        return "Medium"
    return "Low"