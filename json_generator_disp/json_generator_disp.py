import sys
import os
from json_generator_disp.services import JsonBuilder
from json_generator_disp.helpers.logger import logger

logging = logger()

def json_builder(event, context):
    parametrosURL = event["params"]["querystring"]
    parametrosBody = event["body-json"]
    metodo = event["context"]["http-method"]
    grupo = ""

    if "grupo" in event["params"]["path"]:
        grupo = event["params"]["path"]["grupo"]
    else:
        grupo = event["context"]["groups"]

    grupo = "icave_p"
    if "mes" in parametrosURL:
        fecha = parametrosURL["mes"] + "-01"
        sys.argv[2]["global"]["userDb"] = grupo
        monthly_json = JsonBuilder(db_name=grupo, date=fecha)
        monthly_json = monthly_json.build_monthly_json()
        return monthly_json

    if "dia" in parametrosURL:
        fecha = parametrosURL["dia"]
        sys.argv[2]["global"]["userDb"] = grupo
        daily_json = JsonBuilder(db_name=grupo, date=fecha)
        daily_json = daily_json.build_daily_json()
        return daily_json

    return {"statusCode": 400, "body": "Parametros no encontrados"}