from typing import ClassVar

from pydantic import BaseModel

from clickpy.queries.base import BaseClickPyQuery


class KeywordReleasesResumeModel(BaseModel):
    week: int
    month: int
    year: int
    total: int


class KeywordReleasesResumeQuery(BaseClickPyQuery[KeywordReleasesResumeModel]):
    QUERY: ClassVar = """
SELECT
    countIf(DISTINCT version, upload_time > today() - toIntervalWeek(1)) AS week,
    countIf(DISTINCT version, upload_time > today() - toIntervalMonth(1)) AS month,
    countIf(DISTINCT version, upload_time > today() - toIntervalYear(1)) AS year,
    count(DISTINCT version) AS total
FROM (
    SELECT
        arrayJoin(
            CASE
                WHEN position(keywords, ',') > 0 THEN splitByChar(',', keywords)
                ELSE splitByChar(' ', keywords)
            END
        ) AS name,
        version,
        upload_time
    FROM pypi.projects
)
WHERE 
    name = '{keyword}';
"""

    # Request params
    keyword: str
