from pydantic.v1 import validator
from typing import Literal, Union

from halerium_utilities.board.schemas.id_schema import EdgeId
from halerium_utilities.board.schemas.edge import Connections
from halerium_utilities.board.schemas.edge_types import EDGES


# factory for creating type specifics in which all fields are optional and all defaults are None
type_specific_models = {}
for _name, _model in EDGES.items():
    _new_model = type(_model.__name__+"Update", (_model,), {})
    for _field in _new_model.__fields__.values():
        _field.default = None
        _field.required = False
    type_specific_models[_name] = _new_model


class EdgeUpdate(EdgeId):
    type: Literal[tuple(EDGES)]
    connections: Connections = None
    type_specific: Union[(dict, *type_specific_models.values())] = None

    @validator('type_specific')
    def check_type_specific(cls, t, values):
        if t is None:
            return None
        type = values.get("type", tuple(EDGES)[0])
        schema = type_specific_models[type]
        return schema.validate(t)



#
#
# # to build a NodeUpdate class we first build a base in which we remove type and type_specific
# # and make all fields apart from id optional
# # since we inherit from Node we keep e.g. the id validator
# _EdgeUpdate = type("_EdgeUpdate", (Edge,), {})
# for _name in list(_EdgeUpdate.__fields__):
#     if _name in ("type", "type_specific"):
#         try:
#             del _EdgeUpdate.__fields__[_name]
#             del _EdgeUpdate.__validators__[_name]
#         except KeyError:
#             pass
#     elif _name != "id":
#         _EdgeUpdate.__fields__[_name].default = None
#         _EdgeUpdate.__fields__[_name].required = False
#
#
# class EdgeUpdate(_EdgeUpdate):
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
