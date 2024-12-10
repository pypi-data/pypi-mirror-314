from __future__ import annotations

from typing import Any

from vectice.api.json.json_type import TJSON


class ReportOutput(TJSON):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

    @property
    def id(self) -> int:
        return self["id"]

    @property
    def name(self) -> str:
        return str(self["name"])

    @property
    def creator(self) -> dict[str, str]:
        return {"name": self["createdBy"]["name"], "email": self["createdBy"]["email"]}
