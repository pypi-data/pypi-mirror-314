# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from dataclasses import dataclass
from enum import Enum
from uuid import UUID


class IssueType(Enum):
    """General classification of the issue."""

    SCHEMA = "SchemaIssue"
    EMPTY_FRAMES = "EmptyFramesIssue"
    RAIL_SIDE = "RailSide"


@dataclass
class IssueIdentifiers:
    """Information for locating an issue."""

    annotation: UUID | None = None
    frame: int | None = None
    object: UUID | None = None
    sensor: str | None = None


@dataclass
class Issue:
    """An error that was found inside the scene."""

    type: IssueType
    reason: str
    identifiers: IssueIdentifiers | list[str | int]
