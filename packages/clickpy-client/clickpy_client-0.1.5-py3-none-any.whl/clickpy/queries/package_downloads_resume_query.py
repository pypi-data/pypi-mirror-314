from typing import ClassVar

from pydantic import BaseModel

from clickpy.queries.base import BaseClickPyQuery


class PackageDownloadsResumeModel(BaseModel):
    week: int
    month: int
    year: int
    total: int


class PackageDownloadsResumeQuery(BaseClickPyQuery[PackageDownloadsResumeModel]):
    QUERY: ClassVar = """
SELECT 
    sumIf(count, date > today() - toIntervalWeek(1)) AS week,
    sumIf(count, date > today() - toIntervalMonth(1)) AS month,
    sumIf(count, date > today() - toIntervalYear(1)) AS year,
    sum(count) AS total
FROM 
    pypi.pypi_downloads_per_day 
WHERE 
    project = '{package}';
"""

    # Request params
    package: str
