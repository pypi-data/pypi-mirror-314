import asyncio
import json
from aiofs import FileLike, FileLikeSystem
from evsrc.model import (
    Aggregate,
    ConcurrenceError,
    EventStore,
    SnapshotStore,
    Snapshot,
    EventRecord,
    ChangeEvent,
    Version,
)
from .mapping import ValueDictMapper


class JsonEventStore(EventStore):
    """Implement persistence of event records usin json encoding"""

    def __init__(self, fs: FileLikeSystem, template: str = "{}.json"):
        self._fs = fs
        self._fs.template = template

    async def list_versions(self, key: str) -> list[Version]:
        async with self._fs.open(key, "r") as f:
            data = json.loads((await f.read()).decode())
            initial_version = data.get("initial_version", 0)
            return [
                Version(index + initial_version, ts)
                for index, ts in enumerate(data["timestamps"])
            ]

    async def load_events(
        self,
        key: str,
        blank_aggregate: Aggregate,
        from_version_number: int | None = None,
        to_version_number: int | None = None,
    ) -> list[EventRecord]:
        async with self._fs.open(key, "r") as f:
            result = []
            try:
                data = json.loads((await f.read()).decode())
            except FileNotFoundError:
                return []
            version_number = data.get("initial_version", 0) - 1
            for ts, event_data in zip(data["timestamps"], data["events"]):
                version_number += 1
                if (
                    from_version_number is not None
                    and version_number < from_version_number
                ):
                    continue
                if to_version_number is not None and version_number > to_version_number:
                    break

                event_cls = getattr(blank_aggregate, event_data.pop("__event__"))
                result.append(
                    EventRecord(
                        Version(version_number, ts),
                        ValueDictMapper.from_dict(event_cls, event_data),
                    )
                )

            return result

    async def save_events(self, key: str, event_records: list[EventRecord]):
        async with self._fs.open(key, "r+") as f:
            try:
                data = json.loads((await f.read()).decode())
            except FileNotFoundError:
                data = {"timestamps": [], "events": []}

            if (
                "initial_version" in data
                and data["initial_version"] + len(event_records) + 1
                != event_records[0].version.value
            ):
                raise ConcurrenceError(f"Events in {key} are not correlative to saved ")
            if "initial_version" not in data:
                data["initial_version"] = event_records[0].version.value

            timestamps = data["timestamps"]
            events = data["events"]
            for record in event_records:
                timestamps.append(record.version.timestamp)
                event_data = ValueDictMapper.to_dict(record.event)
                event_data["__event__"] = record.event.__class__.__name__
                events.append(event_data)

            await f.write(json.dumps(data).encode())

    async def remove_events(self, key: str, till_version_number: int | None = None):
        if till_version_number is None:
            await self._fs.rm(key)

        async with self._fs.open(key, "r+") as f:
            try:
                data = json.loads((await f.read()).decode())
            except FileNotFoundError:
                return

            timestamps = []
            events = []
            version = data.get("initial_version", 0) - 1
            for ts, event_data in zip(data["timestamps"], data["events"]):
                version += 1
                if version <= till_version_number:
                    continue
                timestamps.append(ts)
                events.append(event_data)

            await f.write(
                json.dumps(
                    {
                        "initial_version": version - len(timestamps) + 1,
                        "timestamps": timestamps,
                        "events": events,
                    }
                ).encode()
            )


class JsonSnapshotStore(SnapshotStore):
    """Implement persistence of Snapshots using json encoding."""

    def __init__(self, fs: FileLikeSystem, template: str = "{}.json"):
        self._fs = fs
        self._fs.template = template

    async def list_versions(self, key: str) -> list[Version]:
        async with self._fs.open(f"{key}/snapshot_versions", "r") as f:
            try:
                data = json.loads((await f.read()).decode())
            except FileNotFoundError:
                return []
            return [
                Version(value, ts)
                for ts, value in zip(data["timestamps"], data["versions"])
            ]

    async def load_snapshot(
        self, key: str, version_number: int | None = None
    ) -> Snapshot | None:
        async with self._fs.open(f"{key}/snapshot_versions", "r") as f:
            try:
                data = json.loads((await f.read()).decode())
            except FileNotFoundError:
                return

            if version_number is None:
                version = Version(data["versions"][-1], data["timestamps"][-1])
            else:
                if version_number not in data["versions"]:
                    return
                version = Version(
                    version_number,
                    data["timestamps"][data["versions"].index(version_number)],
                )

        async with self._fs.open(f"{key}/snapshot__{version.value}", "r") as f:
            try:
                data = json.loads((await f.read()).decode())
            except FileNotFoundError:
                return

            return Snapshot(version, data)

    async def save_snapshot(self, key: str, snap: Snapshot):
        """Save snapshot"""
        await self._save_version(f"{key}/snapshot_versions", snap.version)
        await self._save_content(f"{key}/snapshot__{snap.version.value}", snap.content)

    async def _save_version(self, key: str, version: Version):
        async with self._fs.open(key, "r+") as f:
            try:
                data = json.loads((await f.read()).decode())
            except FileNotFoundError:
                data = {"versions": [], "timestamps": []}

            if data["versions"] and (
                version.value <= data["versions"][-1]
                or version.timestamp < data["timestamps"][-1]
            ):
                raise ConcurrenceError(
                    f'Snap to save at "{key}" has a version newer than the last one'
                )

            data["versions"].append(version.value)
            data["timestamps"].append(version.timestamp)

            await f.write(json.dumps(data).encode())

    async def _save_content(self, key: str, content: bytes):
        async with self._fs.open(key, "w") as f:
            await f.write(json.dumps(content).encode())

    async def remove_snapshots(self, key: str, to_version_number: int | None = None):
        versions = []
        tss = []
        async with self._fs.open(f"{key}/snapshot_versions", "r+") as f:
            try:
                data = json.loads((await f.read()).decode())
            except FileNotFoundError:
                return

            if to_version_number is None:
                to_version_number = data["versions"][-1] - 1

            for ts, version in zip(data["timestamps"], data["versions"]):
                if to_version_number is None or version <= to_version_number:
                    await self._fs.rm(f"{key}/snapshot__{version}")
                else:
                    versions.append(version)
                    tss.append(ts)

            await f.write(
                json.dumps({"timestamps": tss, "versions": versions}).encode()
            )

        if not versions:
            await self._fs.rm(f"{key}/snapshot_versions")
