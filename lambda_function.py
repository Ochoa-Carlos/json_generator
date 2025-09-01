import os  

import sys
import traceback

from json_generator_disp import json_builder

sys.argv.append({'errores': {}})  # type: ignore
sys.argv.append({"global": {"entregas": 0, "recepciones": 0}})  # type: ignore

def lambda_handler(event, context):
    try:
        path = ''
        grupo = ''
        
        if "grupo" in event['params']['path']:
            path = event['context']['resource-path'].split("/")[2]
            grupo = event['params']['path']['grupo']
        else:
            path = event['context']['resource-path'].split("/")[1]
            grupo = event['context']['groups']
        
        print(f'Grupo >{grupo}<')
        
        rutas = {
            "autocar_cancun": json_builder,
        }
        
        if grupo in rutas:
            res = rutas[grupo](event, context)
            return res
        else:
            return {
                'statusCode': 400,
                'body': f"grupo no encontrado"
            }
        
    except Exception as e:
        traceback.print_exc()
        
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        
        grupo = context.log_stream_name
        idrequest = context.aws_request_id
        
        return {
            'statusCode': 400,
            'body': f"Se produjo un error desconocido, póngase en contacto con su asesor. Para agilizar la resolución de este inconveniente comparta los siguientes datos a su asesor. Grupo {grupo} - id {idrequest}"
        }
