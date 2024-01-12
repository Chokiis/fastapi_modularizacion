from models.movie import Movie as MovieModel # Exportar el modelo Movie para utilizarse en métodos.
from schemas.movie import Movie

class MovieService():
    def __init__(self, db) -> None: # Cada vez que se llama este servicio, se envie una sesión a la base de datos.
        self.db = db # Se asigna lo que llega a la case de datos.
        
    def get_movies(self):
        result = self.db.query(MovieModel).all() # Hace una consulta a la base de datos con el modelo Movie.
        return result
    
    def get_movie(self, id): # Se pasa como parámetro el ida buscar.
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first() # Hace una consulta a la base de datos con el modelo Movie filtrado por el ID a buscar y trayendo el primer resultado que encuentre la consulta.
        return result
    
    def get_movie_by_category(self, category):
        result = self.db.query(MovieModel).filter(MovieModel.category == category).all()
        return result
    
    def create_movie(self, movie: Movie):
        new_movie = MovieModel(**movie.model_dump())
        self.db.add(new_movie)
        self.db.commit()
        return
    
    def update_movie(self, id: int, data: Movie): # Pasa el ID para hacer match con la base de datos y 'data' guarda los datos encontrados para ser modificados.
        movie = self.db.query(MovieModel).filter(MovieModel.id == id).first() 
        movie.title = data.title
        movie.overview = data.overview
        movie.year = data.year
        movie.rating = data.rating
        movie.category = data.category
        self.db.commit() # Guarda y actualiza datos.
        return
    
    def delete_movie(self, id: int):
        result = self.get_movie(id)
        self.db.delete(result)
        self.db.commit()
        return