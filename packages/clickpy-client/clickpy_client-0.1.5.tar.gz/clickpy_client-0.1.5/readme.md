# clickpy-client

Client for [clickpy.clickhouse.com](https://clickpy.clickhouse.com) database.

[![PyPI](https://img.shields.io/pypi/v/clickpy-client)](https://pypi.org/project/clickpy-client/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/clickpy-client)](https://pypi.org/project/clickpy-client/)

[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=rocshers_clickpy-client&metric=coverage)](https://sonarcloud.io/summary/new_code?id=rocshers_clickpy-client)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=rocshers_clickpy-client&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=rocshers_clickpy-client)

[![Downloads](https://pypi.rocshers.com/badges/svg/packages/clickpy-client/downloads/total)](https://clickpy.clickhouse.com/dashboard/clickpy-client)
[![GitLab stars](https://img.shields.io/gitlab/stars/rocshers/python/clickpy-client)](https://gitlab.com/rocshers/python/clickpy-client)
[![GitLab last commit](https://img.shields.io/gitlab/last-commit/rocshers/python/clickpy-client)](https://gitlab.com/rocshers/python/clickpy-client)

## Quick start

```bash
pip install clickpy-client
```

```python
import asyncio

from clickpy import ClickPyClient


async def main():
    clickpy = ClickPyClient()

    tables = await clickpy.get_tables()
    for table in tables:
        print(f'Database: {table.database}; table: {table.name} rows: {table.total_rows}')

    keywords = await clickpy.get_keywords_by_releases()
    for keyword in keywords:
        print(f'Database: {keyword.name}; releases: {keyword.releases}')


asyncio.run(main())
```

## Config

The client uses a public connection. But if you have your own DB instance with a similar structure, you can override the access parameters via environment variables.

```bash
CLICKPY_HOST='https://clickpy-clickhouse.clickhouse.com'
CLICKPY_SECURE=True
CLICKPY_USERNAME='play'
CLICKPY_PASSWORD=''
```

## Client Methods

### get_tables

Get all tables in `github` and `pypi` databases.

### get_keywords_by_releases

Get all keywords based on project description. Sorted by number of releases.

## Contribute

Issue Tracker: <https://gitlab.com/rocshers/python/clickpy-client/-/issues>  
Source Code: <https://gitlab.com/rocshers/python/clickpy-client>

Before adding changes:

```bash
make install-dev
```

After changes:

```bash
make format test
```
