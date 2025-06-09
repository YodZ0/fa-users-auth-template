from collections import defaultdict
from typing import Protocol

from sqlalchemy import select, literal_column, union_all
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models.references import Location, Gender, Status
from .schemas import Reference, ReferenceData


class ReferencesRepositoryProtocol(Protocol):

    async def get_all(self) -> ReferenceData: ...


class ReferencesRepositoryImpl:

    tables = [
        ("locations", Location),
        ("genders", Gender),
        ("statuses", Status),
        # others references
    ]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self) -> ReferenceData:
        async with self.session as s:
            combined_query = union_all(
                *(
                    select(
                        literal_column(f"'{table_name}'").label("table_name"),
                        model.id,
                        model.name,
                    )
                    for table_name, model in self.tables
                )
            )
            result = await s.execute(combined_query)

            grouped_data: defaultdict[str, list[Reference]] = defaultdict(list)
            for table_name, id_, name in result:
                grouped_data[table_name].append(Reference(id=id_, name=name))

            return ReferenceData(
                locations=grouped_data["locations"],
                genders=grouped_data["genders"],
                statuses=grouped_data["statuses"],
                # others references
            )
