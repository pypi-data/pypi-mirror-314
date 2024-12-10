from __future__ import annotations

from typing import Any, Dict

from vectice.api.json.report import ReportOutput
from vectice.utils.common_utils import (
    repr_class,
)


class ReportRepresentation:
    """Represents the metadata of a Vectice report.

    A Report Representation shows information about a specific issue from the Vectice app.
    It makes it easier to get and read this information through the API.

    Attributes:
        id (int): The unique identifier of the issue.
        name (str): The name of the issue.
        creator (Dict[str, str]): Creator of the issue.
    """

    def __init__(self, output: ReportOutput):
        self.id = output.id
        self.name = output.name
        self.creator = output.creator

    def __repr__(self):
        return repr_class(self)

    def asdict(self) -> Dict[str, Any]:
        """Transform the ReportRepresentation into a organised dictionary.

        Returns:
            The object represented as a dictionary
        """
        return {
            "id": self.id,
            "name": self.name,
            "creator": self.creator,
        }
