import abc
import csv
import os.path

import aiofiles
from aiofiles import open

from aiospb.data import Metric

from ..data import DataType, PropertySet, PropertyValue


class HistoricalStore(abc.ABC):
    """Store historical changes to retrieve when host application is online"""

    @abc.abstractmethod
    async def save_dtos(self, changes: list[Metric]):
        """Save all change metrics of a scan"""

    @abc.abstractmethod
    async def load_all_dtos(self) -> list[Metric]:
        """Load all historical metric changes"""

    @abc.abstractmethod
    def has_dtos(self) -> bool:
        """Has data stored?"""

    @abc.abstractmethod
    async def clear(self):
        """Clear content of historical"""


class OnmemHistoricalStore(HistoricalStore):
    """Store historical changes on memory. Not recomemded if host will be stopped for a long time"""

    def __init__(self):
        self._dtos = []

    async def save_dtos(self, dtos: list[Metric]):
        self._dtos.extend(dtos)

    async def load_all_dtos(self) -> list[Metric]:
        dtos = [
            Metric(
                dto.timestamp,
                dto.value,
                dto.datatype,
                dto.alias,
                dto.name,
                dto.properties,
                is_historical=True,
            )
            for dto in self._dtos
        ]
        self._dtos.clear()
        return dtos

    def has_dtos(self):
        return bool(self._dtos)

    async def clear(self):
        self._dtos.clear()


class FsHistoricalStore(HistoricalStore):
    """Store historical changes in a plain file from a operating system"""

    def __init__(self, filename: str):
        self._fn = filename
        self._has_dtos = None

    async def save_dtos(self, dtos: list[Metric]):
        async with aiofiles.open(self._fn, "a") as f:
            lines = [self._create_line(dto) for dto in dtos]
            await f.writelines(lines)

        self._has_dtos = True

    def _create_line(self, dto: Metric) -> str:
        quality = dto.properties["quality"].value if "quality" in dto.properties else ""
        return f"{dto.timestamp};{dto.value};{dto.datatype.name};{quality};{dto.alias};{dto.name}\n"

    async def load_all_dtos(self) -> list[Metric]:
        dtos = []
        async with aiofiles.open(self._fn, "r") as f:
            while True:
                line = await f.readline()

                values = line[:-1].split(";")

                if len(values) == 1:
                    break

                ts, value, datatype, quality, alias, name = values
                properties = (
                    PropertySet.from_kwargs(
                        quality=PropertyValue(int(quality), DataType.Int32)
                    )
                    if quality != ""
                    else PropertySet()
                )
                dtos.append(
                    Metric(
                        int(ts),
                        DataType[datatype].convert_value(value),
                        DataType[datatype],
                        int(alias),
                        name,
                        properties,
                        is_historical=True,
                    )
                )

        return dtos

    def has_dtos(self):
        if self._has_dtos is None:
            self._has_dtos = os.path.exists(self._fn)
        return self._has_dtos

    async def clear(self):
        os.remove(self._fn)
        self._has_dtos = False
