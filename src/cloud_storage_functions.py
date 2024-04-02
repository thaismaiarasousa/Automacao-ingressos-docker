import json
from google.cloud import storage

def guardar_en_gcs(data,ruta_archivo):
    partes_ruta = ruta_archivo.split('/')
    
    nombre_bucket = partes_ruta[2]
    
    nombre_archivo = "/".join(partes_ruta[3:])
    
    cliente = storage.Client()
    
    bucket = cliente.bucket(nombre_bucket)
    
    archivo = bucket.blob(nombre_archivo)
    
    json_data = json.dumps(data)
    
    archivo.upload_from_string(json_data, content_type="application/json") # MIME Types

            
def leer_desde_gcs(ruta_archivo):
    # Ejemplo de ruta: gs://nombre_del_bucket/ruta/dentro/del/bucket/archivo.txt
    
    partes_ruta = ruta_archivo.split('/')
    
    nombre_bucket = partes_ruta[2]
    
    nombre_archivo = "/".join(partes_ruta[3:])
    
    cliente = storage.Client()
    
    bucket = cliente.bucket(nombre_bucket)
    
    archivo = bucket.blob(nombre_archivo)
    
    if not archivo.exists():
        return False
    
    contenido_archivo = archivo.download_as_string()
    
    return json.loads(contenido_archivo)
    

    