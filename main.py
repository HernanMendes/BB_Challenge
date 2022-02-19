from urllib import response
import requests
import json
from math import ceil

LIMITE = 50
PRIMER_PAG = 1
OK = 200

# La funcion guardarPelicula() recorre todas las peliculas que llegaron en el response, guarda los datos 
# de cada pelicula en un diccionario y agrega cada diccionario a una lista donde estaran todos los contenidos

def guardarPelicula (response_json, contenidos):
    for i in range (LIMITE):
            movie = {}
            movie["id"] = response_json["data"]["movies"][i]["id"]
            movie["title"] = response_json["data"]["movies"][i]["title"]
            movie["year"] = response_json["data"]["movies"][i]["year"]
            movie["synopsis"] = response_json["data"]["movies"][i]["synopsis"]
            movie["url"] = response_json["data"]["movies"][i]["url"]
            try:
                movie["genres"] = response_json["data"]["movies"][i]["genres"]
            except KeyError:
                movie["genres"] = []
            contenidos.append(movie)

    return contenidos

# Con el movie_count y el limite de paginas por consulta calculamos cuantas paginas deberemos consultar en total

def calcularPaginas (response_json):
    movie_count = response_json["data"]["movie_count"]
    limit = response_json["data"]["limit"]
    total_pages = ceil(movie_count/limit)

    return total_pages

if __name__ == '__main__':
    contenidos = []
    url_list = "https://yts.mx/api/v2/list_movies.json"
    args = { 'limit':LIMITE,'page': PRIMER_PAG }

    response = requests.get(url_list, params=args)

    if response.status_code == OK:
        response_json = json.loads(response.text)       #Diccionario
        #print(response_json)
        ##print(type(json.dumps(response_json, indent=4)))
        ##print(response_json["data"]["movies"][1]["id"])

        total_pages = calcularPaginas(response_json)
        print("Total de paginas: "+str(total_pages))

        for page in range (total_pages):
            args["page"] = page
            response = requests.get(url_list, params=args)

            if response.status_code == OK:
                response_json = json.loads(response.text)
                contenidos = guardarPelicula(response_json,contenidos)

            print("Pagina "+str(page)+" leida.")

        print(json.dumps(contenidos, indent=4))
