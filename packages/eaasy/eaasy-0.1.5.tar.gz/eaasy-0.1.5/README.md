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
from argparse import ArgumentParser, Namespace as ArgumentNamespace

def get_arguments() -> ArgumentNamespace:
    parser = ArgumentParser(description='Alembic migration helper')
    parser.add_argument('sql_url', metavar='sql_url', type=str, help='SQLAlchemy URL')
    parser.add_argument('--path', '-p', metavar='path', type=str, help='Alembic path', default='src/alembic')
    parser.add_argument('--tables-folder', '-t', metavar='tables_folder', type=str, help='Tables folder', default='src/tables')

    args = parser.parse_args()

    if not args.sql_url:
        raise Exception('SQLAlchemy URL is required')

    return args

if __name__ == '__main__':
    args = get_arguments()
    init(args.sql_url, args.path, args.tables_folder)
```

Launch the script to build the alembic folder:

```sh
python alembic_init.py <SQL_DATABASE_URI> # --path src/alembic (optional)
```

Add a table like this:

```python
# src/tables/user.py
from eaasy import PrimaryKey, Audit
from sqlalchemy import Column, String

class UserProperties:
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    email = Column(String, nullable=False)


class User(PrimaryKey, UserProperties, Audit):
    __tablename__ = 'users'
```

And add it to the `src/tables/__init__.py` file:

```python
# src/tables/__init__.py
from .user import User

__all__ = ['User']
```

Run the migration:

```sh
alembic revision --autogenerate -m "Create users table"
alembic upgrade head
```