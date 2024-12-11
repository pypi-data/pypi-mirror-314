import json
from enum import Enum

class EnumEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            result = {"name": obj.name}
            if hasattr(obj, 'code'):
                result["code"] = obj.code
            if hasattr(obj, 'description'):
                result["description"] = obj.description
            return result
        return super().default(obj)