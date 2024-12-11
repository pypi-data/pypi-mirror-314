import json


def JSONReadable(data):
    return json.dumps(data, indent=4, sort_keys=True)


from abc import ABC, abstractmethod


class Serializable(ABC):

    @abstractmethod
    def as_dict(self) -> dict:
        pass

