from ..schemas import QueryBase
from bson import ObjectId
from typing import Optional, List, Union, Tuple
from keble_helpers import is_pydantic_field_empty
from pymongo import ASCENDING, DESCENDING


def cleanse_query_for_first(query: Optional[QueryBase]) -> dict:
    if query is None: return {}
    assert query.filters is None or isinstance(query.filters, dict), "Query.filters only accept dict of Mongo query"
    base = query.filters if query.filters is not None else {}
    base = __build_id_query(base, query)
    return base


def cleanse_query_for_list(query: QueryBase) -> dict:
    base = query.filters if query.filters is not None else {}
    assert query.filters is None or isinstance(query.filters, dict), "Query.filters only accept dict of Mongo query"
    assert query.offset is None or isinstance(query.offset, int), "Offset must be int"
    base = __build_ids_query(base, query)
    return base


def cleanse_query_order_by(query: QueryBase) -> Optional[List[Tuple[str, int]]]:
    if query.order_by is not None:
        assert isinstance(query.order_by,
                          list), "Mongodb accept only List[Tuple[str, ASCENDING | DESCENDING]] type ordering"
        if len(query.order_by) == 0: return None
        for item in query.order_by:
            assert isinstance(item, tuple) and len(item) == 2 and isinstance(item[0], str) and item[1] in [DESCENDING,
                                                                                                           ASCENDING], "Mongodb accept only List[Tuple[str, ASCENDING | DESCENDING]] type ordering"
        return query.order_by


MaybeObjectId = Union[str, ObjectId]


def build_object_id(_id: Union[MaybeObjectId, List[MaybeObjectId]]) -> Union[ObjectId, List[ObjectId]]:
    if isinstance(_id, list): return [build_object_id(i) for i in _id]
    if isinstance(_id, str): return ObjectId(_id)
    return _id


def __build_id_query(base_query: dict, query: QueryBase) -> dict:
    if is_pydantic_field_empty(query, 'id'): return base_query
    # use $and if necessary
    q = {'_id': build_object_id(query.id)}
    return {'$and': [base_query, q]} if '_id' in base_query else {**base_query, **q}


def __build_ids_query(base_query: dict, query: QueryBase) -> dict:
    if is_pydantic_field_empty(query, 'ids'): return base_query
    # use $and if necessary
    q = {'_id': {'$in': build_object_id(query.ids)}}
    return {'$and': [base_query, q]} if '_id' in base_query else {**base_query, **q}


def ensure_object_id(id: MaybeObjectId) -> ObjectId:
    if isinstance(id, str): return ObjectId(id)
    return id
