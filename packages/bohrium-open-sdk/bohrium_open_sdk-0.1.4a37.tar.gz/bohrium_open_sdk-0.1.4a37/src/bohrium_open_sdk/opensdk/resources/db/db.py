# -*- coding: UTF-8 -*-

from typing import Optional, Tuple, List

from bohrium_open_sdk.opensdk._resource import SyncAPIResource
from bohrium_open_sdk.opensdk._response import APIResponse


class AppDB(SyncAPIResource):

    def __init__(self, _client) -> None:
        super().__init__(_client)

    def insert(self, data) -> List:
        response = self._client.post("/openapi/v1/db/app/data/insert", json=data)
        data: dict = APIResponse(response).json
        if data.get("code", None) != 0:
            raise Exception(f"insert failed: {data}")

        return data["data"]["ids"]

    def delete(self, data) -> int:
        response = self._client.delete("/openapi/v1/db/app/data", json=data)
        data: dict = APIResponse(response).json
        if data.get("code", None) != 0:
            raise Exception(f"insert failed: {data}")

        return data["data"]["deletedCount"]

    def update(self, data) -> Tuple[int, Optional[str]]:
        response = self._client.post("/openapi/v1/db/app/data/update", json=data)
        data: dict = APIResponse(response).json
        if data.get("code", None) != 0:
            raise Exception(f"insert failed: {data}")

        return data["data"]["modifyCount"], data["data"]["result"] or None

    def query(self, data) -> Tuple[int, List]:
        response = self._client.post("/openapi/v1/db/app/data/list", json=data)
        data: dict = APIResponse(response).json
        if data.get("code", None) != 0:
            raise Exception(f"insert failed: {data}")

        return data["data"]["count"], data["data"]["list"] or []

    def count(self, data) -> int:
        response = self._client.post("/openapi/v1/db/app/data/count", json=data)
        data: dict = APIResponse(response).json
        if data.get("code", None) != 0:
            raise Exception(f"insert failed: {data}")

        return data["data"]["count"]

    def create_table(self, data) -> str:
        response = self._client.post("/openapi/v1/db/app/table/create", json=data)
        data: dict = APIResponse(response).json
        if data.get("code", None) != 0:
            raise Exception(f"insert failed: {data}")

        return data["data"]["tableId"]

    def delete_table(self, data) -> bool:
        response = self._client.delete("/openapi/v1/db/app/table", json=data)
        data: dict = APIResponse(response).json
        if data.get("code", None) != 0:
            raise Exception(f"insert failed: {data}")
        return data["data"]["result"]

    def get_common_db_file_token(self, file_name: str = ""):
        url = f"/openapi/v1/db/app/file/token?fileName={file_name}"
        response = self._client.get(url)
        if response.status_code != 200:
            raise Exception(f"get upload token failed: {response.text}")
        return APIResponse(response).json
