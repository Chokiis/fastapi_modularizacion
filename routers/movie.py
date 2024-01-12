from fastapi import APIRouter
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middleware.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()

# CONSULTA DE DATOS CON UN QUERY A BASE DE DATOS.
@movie_router.get('/movies', tags = ['Movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies()-> List[Movie]:
    db = Session() # Instancia de la sesion.
    # result = db.query(MovieModel).all() # Se hace una consulta que obtiene todos los datos de ella con el metodo "all()" guardado en una variable llamada result.
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result)) # [Eliminado = content=movies] Se cambia el contenido convertido de result.

# FILTRADO DE DATOS HACIA BASE DE DATOS
@movie_router.get('/movies/{id}', tags=['Movies'], response_model=Movie)
def get_movie(id: int = Path(ge= 1, le=2000)) -> Movie:
    db = Session() # Instancia de la sesión
    # result = db.query(MovieModel).filter(MovieModel.id == id).first() # Hace una consulta mediante un filtro, en el que busca el id del MovieModel (de la bd) con el que ingresa el usuario y regresa el primer resultado encontrado.
    result = MovieService(db).get_movie(id) # Envía el ID al método de get_movie para su filtrado y retorna la información.
    if not result: # Si no hay resultados entonces:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

# FILTRADO DE DATOS HACIA BASE DE DATOS POR CATEGORIA
@movie_router.get('/movies/', tags=['Movies'], response_model=List[Movie])
def get_movie_by_category_filter(category: str = Query(min_length= 5, max_length= 15)) -> List[Movie]:
    db = Session()
    # result = db.query(MovieModel).filter(MovieModel.category == category).all()
    result = MovieService(db).get_movie_by_category(category)
    if not result:
        return JSONResponse(status_code=404, content={"message": "Category not found"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

#POST CON PYDANTIC Y CONEXIÓN A BASE DE DATOS
@movie_router.post('/movies/', tags=['Movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie)-> dict:
    db = Session() # db va a hacer una instancia de Sessión 
    # new_movie = MovieModel(**movie.model_dump()) # Pasa los datos como un diccionario y agregando '**' para pasarlos como parámetros guardado en una variable.
    # db.add(new_movie) # Agrega los nuevos datos a la base de datos con lo guardado en "new_movie".
    # db.commit() # Actualiza y guarda los datos.
    # movies.append(movie) # Se puede eliminar esta línea.
    MovieService(db).create_movie(movie)
    return JSONResponse(status_code=201, content={"Message": "Se ha registrado la película"})



## PUT CON PYDANTIC Y CONEXIÓN A BASE DE DATOS
@movie_router.put('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie)-> dict:
    db = Session()
    # result = db.query(MovieModel).filter(MovieModel.id == id).first() # Filtra los resultados por ID y los guarda.
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "No encontrado"})
    # result.title = movie.title # Asigna los nuevos resultados a 'result.title' y así consecutivamente.
    # result.overview = movie.overview
    # result.year = movie.year
    # result.rating = movie.rating
    # result.category = movie.category
    # db.commit() # Guarda y actualiza los cambios.
    MovieService(db).update_movie(id, movie)
    return JSONResponse(status_code=200, content={'message': "Se ha modificado la película exitosamente"})

# PUT CON PYDANTIC Y CONEXIÓN A BASE DE DATOS
@movie_router.delete('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
def delete_movie(id: int)-> dict:
    db = Session()
    # result = db.query(MovieModel).filter(MovieModel.id == id).first() # Filtra los resultados por ID y los guarda.
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "No encontrado"})
    # db.delete(result) # Elimina la película encontrada con el filtrado.
    # db.commit() # Guarda y actualiza los cambios.
    MovieService(db).delete_movie(id)
    return JSONResponse(status_code=200, content={'message': "Se ha eliminado la película exitosamente"})

########
#
#
#
# CODIGO UTILIZADO DURANTE EL CURSO DE FASTAPI | HISTORIAL DE CÓDIGO
#
#
#
########

## Sin utilizar la clase "Config".
# class Movie(BaseModel):
#     id: Optional[int] = None
#     title: str = Field(default='Mi película', min_length=5, max_length=15)
#     overview: str = Field(default='Descripción de la película', min_length=15, max_length=50)
#     year: int = Field(default=2022, le=2022)
#     rating: float
#     category: str

# @app.get('/movies', tags = ['Movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
# def get_movies()-> List[Movie]:
#     return JSONResponse(status_code=200, content=movies)



# FILTRADO DE DATOS
# @app.get('/movies/{id}', tags=['Movies'], response_model=Movie)
# def get_movie(id: int = Path(ge= 1, le=2000)) -> Movie:
#     for item in movies:
#         if item['id'] == id:
#             return JSONResponse(content=item)
#     return JSONResponse(status_code=404, content=[])

# @app.get('/movies/', tags=['Movies'])
# def get_movies_by_category(category: str, year: int):
    # return category

## POST SIN PYDANTIC
# @app.post('/movies/', tags=['Movies'])
# def create_movie(id: int, title: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
#     movies.append({
#         'id': id,
#         'title': title,
#         'overview': overview,
#         'year': year,
#         'rating': rating,
#         'category': category
#     })
#     return moviesimport DE DATOS:


## POST CON PYDANTIC
# @app.post('/movies/', tags=['Movies'], response_model=dict, status_code=201)
# def create_movie(movie: Movie)-> dict:
#     movies.append(movie)
#     return JSONResponse(status_code=201, content={"Message": "Se ha registrado la película"})

## PUT SIN PYDANTIC
# @app.put('/movies/{id}', tags = ['Movies'])
# def update_movie(id: int, title: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
#     for item in movies:
#         if item['id'] == id:
#             item['title'] = title
#             item['overview'] = overview
#             item['year'] = year
#             item['rating'] = rating
#             item['category'] = category
#             return movies

## PUT CON PYDANTIC
# @app.put('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
# def update_movie(id: int, movie: Movie)-> dict:
#     for item in movies:
#         if item['id'] == id:
#             item['title'] = movie.title
#             item['overview'] = movie.overview
#             item['year'] = movie.year
#             item['rating'] = movie.rating
#             item['category'] = movie.category
#             return JSONResponse(status_code=200, content={"Message": "Se ha modificado la película"})



# DELETE CON PYDANTIC
# @app.delete('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
# def delete_movie(id: int)-> dict:
#     for item in movies:
#         if item['id'] == id:
#             movies.remove(item)
#             return JSONResponse(status_code=200, content={"Message": "Se ha eliminado la película"})