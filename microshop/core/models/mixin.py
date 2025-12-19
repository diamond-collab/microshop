from sqlalchemy import ForeignKey
from sqlalchemy.orm import declared_attr, Mapped, mapped_column, relationship


class RelationMixin:
    # Название таблицы, на которую делаем связь
    _target_table: str
    # Название поля в связанной таблице
    _target_column: str
    # Имя атрибута в обратной связи (back_populates)
    _back_populates: str | None = None
    # Дополнительно уникальное поле или nullable
    _unique: bool = False
    _nullable: bool = False

    @declared_attr
    def foreign_key(cls) -> Mapped[int]:
        return mapped_column(
            ForeignKey(f'{cls._target_table}.{cls._target_column}'),
            unique=cls._unique,
            nullable=cls._nullable,
        )

    @declared_attr
    def relation(cls) -> Mapped:
        return relationship(
            cls._target_table.capitalize(),
            back_populates=cls._back_populates,
        )
