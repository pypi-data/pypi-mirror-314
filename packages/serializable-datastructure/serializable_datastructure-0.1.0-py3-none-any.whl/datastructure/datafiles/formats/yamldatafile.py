import yaml
from typing import Dict, Type

from .abstractdatafileformat import AbstractDataFileFormat


class YamlDataFile(AbstractDataFileFormat):
    extension = ".yaml"

    @classmethod
    def _dump(cls: Type["AbstractDataFileFormat"], filepath: str, dataDict: Dict) -> None:
        with open(filepath, "w", encoding="utf-8") as f:
            yaml.dump(
                dataDict,
                f,
                Dumper=yaml.CSafeDumper,
                allow_unicode=True,
                indent=4,
                default_flow_style=False,
                encoding="utf-8",
            )

    @classmethod
    def _load(cls: Type["AbstractDataFileFormat"], filepath: str) -> Dict:

        with open(filepath, "r", encoding="utf-8") as f:
            return yaml.load(f, Loader=yaml.CLoader)
