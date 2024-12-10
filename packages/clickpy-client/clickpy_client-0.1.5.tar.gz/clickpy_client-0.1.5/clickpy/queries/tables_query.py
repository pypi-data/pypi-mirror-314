from datetime import datetime
from typing import ClassVar, Optional
from uuid import UUID

from pydantic import BaseModel

from clickpy.queries.base import BaseClickPyQuery


class TableModel(BaseModel):
    database: str
    name: str
    uuid: UUID
    engine: str
    is_temporary: int
    data_paths: list[str]
    metadata_path: str
    metadata_modification_time: datetime
    metadata_version: int
    dependencies_database: list[str]
    dependencies_table: list[str]
    create_table_query: str
    engine_full: str
    as_select: str
    partition_key: str
    sorting_key: str
    primary_key: str
    sampling_key: str
    storage_policy: str
    total_rows: Optional[int]
    total_bytes: Optional[int]
    total_bytes_uncompressed: Optional[int]
    parts: Optional[int]
    active_parts: Optional[int]
    total_marks: Optional[int]
    lifetime_rows: Optional[int]
    lifetime_bytes: Optional[int]
    comment: str
    has_own_data: int
    loading_dependencies_database: list[str]
    loading_dependencies_table: list[str]
    loading_dependent_database: list[str]
    loading_dependent_table: list[str]


class TablesQuery(BaseClickPyQuery[list[TableModel]]):
    QUERY: ClassVar = """
SELECT
  *
FROM
  system.tables
WHERE
  database IN ({databases}); 
"""

    # Request params
    databases: list[str] = ['github', 'pypi']
