from typing import ClassVar

from pydantic import BaseModel

from clickpy.queries.base import BaseClickPyQuery


class KeywordDownloadsResumeModel(BaseModel):
    week: int
    month: int
    year: int
    total: int


class KeywordDownloadsResumeQuery(BaseClickPyQuery[KeywordDownloadsResumeModel]):
    QUERY: ClassVar = """
SELECT 
    SUMIf(p.count, p.date > today() - toIntervalWeek(1)) AS week,
    SUMIf(p.count, p.date > today() - toIntervalMonth(1)) AS month,
    SUMIf(p.count, p.date > today() - toIntervalYear(1)) AS year,
    SUM(p.count) AS total
FROM 
    pypi.pypi_downloads_per_day p
WHERE 
    p.project IN (
        SELECT
            DISTINCT name
        FROM (
            SELECT 
                arrayJoin(
                    multiIf(
                        position(keywords, ',') > 0, 
                        splitByChar(',', keywords), 
                        splitByChar(' ', keywords)
                    )
                ) AS keyword,
                name
            FROM pypi.projects
        )
        WHERE keyword = '{keyword}'
    );
"""

    # Request params
    keyword: str
