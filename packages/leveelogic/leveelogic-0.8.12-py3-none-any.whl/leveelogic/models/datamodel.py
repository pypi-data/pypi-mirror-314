import simplejson as json
from pydantic import BaseModel
from pathlib import Path


class DataModel(BaseModel):
    """ "Base class for all json serializable objects"""

    def to_json(self, indent: int = 4):
        """Convert to json string"""
        if indent != 0:
            return json.dumps(self.model_dump(), indent=indent)
        else:
            return json.dumps(self.model_dump())

    @classmethod
    def from_json(cls, json_str) -> "DataModel":
        """Generate class from json string"""
        return cls(**json.loads(json_str))

    @classmethod
    def parse(cls, filename: str) -> "DataModel":
        json_str = open(filename, "r").read()
        return cls(**json.loads(json_str))

    def serialize(self, filename: str) -> str:
        """Write to file

        Args:
            filepath (str): path to the file
            filename (str): filename

        Returns:
            str: absolute filename
        """
        path = Path(filename).resolve().parent
        path.mkdir(parents=True, exist_ok=True)
        with open(filename, "w") as outfile:
            json.dump(self.model_dump(), outfile, ignore_nan=True)
