# 1. Library imports
import uvicorn
from typing import List
from models import BaseSqlBasket
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
import pymysql
from urllib.parse import urlparse
from dotenv import load_dotenv
import os
import pickle
import pandas as pd

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

app = FastAPI()

# Load the pickled model
# model = pickle.load(open('model.pkl', 'rb'))


def connect():
    # Récupérer l'URL de la base de données à partir des variables d'environnement
    database_url = os.getenv("DATABASE_URL")

    # Extraire les composants de l'URL de la base de données
    url_components = urlparse(database_url)
    db_host = url_components.hostname
    db_user = url_components.username
    db_password = url_components.password
    db_name = url_components.path.strip('/')

    # Configurer la connexion à la base de données MySQL
    conn = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    return conn

# Petit test de co avec method get sur le home /
# @app.get("/")
# async def get_items() -> List[Data]:
#     # Effectuer des opérations sur la base de données
#     with conn.cursor() as cursor:
#         cursor.execute("SELECT * FROM data")
#         results = cursor.fetchall()

#     # Convertir les résultats en une liste d'objets Test a refacto par la suite
#     items = []
#     for row in results:
#         data_dict = {
#             "id": row[0],
#             "QUARTER" : row[1],
#             "MONTH" : row[2],
#             "DAY_OF_MONTH" : row[3],
#             "DAY_OF_WEEK": row[4],
#             "ORIGIN_AIRPORT_ID": row[5],
#             "DEST_AIRPORT_ID": row[6],
#             "DEP_TIME": row[7],
#             "ARR_TIME": row[8],
#             "VACATION": row[9]
#         }

#         data_user = Data(**data_dict)
#         items.append(data_user)

#     # Retourner les résultats de l'API
#     return items


@app.get("/")
async def get_homes():
    return {"Hello": "la P21"}


@app.get("/test")
async def get_items():
    conn = connect()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM base_sql_basket LIMIT 6")
        results = cursor.fetchall()
    conn.close()
    return {"items": results}


# # 4. Run the API with uvicorn
# #    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
