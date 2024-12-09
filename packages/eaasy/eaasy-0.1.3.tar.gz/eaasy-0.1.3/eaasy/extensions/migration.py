from subprocess import run
import argparse

def get_arguments() -> dict:
    parser = argparse.ArgumentParser(description='Alembic migration helper')
    parser.add_argument('sql_url', metavar='sql_url', type=str, help='SQLAlchemy URL')
    parser.add_argument('--path', metavar='path', type=str, help='Alembic path', default='src/alembic')

    args = parser.parse_args()

    if not args.sql_url:
        raise Exception('SQLAlchemy URL is required')

    return vars(args)


def init(sql_url: str, path: str = 'src/alembic') -> None:
    run(['alembic', 'init', path])
    env_file = path + '/env.py'
    add_string_to_file(env_file, 'from eaasy.domain.database import Base', 0)
    replace_string_in_file(env_file, 'target_metadata = None', 'target_metadata = Base.metadata')
    replace_string_in_file('alembic.ini', 'sqlalchemy.url = driver://user:pass@localhost/dbname', f'sqlalchemy.url = {sql_url}')

def add_string_to_file(file_path: str, string_to_add: str, line_number: int):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    index = max(0, min(line_number - 1, len(lines)))
    lines.insert(index, string_to_add + '\n')
    with open(file_path, 'w') as file:
        file.writelines(lines)

def replace_string_in_file(file_path: str, string_to_replace: str, new_string: str):
    with open(file_path, 'r') as file:
        filedata = file.read()
    newdata = filedata.replace(string_to_replace, new_string)
    with open(file_path, 'w') as file:
        file.write(newdata)


if __name__ == '__main__':
    arguments = get_arguments()

    init(arguments['sql_url'], arguments['path'])