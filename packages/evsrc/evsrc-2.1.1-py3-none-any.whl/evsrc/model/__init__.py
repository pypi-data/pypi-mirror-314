from dataclasses import dataclass

from dataclasses import dataclass, fields
from typing import Any, Callable, Protocol, Self, get_origin, runtime_checkable


@dataclass(frozen=True)
@runtime_checkable
class Value(Protocol):
    """Base class for all Value Objects, no other requirements, but it must be a dataclass"""

    def __post_init__(self):
        for field in fields(self):
            value = getattr(self, field.name)
            if get_origin(field.type) is tuple and type(value) is not tuple:
                object.__setattr__(self, field.name, tuple(value))


@dataclass(frozen=True)
class ChangeEvent(Value, Protocol):
    """Change of the state of an aggregate"""

    def apply_on(self, aggregate: "Aggregate"):
        """Apply event over aggregate"""


class Aggregate(Protocol):
    """Base of all aggregates under event sourcing approach"""

    @property
    def key(self) -> str:
        """Unique key between same type of aggregate"""

    def add_event_observer(self, callback: Callable[[ChangeEvent, Self], None]):
        """Add a observer of event changes"""

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> Self:
        """Construct the aggregate, not compulsory to implement"""
        raise NotImplementedError()

    def as_dict(self) -> dict[str, Any]:
        """Create a snap, not compulsory to implement"""
        raise NotImplementedError()


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
