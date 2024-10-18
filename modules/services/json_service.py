import json
from modules.core.singleton import Singleton


class JsonService(metaclass=Singleton):
    def __init__(self):
        pass

    def to_json(self, obj: object):
        return json.dumps(
            obj, default=lambda o: o.__dict__, ensure_ascii=False, indent=4
        )

    def to_file(self, obj: object, file_path: str):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(self.to_json(obj))

    def to_object(self, json_str: str, cls: type):
        return json.loads(json_str, object_hook=lambda d: cls(**d))

    def to_object_from_file(self, file_path: str, cls: type):
        with open(file_path, "r", encoding="utf-8") as f:
            return self.to_object(f.read(), cls)

    def get_json_string_from_file(self, file_path: str):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
