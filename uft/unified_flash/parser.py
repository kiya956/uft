import yaml
import jsonschema
from jsonschema import validate

LAUNCHER_SCHEMA = {
    "type": "object",
    "properties": {
        "items": {
            "type": "array",
            "minItems": 1,
            "urls": {
                "type": "object",
                "properties": {
                    "url": {"type": "string"},
                    "sha256sum": {"type": "string"},
                },
                "required": ["url",]
            },
        "provision": {"type": "string"},
        "extra_args": {"type": "string"},
        },
    },
    "required": ["provision"]
}

class DescriptorParser:
    """for verify tplan"""

    def __init__(self, file):
        try:
            with open(file, "r", encoding="utf-8") as fp:
                self._data = yaml.load(fp, Loader=yaml.FullLoader)
        except FileNotFoundError:
            print("Error: config yaml not found")
            self._data = None

        self.validate_data()

    @property
    def data(self):
        """get data"""
        return self._data

    def validate_data(self):
        """validate iot sanit tplan json"""

        try:
            validate(instance=self._data, schema=LAUNCHER_SCHEMA)
            print("the JSON data is valid")
        except jsonschema.exceptions.ValidationError as err:
            raise ValueError(f"the JSON data is invalid, err {err}") from err


