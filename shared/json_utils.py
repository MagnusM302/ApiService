#json_utils.py
from bson import ObjectId

class JsonUtils:
    @staticmethod
    def convert_to_json_serializable(data):
        if isinstance(data, ObjectId):
            return str(data)
        elif isinstance(data, dict):
            return {k: JsonUtils.convert_to_json_serializable(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [JsonUtils.convert_to_json_serializable(item) for item in data]
        return data
