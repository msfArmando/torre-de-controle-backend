from datetime import datetime, timedelta
from app.mysql_database import MySQLDatabase, Fardo, Alcool, BigBag, Saco, FilaOrganizacao
from sqlalchemy import select, join, func, and_, text
from sqlalchemy.orm import Session
import time

async def get_fila_carregamento_kpis():

    response: list[dict] = list()
    classList = [Fardo, Alcool, BigBag, Saco]
    engine = MySQLDatabase.engine

    end_date = datetime.now()
    end_date_format = end_date.replace(hour=23, minute=59, second=59, microsecond=0)

    start_date_inicial = datetime.now()

    start_date = start_date_inicial - timedelta(days=30)
    start_date_subquery = start_date_inicial - timedelta(days=8)
    
    start_date_format = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
    start_date_subquery_format = start_date_subquery.replace(hour=0, minute=0, second=0, microsecond=0)

    with Session(engine) as conn:

        for class_fila in classList:

            subquery_quantidade = (
                select(
                    class_fila.id_organizacao,
                    (func.count(class_fila.id_fila) / 8).label('quantidade')
                ).where(and_(class_fila.retorno >= start_date_subquery_format, class_fila.retorno < end_date_format))
                .group_by(class_fila.id_organizacao)
            )

            subquery_tempoc = (
                select(
                    class_fila.id_organizacao,
                    func.sec_to_time(func.sum(func.time_to_sec(class_fila.tempo_carregamento)) / func.count(class_fila.tempo_carregamento)).label('tempo_carregamento')
                ).where(and_(class_fila.retorno >= start_date_subquery_format, class_fila.retorno < end_date_format))
                .group_by(class_fila.id_organizacao)
            )

            T2 = subquery_quantidade.subquery(name="T2")
            T3 = subquery_tempoc.subquery(name="T3")

            stmt = (
                select(
                    FilaOrganizacao.nomefantasia.label('organizacao'),
                    func.round((func.count(class_fila.id_fila) / 30)).label('quantidade_media_30_dias'),
                    T2.c.quantidade.label('quantidade_media_8_dias'),
                    func.sec_to_time(func.sum(func.time_to_sec(class_fila.tempo_carregamento)) / func.count(class_fila.tempo_carregamento)).label('tempo_carregamento_medio_30_dias'),
                    T3.c.tempo_carregamento.label('tempo_carregamento_media_8_dias')
                )
                .select_from(class_fila)
                .outerjoin(FilaOrganizacao, class_fila.id_organizacao == FilaOrganizacao.id_organizacao)
                .outerjoin(T2, T2.c.id_organizacao == class_fila.id_organizacao)
                .outerjoin(T3, T3.c.id_organizacao == class_fila.id_organizacao)
                .where(and_(class_fila.retorno >= start_date_format, class_fila.retorno < end_date_format))
                .group_by(class_fila.id_organizacao)
            )


            with conn.begin():
                result = conn.execute(stmt)
                for row in result.fetchall():

                    print('consulta funcionou', flush=True)
                    print(row, flush=True)

                    tempo_carrego_medio_1 = row[3] or 0
                    tempo_carrego_medio_2 = row[4] or 0

                    dict_fila = {
                        "organizacao": row[0],
                        "quantidade_media_30_dias": round(row[1] or 0, 0),
                        "quantidade_media_8_dias": round(row[2] or 0, 0),
                        "tempo_carregamento_medio_30_dias": (
                            f"{int(tempo_carrego_medio_1.total_seconds() // 3600):02d}:{int((tempo_carrego_medio_1.total_seconds() % 3600) // 60):02d}" 
                            if tempo_carrego_medio_1 else None
                        ),
                        "tempo_carregamento_medio_8_dias": (
                            f"{int(tempo_carrego_medio_2.total_seconds() // 3600):02d}:{int((tempo_carrego_medio_2.total_seconds() % 3600) // 60):02d}" 
                            if tempo_carrego_medio_2 else None
                        ),
                        "fila": str(class_fila.__tablename__).split('_')[1].upper()
                    }

                    response.append(dict_fila)

        conn.commit()

    return response
        