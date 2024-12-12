from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic.v1 import Field, StrictBool, StrictFloat, StrictInt, StrictStr

from kelvin.api.client.base_model import BaseModelRoot
from kelvin.api.client.data_model import DataModelBase


class ErrorObject(DataModelBase):
    """
    ErrorObject object.

    Parameters
    ----------
    name: Optional[StrictStr]
    title: Optional[StrictStr]
    description: Optional[StrictStr]
    solution: Optional[StrictStr]
    payload: Optional[Union[Dict[str, Any], List[Union[StrictInt, StrictFloat, StrictStr, StrictBool, Dict[str, Any]]]]]

    """

    name: Optional[StrictStr] = Field(None, description="ID of the error.")
    title: Optional[StrictStr] = Field(None, description="Title of the error.")
    description: Optional[StrictStr] = Field(None, description="A description of what the problem may be.")
    solution: Optional[StrictStr] = Field(None, description="A possible solution to the problem.")
    payload: Optional[
        Union[Dict[str, Any], List[Union[StrictInt, StrictFloat, StrictStr, StrictBool, Dict[str, Any]]]]
    ] = Field(
        None,
        description="Optional additional information. For example an array of objects listing all the errors that triggered the 4XX response.",
    )


class Error(BaseModelRoot[Union[ErrorObject, List[ErrorObject]]]):
    """
    Error object.

    Parameters
    ----------
    __root__: Union[ErrorObject, List[ErrorObject]]

    """

    __root__: Union[ErrorObject, List[ErrorObject]]


class Type(Enum):
    system = "system"


class ErrorLegacy(DataModelBase):
    """
    ErrorLegacy object.

    Parameters
    ----------
    description: Optional[StrictStr]
    name: Optional[StrictStr]
    payload: Optional[List[Dict[str, Any]]]
    solution: Optional[StrictStr]
    title: Optional[StrictStr]
    type: Optional[Type]

    """

    description: Optional[StrictStr] = Field(None, description="Description of what the error is about.")
    name: Optional[StrictStr] = Field(None, description="Unique identifier name of the error.")
    payload: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="A dictionary of all the individual error names, error titles, descriptions and solutions within the submitted information.",
    )
    solution: Optional[StrictStr] = Field(None, description="Possible solutions to resolve the error.")
    title: Optional[StrictStr] = Field(None, description="The Display name (title) of the error.")
    type: Optional[Type] = Field(None, description="The type of error that has occured, e.g. `system`.")
