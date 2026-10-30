from datetime import datetime, timedelta
import httpx
from app.config import settings
import asyncio
from app.oracle_database import DataBase, AcumuladoSafra, SafraOrg
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, func

async def get_dias_safra(today_date) -> int:

    engine = DataBase.engine

    with Session(engine) as conn:
        stmt = (
            select(
                AcumuladoSafra.acum_re_mediasaf
            )
            .join(
                SafraOrg, and_(AcumuladoSafra.safra_st_codigo == SafraOrg.safra_st_codigo, 
                               AcumuladoSafra.fil_in_codigo == SafraOrg.fil_in_codigo)
            ).where(
                and_(AcumuladoSafra.acum_dt_movimento == func.to_date(today_date, 'DD/MM/YY'),
                    AcumuladoSafra.fil_in_codigo == 3,
                    SafraOrg.safra_st_situacao == 'CR',
                    AcumuladoSafra.var_in_codigo == 1034
                )
            )
        )

        with conn.begin():
            result = conn.execute(stmt).scalar()

        return int(result)

async def get_pantera_data(start_date_str, end_date_str):

    url = f"{settings.PANTERA_URL}/{start_date_str}/{end_date_str}"
    headers = {"Authorization": settings.PANTERA_TOKEN}

    max_tries = 3
    wait_time = 2

    async with httpx.AsyncClient() as client:
        for trying in range(1, max_tries + 1):
            try:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                break
            except:
                if trying == max_tries:
                    raise
                await asyncio.sleep(wait_time)

    dados_brutos = response.json()

    final_response = []

    for item in dados_brutos:

        causa = item.get("id_causa_incendio")
        id_report = item.get("id_report")

        acionamento_list = item.get("acionamentos")

        if isinstance(acionamento_list, list) and acionamento_list:

            id_acionamento = acionamento_list[0].get("id_acionamento")
            dt_acionamento = acionamento_list[0].get("dt_acionamento")
            dt_chegada = acionamento_list[0].get("dt_chegada")

            dt_acionamento_format = datetime.fromisoformat(dt_acionamento)
            dt_acionamento_format_str = dt_acionamento_format.strftime("%d/%m/%y %H:%M:%S")

            dt_chegada_format = datetime.fromisoformat(dt_chegada)
            dt_chegada_format_str = dt_chegada_format.strftime("%d/%m/%y %H:%M:%S")

            diferenca_datas = dt_chegada_format - dt_acionamento_format

            total_segundos = diferenca_datas.total_seconds()

            total_minutos = diferenca_datas.total_seconds() / 60
            
            response_dict = {
                "id_report": id_report,
                "id_acionamento": id_acionamento,
                "dt_acionamento": dt_acionamento_format_str,
                "dt_chegada": dt_chegada_format_str,
                "intervalo": diferenca_datas,
                "total_segundos": total_segundos,
                "total_minutos": total_minutos,
            }
            if causa == 2:
                final_response.append(response_dict)
        else:
            response_dict = {
                "id_report": id_report,
                "id_acionamento": "",
                "dt_acionamento": "",
                "dt_chegada": "",
                "total_segundos": 0.0,
                "total_minutos": 0.0,
            }
            if causa == 2:
                final_response.append(response_dict)

    return final_response

async def buscar_relatorio_pantera() -> dict:
    
    today = datetime.now()
    start_date = today - timedelta(days=8)
    start_date_str = start_date.strftime("%Y-%m-%d")

    end_date_str = today.strftime("%Y-%m-%d")

    final_response = await get_pantera_data(start_date_str, end_date_str)

    return final_response

async def buscar_relatorio_comparativo_safra() -> dict:

    today = datetime.now()
    
    dias_correntes_safra = await get_dias_safra((today - timedelta(days=1)).strftime('%d/%m/%Y'))
    
    start_date_safra_corrente = today - timedelta(days=dias_correntes_safra)
    start_date_safra_corrente_str = start_date_safra_corrente.strftime("%Y-%m-%d")

    end_date_str = today.strftime("%Y-%m-%d")

    final_response = await get_pantera_data(start_date_safra_corrente_str, end_date_str)

    return final_response