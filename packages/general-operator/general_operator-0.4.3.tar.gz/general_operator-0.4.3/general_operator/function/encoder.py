from pydantic import BaseModel
from ..app.SQL.database import Base
from fastapi.encoders import jsonable_encoder

def custom_jsonable_encoder(obj, depth: int, current_depth: int = 0, exclude=None):
    if exclude is None:
        exclude = set()
    if isinstance(obj, dict):
        if current_depth >= depth:
            return {}
        return {key: custom_jsonable_encoder(value, depth, current_depth + 1, exclude)
                for key, value in obj.items() if key not in exclude}
    if isinstance(obj, list):
        if current_depth >= depth:
            return []
        return [custom_jsonable_encoder(item, depth, current_depth + 1, exclude)
                for item in obj]
    if isinstance(obj, BaseModel):
        keyValue = obj.dict()
        return custom_jsonable_encoder(keyValue, depth, current_depth)
    if isinstance(obj, Base):
        data = vars(obj)
        exclude.add("_sa_instance_state")
        return custom_jsonable_encoder(data, depth, current_depth, exclude)
    # Use FastAPI's default jsonable_encoder for other types
    return jsonable_encoder(obj, exclude=exclude)