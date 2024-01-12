from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import engine, Base
from middleware.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import user_router

app = FastAPI()
app.title = "VINOC"
app.version = '0.0.1'

app.add_middleware(ErrorHandler) # Se añade el middleware y se pasa el middleware que se va a ejecutar en la aplicación.

# Routers
app.include_router(user_router)
app.include_router(movie_router)

Base.metadata.create_all(bind=engine)

movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planteta llamado Pandora viven los Na'vi",
        'year': '2009',
        'rating': 7.8,
        'category': 'Suspenso'
    },
    {
        'id': 2,
        'title': 'Avatar 2',
        'overview': "En un exuberante planteta llamado Pandora viven los Na'vi",
        'year': 2022,
        'rating': 7.8,
        'category': 'Acción'
    },
    {
        'id': 3,
        'title': 'Avatar 3',
        'overview': "En un exuberante planteta llamado Pandora viven los Na'vi",
        'year': 2022,
        'rating': 7.8,
        'category': 'Suspenso'
    },
]


@app.get('/', tags=['Home'])
def message():
    return HTMLResponse('<h1>Hello World</h1>')
    # return {'Hello' : 'World'} 

