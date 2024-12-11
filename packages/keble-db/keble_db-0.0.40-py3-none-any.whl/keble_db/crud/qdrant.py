from typing import Any
from typing import Generic, List, Optional, Type, TypeVar, Sequence, Tuple

from pydantic import BaseModel
from qdrant_client import QdrantClient, models as qdrant_models
from qdrant_client.conversions import common_types as qdrant_types

from .qdrant_util import cleanse_query_for_search
from ..schemas import QueryBase

ModelType = TypeVar("ModelType", bound=BaseModel)
VectorModelType = TypeVar("VectorModelType", bound=BaseModel)


class Record(qdrant_types.Record):
    payload: Optional[Any] = None
    score: Optional[float] = None
    vector: Optional[VectorModelType] = None


class QdrantCRUDBase(Generic[ModelType, VectorModelType]):

    def __init__(self, model: Type[ModelType], vector_model: Type[VectorModelType], collection: str):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD) in Qdrant

        **Parameters**
        * `model`: A Qdrant Alchemy model class
        """
        self.model: Type[ModelType] = model
        self.vector_model: Type[VectorModelType] = vector_model
        self.collection = collection

    def __is_result_success(self, result: qdrant_types.UpdateResult):
        return result.status.lower() == qdrant_models.UpdateStatus.COMPLETED.value.lower()

    def __convert_record(self, record: qdrant_types.Record) -> Record:
        return Record(**record.model_dump(exclude={"payload", "vector"}),
                      payload=self.model(**record.payload) if record.payload is not None else None,
                      vector=self.vector_model(**record.vector) if record.vector is not None else None
                      )

    def __convert_records(self, records: List[qdrant_types.Record]) -> List[Record]:
        return [self.__convert_record(record=record) for record in records]

    def get_multi_records_by_ids(
            self,
            client: QdrantClient,
            *,
            _ids: Sequence[qdrant_types.PointId],
            **kwargs
    ) -> List[Record]:
        return self.__convert_records(client.retrieve(
            self.collection,
            ids=_ids,
            **kwargs
        ))

    def get_multi_by_ids(
            self,
            client: QdrantClient,
            *,
            _ids: Sequence[qdrant_types.PointId],
            **kwargs
    ) -> List[ModelType]:
        records = self.get_multi_records_by_ids(client, _ids=_ids, **kwargs)
        return [r.payload for r in records]

    def first_record_by_id(
            self,
            client: QdrantClient,
            *,
            _id: qdrant_types.PointId,
            **kwargs
    ) -> Optional[Record]:
        records: List[Record] = self.get_multi_records_by_ids(client, _ids=[_id], **kwargs)
        if len(records) < 1: return None
        return records[0]

    def first_by_id(
            self,
            client: QdrantClient,
            *,
            _id: qdrant_types.PointId,
            **kwargs
    ) -> Optional[ModelType]:
        record = self.first_record_by_id(client, _id=_id, **kwargs)
        if record is not None: return record.payload

    def search(self, client: QdrantClient, *, vector: List[float], vector_key: str, query: Optional[QueryBase] = None,
               score_threshold: float = 0.76,
               # 0.76 ~ 0.8 is a decent threshold base on our test, among different languages
               **kwargs
               ) -> List[Record]:
        filter_ = cleanse_query_for_search(query, offset_type="int")
        scored_points: List[qdrant_types.ScoredPoint] = client.search(
            self.collection,
            query_filter=filter_,
            query_vector=(vector_key, vector),
            limit=query.limit,
            offset=query.offset,
            score_threshold=score_threshold,
            **kwargs
        )
        return [Record(**sp.model_dump(include={"score", "shard_key", "id"}),
                       payload=self.model(**sp.payload) if sp.payload is not None else None,
                       vector=self.vector_model(**sp.vector) if sp.vector is not None else None) for sp in
                scored_points]

    def scroll_records(self, client: QdrantClient, *, query: QueryBase, **kwargs) -> Tuple[
        List[Record], Optional[qdrant_types.PointId]]:
        filter_ = cleanse_query_for_search(query, offset_type="str")
        assert query.limit is not None, "You need to provide limit to perform a scroll in Qdrant"
        records, next_point_id = client.scroll(
            self.collection,
            scroll_filter=filter_,
            limit=query.limit,
            offset=query.offset,
            **kwargs
        )
        return self.__convert_records(records), next_point_id

    def scroll(self, client: QdrantClient, *, query: QueryBase, **kwargs) -> Tuple[
        List[ModelType], Optional[qdrant_types.PointId]]:
        records, next_point_id = self.scroll_records(client, query=query, **kwargs)
        return [record.payload for record in records], next_point_id

    def create(
            self,
            client: QdrantClient,
            vector: VectorModelType,
            payload: ModelType,
            _id: qdrant_types.PointId,
            **kwargs
    ) -> bool:
        vector_dict = vector.model_dump(exclude_none=True, exclude_unset=True)
        _, status = client.upsert(
            collection_name=self.collection,
            points=[
                qdrant_models.PointStruct(
                    id=_id,
                    vector=vector_dict,
                    payload=payload.model_dump(),
                )
            ],
            **kwargs
        )
        status = status[1] if isinstance(status, tuple) and len(status) > 1 else status
        return str(status).lower() == qdrant_models.UpdateStatus.COMPLETED.value.lower()

    def create_multi(
            self,
            client: QdrantClient,
            *,
            payloads_and_vectors: List[Tuple[str, ModelType, VectorModelType]],
            **kwargs
    ) -> bool:

        points: List[qdrant_models.PointStruct] = [
            qdrant_models.PointStruct(
                id=_id,
                vector=vector.model_dump(exclude_none=True, exclude_unset=True),
                payload=payload.model_dump(),
            )
            for _id, payload, vector in payloads_and_vectors
        ]

        _, status = client.upsert(
            collection_name=self.collection,
            points=points,
            **kwargs
        )
        status = status[1] if isinstance(status, tuple) and len(status) > 1 else status
        return str(status).lower() == qdrant_models.UpdateStatus.COMPLETED.value.lower()

    def delete(
            self,
            client: QdrantClient,
            *,
            _id: qdrant_types.PointId,
            **kwargs
    ) -> bool:
        update_result: qdrant_types.UpdateResult = client.delete(
            self.collection,
            points_selector=[_id],
            **kwargs
        )
        return self.__is_result_success(update_result)

    def delete_multi(self, client: QdrantClient, *, query: QueryBase, **kwargs):
        query: dict = query.model_dump(exclude_none=True, exclude_unset=True, exclude_defaults=True)
        filters_exist = "filters" in query and query["filters"] is not None
        ids_exist = "ids" in query and query["ids"] is not None
        assert filters_exist or ids_exist, "you must set query.ids or query.filters to delete_multi in qdrant"

        if ids_exist:
            points_selector = qdrant_models.PointIdsList(points=query["ids"])
        elif filters_exist:
            points_selector = qdrant_models.FilterSelector(filter=query["filters"])
        else:
            raise Exception("you must set query.ids or query.filters to delete_multi in qdrant")

        update_result: qdrant_types.UpdateResult = client.delete(
            self.collection,
            points_selector=points_selector,
            **kwargs
        )
        return self.__is_result_success(update_result)

    def update_payload(self, client: QdrantClient, *, _id: qdrant_types.PointId, payload: ModelType, **kwargs):
        """Set Payload key value, not completely override entire payload object"""
        old_payload = self.first_by_id(client, _id=_id)
        if old_payload is not None:
            obj_dict = old_payload.model_dump()
            obj_dict.update(payload.model_dump())
            res = client.set_payload(
                collection_name=self.collection,
                payload=self.model(**obj_dict).model_dump(),
                points=[_id],
                **kwargs
            )
            return self.__is_result_success(res)
        return False

    def overwrite_payload(self, client: QdrantClient, *, _id: qdrant_types.PointId, payload: ModelType, **kwargs):
        """Completely override entire payload object, replace entire old payload"""
        res = client.overwrite_payload(
            collection_name=self.collection,
            payload=payload.model_dump(),
            points=[_id],
            **kwargs
        )
        return self.__is_result_success(res)

    def update_vector(self, client: QdrantClient, *, _id: qdrant_types.PointId, vector: VectorModelType,
                      **kwargs) -> bool:
        res = client.update_vectors(
            collection_name=self.collection,
            points=[
                qdrant_models.PointVectors(
                    id=_id,
                    vector=vector.model_dump(exclude_none=True, exclude_unset=True)
                )
            ],
            **kwargs
        )
        return self.__is_result_success(res)