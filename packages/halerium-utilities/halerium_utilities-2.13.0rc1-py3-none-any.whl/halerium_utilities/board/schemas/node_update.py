from pydantic.v1 import BaseModel, ConfigDict, Field, validator
from typing import Literal, Union

from halerium_utilities.board.schemas.id_schema import NodeId
from halerium_utilities.board.schemas.node_types import NODES


# factory for creating type specifics in which all fields are optional and all defaults are None
type_specific_models = {}
for _name, _model in NODES.items():
    _new_model = type(_model.__name__+"Update", (_model,), {})
    for _field in _new_model.__fields__.values():
        _field.default = None
        _field.required = False
    type_specific_models[_name] = _new_model


class PositionUpdate(BaseModel):
    x: int = None
    y: int = None


class SizeUpdate(BaseModel):
    width: int = Field(None, ge=0, description="The width of the node in pixels")
    height: int = Field(None, ge=0, description="The height of the node in pixels")


class NodeUpdate(NodeId):
    type: Literal[tuple(NODES)]
    position: PositionUpdate = None
    size: SizeUpdate = None
    type_specific: Union[(dict, *type_specific_models.values())] = None

    @validator('type_specific')
    def check_type_specific(cls, t, values):
        if t is None:
            return None
        type = values.get("type", tuple(NODES)[0])
        schema = type_specific_models[type]
        return schema.validate(t)



#
#
#
#
# # to build a NodeUpdate class we first build a base in which we remove type and type_specific
# # and make all fields apart from id optional
# # since we inherit from Node we keep e.g. the id validator
# _NodeUpdate = type("_NodeUpdate", (Node,), {})
# for _name in list(_NodeUpdate.__fields__):
#     if _name in ("type", "type_specific"):
#         try:
#             del _NodeUpdate.__fields__[_name]
#             del _NodeUpdate.__validators__[_name]
#         except KeyError:
#             pass
#     elif _name != "id":
#         _NodeUpdate.__fields__[_name].default = None
#         _NodeUpdate.__fields__[_name].required = False
#
#
# # then we create the actual NodeUpdate class by re-adding the type_specific field with
# # the type_specific update classes and a new validator
# class NodeUpdate(_NodeUpdate):
#     type_specific: Optional[Union[(Dict,) + tuple(type_specific_models.values())]]
#
#     @validator('type_specific')
#     def check_type_specific(cls, t):
#         # if no type_specific content is there do nothing
#         if len(t) == 0:
#             return BaseModel.validate(t)
#
#         # find key matches with type specific models
#         matches = {}
#         for name, model in type_specific_models.items():
#             matches[model] = len(set(model.__fields__) & set(t))
#
#         max_matches = max(matches.values())
#
#         candidates = []
#         for model, num_matches in matches.items():
#             if num_matches == max_matches:
#                 candidates.append(model)
#                 try:
#                     return model.validate(t)
#                 except ValidationError:
#                     pass
#
#         raise ValidationError(f"Could not validate {t} with with {candidates}.")
#
