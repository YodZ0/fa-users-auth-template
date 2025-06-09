from fastapi import Query, HTTPException, status
from typing import Optional, List, Set, Callable
from .schemas import SortSchema, QuerySchema


def parse_sort_fields(
    sort: Optional[List[str]],
    allowed_fields: Optional[Set[str]] = None,
) -> List[SortSchema]:
    if sort is None:
        return [SortSchema(field="id")]

    parsed_sort = []
    for field in sort:
        if field.startswith("-"):
            field = field[1:]
            s = SortSchema(field=field)
        else:
            s = SortSchema(field=field, order="asc")

        if field not in allowed_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Sorting by '{field}' is not allowed. Allowed fields: {allowed_fields}.",
            )

        parsed_sort.append(s)

    return parsed_sort


def get_query_params(allowed_sort_fields: Optional[Set[str]] = None) -> Callable:
    def dependency(
        limit: int = Query(10, gt=0, le=50),
        offset: int = Query(0, ge=0),
        sort: Optional[List[str]] = Query(
            None,
            description=f"Allowed fields: {allowed_sort_fields}",
        ),
    ) -> QuerySchema:
        parsed_sort = parse_sort_fields(
            sort=sort,
            allowed_fields=allowed_sort_fields,
        )
        return QuerySchema(limit=limit, offset=offset, sort=parsed_sort)

    return dependency
