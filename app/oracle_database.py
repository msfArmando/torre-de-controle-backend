import oracledb
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, registry
from app.config import settings
from datetime import datetime
from sqlalchemy.orm import Session
from pathlib import Path
import os

rg = registry()

try:
    oracledb.init_oracle_client(lib_dir=os.getenv("ORACLE_INSTANTCLIENT_DIR") or None)
except oracledb.ProgrammingError:
    pass

class DataBase:
    db_url = f"oracle+oracledb://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/?service_name={settings.DB_NAME}"
    engine = create_engine(db_url)

def get_session_ionics():
    db_url = f"oracle+oracledb://{settings.DB_USER_IONICS}:{settings.DB_PASS_IONICS}@{settings.DB_HOST}:{settings.DB_PORT}/?service_name={settings.DB_NAME}"
    engine = create_engine(db_url)
    with Session(engine) as conn:
        yield conn

@rg.mapped_as_dataclass
class AcumuladoSafra:
    __tablename__ = 'agr_sci_acumulado'

    acum_re_mediasaf: Mapped[float] = mapped_column('acum_re_mediasaf')
    safra_st_codigo: Mapped[str] = mapped_column('safra_st_codigo', primary_key=True)
    fil_in_codigo: Mapped[str] = mapped_column('fil_in_codigo')
    acum_dt_movimento: Mapped[float] = mapped_column('acum_dt_movimento')
    var_in_codigo: Mapped[int] = mapped_column('var_in_codigo')

@rg.mapped_as_dataclass
class SafraOrg:
    __tablename__ = 'agr_safraorg'

    safra_st_codigo: Mapped[str] = mapped_column('safra_st_codigo', primary_key=True)
    fil_in_codigo: Mapped[int] = mapped_column('fil_in_codigo')
    safra_st_situacao: Mapped[str] = mapped_column('safra_st_situacao')
    

@rg.mapped_as_dataclass
class Abastecimento:
    __tablename__ = 'm_abastecimento'

    i_cod_m_abastecimento: Mapped[int] = mapped_column('i_cod_m_abastecimento', primary_key=True)
    dt_abastecimento: Mapped[datetime] = mapped_column('dt_abastecimento')
    f_quantidade: Mapped[float] = mapped_column('f_quantidade')
    i_cod_bs_tipo_autoriz_veic: Mapped[int] = mapped_column(ForeignKey('bs_tipo_autoriz_veic.i_cod_bs_tipo_autoriz_veic'))
    i_cod_m_bico_combust: Mapped[int] = mapped_column(ForeignKey('m_bico_combust.i_cod'))
    i_cod_bba_usuario: Mapped[int] = mapped_column(ForeignKey('bba_usuario.i_cod'))
    i_cod_m_veiculo: Mapped[int] = mapped_column(ForeignKey('m_veiculo.i_cod'))

@rg.mapped_as_dataclass
class AutorizacaoVeiculo:
    __tablename__ = 'bs_tipo_autoriz_veic'

    i_cod_bs_tipo_autoriz_veic: Mapped[int] = mapped_column('i_cod_bs_tipo_autoriz_veic', primary_key=True)
    s_tipo_autoriz_veic: Mapped[str] = mapped_column('s_tipo_autoriz_veic')

@rg.mapped_as_dataclass
class BicoCombustivel:
    __tablename__ = 'm_bico_combust'

    i_cod: Mapped[int] = mapped_column('i_cod', primary_key=True)
    s_desc: Mapped[str] = mapped_column('s_desc')

@rg.mapped_as_dataclass
class BbaUsuario:
    __tablename__ = 'bba_usuario'

    i_cod: Mapped[int] = mapped_column('i_cod', primary_key=True)

@rg.mapped_as_dataclass
class MVeiculo:
    __tablename__ = 'm_veiculo'

    i_cod: Mapped[int] = mapped_column('i_cod', primary_key=True)