"""Give to developer clients a quick on memory implementation for testing purpose
Don't mock, use this Fake Implementations for your tests"""

from typing import Type
from ..model import (
    Aggregate,
    EventStore,
    SnapshotStore,
    Version,
    Snapshot,
    EventRecord,
    ConcurrenceError,
)


class OnmemEventStore(EventStore):
    """Implementation of EventStore on memory for testing purpose"""

    def __init__(self):
        self._data = {}

    async def list_versions(self, key: str) -> list[Version]:
        return [record.version for record in self._data[key]]

    async def load_events(
        self,
        key: str,
        _: Aggregate,
        from_version_number: int = 0,
        to_version_number: int = 0,
    ) -> list[EventRecord]:
        if key not in self._data:
            return []

        def filter_fn(record):
            return (
                not from_version_number or from_version_number <= record.version.value
            ) and (not to_version_number or to_version_number >= record.version.value)

        return [record for record in self._data[key] if filter_fn(record)]

    async def save_events(self, key: str, event_records: list[EventRecord]):
        if key not in self._data:
            self._data[key] = []

        if (
            self._data[key]
            and self._data[key][-1].version.value + 1 != event_records[0].version.value
        ):
            raise ConcurrenceError(f'Aggregate "{key}" has not continous version')
        self._data[key].extend(event_records)

    async def remove_events(self, key: str, till_version_number: int | None = None):
        if till_version_number is None:
            self._data.pop(key)
            return

        self._data[key] = [
            record
            for record in self._data[key]
            if record.version.value > till_version_number
        ]


class OnmemSnapshotStore(SnapshotStore):
    """Implementatioin of SnapshotStore on memory for testing purpose"""

    def __init__(self):
        self._data = {}

    async def list_versions(self, key: str) -> list[Version]:
        if key not in self._data:
            return []
        return [snap.version for snap in self._data[key]]

    async def load_snapshot(
        self, key: str, version_number: int | None = None
    ) -> Snapshot | None:
        if key not in self._data:
            return

        if version_number is None:
            return self._data[key][-1]

        for snap in self._data[key]:
            if snap.version.value == version_number:
                return snap

    async def save_snapshot(self, key: str, snap: Snapshot):
        if key not in self._data:
            self._data[key] = []

        if self._data[key] and (
            self._data[key][-1].version.value >= snap.version.value
            or self._data[key][-1].version.timestamp > snap.version.timestamp
        ):
            raise ConcurrenceError(f'Snapshot for "{key}" is previous to the stored')
        self._data[key].append(snap)

    async def remove_snapshots(self, key: str, to_version_number: int | None = None):
        if key not in self._data:
            return

        if to_version_number is None:
            self._data[key] = self._data[key][-1:]
            return

        self._data[key] = [
            snap for snap in self._data[key] if snap.version.value > to_version_number
        ]
