from typing import Union
from mangum import Mangum
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
import yaml
import os

app = FastAPI()
handler = Mangum(app)

# Cargamos la configuración desde el archivo YAML
with open('./config.yaml', "r") as config_file:
    config = yaml.load(config_file, Loader=yaml.FullLoader)

# Función para obtener la ruta del archivo JSON según el dominio
def get_json_path(request: Request):
   domain = request.url.netloc.split(".")[0]
   if domain in config.get("json_files", {}):
      json_path = config["json_files"][domain]
      return json_path
   else:
      return None

@app.get("/")
def read_root(request: Request):
   return {"Welcome to": "My first FastAPI deployment using Docker image", "url":request.url.netloc}

@app.get("/{text}")
def read_text(text: str, request: Request):
   json_path = get_json_path(request)
   
   if json_path is not None:
      if os.path.exists(json_path):
         with open(json_path, "r") as json_file:
               json_data = json_file.read()
         return JSONResponse({"result": text, "json_data": json_data})
      else:
         return JSONResponse(content={"error": "Archivo JSON no encontrado"}, status_code=404)
   else:
      return JSONResponse(content={"dominio": "No registrado"}, status_code=404)


@app.get("/items/{item_id}")
def read_item(item_id: int, request: Request, q: Union[str, None] = None):
   json_path = get_json_path(request)
   
   if json_path is not None:
      if os.path.exists(json_path):
         with open(json_path, "r") as json_file:
               json_data = json_file.read()
         return JSONResponse({"item_id": item_id, "q": q, "json_data": json_data})
      else:
         return JSONResponse(content={"error": "Archivo JSON no encontrado"}, status_code=404)
   else:
      return JSONResponse(content={"dominio": "No registrado"}, status_code=404)

if __name__ == "__main__":
   uvicorn.run(app, host="0.0.0.0", port=8080)
