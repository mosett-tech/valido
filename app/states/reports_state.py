import reflex as rx
from typing import TypedDict, Literal
import datetime
import asyncio

ReportType = Literal["Sales", "Warranty", "Claims", "Customer"]
ReportFormat = Literal["PDF", "Excel", "CSV", "JSON"]
ReportStatus = Literal["Completed", "Processing", "Failed"]


class Report(TypedDict):
    id: str
    type: ReportType
    format: ReportFormat
    date_range: str
    generated_at: str
    status: ReportStatus
    download_url: str


class ReportsState(rx.State):
    report_types: list[ReportType] = ["Sales", "Warranty", "Claims", "Customer"]
    report_formats: list[ReportFormat] = ["PDF", "Excel", "CSV", "JSON"]
    report_history: list[Report] = []
    selected_report_type: ReportType = "Sales"
    selected_format: ReportFormat = "PDF"
    start_date: str = (datetime.date.today() - datetime.timedelta(days=30)).isoformat()
    end_date: str = datetime.date.today().isoformat()
    is_generating: bool = False
    scheduled_reports: list[dict] = []

    @rx.event(background=True)
    async def generate_report(self):
        async with self:
            self.is_generating = True
            new_report_id = f"report-{len(self.report_history) + 1:03d}"
            report = {
                "id": new_report_id,
                "type": self.selected_report_type,
                "format": self.selected_format,
                "date_range": f"{self.start_date} to {self.end_date}",
                "generated_at": datetime.datetime.now().isoformat(),
                "status": "Processing",
                "download_url": "#",
            }
            self.report_history.insert(0, report)
        await asyncio.sleep(2)
        async with self:
            for i, r in enumerate(self.report_history):
                if r["id"] == new_report_id:
                    self.report_history[i]["status"] = "Completed"
                    self.report_history[i]["download_url"] = (
                        f"/downloads/{new_report_id}.{self.selected_format.lower()}"
                    )
                    break
            self.is_generating = False