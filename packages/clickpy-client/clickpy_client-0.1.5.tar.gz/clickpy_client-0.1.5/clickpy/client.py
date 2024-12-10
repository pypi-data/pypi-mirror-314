import logging
import re
from contextlib import asynccontextmanager
from typing import Any, Optional, get_origin

import httpx
from pydantic import BaseModel, TypeAdapter

from clickpy.queries.base import BaseClickPyQuery, TModel
from clickpy.queries.keyword_downloads_resume_query import KeywordDownloadsResumeQuery
from clickpy.queries.keyword_packages_resume_query import KeywordPackagesResumeQuery
from clickpy.queries.keyword_releases_resume_query import KeywordReleasesResumeQuery
from clickpy.queries.keywords_by_releases_query import KeywordsByReleasesQuery
from clickpy.queries.package_downloads_resume_query import PackageDownloadsResumeQuery
from clickpy.queries.package_releases_resume_query import PackageReleasesResumeQuery
from clickpy.queries.tables_query import TablesQuery
from clickpy.settings import CLICK_PY_DATA_BASE_SETTING

logger = logging.getLogger('clickpy')


class ClickHouseResponse(BaseModel):
    class ClickHouseStatisticsResponse(BaseModel):
        elapsed: float
        rows_read: int
        bytes_read: int

    meta: list[dict[str, str]]
    rows: int
    statistics: ClickHouseStatisticsResponse
    data: Any


class ClickPyClient(object):
    def __init__(self) -> None:
        self.http_client = httpx.AsyncClient()

    @asynccontextmanager
    async def lifespan(self, *args: Any, **kwargs: Any):
        yield
        await self.http_client.aclose()

    async def query(self, method: BaseClickPyQuery[TModel]) -> TModel:
        query = method.query()
        query = re.sub(r'\s+', ' ', query).strip()

        http_response = await self.http_client.post(
            CLICK_PY_DATA_BASE_SETTING.HOST,
            auth=(CLICK_PY_DATA_BASE_SETTING.USERNAME, CLICK_PY_DATA_BASE_SETTING.PASSWORD),
            headers={'Content-Type': 'application/json'},
            params={
                'default_format': 'JSON',
                'query': query,
            },
        )

        try:
            http_response.raise_for_status()

        except Exception as ex:  # pragma: no cover
            raise RuntimeError(f'Error: {http_response.text}') from ex

        response = ClickHouseResponse.model_validate_json(http_response.content)

        logger.info(
            'Query: "%s"; Elapsed: %s; Rows: %s; Rows_read: %s; Bytes_read: %s',
            query,
            response.rows,
            response.statistics.elapsed,
            response.statistics.rows_read,
            response.statistics.bytes_read,
            extra={
                'query': query,
                'rows': response.rows,
                'elapsed': response.statistics.elapsed,
                'rows_read': response.statistics.rows_read,
                'bytes_read': response.statistics.bytes_read,
            },
        )

        if get_origin(method.Model) is list:
            return TypeAdapter(method.Model).validate_python(response.data)

        return TypeAdapter(method.Model).validate_python(response.data[0])

    async def get_tables(self, databases: Optional[list[str]] = None) -> TablesQuery.Model:
        if databases is None:
            databases = ['github', 'pypi']

        return await self.query(TablesQuery(databases=databases))

    async def get_keywords_by_releases(self, *args: Any, **kwargs: Any) -> KeywordsByReleasesQuery.Model:
        return await self.query(KeywordsByReleasesQuery(*args, **kwargs))

    async def get_package_downloads_resume(self, package: str) -> PackageDownloadsResumeQuery.Model:
        return await self.query(PackageDownloadsResumeQuery(package=package))

    async def get_package_releases_resume(self, package: str) -> PackageReleasesResumeQuery.Model:
        return await self.query(PackageReleasesResumeQuery(package=package))

    async def get_keyword_releases_resume(self, keyword: str) -> KeywordReleasesResumeQuery.Model:
        return await self.query(KeywordReleasesResumeQuery(keyword=keyword))

    async def get_keyword_packages_resume(self, keyword: str) -> KeywordPackagesResumeQuery.Model:
        return await self.query(KeywordPackagesResumeQuery(keyword=keyword))

    async def get_keyword_downloads_resume(self, keyword: str) -> KeywordDownloadsResumeQuery.Model:
        return await self.query(KeywordDownloadsResumeQuery(keyword=keyword))
