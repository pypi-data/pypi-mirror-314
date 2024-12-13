# ageqrp

Query Results Parser (QRP) for Apache AGE database queries using psycopg

## Urls

- PyPi: https://pypi.org/project/ageqrp/
- GitHub: https://github.com/cjoakim/ageqrp

## Features

- Easy to use
- Transforms the augmented AGE JSON into regular JSON


## Quick start


### Installation

```
$ pip install ageqrp
```

### Use

```
import json

from ageqrp import QueryResultParser

import psycopg_pool

...

# This example is from a FastAPI web application

async def post_query(req: Request, query_type):
    form_data = await req.form()
    cypher_query = form_data.get("cypher_query").replace("\r\n", "").strip()
    result_objects = list()
    qrp = QueryResultParser()
        
    try:
        async with req.app.async_pool.connection() as conn:
            async with conn.cursor() as cursor:
                try:
                    await asyncio.wait_for(cursor.execute(cypher_query), timeout=10.0)
                    results = await cursor.fetchall()
                    for row in results:
                        # psycopg results parsed into regular JSON objects here
                        result_objects.append(qrp.parse(row))
```

The above cypher_query may look something like this:

```
select * from ag_catalog.cypher('legal_cases',
  $$ MATCH (c:Case {id: 999494})-[r:cites*1..2]->(c2:Case) RETURN c,r limit 100 $$)
  as (c agtype, r agtype);
```

Also see file **sample-program.py** in the GitHub repo as well as the unit tests
in the tests/ directory.

---

## Changelog

Current version: 0.2.0

-  2024/12/12, version 0.2.0, Docs and tests enhanced
-  2024/12/01, version 0.1.0, Initial Production release
