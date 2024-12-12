from typing import List, Optional, Dict, Union
import httpx
import requests
import io
from loguru import logger
from tgshops_integrations.nocodb_connector.model_mapping import ID_FIELD


def custom_key_builder(func, *args, **kwargs) -> str:
    """
    Custom key builder for caching.
    Excludes 'self' by starting args processing from args[1:].
    """
    args_key_part = "-".join(str(arg) for arg in args[1:])
    kwargs_key_part = "-".join(f"{key}-{value}" for key, value in sorted(kwargs.items()))
    return f"{func.__name__}-{args_key_part}-{kwargs_key_part}"


class NocodbClient:
    def __init__(self, NOCODB_HOST: Optional[str] = None, NOCODB_API_KEY: Optional[str] = None, SOURCE: Optional[str] = None):
        self.NOCODB_HOST = NOCODB_HOST
        self.NOCODB_API_KEY = NOCODB_API_KEY
        self.SOURCE = SOURCE
        self.httpx_client = httpx.AsyncClient(timeout=60.0)
        self.httpx_client.headers = {"xc-token": self.NOCODB_API_KEY}

    def construct_get_params(
        self,
        required_fields: Optional[List[str]] = None,
        projection: Optional[List[str]] = None,
        extra_where: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None
    ) -> Dict[str, Union[str, int]]:
        """
        Constructs GET parameters for API requests.
        """
        params = {}
        if projection:
            params["fields"] = ','.join(projection)
        if required_fields:
            params["where"] = "~and".join(f"({field},isnot,null)" for field in required_fields)
        if extra_where:
            params["where"] = f"{params.get('where', '')}~and{extra_where}" if params.get("where") else extra_where
        if offset is not None:
            params["offset"] = offset
        if limit is not None:
            params["limit"] = limit
        return params

    async def get_table_records(
        self,
        table_name: str,
        required_fields: Optional[List[str]] = None,
        projection: Optional[List[str]] = None,
        extra_where: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[dict]:
        """
        Fetches records from a specified table.
        """
        url = f"{self.NOCODB_HOST}/tables/{table_name}/records"
        params = self.construct_get_params(required_fields, projection, extra_where, limit=limit)
        response = await self.httpx_client.get(url, params=params)
        if response.status_code == 200:
            return response.json().get("list", [])
        logger.error(f"Error fetching records: {response.text}")
        raise Exception(response.text)
    
    async def get_table_records_v2(self,
                                   table_name: str,
                                   required_fields: list = None,
                                   projection: list = None,
                                   extra_where: str = None,
                                   offset: int = None,
                                   limit: int = 25) -> dict:
        url = f"{self.NOCODB_HOST}/tables/{table_name}/records"
        extra_params = self.construct_get_params(required_fields, projection, extra_where, offset=offset, limit=limit)
        response = await self.httpx_client.get(url, params=extra_params)
        if response.status_code == 200:
            return response.json()
        raise Exception(response.text)

    async def get_table_record(self,
                               table_name: str,
                               record_id: str,
                               required_fields: list = None,
                               projection: list = None) -> dict:
        url = f"{self.NOCODB_HOST}/tables/{table_name}/records/{record_id}"
        extra_params = self.construct_get_params(required_fields, projection)
        response = await self.httpx_client.get(url, params=extra_params)
        if response.status_code == 200:
            return response.json()
        raise Exception(response.text)

    async def create_table_record(self, table_name: str, record: dict) -> dict:
        """
        Creates a new record in a table.
        """
        url = f"{self.NOCODB_HOST}/tables/{table_name}/records"
        response = await self.httpx_client.post(url, json=record)
        if response.status_code == 200:
            record["id"] = response.json().get("id") or response.json().get("Id")
            return record
        logger.error(f"Error creating record: {response.text}")
        raise Exception(response.text)

    async def delete_table_record(self, table_name: str, record_id: str) -> dict:
        """
        Deletes a record from a specified table.
        """
        url = f"{self.NOCODB_HOST}/tables/{table_name}/records"
        response = requests.delete(url, json={"Id": record_id}, headers=self.httpx_client.headers)
        if response.status_code == 200:
            logger.info(f"Deleted record {record_id}")
            return response.json()
        logger.error(f"Error deleting record: {response.text}")
        raise Exception(response.text)

    async def get_product_categories(self, table_id: str, table_name: str) -> Dict[str, str]:
        """
        Fetches product categories from a specified table.
        """
        url = f"{self.NOCODB_HOST}/tables/{table_id}/records"
        params = self.construct_get_params(limit=75)
        response = await self.httpx_client.get(url, params=params)
        if response.status_code == 200:
            return {category[table_name]: category["Id"] for category in response.json().get("list", [])}
        logger.error(f"Error fetching categories: {response.text}")
        raise Exception(response.text)

    async def create_product_category(
        self, table_id: str, category_name: str, table_name: str, category_id: int = 0
    ) -> dict:
        """
        Creates a new product category in a specified table.
        """
        url = f"{self.NOCODB_HOST}/tables/{table_id}/records"
        record = {table_name: category_name, "Id": category_id}
        response = await self.httpx_client.post(url, json=record)
        if response.status_code == 200:
            return record
        logger.error(f"Error creating product category: {response.text}")
        raise Exception(response.text)

    async def get_table_meta(self, table_name: str) -> dict:
        """
        Fetches metadata of a table.
        """
        url = f"{self.NOCODB_HOST.replace('/api/v2', '/api/v1')}/db/meta/tables/{table_name}"
        response = await self.httpx_client.get(url)
        if response.status_code == 200:
            return response.json()
        logger.error(f"Error fetching table metadata: {response.text}")
        raise Exception(response.text)

    async def get_all_tables(self, source: Optional[str] = None) -> Dict[str, str]:
        """
        Fetches all tables from the specified project source.
        """
        source = source or self.SOURCE
        url = f"{self.NOCODB_HOST.replace('/api/v2', '/api/v1')}/db/meta/projects/{source}/tables?includeM2M=false"
        response = await self.httpx_client.get(url)
        if response.status_code == 200:
            tables_info = response.json().get('list', [])
            self.tables_list = {table["title"]: table["id"] for table in tables_info}
            return self.tables_list
        logger.error(f"Failed to fetch tables: {response.text}")
        raise Exception(response.text)

    async def get_sources(self) -> list:
        """
        Fetches all project sources.
        """
        url = f"{self.NOCODB_HOST.replace('/api/v2', '/api/v1')}/db/meta/projects/"
        response = await self.httpx_client.get(url)
        if response.status_code == 200:
            return response.json().get('list', [])
        logger.error(f"Failed to fetch sources: {response.text}")
        raise Exception(response.text)

    async def get_table_meta(self, table_name: str) -> dict:
        """
        Fetches metadata of a specified table.
        """
        url = f"{self.NOCODB_HOST.replace('/api/v2', '/api/v1')}/db/meta/tables/{table_name}"
        response = await self.httpx_client.get(url)
        if response.status_code == 200:
            return response.json()
        logger.error(f"Failed to fetch table metadata: {response.text}")
        raise Exception(response.text)

    async def create_table_column(self, table_name: str, name: str) -> dict:
        """
        Creates a new column in the specified table.
        """
        url = f"{self.NOCODB_HOST.replace('/api/v2', '/api/v1')}/db/meta/tables/{table_name}/columns"
        payload = {
            "column_name": name,
            "dt": "character varying",
            "dtx": "specificType",
            "ct": "varchar(45)",
            "clen": 45,
            "dtxp": "45",
            "dtxs": "",
            "altered": 1,
            "uidt": "SingleLineText",
            "uip": "",
            "uicn": "",
            "title": name
        }
        response = await self.httpx_client.post(url, json=payload)
        if response.status_code == 200:
            return response.json()
        logger.error(f"Failed to create table column: {response.text}")
        raise Exception(response.text)

    async def link_table_record(
        self,
        base_id: str,
        fk_model_id: str,
        record_id: str,
        source_column_id: str,
        linked_record_id: str
    ) -> dict:
        """
        Links a record to another record in a many-to-many relationship.
        """
        url = f"{self.NOCODB_HOST.replace('/api/v2', '/api/v1')}/db/data/noco/{base_id}/{fk_model_id}/{record_id}/mm/{source_column_id}/{linked_record_id}"
        response = await self.httpx_client.post(url, headers=self.httpx_client.headers)
        if response.status_code == 200:
            return response.json()
        logger.error(f"Failed to link table record: {response.text}")
        raise Exception(response.text)

    async def unlink_table_record(
        self,
        base_id: str,
        fk_model_id: str,
        record_id: str,
        source_column_id: str,
        linked_record_id: str
    ) -> dict:
        """
        Unlinks a record from another record in a many-to-many relationship.
        """
        url = f"{self.NOCODB_HOST.replace('/api/v2', '/api/v1')}/db/data/noco/{base_id}/{fk_model_id}/{record_id}/mm/{source_column_id}/{linked_record_id}"
        response = await self.httpx_client.delete(url)
        if response.status_code == 200:
            return response.json()
        logger.error(f"Failed to unlink table record: {response.text}")
        raise Exception(response.text)

    async def save_image_to_nocodb(
        self,
        image_url: str,
        image_name: str,
        source_column_id: str,
        product_table_name: str,
        images_column_id: str
    ) -> Optional[str]:
        """
        Saves an image to NocoDB's storage.
        """
        try:
            response = requests.get(image_url)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Error loading image from URL {image_url}: {e}")
            return None

        file = io.BytesIO(response.content)
        file_size = file.getbuffer().nbytes

        if not file_size:
            logger.error(f"Image file from {image_url} is empty.")
            return None

        files = {'file': (image_name, file, 'image/jpeg')}
        url = f"{self.NOCODB_HOST.replace('/api/v2', '/api/v1')}/db/storage/upload?path=noco/{source_column_id}/{product_table_name}/{images_column_id}"
        try:
            response = await self.httpx_client.post(url, files=files, timeout=httpx.Timeout(200.0))
            if response.status_code == 200:
                return response.json()[0].get('url', None)
            logger.error(f"Error saving image {image_name}: {response.text}")
        except Exception as e:
            logger.error(f"Unexpected error saving image {image_name}: {e}")
        return None
