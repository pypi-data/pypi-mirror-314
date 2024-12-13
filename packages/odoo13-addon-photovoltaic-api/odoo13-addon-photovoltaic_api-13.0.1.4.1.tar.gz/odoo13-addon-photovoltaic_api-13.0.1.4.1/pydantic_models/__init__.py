from typing import Any
from odoo import fields, models
from pydantic.utils import GetterDict
from pydantic import BaseModel

def false_to_none(obj, key, default=None):
    # from https://github.com/OCA/rest-framework/blob/15.0/pydantic/utils.py#L53
    res = getattr(obj, key)
    if isinstance(obj, models.BaseModel) and key in obj._fields:
        field = obj._fields[key]
        if res is False and field.type != "boolean":
            return None
        if field.type == "date" and not res:
            return None
        if field.type == "datetime":
            if not res:
                return None
            # Get the timestamp converted to the client's timezone.
            # This call also add the tzinfo into the datetime object
            return fields.Datetime.context_timestamp(self._obj, res)
        if field.type == "many2one" and not res:
            return None
        if field.type in ["one2many", "many2many"]:
            return list(res)
    return res

# from https://github.com/OCA/rest-framework/blob/15.0/pydantic/utils.py
class OdooGetter(GetterDict):
    def get(self, key: Any, default: Any = None) -> Any:
        return false_to_none(self._obj, key, default)

class OrmModel(BaseModel):
    class Config:
        orm_mode = True
        getter_dict = OdooGetter
