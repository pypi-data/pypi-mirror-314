# single file reader, implement device.DeviceReader, for test

import typing as t
from pathlib import Path

from cathodic_collect.reader import device


def get_reader(base_dir: Path) -> t.Type[device.DeviceReader]:
    class DeviceReader(device.DeviceReader):
        """single file device reader"""

        def get_workdir(self) -> Path:
            return base_dir

        def read_stage(
            self, stage: int, file_id: int, ctype: t.Literal["ac", "dc"]
        ) -> Path:
            # current format.
            return base_dir / f"out{stage}-{ctype}.csv"

    return DeviceReader


def get_real_reader(base_dir: Path) -> t.Type[device.DeviceReader]:
    class DeviceReader(device.DeviceReader):
        """real device reader"""

        def get_workdir(self) -> Path:
            return base_dir

        def read_stage(
            self, stage: int, file_id: int, ctype: t.Literal["ac", "dc"]
        ) -> Path:
            # current format.
            return base_dir / f"result_{ctype}_{file_id}_{stage}.csv"

    return DeviceReader
