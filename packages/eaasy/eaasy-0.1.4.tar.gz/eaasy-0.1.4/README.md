# Environemnt As A Software

Build an environment with a database and a REST API.

## Requirements

- Python 3.12
- PostgreSQL 13.4
- Redis 6.2.6 (optional but recommended)


## Initial Setup

Create a database in PostgreSQL:

```sql
create database database_name;
```

Create a virtual environment and install the dependencies:

```sh
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Set the environment variables.
```
POSTGRES_URI=<SQL_DATABASE_URI>

# macOS only
OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
```

Initialize alembic:


```python
# alembic_init.py
from eaasy.extensions.migration import init
from argparse import ArgumentParser

def get_arguments() -> dict:
    parser = ArgumentParser(description='Alembic migration helper')
    parser.add_argument('sql_url', metavar='sql_url', type=str, help='SQLAlchemy URL')
    parser.add_argument('--path', '-p', metavar='path', type=str, help='Alembic path', default='src/alembic')

    args = parser.parse_args()

    if not args.sql_url:
        raise Exception('SQLAlchemy URL is required')

    return args

if __name__ == '__main__':
    args = get_arguments()
    init(args.sql_url, args.path)
```

Launch the script to build the alembic folder:

```sh
python alembic_init.py <SQL_DATABASE_URI> # --path src/alembic (optional)
```