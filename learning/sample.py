import json
from learning import learning_utils

class Sample:
    def __init__(self, json_str=None, data=None, label=None):
        """
        Initialize a new sample. Must be given either a json string or
        data and label as parameters
        :param json_str: Source sample from json string
        :param data: Source sample from data, label must also be given
        :param label: Source sample from label, data must also be given
        """
        if json_str is not None:
            src = json.loads(json_str)
            self._data = src["data"]
            self._label = src["label"]
        elif data is not None and label is not None:
            self._data = data
            self._label = label
        else:
            raise Exception("Sample1D needs either json_str or data and label")

    @property
    def label(self):
        """
        Sample label is read only
        :return: Sample label
        """
        return self._label

    @property
    def data(self):
        """
        Sample data is read only
        :return: Sample data
        """
        return self._data

    def __str__(self):
        """
        Gives the sample in JSON representation
        :return: JSON string
        """
        return json.dumps({
            "data": self._data,
            "label": self._label
        })

    def save(self):
        """
        Saves the sample to "samples.txt"
        TODO: maybe replace this with DB
        """
        with open("samples.txt", "a") as f:
            f.write(str(self) + "\n")

    def normalize(self):
        """
        Normalizes the sample's data
        """
        d = learning_utils.convert_data_to_2d(self._data)
        d = learning_utils.normalize_2d(d)
        self._data = learning_utils.convert_data_to_1d(d)
