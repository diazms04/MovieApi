from fastapi import APIRouter
from fastapi import Path, Query, Depends
from fastapi.responses import JSONResponse
from typing import List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService 
from schemas.movie import Movie

movie_router = APIRouter()



@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(content=jsonable_encoder(result))

#Parametros de ruta
@movie_router.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(content={'message': "No encontrado"})
    return JSONResponse(content=jsonable_encoder(result))

#Parametros query
@movie_router.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies_by_category(category)
    if not result:
        return JSONResponse(content={'message': "Category No encontrado"})
    return JSONResponse(content=jsonable_encoder(result))

#Metodo post
"""
@app.post('/movies', tags=['movies'])
def create_movie(id: int = Body(), title: str = Body(), overview:str = Body(), year:int = Body(), rating:float = Body(), category:str = Body()):
    movies.append({
        "id": id,
        "title": title,
        "overview": overview,
        "year": year,
        "rating": rating,
        "category": category,
    })
    return movies

"""
@movie_router.post('/movies', tags=['movies'], response_model=dict)
def create_movie(movie: Movie) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)
    return JSONResponse(content={"message": "Se ha registrado la pelicula"})


#Metodo put
@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(content={'message': "No encontrado"})
    MovieService(db).update_movie(id, movie)
    return JSONResponse(content={"message": "Se ha modificado la pelicula"})

@movie_router.delete('/movies/{id}', tags=['movies'],response_model=dict)
def delete_movie(id:int) -> dict:
    db = Session()
    result : MovieModel = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(content={'message': "No encontrado"})
    MovieService(db).delete_movie(id)
    return JSONResponse(content = {'message': "Se ha eliminado la pelicula"})
