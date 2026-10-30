from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import aiohttp

async def get_total_devices_and_their_disponibilities(usina_token, api_url, session):

        headers = {"x-api-key": usina_token, "accept": "application/json"}
        
        async with session.get(f"{api_url}/metrics/iot_performance", headers=headers) as requests:            
            devices_json = await requests.json()
            return devices_json["total_sensors"], devices_json["offline_sensors"]

async def get_total_off_sla_by_usina(usina_token, api_url, session) -> int:
        
        off_sla: list[dict] = list()
        now: datetime = datetime.now()
        thirteen_days_earlier: datetime = now - timedelta(days=8)
    
        timestamp_now: int = int(now.timestamp())
        timestamp_sde: int = int(thirteen_days_earlier.timestamp())
    
        headers: dict = {"x-api-key": usina_token, "accept": "application/json"}
        base_params: dict = {
            "start_time": timestamp_sde,
            "end_time": timestamp_now,
            "has_financial_return": "false",
            "group_by_spot": "false",
            "limit": 1000,
            "offset": 0,
        }

        response_closed = []
        response_pending = []

        async with session.get(f"{api_url}/diagnostics", headers=headers, params={**base_params, "status": "concluded"}) as requests_closed:
            response_closed = await requests_closed.json()
            response_closed_items = response_closed.get('items', [])

        async with session.get(f"{api_url}/diagnostics", headers=headers, params={**base_params, "status": "pending"}) as requests_pending:
            response_pending = await requests_pending.json()
            response_pending_items = response_pending.get('items', [])
    
        total_closed_duration = 0
        total_pending_duration = 0

        for alarm in response_closed_items:
            duration = alarm["end_time"] - alarm["start_time"]
            
            if duration > 36000:
                total_closed_duration += duration
                off_sla.append(alarm)
    
        for alarm_pending in response_pending_items:
            elapsed = timestamp_now - alarm_pending["start_time"]
            
            if elapsed > 36000:
                total_pending_duration += elapsed
                off_sla.append(alarm_pending)

        try:
            average_duration = (total_closed_duration + total_pending_duration) / len(off_sla)
        except Exception:
            average_duration = 0

        return len(off_sla), average_duration

async def get_data_iotebe_from_api() -> list[dict]:

    load_dotenv()
    
    response_dict: list[dict] = list()

    credentials: dict = {
        "USICODA": os.getenv("API_KEY_TEBE_USICODA"),
        "COMVAP": os.getenv("API_KEY_TEBE_COMVAP"),
        "GIASA": os.getenv("API_KEY_TEBE_GIASA")
    }

    api_url: str = os.getenv("URL_TEBE")

    async with aiohttp.ClientSession() as session:
        for key, value in credentials.items():
            usina = key
            off_sla, average_duration = await get_total_off_sla_by_usina(value, api_url, session)
            total_sensors, offline_sensors = await get_total_devices_and_their_disponibilities(value, api_url, session)
            online_sensors = total_sensors - offline_sensors

            horas = int(float(average_duration) // 3600)
            print('Passou', flush=True)
            minutos = int((float(average_duration) % 3600) // 60)
            segundos = int(float(average_duration) % 60)

            average_duration_in_hours_minute = f"{horas:02d}:{minutos:02d}"

            result_dict = {
                "usina": usina,
                "off_sla": off_sla,
                "online_sensors": online_sensors,
                "total_sensors": total_sensors,
                "media_atual_horas": average_duration_in_hours_minute
            }

            response_dict.append(result_dict)

    return response_dict


