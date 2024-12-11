from abc import ABC, abstractmethod

from injector import inject

from griff.infra.persistence.persistence import (
    Persistence,
    QueryRowResult,
    QueryResult,
    QueryRowResults,
    Id,
)
from griff.infra.persistence.serialized_persistence import SerializedPersistence
from griff.services.json.json_service import JsonService
from griff.services.query_runner.query_runner_service import QueryRunnerService


class DbPersistence(Persistence, ABC):
    @inject
    def __init__(self, query_runner_service: QueryRunnerService):
        super().__init__()
        self._query_runner_service = query_runner_service
        self._query_runner_service.set_sql_queries(
            self._get_relative_sql_queries_path()
        )

    async def _insert(self, data: dict) -> None:
        await self._run_query(query_name="insert", **data)

    async def _update(self, data: dict) -> None:
        await self._run_query(query_name="update", **data)

    async def _delete(self, persistence_id: Id) -> None:
        await self._run_query(
            query_name="delete", **self._get_pk_from_persistence_id(persistence_id)
        )

    async def _get_by_id(self, persistence_id: Id) -> QueryRowResult:
        return await self._run_get_query(
            query_name="get_by_id", **self._get_pk_from_persistence_id(persistence_id)
        )

    async def _list_all(self) -> QueryRowResults:
        return await self._run_query(query_name="list_all")  # type: ignore

    async def _run_query(self, query_name, **query_params) -> QueryResult:
        return await self._query_runner_service.run_query(query_name, **query_params)

    async def _run_get_query(self, query_name, **query_params) -> QueryRowResult:
        return await self._query_runner_service.run_query(query_name, **query_params)

    @abstractmethod
    def _get_relative_sql_queries_path(self) -> str:  # pragma: no cover
        pass


class SerializedDbPersistence(
    SerializedPersistence, DbPersistence, ABC
):  # pragma: no cover
    @inject
    def __init__(
        self, query_runner_service: QueryRunnerService, json_service: JsonService
    ):
        SerializedPersistence.__init__(self, json_service)
        DbPersistence.__init__(self, query_runner_service)
