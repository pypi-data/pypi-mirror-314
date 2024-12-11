from ..schemas import QueryBase
from typing import Optional, Literal


def cleanse_query_for_search(query: Optional[QueryBase], offset_type: Literal["int", "str"] = "int") -> dict:
    if offset_type == "int":
        assert query.offset is None or isinstance(query.offset, int), "Offset must be int in Qdrant searching"
    elif offset_type == "str":
        assert query.offset is None or isinstance(query.offset, str), "Offset must be id (str) in Qdrant querying"
    assert query.id is None, "QueryBase's 'id' key should not being use for similarity search in qdrant"
    assert query.ids is None, "QueryBase's 'ids' key should not being use for similarity search in qdrant"
    assert query.order_by is None, "QueryBase's 'order_by' key should not being use for similarity search in qdrant"
    assert query.filters is None or isinstance(query.filters, dict), "Query.filters only accept dict of qdrant query"

    if query is None: return {}
    base = query.filters if query.filters is not None else {}

    # forbidden id and ids in filters
    if "id" in base: raise AssertionError(
        f"You should not include 'id' in your QueryBase.filters when searching Qdrant")
    if "ids" in base: raise AssertionError(
        f"You should not include 'ids' in your QueryBase.filters when searching Qdrant")
    return base
