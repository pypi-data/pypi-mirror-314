from sqlalchemy import create_engine, Column, Integer, DateTime, func
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker
import os

Base = declarative_base()

def get_session_factory():
    POSTGRES_URI = os.getenv('POSTGRES_URI')

    if not POSTGRES_URI:
        raise EnvironmentError(
            "Missing 'POSTGRES_URI' environment variable")  # pragma: no cover

    # Proceed to create the engine
    engine = create_engine(POSTGRES_URI)

    return sessionmaker(bind=engine)

class BaseEntity(Base):
    __abstract__ = True

    @classmethod
    def column_list(cls) -> list[Column]:
        return list(cls.__table__.columns)
    
    # Session
    @classmethod
    def get_session(cls) -> scoped_session:  # pragma: no cover
        return scoped_session(get_session_factory())
    
    # CRUD Errors
    @classmethod
    def not_found(cls, **kwargs):
        raise Exception({
            'status_code': 404,
            'message': f'{cls.__name__} with {kwargs} not found',
            'data': kwargs,
        })

    @classmethod
    def already_exists(cls, details, **kwargs):
        raise Exception({
            'status_code': 409,
            'message': f'{cls.__name__} {details}',
            'data': kwargs,
        })

    @classmethod
    def failure(cls, message: str, **kwargs):
        raise Exception({
            'status_code': 500,
            'message': message,
            'data': kwargs,
        })

class PrimaryKey(BaseEntity):
    __abstract__ = True

    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)

    @classmethod
    def get_by_id(cls, id: int):
        data = cls.get_session().query(cls).get(id)
        return data if data else cls.not_found(id=id)

class Audit:
    __abstract__ = True

    createdAt = Column(DateTime, nullable=False, default=func.now())
    updatedAt = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    deletedAt = Column(DateTime, nullable=True)