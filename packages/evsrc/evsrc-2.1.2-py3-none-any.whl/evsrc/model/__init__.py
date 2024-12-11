from dataclasses import dataclass
from .domain import ChangeEvent, Aggregate, Value
from typing import Protocol, Any


class ConcurrenceError(Exception):
    """An aggregate has been modified at the same time by several clients"""


@dataclass
class Version:
    value: int
    timestamp: int  # in ms


@dataclass
class EventRecord:
    version: Version
    event: ChangeEvent


class EventStore(Protocol):
    """Interface to manage aggregate events at persistence layer"""

    async def list_versions(self, key: str) -> list[Version]:
        ...

    async def load_events(
        self,
        key: str,
        blank_aggregate: Aggregate,
        from_version_number: int | None = None,
        to_version_number: int | None = None,
    ) -> list[EventRecord]:
        ...

    async def save_events(self, key: str, event_records: list[EventRecord]):
        ...

    async def remove_events(self, key: str, till_version_number: int | None = None):
        ...


@dataclass
class Snapshot:
    version: Version
    content: dict[str, Any]


class SnapshotStore(Protocol):
    """Interfae to manage aggregate snapshots at persistence layer"""

    async def list_versions(self, key: str) -> list[Version]:
        ...

    async def load_snapshot(
        self, key: str, version_number: int | None = None
    ) -> Snapshot | None:
        ...

    async def save_snapshot(self, key: str, snap: Snapshot):
        ...

    async def remove_snapshots(self, key: str, to_version_number: int | None = None):
        """Remove snapshots till concrete version"""
