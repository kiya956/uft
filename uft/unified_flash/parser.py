import yaml

class DescriptorParser:
    """for verify tplan"""

    def __init__(self, file):
        try:
            with open(file, "r", encoding="utf-8") as fp:
                self._data = yaml.load(fp, Loader=yaml.FullLoader)
        except FileNotFoundError:
            print("Error: config yaml not found")
            self._data = None

    @property
    def data(self):
        """get data"""
        return self._data

