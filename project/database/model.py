from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


class Model(DeclarativeBase):
    __abstract__ = True

    # Добавляем конфигурацию датаклассов
    __mapper_args__ = {"eager_defaults": True}
