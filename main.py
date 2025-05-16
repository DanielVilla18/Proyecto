"""
Imagina que es API es una biblioteca de peliculas
la funcion load_movies () es como una biblioteca que carga el catalogo del libros (peliculas)
la funcion get_movies () muestra todo el catalogo cuando alguien lo pide.
La funcion get_movie(id) es como si alguien preguntara por un libro en especifico, es decir por un codigo de identificacion
La funcion chatbot(query) es un asistente que busca peliculas segun palabras clave y sinonimo
La funcion get_movies_by_category(category) ayuda a encontrar peliculas segun su genero(accion, comedia, etc...)
"""

#Improtamos las herramientas necesarias para continuar nuestra API
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse #HTMLResponse nos ayuda a mostras respuesta en HTML y JSONResponse nos ayuda a mostras respuesta en JSON.
import pandas as pd #pandas nos ayuda a manejar datos en forma de tabla como si fuese un excel.
import nltk #nltk nos ayuda a procesar texto y analizar palabras.
from nltk.tokenize import word_tokenize #word_tokenize nos ayuda a tokenizar texto, es decir, a convertir texto en palabras.
from nltk.corpus import wordnet #wordnet nos ayuda a obtener sinonimos de una palabra.

#indicamos la ruta donde nltk buscara los datos descargados.
nltk.data.path.append('C:\Users\Tatiana\AppData\Roaming\nltk_data')
nltk.download('punkt')


