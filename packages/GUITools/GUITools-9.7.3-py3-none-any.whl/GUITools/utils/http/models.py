from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, Literal

class DataFetchHttpResult(BaseModel):
    name : str = Field(..., description="")
    success : bool  = Field(..., description="")
    content : dict | list[dict] = Field(..., description="")
    status_code : int = Field(..., description="")
    delay : float = Field(..., description="")

class HttpMethod(Enum):
    GET = "Get"
    POST = "Post"
    PUT = "Put"
    DELETE = "Delete"

class DataFetchHttp:
    def __init__(self, name : str, endpoint : str, http_method : HttpMethod, data : dict = {}):
        self.name = name
        self.endpoint = endpoint
        self.http_method = http_method
        self.data = data

class BaseError(BaseModel):
    """
    Base class to represent errors in the system.
    """
    message: str = Field(..., description="A descriptive error message.")
    status_code: Optional[int] = Field(
        None, description="The status code associated with the error (if applicable)."
    )
    code: Optional[str] = Field(
        None, description="The error code (if available)."
    )
    type: Optional[str] = Field(
        None, description="The type of the error (if available)."
    )


class InternalServerError(BaseError):
    """
    Represents an internal server error.
    """
    message: str = Field(
        "Internal server error", description="The error message."
    )


class UnavailableService(BaseError):
    """
    Represents an unavailable service error.
    """
    message: Literal["Database unavailable"] = Field(
        "Database unavailable", description="The unavailable service message."
    )


