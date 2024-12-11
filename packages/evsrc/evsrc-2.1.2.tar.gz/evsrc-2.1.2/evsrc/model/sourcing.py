import asyncio
from typing import Callable, Any, TypeVar
from . import (
    EventRecord,
    EventStore,
    Snapshot,
    SnapshotStore,
    Version,
    Aggregate,
    ChangeEvent,
)
from ..time import RealClock, Clock
from weakref import WeakValueDictionary


class EventHandler:
    """Help the hangling of events by aggregates.
    Its use is optional
    """

    def __init__(self, aggregate: Aggregate):
        self._history = []
        self._observers = set()
        self._aggregate = aggregate

    def add_observer(self, callback: Callable[[ChangeEvent, Any], None]):
        """Add callback to be used when a event is trigered, it avoids accidental duplication"""
        if callback in self._observers:
            return

        self._observers.add(callback)
        for event in self._history:
            callback(event, self._aggregate)

    def register_event(self, event: ChangeEvent):
        """Register event to history"""
        self._history.append(event)
        for callback in self._observers:
            callback(event, self._aggregate)


T = TypeVar("T", bound=Aggregate)


class SourcingHandler:
    """Help to construct aggregate stores or repositories to the developer"""

    def __init__(
        self,
        event_store: EventStore | None = None,
        snap_store: SnapshotStore | None = None,
        clock: Clock | None = None,
    ):
        if event_store is None and snap_store is None:
            raise ValueError("Event store or/and snap store shall be supplied")

        self._event_store = event_store
        self._snap_store = snap_store
        self._clock = clock or RealClock()
        self._observers = []
        self._aggregates = WeakValueDictionary()
        self._event_records = {}

    def add_observer(
        self, callback: Callable[[str, EventRecord], None], pattern: str = ""
    ):
        """Notify about eventchanges to any observer
        Useful for the implementation of projections"""

        self._observers.append(callback)

    async def version_history(self, key: str) -> list[Version]:
        """List all versions of a aggregate."""
        if self._event_store:
            return await self._event_store.list_versions(key)
        if self._snap_store:
            return await self._snap_store.list_versions(key)
        return []

    async def construct_aggregate(
        self, key: str, blank_aggregate: T, to_version_number: int | None = None
    ) -> T | None:
        """Construct an aggregate from persistence layer. Default is last version."""

        from_version_number = 0
        if self._snap_store:
            snap = await self._snap_store.load_snapshot(key)
            if not snap:
                return
            from_version_number = snap.version.value + 1
            blank_aggregate = blank_aggregate.from_dict(snap.content)

        if self._event_store:
            records = await self._event_store.load_events(
                key, blank_aggregate, from_version_number, to_version_number
            )
            for record in records:
                record.event.apply_on(blank_aggregate)
            if records:
                from_version_number = records[-1].version.value + 1

        self._link_aggregate(key, blank_aggregate, from_version_number)
        return blank_aggregate

    def _link_aggregate(self, key, aggregate, from_version_number):
        def callback(event: ChangeEvent, _: Aggregate):
            if key not in self._event_records:
                self._event_records[key] = [
                    EventRecord(
                        Version(from_version_number, self._clock.timestamp()), event
                    )
                ]
            else:
                next_version = self._event_records[key][-1].version.value + 1
                self._event_records[key].append(
                    EventRecord(Version(next_version, self._clock.timestamp()), event)
                )

        self._clean_destroyed_aggregates()
        aggregate.add_event_observer(callback)
        self._aggregates[key] = aggregate

    def _clean_destroyed_aggregates(self):
        for key in set(self._event_records.keys()) - set(self._aggregates.keys()):
            self._event_records.pop(key)

    async def _notify(self, key):
        await asyncio.gather(
            *[self._notify_to_observer(callback, key) for callback in self._observers]
        )

    async def _notify_to_observer(self, callback, key):
        for record in self._event_records.get(key, []):
            await callback(key, record)

    async def save_events(self, key: str, aggregate: Aggregate):
        """Store the events of an aggregate to persistence layer.
        Only if event_store is injected"""
        if self._event_store:
            if key not in self._aggregates:  # New
                self._link_aggregate(key, aggregate, 0)

            await self._notify(key)
            records = self._event_records.pop(key, [])
            if records:
                await self._event_store.save_events(key, records)

    async def save_snapshot(self, key: str, aggregate: Aggregate):
        """Store a snapshot of the aggregate to persistence layer.
        Only if the snap_store is injected"""
        if not self._snap_store:
            raise ValueError(f"Snapstore is not injected")

        if key not in self._aggregates:  # New
            self._link_aggregate(key, aggregate, 0)

        if key not in self._event_records:
            version = Version(0, self._clock.timestamp())
        else:
            version = self._event_records[key][-1].version

        await self._notify(key)
        self._event_records.pop(key, [])
        await self._snap_store.save_snapshot(
            key, Snapshot(version, aggregate.as_dict())
        )
