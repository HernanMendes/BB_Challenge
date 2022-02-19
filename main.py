from urllib import response
import requests
import json
from math import ceil

LIMITE = 50
PRIMER_PAG = 1
OK = 200
ERROR_NOT_FOUND = 404
JSON_FILE = 'data.json'

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
    args = { 'limit':LIMITE,'page': PRIMER_PAG }
    url_list = "https://yts.mx/api/v2/list_movies.json"
    url_comments = "https://yts.mx/api/v2/movie_comments.json?movie_id="
    url_details = "https://yts.mx/api/v2/movie_details.json?movie_id="
    
    response = requests.get(url_list, params=args)

    if response.status_code == OK:
        response_json = json.loads(response.text)       #Diccionario
        #print(response_json)
        ##print(type(json.dumps(response_json, indent=4)))
        ##print(response_json["data"]["movies"][1]["id"])

        total_pages = calcularPaginas(response_json)
        print("Total de paginas: "+str(total_pages))

        #for page in range (1,5):        #Uso este para hacer pruebas acotadas
        for page in range (1,total_pages+1):
            args["page"] = page
            response = requests.get(url_list, params=args)

            if response.status_code == OK:
                response_json = json.loads(response.text)
                contenidos = guardarPelicula(response_json,contenidos)

            print("Pagina "+str(page)+" leida.")

        ## El endpoint de "Movie Comments" devuelve Error 404 - Not Found, pero dejo comentada la logica que habia pensado
        '''
        for pelicula in contenidos:
            response = requests.get(url_comments+str(pelicula["id"]))
            
            if response.status_code == OK:
                response_json = json.loads(response.text)
                pelicula["comments"] = response_json["data"]["comments"]
            elif response.status_code == ERROR_NOT_FOUND:
                print("ERROR 404: NOT FOUND")
        '''
        for pelicula in contenidos:
            response = requests.get(url_details+str(pelicula["id"]))
            
            if response.status_code == OK:
                response_json = json.loads(response.text)
                pelicula["like_count"] = response_json["data"]["movie"]["like_count"]

            print("Pelicula "+str(pelicula["id"])+" leida.")

        ##print(json.dumps(contenidos, indent=4))

        with open(JSON_FILE, 'w') as file:
            json.dump(contenidos, file, indent=4)
