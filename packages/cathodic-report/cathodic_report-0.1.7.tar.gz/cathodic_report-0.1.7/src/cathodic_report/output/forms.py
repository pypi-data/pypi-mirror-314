"""All string here is word filename."""

from pathlib import Path

from pydantic import BaseModel


class HeaderOutput(BaseModel):
    beginning: str
    summary_table: str
    graph: str


class DeviceOutput(BaseModel):
    id: int
    header: str
    tables: list[str]
    graph: str


class ReportOutput(BaseModel):
    header: HeaderOutput
    devices: list[DeviceOutput]
