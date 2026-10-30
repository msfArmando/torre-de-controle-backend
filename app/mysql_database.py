from app.config import settings
from sqlalchemy.orm import registry, Mapped, mapped_column
from sqlalchemy import create_engine, ForeignKey
from datetime import datetime

rg = registry()

class MySQLDatabase:
    db_url = f'mysql+pymysql://{settings.MYSQL_DB_USER}:{settings.MYSQL_DB_PASS}@{settings.MYSQL_DB_HOST}:{settings.MYSQL_DB_PORT}/{settings.MYSQL_DB_NAME}?charset=utf8'
    engine = create_engine(db_url)

@rg.mapped_as_dataclass
class Fardo:
    __tablename__ = 'fila_fardo'

    id_fila: Mapped[int] = mapped_column('id_fila', primary_key=True)
    id_organizacao: Mapped[int] = mapped_column(ForeignKey('fila_organizacao.id_organizacao'))
    tempo_carregamento: Mapped[int] = mapped_column('tempo_carregamento')
    retorno: Mapped[datetime] = mapped_column('retorno')

@rg.mapped_as_dataclass
class Alcool:
    __tablename__ = 'fila_alcool'

    id_fila: Mapped[int] = mapped_column('id_fila', primary_key=True)
    id_organizacao: Mapped[int] = mapped_column(ForeignKey('fila_organizacao.id_organizacao'))
    tempo_carregamento: Mapped[int] = mapped_column('tempo_carregamento')
    retorno: Mapped[datetime] = mapped_column('retorno')

@rg.mapped_as_dataclass
class BigBag:
    __tablename__ = 'fila_bigbag'

    id_fila: Mapped[int] = mapped_column('id_fila', primary_key=True)
    id_organizacao: Mapped[int] = mapped_column(ForeignKey('fila_organizacao.id_organizacao'))
    tempo_carregamento: Mapped[int] = mapped_column('tempo_carregamento')
    retorno: Mapped[datetime] = mapped_column('retorno')

@rg.mapped_as_dataclass
class Saco:
    __tablename__ = 'fila_saco50kg'

    id_fila: Mapped[int] = mapped_column('id_fila', primary_key=True)
    id_organizacao: Mapped[int] = mapped_column(ForeignKey('fila_organizacao.id_organizacao'))
    tempo_carregamento: Mapped[int] = mapped_column('tempo_carregamento')
    retorno: Mapped[datetime] = mapped_column('retorno')

@rg.mapped_as_dataclass
class FilaOrganizacao:

    __tablename__ = 'fila_organizacao'
    
    id_organizacao: Mapped[int] = mapped_column('id_organizacao', primary_key=True)
    nomefantasia: Mapped[str] = mapped_column('nomefantasia') 