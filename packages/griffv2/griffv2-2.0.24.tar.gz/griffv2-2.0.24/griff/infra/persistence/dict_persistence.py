import copy
from typing import Dict, List, Callable, Any

from griff.infra.persistence.persistence import (
    Persistence,
    QueryRowResult,
    QueryResult,
    QueryRowResults,
    Id,
    IdName,
    IdValue,
)
from griff.infra.persistence.serialized_persistence import SerializedPersistence
from griff.services.json.json_service import JsonService

QueryName = str
QueryCallable = Callable[..., QueryResult]


def _has_filters_match(data: Dict[str, Dict], filters: Dict[str, Any]) -> bool:
    for attr, value in filters.items():
        if data.get(attr) != value:
            return False
    return True


class DictPersistence(Persistence):
    _pk: List[IdName] = ["entity_id"]

    def __init__(self, initial_data: List[Dict] | None = None):
        self._internal_storage: List = []
        self.reset(initial_data)

    async def _insert(self, data: dict) -> None:
        idx = self._search_idx_from_data(data)
        if idx is None:
            self._internal_storage.append(data)
            return None
        pk = self._get_pk_from_data(data)
        raise ValueError(f"id '{self._pk_str(pk)}' already exists")

    async def _update(self, data: dict) -> None:
        idx = self._search_idx_from_data(data)
        if idx is not None:
            self._internal_storage[idx] = data
            return None
        pk = self._get_pk_from_data(data)
        raise ValueError(f"id '{self._pk_str(pk)}' does not exists")

    async def _delete(self, persistence_id: Id) -> None:
        idx = self._search_idx_from_persistence_id(persistence_id)
        if idx is not None:
            self._internal_storage.pop(idx)
            return None
        pk = self._get_pk_from_persistence_id(persistence_id)
        raise ValueError(f"id '{self._pk_str(pk)}' does not exists")

    async def _get_by_id(self, persistence_id: Id) -> QueryRowResult:
        idx = self._search_idx_from_persistence_id(persistence_id)
        if idx is not None:
            return copy.deepcopy(self._internal_storage[idx])
        pk = self._get_pk_from_persistence_id(persistence_id)
        raise ValueError(f"id '{self._pk_str(pk)}' not found")

    async def _list_all(self) -> QueryRowResults:
        return copy.deepcopy(list(self._internal_storage))

    async def _run_query(self, query_name: str, **query_params) -> QueryResult:
        if self._has_custom_queries(query_name):
            return self._run_custom_queries(query_name, **query_params)
        if "list_all" == query_name:
            return copy.deepcopy(list(self._internal_storage))
        if "get_by_" in query_name:
            return self._get_by_attrs(**query_params)
        if "list_by_" in query_name:
            return self._list_by_attrs(**query_params)
        raise RuntimeError(f"Query {query_name} not found")

    def reset(self, initial_data: List[Dict] | None = None):
        if initial_data is None:
            self._internal_storage = []
            return None
        self._internal_storage = [
            self._prepare_to_save(r) for r in copy.deepcopy(initial_data)
        ]

    @property
    def _queries(self) -> Dict[QueryName, QueryCallable]:
        return {}

    def _has_custom_queries(self, query_name: str) -> bool:
        return query_name in self._queries

    def _run_custom_queries(self, query_name: str, **query_params):
        return self._queries[query_name](**query_params)

    def _searchable_internal_storage(self) -> List:
        if self._internal_storage:
            return self._prepare_row_results(
                [copy.deepcopy(r) for r in self._internal_storage]
            )
        return self._internal_storage  # pragma: no cover

    def _get_by_attrs(
        self, filtering_callable: Callable = _has_filters_match, **query_params
    ):
        for idx, e in enumerate(self._searchable_internal_storage()):
            if filtering_callable(e, query_params):
                return self._internal_storage[idx]
        return None

    def _list_by_attrs(
        self, filtering_callable: Callable = _has_filters_match, **query_params
    ):
        result = []
        for idx, e in enumerate(self._searchable_internal_storage()):
            if filtering_callable(e, query_params):
                result.append(self._internal_storage[idx])
        return result

    def _search_idx_from_data(self, data: Dict):
        pk = self._get_pk_from_data(data)
        return self._search_idx_from_pk(pk)

    def _search_idx_from_persistence_id(self, persistence_id: Id):
        pk = self._get_pk_from_persistence_id(persistence_id)
        return self._search_idx_from_pk(pk)

    def _search_idx_from_pk(self, pk: Dict[IdName, IdValue]):
        for idx, r in enumerate(self._internal_storage):
            if self._row_has_pk(r, pk):
                return idx
        return None

    @staticmethod
    def _row_has_pk(r, id):
        for k, v in id.items():
            if r.get(k) != v:
                return False
        return True

    @staticmethod
    def _pk_str(pk: Dict[IdName, IdValue]) -> str:
        ids_txt = [f"{k}={v}" for k, v in pk.items()]
        return ", ".join(ids_txt)


class SerializedDictPersistence(SerializedPersistence, DictPersistence):
    def __init__(self, initial_data: List[Dict] | None = None):
        SerializedPersistence.__init__(self, JsonService())
        DictPersistence.__init__(self, initial_data)
