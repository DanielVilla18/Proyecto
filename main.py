"""
Imagina que es API es una biblioteca de peliculas
la funcion load_movies () es como una biblioteca que carga el catalogo del libros (peliculas)
la funcion get_movies () muestra todo el catalogo cuando alguien lo pide.
La funcion get_movie(id) es como si alguien preguntara por un libro en especifico, es decir por un codigo de identificacion
La funcion chatbot(query) es un asistente que busca peliculas segun palabras clave y sinonimo
La funcion get_movies_by_category(category) ayuda a encontrar peliculas segun su genero(accion, comedia, etc...)
"""

#Improtamos las herramientas necesarias para continuar nuestra API
from fastapi import FastAPI, HTTPException # FastAPI nos ayuda a crear la API, HTTPException nos ayuda a mostrar errores.
from fastapi.responses import HTMLResponse, JSONResponse #HTMLResponse nos ayuda a mostras respuesta en HTML y JSONResponse nos ayuda a mostras respuesta en JSON.
import pandas as pd #pandas nos ayuda a manejar datos en forma de tabla como si fuese un excel.
import nltk #nltk nos ayuda a procesar texto y analizar palabras.
from nltk.tokenize import word_tokenize #word_tokenize nos ayuda a tokenizar texto, es decir, a convertir texto en palabras.
from nltk.corpus import wordnet #wordnet nos ayuda a obtener sinonimos de una palabra.

#indicamos la ruta donde nltk buscara los datos descargados.
nltk.data.path.append('C:/Users/Tatiana/AppData/Roaming/nltk_data')     

# Descargamos las herramientas necesarias de nltk para el analisis de texto

nltk.download('punkt') #Es un paquete para dividir el texto en oraciones.
nltk.download('wordnet') #Es un paquete para obtener sinonimos de una palabras en ingles

# Funcion para cargar las peliculas desde un archivo csv

def load_movies():
    #Leemos el archivo que contiene la informacion de peliculas y seleccionamos las columnas que nos interesan
    df = pd.read_csv("Dataset/netflix_titles.csv")[['show_id', 'title','release_year','listed_in', 'rating', 'description']]

    # Renombramos las columnas para que sean mas faciles de entender
    df.columns = ['id', 'title','year','category', 'rating', 'overview']

    # Llenamos los espacios vacion con texto vacio y convertimos los datos en una lista de diccionarios
    return df.fillna('').to_dict(orient= 'records')

# Cargamos las peluclas al inciar la API para no leer el archivo cada vez que alguien pregunte por ellas
movies_list = load_movies()     

# Funcion para encontrar sinonimos de una palabra

def get_synonyms(word):
    # Usamos WordNet para encontrar palabras que significan lo mismo
    return{lemma.name().lower() for syn in wordnet.synsets(word) for lemma in syn.lemmas()}

# Creamos la aplicacion FastAPI, que sera el motor de nuestra API

app = FastAPI(title="Mi API de Peliculas", version ="1.0.0")

# Ruta de incio: cuando alguien acceda a la API sin especificar nada, se le mostrara un mensaje de bienvenida

@app.get('/', tags=['Home'])
def home():
    # Cuando entremos en el navegador a http://127.0.0.1:8000/ veremos un mensaje de bienvenida.
    return HTMLResponse('<h1>Bienvenido a mi API de Peliculas<h1>')

# Obteniendo la lista de peliculas
# Creamos uan ruta para obtener todas las peliculas

# Ruta para obtener todas las peliculas disponibles

@app.get('/movies', tags=['Movies'])
def get_movies():
    # Si hay peliculas las enviamos, si no mostramos un error
    return movies_list or HTTPException(status_code=500, detail="No hay datos de peliculas disponibles")


# Ruta para obtener una pelicula por su ID
@app.get('/movies/{id}', tags=['Movies'])
def get_movie(id: str):
    # Buscamos en la lista de peliculas la que tenga el mismo ID
    return next ((m for m in movies_list if m['id'] == id), {"detalle": "Pelicula no encontrada"})

# Ruta del chatbot que responde con peliculas segun palabras clave de la categoria
@app.get('/chatbot/', tags=['Chatbot'])
def chatbot(query: str):
    # Dividimos la consulta en palabras clave, para entender mejor la intencion del usuario
    query_words = word_tokenize(query.lower())
    
    
    # Buscamos sinonimos de las palabras clave para ampliar la busqueda
    synonyms = {word for q in query_word for word in get_synonyms(q)} | set(query_words)


    # Filtramos la lista de peliculas buscando coincidencias en la categoria 
    results = [m for m in movies_list if any(s in m['category'].lower() for s in synonyms)]

    # Si encontramos peliculas, enviaos la lista; si no, mostramos un mensaje que no se encontraron coincidencias
    
    return JSONResponse(content={
        "respuesta": "Aqui tienes algunas peliculas relacionadas." if results else "No se encontraron peliculas en esa categoria.",
        "peliculas": results
    })
    
# Ruta para buscar peliculas por categoria especifica

@app.get('/movies/', tags=['Movies'])
def get_movies_by_category(category: str):
    # Filtramos la lista de peliculas buscando coincidencias en la categoria
    return [m for m in movies_list if category.lower() in m['category'].lower()]





