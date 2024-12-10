from .config import BYTERAT_URL
from .queries import GET_OBSERVATION_DATA, GET_DATASET_CYCLE_DATA, GET_METADATA
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.requests import RequestsHTTPTransport
import pandas as pd
from typing import Optional, List
import asyncio
import json


class ByteratData:
    def __init__(self, data: List[str], continuation_token: Optional[str]) -> None:
        self.data = pd.DataFrame([json.loads(entry) for entry in data])
        self.continuation_token = continuation_token


class ByteratClientAsync:
    def __init__(self, token: str) -> None:
        self.token = token
        self.transport = AIOHTTPTransport(BYTERAT_URL, headers={"Authorization": token})
        self.client = Client(transport=self.transport, fetch_schema_from_transport=True)

    async def get_observation_metrics(
        self, continuation_token: Optional[str] = None
    ) -> ByteratData:
        query = gql()

        async with self.client as session:
            response = await session.execute(
                query, variable_values={"continuation_token": continuation_token}
            )

        # Extract data and continuation token
        data = response["get_observation_data"]["data"]
        continuation_token = response["get_observation_data"].get("continuation_token")

        # Convert to DataFrame and return
        return ByteratData(data, continuation_token)

    async def get_observation_metrics_by_dataset_key(
        self, dataset_key: str, continuation_token: Optional[str] = None
    ) -> ByteratData:
        query = gql(GET_OBSERVATION_DATA)

        async with self.client as session:
            response = await session.execute(
                query,
                variable_values={
                    "dataset_key": dataset_key,
                    "continuation_token": continuation_token,
                },
            )

        # Extract data and continuation token
        data = response["get_observation_data"]["data"]
        continuation_token = response["get_observation_data"].get("continuation_token")

        # Convert to DataFrame and return
        return ByteratData(data, continuation_token)

    async def get_observation_metrics_by_dataset_key_and_dataset_cycle(
        self, dataset_key: str, dataset_cycle: int, continuation_token: Optional[str] = None
    ) -> ByteratData:
        query = gql(GET_OBSERVATION_DATA)

        async with self.client as session:
            response = await session.execute(
                query, variable_values={"dataset_key": dataset_key, "dataset_cycle": dataset_cycle}
            )

        # Extract data and continuation token
        data = response["get_observation_data"]["data"]
        continuation_token = response["get_observation_data"].get("continuation_token")

        # Convert to DataFrame and return
        return ByteratData(data, continuation_token)

    async def get_observation_metrics_by_filename(
        self, file_name: str, continuation_token: Optional[str] = None
    ) -> ByteratData:
        query = gql(GET_OBSERVATION_DATA)

        async with self.client as session:
            response = await session.execute(query, variable_values={"file_name": file_name})

        # Extract data and continuation token
        data = response["get_observation_data"]["data"]
        continuation_token = response["get_observation_data"].get("continuation_token")

        # Convert to DataFrame and return
        return ByteratData(data, continuation_token)

    async def get_metadata(self, continuation_token: Optional[str] = None) -> ByteratData:
        query = gql(GET_METADATA)

        async with self.client as session:
            response = await session.execute(
                query, variable_values={"continuation_token": continuation_token}
            )

        data = response["get_metadata"]["data"]
        continuation_token = response["get_metadata"].get("continuation_token")

        return ByteratData(data, continuation_token)

    async def get_metadata_by_dataset_key(
        self, dataset_key: str, continuation_token: Optional[str] = None
    ) -> ByteratData:
        query = gql(GET_METADATA)

        async with self.client as session:
            response = await session.execute(
                query,
                variable_values={
                    "dataset_key": dataset_key,
                    "continuation_token": continuation_token,
                },
            )

        data = response["get_metadata"]["data"]
        continuation_token = response["get_metadata"].get("continuation_token")

        return ByteratData(data, continuation_token)

    async def get_dataset_cycle_data(self, continuation_token: Optional[str] = None) -> ByteratData:
        query = gql(GET_DATASET_CYCLE_DATA)

        async with self.client as session:
            response = await session.execute(
                query,
                variable_values={
                    "continuation_token": continuation_token,
                },
            )

        data = response["get_dataset_cycle_data"]["data"]
        continuation_token = response["get_dataset_cycle_data"].get("continuation_token")

        return ByteratData(data, continuation_token)

    async def get_dataset_cycle_data_by_dataset_key(
        self, dataset_key: str, continuation_token: Optional[str] = None
    ) -> ByteratData:
        query = gql(GET_DATASET_CYCLE_DATA)

        async with self.client as session:
            response = await session.execute(
                query,
                variable_values={
                    "dataset_key": dataset_key,
                    "continuation_token": continuation_token,
                },
            )

        data = response["get_dataset_cycle_data"]["data"]
        continuation_token = response["get_dataset_cycle_data"].get("continuation_token")

        return ByteratData(data, continuation_token)

    async def get_dataset_cycle_data_by_dataset_key_and_dataset_cycle(
        self, dataset_key: str, dataset_cycle: int, continuation_token: Optional[str] = None
    ) -> ByteratData:
        query = gql(GET_DATASET_CYCLE_DATA)

        async with self.client as session:
            response = await session.execute(
                query,
                variable_values={
                    "dataset_key": dataset_key,
                    "dataset_cycle": dataset_cycle,
                    "continuation_token": continuation_token,
                },
            )

        data = response["get_dataset_cycle_data"]["data"]
        continuation_token = response["get_dataset_cycle_data"].get("continuation_token")

        return ByteratData(data, continuation_token)

    async def get_dataset_cycle_data_by_filename(
        self, file_name: str, continuation_token: Optional[str] = None
    ) -> ByteratData:
        query = gql(GET_DATASET_CYCLE_DATA)

        async with self.client as session:
            response = await session.execute(
                query,
                variable_values={
                    "file_name": file_name,
                    "continuation_token": continuation_token,
                },
            )

        data = response["get_dataset_cycle_data"]["data"]
        continuation_token = response["get_dataset_cycle_data"].get("continuation_token")

        return ByteratData(data, continuation_token)


class ByteratClientSync:
    def __init__(self, token: str) -> None:
        self.token = token
        self.transport = RequestsHTTPTransport(
            url=BYTERAT_URL,
            headers={"Authorization": token},
            verify=True,
            retries=3,
        )
        self.client = Client(transport=self.transport, fetch_schema_from_transport=True)

    def __get_observation_metrics(
        self,
        continuation_token: Optional[str] = None,
        dataset_key: Optional[str] = None,
        dataset_cycle: Optional[str] = None,
        file_name: Optional[str] = None,
    ) -> ByteratData:
        query = gql(GET_OBSERVATION_DATA)

        resp = self.client.execute(
            query,
            variable_values={
                "continuation_token": continuation_token,
                "dataset_key": dataset_key,
                "dataset_cycle": dataset_cycle,
                "file_name": file_name,
            },
        )

        data = resp["get_observation_data"]["data"]
        continuation_token = resp["get_observation_data"].get("continuation_token")
        return ByteratData(data, continuation_token)

    def get_observation_metrics(self, continuation_token: Optional[str] = None) -> ByteratData:
        query = gql(GET_OBSERVATION_DATA)

        resp = self.client.execute(
            query,
            variable_values={
                "continuation_token": continuation_token,
            },
        )

        data = resp["get_observation_data"]["data"]
        continuation_token = resp["get_observation_data"].get("continuation_token")
        return ByteratData(data, continuation_token)

    def get_observation_metrics_by_dataset_key(
        self, dataset_key: str, continuation_token: Optional[str] = None
    ) -> ByteratData:
        return self.__get_observation_metrics(
            continuation_token=continuation_token,
            dataset_key=dataset_key,
        )

    def get_observation_metrics_by_dataset_key_and_dataset_cycle(
        self, dataset_key: str, dataset_cycle: int, continuation_token: Optional[str] = None
    ) -> ByteratData:
        return self.__get_observation_metrics(
            continuation_token=continuation_token,
            dataset_key=dataset_key,
            dataset_cycle=dataset_cycle,
        )

    def get_observation_metrics_by_filename(
        self, file_name: str, continuation_token: Optional[str] = None
    ) -> ByteratData:
        query = gql(GET_OBSERVATION_DATA)

        resp = self.client.execute(
            query,
            variable_values={
                "continuation_token": continuation_token,
                "file_name": file_name,
            },
        )

        data = resp["get_observation_data"]["data"]
        continuation_token = resp["get_observation_data"].get("continuation_token")
        return ByteratData(data, continuation_token)

    def __get_dataset_cycle_metrics(
        self,
        continuation_token: Optional[str] = None,
        dataset_key: Optional[str] = None,
        dataset_cycle: Optional[str] = None,
        file_name: Optional[str] = None,
    ) -> ByteratData:
        query = gql(GET_DATASET_CYCLE_DATA)

        resp = self.client.execute(
            query,
            variable_values={
                "continuation_token": continuation_token,
                "dataset_key": dataset_key,
                "dataset_cycle": dataset_cycle,
                "file_name": file_name,
            },
        )

        data = resp["get_dataset_cycle_data"]["data"]
        continuation_token = resp["get_dataset_cycle_data"].get("continuation_token")
        return ByteratData(data, continuation_token)

    def get_dataset_cycle_data(self, continuation_token: Optional[str] = None) -> ByteratData:
        query = gql(GET_DATASET_CYCLE_DATA)

        resp = self.client.execute(
            query,
            variable_values={
                "continuation_token": continuation_token,
            },
        )

        data = resp["get_dataset_cycle_data"]["data"]
        continuation_token = resp["get_dataset_cycle_data"].get("continuation_token")
        return ByteratData(data, continuation_token)

    def get_dataset_cycle_data_by_dataset_key(
        self, dataset_key: str, continuation_token: Optional[str] = None
    ) -> ByteratData:
        return self.__get_dataset_cycle_metrics(
            continuation_token=continuation_token,
            dataset_key=dataset_key,
        )

    def get_dataset_cycle_data_by_dataset_key_and_dataset_cycle(
        self, dataset_key: str, dataset_cycle: int, continuation_token: Optional[str] = None
    ) -> ByteratData:
        return self.__get_dataset_cycle_metrics(
            continuation_token=continuation_token,
            dataset_key=dataset_key,
            dataset_cycle=dataset_cycle,
        )

    def get_dataset_cycle_data_by_filename(
        self, file_name: str, continuation_token: Optional[str] = None
    ) -> ByteratData:
        query = gql(GET_DATASET_CYCLE_DATA)

        resp = self.client.execute(
            query,
            variable_values={
                "continuation_token": continuation_token,
                "file_name": file_name,
            },
        )

        data = resp["get_dataset_cycle_data"]["data"]
        continuation_token = resp["get_dataset_cycle_data"].get("continuation_token")
        return ByteratData(data, continuation_token)

    def __get_metadata(
        self,
        continuation_token: Optional[str] = None,
        dataset_key: Optional[str] = None,
    ) -> ByteratData:
        query = gql(GET_METADATA)

        resp = self.client.execute(
            query,
            variable_values={
                "continuation_token": continuation_token,
                "dataset_key": dataset_key,
            },
        )

        data = resp["get_metadata"]["data"]
        continuation_token = resp["get_metadata"].get("continuation_token")
        return ByteratData(data, continuation_token)

    def get_metadata(self, continuation_token: Optional[str] = None) -> ByteratData:
        return self.__get_metadata(continuation_token=continuation_token)

    def get_metadata_by_dataset_key(
        self, dataset_key: str, continuation_token: Optional[str] = None
    ) -> ByteratData:
        return self.__get_metadata(continuation_token=continuation_token, dataset_key=dataset_key)
