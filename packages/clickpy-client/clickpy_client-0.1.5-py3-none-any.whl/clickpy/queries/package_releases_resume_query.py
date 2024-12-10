from typing import ClassVar

from pydantic import BaseModel

from clickpy.queries.base import BaseClickPyQuery


class PackageReleasesResumeModel(BaseModel):
    week: int
    month: int
    year: int
    total: int


class PackageReleasesResumeQuery(BaseClickPyQuery[PackageReleasesResumeModel]):
    QUERY: ClassVar = """
SELECT
    countIf(DISTINCT version, upload_time > today() - toIntervalWeek(1)) AS week,
    countIf(DISTINCT version, upload_time > today() - toIntervalMonth(1)) AS month,
    countIf(DISTINCT version, upload_time > today() - toIntervalYear(1)) AS year,
    count(DISTINCT version) AS total
FROM
    pypi.projects
WHERE
    name = '{package}'
"""

    # Request params
    package: str
