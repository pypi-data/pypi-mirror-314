import pandas as pd
from datetime import date, datetime
from enum import Enum
from inspect import isclass
from typing import Any, Dict, Type

from .datafiles.interface import DataFileInterface

class DataStructure:

    # Class attributes
    readOnly: bool = False

    def __init__(self, **kwargs) -> None:
        super().__init__()
        
        # Init all attributes
        self.__attributes = kwargs

    @property
    def attributes(self) -> Dict[str, Any]:
        return self.__attributes

    def __iter__(self):
        # Get the attributes of the Box class
        for key, value in self.attributes.items():

            if isinstance(value, DataStructure):
                yield key, dict(value)
            elif isinstance(value, list):
                yield key, [
                    dict(item) if isinstance(item, DataStructure) else item
                        for item in value
                ]
            elif isinstance(value, dict):
                yield key, {
                    subkey: dict(subvalue)
                    if isinstance(subvalue, DataStructure)
                    else subvalue
                    for subkey, subvalue in value.items()
                }
            elif isinstance(value, set):
                yield key, {
                    item.__dict__ if isinstance(item, DataStructure) else item
                    for item in value
                }
            elif isinstance(value, tuple):
                yield key, tuple(
                    item.__dict__ if isinstance(item, DataStructure) else item
                    for item in value
                )
            elif isinstance(value, pd.DataFrame):
                yield key, value.to_dict()
            elif isclass(value):
                yield key, value.__name__
            elif isinstance(value, Enum):
                yield key, value.value
            elif isinstance(value, (date, datetime)):
                yield key, value.isoformat()
            else:
                yield key, value

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({dict(self)})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def copy(self) -> "DataStructure":
        return self.__class__(**dict(self))

    def dump(self, filepath: str) -> None:
        # Call the _dump method
        DataFileInterface.dump(filepath, dict(self))
    
    def setAttribute(self, key: str, value: Any):
        if self.__class__.readOnly:
            raise ValueError(f"Can't set {key} attribute: {self.__class__.__name__} is read-only")
        
        self.__attributes[key] = value

    @classmethod
    def load(cls: Type["DataStructure"], filepath: str) -> "DataStructure":
        # Load the data from the file
        dataDict = DataFileInterface.load(filepath)

        # Create a new data structure object
        return cls(**dataDict)
