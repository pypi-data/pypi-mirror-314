from eaasy import BaseEntity
from flask_restx import Namespace, Model, OrderedModel, fields
from datetime import datetime, timezone

def buil_model(entity: BaseEntity) -> tuple[Namespace, Model | OrderedModel]:
    namespace = Namespace(entity.__name__, description=f"{entity.__name__} operations", path=f"/{entity.__name__.lower()}")
    model_name = entity.__name__
    model_properties = {}
    column_list = entity.column_list()
    for prop in column_list:
        if not prop.name.startswith('_'):
            if f'{prop.type}' == 'INTEGER':
                model_properties[prop.name] = fields.Integer(
                    required=not prop.nullable, 
                    description=prop.name,
                    default=0 if not prop.nullable else None,
                    example=0)
            elif f'{prop.type}' == 'VARCHAR':
                model_properties[prop.name] = fields.String(
                    required=not prop.nullable, 
                    description=prop.name,
                    default='' if not prop.nullable else None,
                    example='')
            elif f'{prop.type}' == 'DATETIME':
                model_properties[prop.name] = fields.DateTime(
                    required=not prop.nullable, 
                    description=prop.name,
                    default=datetime.strftime(datetime.now(timezone.utc), '%Y-%m-%dT%H:%M:%S') if not prop.nullable else None,
                    example=datetime.strftime(datetime.now(timezone.utc), '%Y-%m-%dT%H:%M:%S'))
            elif f'{prop.type}' == 'BOOLEAN':
                model_properties[prop.name] = fields.Boolean(
                    required=not prop.nullable, 
                    description=prop.name,
                    default=False,
                    example=False)
            else:
                print(f"\033[33mType {prop.type} not supported\033[0m")
    
    model = namespace.model(model_name, model_properties)

    return namespace, model