from typing import List, Dict
from typing import Optional, Mapping, Union

from pymongo import IndexModel
from pymongo import MongoClient
from qdrant_client import QdrantClient
from qdrant_client.http import models as qdrant_models
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant_client.http.models import PayloadSchemaType
from redis import Redis as R, ConnectionPool
from sqlalchemy import Engine
from sqlmodel import create_engine, Session

from .schemas import DbSettingsABC
import logging

logger = logging.getLogger(__name__)

class Db:

    def __init__(self, settings: DbSettingsABC):
        self.__settings = settings
        self.__redis_pool = ConnectionPool.from_url(settings.redis_uri,
                                                    decode_responses=True) if settings.redis_uri is not None else None
        self.__sql_read_engine = create_engine(
            str(settings.sql_read_uri if settings.sql_read_uri is not None else settings.sql_uri),
            pool_pre_ping=True,
            pool_size=1000,
            max_overflow=10,
            pool_recycle=3600,
            pool_use_lifo=True,
            echo=False,
        ) if settings.sql_read_uri is not None or settings.sql_uri is not None else None
        self.__sql_write_engine = create_engine(
            str(settings.sql_write_uri if settings.sql_write_uri is not None else settings.sql_uri),
            pool_pre_ping=True,
            pool_size=1000,
            max_overflow=10,

            pool_recycle=3600,
            pool_use_lifo=True,
            echo=False
        ) if settings.sql_write_uri is not None or settings.sql_uri is not None else None


        self._sql_read_instance = None
        self._sql_write_instance = None
        self._redis_instance = None
        self._mongo_instance = None
        self._qdrant_instance = None

    @property
    def sql_write_engine(self) -> Optional[Engine]:
        return self.__sql_write_engine

    @property
    def sql_read_engine(self) -> Optional[Engine]:
        return self.__sql_read_engine

    def get_redis(self, *, force_new_instance: bool = False) -> Optional[R]:
        """Return conn to redis
        You do not need to explicitly close the redis conn"""
        if self.__redis_pool is None: return None
        if force_new_instance: return R(connection_pool=self.__redis_pool)
        if not force_new_instance and self._redis_instance is not None: return self._redis_instance
        self._redis_instance = R(connection_pool=self.__redis_pool)
        return self._redis_instance

    def get_mongo(self, *, new_instance: bool = True) -> Optional[MongoClient]:
        """Return a mongo conn
        You do not need to close PyMongo connections. Leave them open so that PyMongo connection pooling gives you the most efficient performance"""
        if self.__settings.mongo_db_uri is None:
            return None

        if new_instance:
            return MongoClient(self.__settings.mongo_db_uri, uuidRepresentation="standard")

        if not new_instance:
            if self._mongo_instance and not self._mongo_instance.closed:
                return self._mongo_instance

        self._mongo_instance = MongoClient(self.__settings.mongo_db_uri, uuidRepresentation="standard")
        return self._mongo_instance

    def get_qdrant_client(self, *, new_instance: bool = True) -> Optional[QdrantClient]:
        if self.__settings.qdrant_host is None or self.__settings.qdrant_port is None: return None
        if new_instance: return QdrantClient(host=self.__settings.qdrant_host, port=self.__settings.qdrant_port, timeout=120)
        if not new_instance and  self._qdrant_instance is not None: return self._qdrant_instance
        self._qdrant_instance = QdrantClient(host=self.__settings.qdrant_host, port=self.__settings.qdrant_port, timeout=120)
        return self._qdrant_instance

    def get_sql_write_client(self, *, new_instance: bool = True) -> Optional[Session]:
        if self.sql_write_engine is None: return None
        if new_instance: return Session(self.sql_write_engine)
        if not new_instance and self._sql_write_instance is not None: return self._sql_write_instance
        self._sql_write_instance = Session(self.sql_write_engine)
        return self._sql_write_instance

    def get_sql_read_client(self, *, new_instance: bool = True) -> Optional[Session]:
        if self.sql_read_engine is None: return None
        if new_instance: return Session(self.sql_read_engine)
        if not new_instance and self._sql_read_instance is not None: return self._sql_read_instance
        self._sql_read_instance = Session(self.sql_read_engine)
        return self._sql_read_instance

    @staticmethod
    def ready_mongo(client: MongoClient):
        # check by list
        client.list_databases()


    @staticmethod
    def ready_mongo_indexes(
            client: MongoClient,
            db_name: str,
            collection_name: str,
            indexes: List[Dict[str, Union[int, str]]]
    ) -> None:
        """
        Ensure MongoDB indexes exist. Creates them if not.

        :param client: MongoClient instance
        :param db_name: Name of the MongoDB database
        :param collection_name: Name of the MongoDB collection
        :param indexes: List of dictionaries defining the index fields and their types.
                        - For normal ascending/descending indexes, use 1 (ascending) or -1 (descending).
                        - For text search indexes, use "text".
                        Example: [{"field1": 1, "field2": -1}, {"field3": "text"}]
        """
        collection = client[db_name][collection_name]
        existing_indexes = collection.index_information()

        # Create index models based on the input
        indexes_need_to_create = []
        for index in indexes:
            compound_index_key = [(field, order) for field, order in index.items()]

            # Check if the index already exists in the collection
            if not any(compound_index_key == idx.get('key') for idx in existing_indexes.values()):
                index_model = IndexModel(compound_index_key)
                indexes_need_to_create.append(index_model)
        if len(indexes_need_to_create) >0:
            collection.create_indexes(indexes_need_to_create)


    @staticmethod
    def ready_redis(redis: R):
        # check by get key
        redis.get("k")

    @staticmethod
    def ready_qdrant(client: QdrantClient, collection: str,
                     vectors_config: Union[qdrant_models.VectorParams, Mapping[str, qdrant_models.VectorParams]]):
        # need to check database exist or not
        try:
            client.get_collection(collection_name=collection)
        except (AssertionError, UnexpectedResponse) as e:
            # collection not found, or connection error. Try to create
            client.create_collection(
                collection_name=collection,
                vectors_config=vectors_config,
            )

    @staticmethod
    def ready_qdrant_indexes(
            client: QdrantClient,
            collection_name: str,
            indexes: List[Dict[str, PayloadSchemaType]]
    ) -> None:
        """
        Ensure Qdrant payload indexes exist. Creates them if not.

        :param client: QdrantClient instance
        :param collection_name: Name of the Qdrant collection
        :param indexes: List of dictionaries where keys are field names and values are their corresponding types (PayloadSchemaType).
                        Example: [{"field1": PayloadSchemaType.INTEGER}, {"field2": PayloadSchemaType.KEYWORD}]
        """
        try:
            collection_info = client.get_collection(collection_name)
            existing_indexes = collection_info.payload_schema or {}

            for index in indexes:
                for field_name, schema_type in index.items():
                    if field_name not in existing_indexes:
                        client.create_payload_index(
                            collection_name=collection_name,
                            field_name=field_name,
                            field_schema=qdrant_models.PayloadSchemaType(schema_type)
                        )
        except (AssertionError, UnexpectedResponse):
            logger.critical(f"[Db] Collection {collection_name} does not exist or failed to retrieve collection info.")

    @staticmethod
    def try_close(*sessions: Optional[MongoClient | R | Session | QdrantClient]):
        for session in sessions:
            if session is not None:
                try:
                    session.close()
                except Exception as e:
                    logger.error(f"[Db] Failed to close a db session due to {e}")
