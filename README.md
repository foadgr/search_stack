# Search Stack


## Objective
The objective of this task is to create a web application allowing users to search by gene name for genomic variants rendered in a tabular view.

## Features

Features include :
* A rendered search result from a gene selection input allowing the user to view a list of genomic variants alongside variant-specific various attributes.
* Searches are throttled when the search is fewer than 3 characters and debounced when over 3 characters, thus allowing for fewer XHR requests to the API server.
* A RESTful endpoint supporting the functionality of querying by gene name.

## Installation
1. Create a virtual [conda] (Python 3) environment called `search_stack-env` with Python and pip

```bash
➜  conda create --name search_stack-env python=3.6 pip
➜  source activate search_stack-env
(search_stack-env) ➜
```
[conda]: https://docs.anaconda.com/anaconda/install/ "Anaconda Installation"

2. Clone the repository and install package requirements.

```bash
(search_stack-env) ➜ git clone https://github.com/foadgr/search_stack.git
(search_stack-env) ➜ cd search_stack
(search_stack-env) ➜ pip install -r requirements.txt
```


### Install PostgreSQL
A PostgreSQL database image can be pulled from [Docker].
```bash
sudo docker run --name app_db -p 5433:5432 \
                -e POSTGRES_PASSWORD= \
                -d fgreen
```

### Install PostgREST
Install the latest version of [PostgREST], make the package executable, and run the server based on the server configuration in `config/setup/db.conf`.

```bash
# download from https://github.com/PostgREST/postgrest/releases/latest
(search_stack-env) ➜ tar xfJ postgrest-v6.0.2-osx.tar.xz
(search_stack-env) ➜ cp postgrest /usr/local/bin
(search_stack-env) ➜ postgrest config/setup/db.conf

#You should see
Listening on port 3000
Attempting to connect to the database...
Connection successful
```

### Install the front-end client
Install the React Javascript client, run the build, and start the server. The client can be viewed at [http://localhost:8080].

```bash
npm install
npm run build
npm start
```

[PostgREST]: https://github.com/PostgREST/postgrest/releases/tag/v6.0.2
[Docker]: https://www.docker.com/community-edition#download
[http://localhost:8080]: [http://localhost:8080]

## Setup
### Load source data
Extract genomic variatns source data from web source, data cleaning, and load to `app_db` genomic variants data from web source.
```bash
(search_stack-env) ➜ python search_stack/insert.py
```

Note: running `insert.py` will also create all SQL components, tables/view, and table indexes. For the purpose of gene lookup in this exercise, a regular B-Tree index with the `varchar_pattern_ops` operator class will help speed up search queries. Additionally, querying only the gene prefix will help save space for the index.
```sql
CREATE INDEX ON api.variants (substr(gene, 1, 4) varchar_pattern_ops);
```
This will work alongside the main REST endpoint in the search query:
```sql
SELECT gene FROM api.variants WHERE subtr(gene, 1, 4) LIKE '{user input}%'
```
