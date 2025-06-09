import uuid
from typing import Any, Generic, TypeVar

from fastapi import HTTPException, status

from .models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class ModelNotFoundException(HTTPException, Generic[ModelType]):
    """
    Model not found exception.
    """

    def __init__(
        self,
        model: type[ModelType],
        model_id: uuid.UUID | int | None = None,
        headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Unable to find the {model.__name__} with id {model_id}."
                if model_id is not None
                else f"{model.__name__} id not found."
            ),
            headers=headers,
        )


class ModelAlreadyExistsError(Exception):
    """
    Error that occurs when trying to create a model with an existing unique field.
    """

    def __init__(self, field: str, message: str, *args: object) -> None:
        super().__init__(*args)
        self.field = field
        self.message = message


class ValidationError(Exception):
    """
    Validation error.
    """

    def __init__(self, field: str | list[str], message: str, *args: object) -> None:
        super().__init__(*args)
        self.field = field
        self.message = message


class SortingFieldNotFoundError(Exception):
    """
    Error that occurs when the sorting field cannot be found.
    """

    def __init__(self, field: str, *args: object) -> None:
        super().__init__(*args)
        self.message = f"Sorting field not found: {field}"


class FilteringFieldNotFoundError(Exception):
    """
    Error that occurs when the filtering field cannot be found.
    """

    def __init__(self, field: str, *args: object) -> None:
        super().__init__(*args)
        self.message = f"Filtering field not found: {field}"
