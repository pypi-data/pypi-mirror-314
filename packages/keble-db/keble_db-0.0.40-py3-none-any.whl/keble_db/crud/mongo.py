from typing import Generic, List, Optional, Type, TypeVar

from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.results import InsertOneResult, InsertManyResult, UpdateResult, DeleteResult

from .mongo_util import cleanse_query_for_first, cleanse_query_order_by, cleanse_query_for_list, MaybeObjectId, \
    build_object_id
from ..schemas import QueryBase

ModelType = TypeVar("ModelType", bound=BaseModel)


class MongoCRUDBase(Generic[ModelType]):

    def __init__(self, model: Type[ModelType], collection: str, database: str, *,
                 searchable: Optional[List[str]] = None):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD), in Mongo
        """
        self.model = model
        self.collection = collection
        self.searchable = searchable
        self.database = database

    def first(self, m: MongoClient, *, query: Optional[QueryBase] = None, project: Optional[dict] = None, **kwargs) -> \
            Optional[ModelType]:
        doc = self.first_doc(m, query=query, project=project, **kwargs)
        return self.model(**doc) if doc is not None else None

    def first_doc(self, m: MongoClient, *, query: Optional[QueryBase] = None, project: Optional[dict] = None,
                  **kwargs) -> Optional[dict]:
        doc: Optional[dict] = m[self.database][self.collection].find_one({**cleanse_query_for_first(query)},
                                                                         project, **kwargs,
                                                                         sort=cleanse_query_order_by(query))
        return doc

    def get_multi(
            self, m: MongoClient, *, query: QueryBase
    ) -> List[ModelType]:
        assert query.offset is not None and query.limit is not None, 'offset and limit is require for listing query'
        _sort = cleanse_query_order_by(query)
        cursor = m[self.database][self.collection].find(
            {**cleanse_query_for_list(query)})
        if _sort is not None and len(_sort) > 0:
            cursor = cursor.sort(_sort)
        docs: List[dict] = list(cursor.skip(query.offset).limit(query.limit))
        return [self.model(**doc) for doc in docs]

    def create(self, m: MongoClient, *, obj_in: ModelType) -> InsertOneResult:
        return m[self.database][self.collection].insert_one(obj_in.model_dump())

    def create_multi(self, m: MongoClient, *, obj_in_list: List[ModelType]) -> InsertManyResult:
        return m[self.database][self.collection].insert_many(
            [obj_in.model_dump() for obj_in in obj_in_list])

    def update(
            self, m: MongoClient, *, _id: MaybeObjectId, obj_in: dict,
    ) -> UpdateResult:
        return m[self.database][self.collection].update_one({'_id': build_object_id(_id)},
                                                            {'$set': obj_in})

    def hide(
            self, m: MongoClient, *, _id: MaybeObjectId,
    ) -> UpdateResult:
        return self.update(m, _id=_id, obj_in={"update": True})

    def delete(
            self, m: MongoClient, *, _id: MaybeObjectId,
    ) -> DeleteResult:
        return m[self.database][self.collection].delete_one({"_id": build_object_id(_id)})

    def delete_multi(
            self, m: MongoClient, *, query: QueryBase
    ) -> DeleteResult:
        query: dict = query.model_dump(exclude_none=True, exclude_unset=True, exclude_defaults=True)
        assert "filters" in query and query[
            "filters"] is not None, "you must set, and only set query.filters to delete_multi in mongodb"
        return m[self.database][self.collection].delete_many(query["filters"])

    def first_by_id(self, m: MongoClient, *, _id: MaybeObjectId, **kwargs) -> Optional[ModelType]:
        return self.first(m, query=QueryBase(id=_id if isinstance(_id, str) else str(_id)),
                          **kwargs)  # convert type for inserted_id

    def first_doc_by_id(self, m: MongoClient, *, _id: MaybeObjectId, **kwargs) -> Optional[dict]:
        return self.first_doc(m, query=QueryBase(id=_id if isinstance(_id, str) else str(_id)),
                              **kwargs)  # convert type for inserted_id
