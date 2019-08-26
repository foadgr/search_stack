## Docker


PostgREST serves a fully RESTful API from any existing PostgreSQL database. It provides a cleaner, more standards-compliant, faster API than you are likely to write from scratch.

Image contains
<!-- https://github.com/suzel/docker-postgrest -->
- postgrest
- pgweb
- postgres alpine

Build the custom Docker image and start running the container:
```bash
docker-compose up -d --build
docker-compose up
```

The docker-entrypoint-initdb.d folder will only be run once while the container is created (instantiated) so you actually have to do a docker-compose down -v to re-activate this for the next run.
```bash
docker-compose down -v
```

```
Description of n_distinct
-1 indicates that each row in the column is unique.

>=1 indicates the number of unique values in the column
<1 indicates the number/total number of unique values in the column

Description of correlation
It indicates the linear correlation between this column and the data stack storage, where 1 indicates perfect positive correlation. As the value gets closer to 0, the data distribution is more discrete. <0 indicates an inverse correlation.
```

```sql
select tablename,attname,n_distinct,correlation
from pg_stats where tablename='variant_results'
```

```
sequelize-auto -h localhost -d app_db -u fgreen -p 5432 -e postgres -o "./src/models" -t variant_results
```
