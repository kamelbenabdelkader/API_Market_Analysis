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


# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

app = FastAPI()

# Load the pickled model
# model = pickle.load(open('model.pkl', 'rb'))

# Chargement du fichier pickle
with open('basket_pays.pkl', 'rb') as f:
    data_dict = pickle.load(f)


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


@app.get("/")
async def get_homes():
    return {"Hello": "la P21"}


@app.get("/france")
async def get_items_france():
    conn = connect()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM base_sql_basket WHERE Country = 'France'")
        results = cursor.fetchall()
    conn.close()
    return {"items": results}

@app.get("/portugal", response_model=List[BaseSqlBasket])
async def get_items_portugal():
    conn = connect()
    items = []
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM base_sql_basket WHERE Country = 'Portugal'")
        results = cursor.fetchall()
        for row in results:
            item = dict(zip(cursor.column_names, row))
            items.append(BaseSqlBasket(**item))
    conn.close()


@app.get("/{country}")
async def get_items_country(country: str):
    conn = connect()
    cursor = conn.cursor()

    # Requête SQL avec paramètre de pays
    query = """
        SELECT InvoiceNo, Description, SUM(Quantity) AS TotalQuantity
        FROM base_sql_basket
        WHERE Country = %s
        GROUP BY InvoiceNo, Description
    """

    # Exécution de la requête SQL avec le paramètre de pays
    cursor.execute(query, (country,))

    # Récupération des résultats de la requête
    results = cursor.fetchall()

    # Fermeture de la connexion à la base de données
    cursor.close()
    conn.close()

    # Retourne les résultats
    return {"items": results}

@app.get("/france")
async def get_items_france():
    conn = connect()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM base_sql_basket WHERE Country = 'France'")
        results = cursor.fetchall()
    conn.close()
    return {"items": results}


# @app.get("/country/{country}")
# async def get_items_country(country: str):
#     conn = connect()
#     with conn.cursor() as cursor:
#         cursor.execute(f"SELECT * FROM base_sql_basket WHERE Country = '{country}'")
#         results = cursor.fetchall()
#     conn.close()
#     return {"items": results}



# # Définition de la route de l'API
# @app.get("/data/{pays}")
# def get_data(pays: str):
#     if pays in data_dict:
#         data = data_dict[pays]
#         # Convertir DataFrame en dictionnaire JSON
#         data_dict_json = data.to_dict(orient="records")
#         # Sérialiser le dictionnaire en JSON
#         data_json = json.dumps(data_dict_json)
#         return data_json
#     else:
#         return {"error": "Pays non trouvé"}




# # 4. Run the API with uvicorn
# #    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
