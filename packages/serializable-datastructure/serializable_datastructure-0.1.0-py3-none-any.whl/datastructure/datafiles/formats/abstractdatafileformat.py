import os
from typing import Dict, Optional, Type


class AbstractDataFileFormat:
    extension: Optional[str] = None

    @classmethod
    def _dump(
        cls: Type["AbstractDataFileFormat"],
        filepath: str,
        dataDict: Dict,
    ) -> None:
        raise NotImplementedError(f"{cls.__name__}._dump method must be implemented")

    @classmethod
    def _load(cls: Type["AbstractDataFileFormat"], path: str) -> Dict:
        raise NotImplementedError(f"{cls.__name__}._load method must be implemented")

    @classmethod
    def __isValidFilePath(cls: Type["AbstractDataFileFormat"], filepath: str) -> str:
        # Check if extension is not None
        if cls.extension is None:
            raise ValueError(f"{cls}.extension class attribute must be defined")

        # Check if the filepath is a string
        if not isinstance(filepath, str):
            raise TypeError("filepath must be a string")

        # Check if the filepath is empty
        if filepath == "":
            raise ValueError("filepath must not be empty")

        # Check if extension is correct
        if not filepath.endswith(cls.extension):
            raise ValueError(f"File extension must be {cls.extension}")

        # Check if relative path is provided
        if not os.path.isabs(filepath):
            # Build the absolute path
            filepath = os.path.abspath(filepath)

        return filepath

    @classmethod
    def __isValidDataDict(cls: Type["AbstractDataFileFormat"], dataDict: Dict) -> None:
        # Check if the dataDict is a dictionary
        if not isinstance(dataDict, dict):
            raise TypeError("dataDict must be a dictionary")

        # Check if the dataDict is empty
        if not dataDict:
            raise ValueError("dataDict must not be empty")

    @classmethod
    def dump(
        cls: Type["AbstractDataFileFormat"],
        filepath: str,
        dataDict: Dict,
    ) -> None:
        # Check if the path is valid
        filepath = cls.__isValidFilePath(filepath)

        # Check if the dataDict is valid
        cls.__isValidDataDict(dataDict)

        # Check if directory exists
        if not os.path.exists(dirname := os.path.dirname(filepath)):
            raise FileNotFoundError(f"Directory {dirname} does not exist")

        # Call the _dump method
        cls._dump(filepath, dataDict)

    @classmethod
    def load(cls: Type["AbstractDataFileFormat"], filepath: str) -> Dict:
        # Check if the path is valid
        filepath = cls.__isValidFilePath(filepath)

        # Check if the file exists
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File {filepath} does not exist")

        # Call the _load method
        return cls._load(filepath)

if __name__ == "__main__":

    class JsonDataFile(AbstractDataFileFormat):
        extension = ".json"

        @staticmethod
        def _dump(filepath: str, dataDict: Dict) -> None:
            import json

            with open(filepath, "w") as f:
                json.dump(dataDict, f, indent=4, sort_keys=True)

    boxData = JsonDataFile.dump(
        ".test/box.json",
        {"length": 10, "width": 5, "height": 3},
    )
