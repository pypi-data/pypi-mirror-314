from typing import ClassVar

from pydantic import BaseModel

from clickpy.queries.base import BaseClickPyQuery


class KeywordsByReleasesModel(BaseModel):
    name: str
    releases: int


class KeywordsByReleasesQuery(BaseClickPyQuery[list[KeywordsByReleasesModel]]):
    QUERY: ClassVar = """
SELECT
    name,
    COUNT(*) AS releases
FROM (
    SELECT
        arrayJoin(
            CASE
                WHEN position(keywords, ',') > 0 THEN splitByChar(',', keywords)
                ELSE splitByChar(' ', keywords)
            END
        ) AS name
    FROM pypi.projects
)
GROUP BY name
ORDER BY releases DESC
LIMIT {limit}
OFFSET {offset};
"""

    # Request params
    limit: int = 100
    offset: int = 0

    def query(self) -> str:
        return super().query()
