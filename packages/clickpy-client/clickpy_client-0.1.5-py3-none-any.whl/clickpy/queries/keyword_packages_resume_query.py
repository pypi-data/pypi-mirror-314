from typing import ClassVar

from pydantic import BaseModel

from clickpy.queries.base import BaseClickPyQuery


class KeywordPackagesResumeModel(BaseModel):
    week: int
    month: int
    year: int
    total: int


class KeywordPackagesResumeQuery(BaseClickPyQuery[KeywordPackagesResumeModel]):
    QUERY: ClassVar = """
SELECT
    countIf(DISTINCT name, upload_time > today() - toIntervalWeek(1)) AS week,
    countIf(DISTINCT name, upload_time > today() - toIntervalMonth(1)) AS month,
    countIf(DISTINCT name, upload_time > today() - toIntervalYear(1)) AS year,
    count(DISTINCT name) AS total
FROM (
    SELECT
        arrayJoin(
            CASE
                WHEN position(keywords, ',') > 0 THEN splitByChar(',', keywords)
                ELSE splitByChar(' ', keywords)
            END
        ) AS keyword,
        name,
        upload_time
    FROM pypi.projects
)
WHERE 
    keyword = '{keyword}';
"""

    # Request params
    keyword: str
