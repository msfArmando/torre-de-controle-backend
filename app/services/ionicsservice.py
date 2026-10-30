from app.oracle_database import DataBase, Abastecimento, AutorizacaoVeiculo, BicoCombustivel, BbaUsuario, MVeiculo
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from datetime import timedelta, datetime

async def get_ionics_kpis(session: Session):
    engine = DataBase.engine
    end_date = datetime.now() + timedelta(days=1)
    end_date_str = end_date.strftime("%Y-%m-%d")
    end_date_format = datetime.strptime(end_date_str, "%Y-%m-%d")
    start_date = end_date_format - timedelta(days=8)

    stmt = (
        select(
            Abastecimento.i_cod_m_abastecimento.label('cod_abastecimento'),
            Abastecimento.dt_abastecimento.label('dt_abastecimento'),
            Abastecimento.f_quantidade.label('quantidade'),
            AutorizacaoVeiculo.s_tipo_autoriz_veic.label('autorizacao_veiculo'),
            BicoCombustivel.s_desc.label('bico'))
            .join(AutorizacaoVeiculo, Abastecimento.i_cod_bs_tipo_autoriz_veic == AutorizacaoVeiculo.i_cod_bs_tipo_autoriz_veic)
            .join(BicoCombustivel, Abastecimento.i_cod_m_bico_combust == BicoCombustivel.i_cod)
            .join(BbaUsuario, Abastecimento.i_cod_bba_usuario == BbaUsuario.i_cod)
            .join(MVeiculo, Abastecimento.i_cod_m_veiculo == MVeiculo.i_cod)
            .where(and_(Abastecimento.dt_abastecimento >= start_date, Abastecimento.dt_abastecimento < end_date_format))
    )

    count_manual: int = 0
    count_auto: int = 0
    count_diesel_litros: float = 0.0

    with session.begin():
        result = session.execute(stmt)
        for row in result.fetchall():
            if (row[3] == 'Teclado') and ('BICO DIESEL' in row[4] or 'BICO COMBOIO' in row[4]):
                count_manual += 1
            elif (row[3] == 'Div') and ('BICO DIESEL' in row[4] or 'BICO COMBOIO' in row[4]):
                count_auto += 1

            if 'BICO DIESEL' in row[4] or 'BICO COMBOIO' in row[4]:
                count_diesel_litros += float(row[2])

    session.commit()
    
    return {
        'quantidade_manual_teclado': count_manual,
        'quantidade_auto_div': count_auto,
        'quantidade_diesel_litros': float("{:.2f}".format(count_diesel_litros))
    }