# Curso de FastAPI: Base de Dato y Modularización.

### ¿Qué se verá en la sesión?
- Conexión a Base de Datos.
- Modularización.
- Despliegue.

### Estructura de la aplicación.
    config/
    middleware/
    models/
    routers/
    services/
    schemas/
    main.py
    __init__.py

### Conocimientos previos para iniciar el curso:
- Curso de Introducción a FastAPI.
- Curso de Fundam entos de Base de Datos.
- Curso de Git y GitHub.

### ¿Qué es un ORM?
Es una librería que nos permite la manipulación de tablas de una base de datos como si fueran objetos de nuestra aplicación.

### ¿Qué es el ORM SQLAlchemy?
Es una librería para Python que facilita el acceso a una base de datos relacional mapeando tablas SQL a clases.

## Instalación y configuración de SQLAlchemy
Se recomienda la instalación de una extensión que nos ayude a gestionar nuestra base de datos, la extensión se nombra "SQLite Viewer" (link: https://marketplace.visualstudio.com/items?itemName=qwtel.sqlite-viewer).

### Instalar el módulo SQLAlchemy.
* En terminal ejecutar el siguiente comando de instalación.
    ```shell
    pip install sqlalchemy
    ```
## Crear una carpeta.
Se recomienda seguir la estructura de carpetas para una mejor gestión de la app, para ello se recomienda crear una carpeta "config" en el mismo nivel en donde se ubica el archivo "main.py"

- Dentro de la misma carpeta, se crean los siguientes archivos:
    ```shell
    __init__.py
    database.py
    ```
- Dentro del archivo "database.py" crear la siguiente sintaxis:
    ```python
    import os # Esta librería ayuda a acceder al sistema de archivos, manipular y obtener información.
    from sqlalchemy import create_engine
    from sqlalchemy.orm.session import sesionmaker
    from sqlalchemy.ext.declarative import declarative_base

    # Nombre de la base de datos
    sqlite_file_name = "database.sqlite"

    # Es el directorio del archivo database.py
    base_dir = os.path.dirname(os.path.realpath(__file__)) 

    # Es la forma en la que se conecta a una base de datos.
    database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}" 

    # Representa el motor de la base de datos.
    # Con el comando echo=True se muestra por consola lo que está realizando.
    engine = create_engine(database_url, echo=True)

    # Se crea una Session y se enlaza a la base de datos a través del comando bind.
    Session = sessionmaker(bind=engine)

    # Sirve para manipular las tablas de la base de datos.
    Base = declarative_base()
    ```
Para continuar con la configuración, se necesita crear una carpeta llamada "models" para guardar nuestros modelos de base de datos, se crea en el mismo nivel que "main.py" y crear su priorio archivo ini,py en la carpeta.

- Posteriormente se van a crear los siguientes archivos en la carpeta "models":
    ```
    movie.py
    __init__.py
    ```

* Dentro del archivo "movie.py" crear una clase con las siguientes características.

    ```python
    from config.database import Base
    from sqlalchemy import Column, Integer, String, Float

    # Movie hereda de Base
    class Movie(Base):
        
        # Nombre de la tabla.
        __tablename__ = "movies"
        
        # Columnas de la tabla.
        id = Column(Integer, primary_key = True)
        title = Column(String)
        overview = Column(String)
        year = Column(Integer)
        rating = Column(Float)
        category = Column(String)
    ```
- Y en el archivo main, se tiene que importar las clases que se acaban de crear (como Movie) y el archivo de la base de datos para que pueda crear la tabla, para ello se agrega lo siguiente a main:

    ```python
    from config.database import Session, engine, Base
    from models.movie import Movie
    
    Base.metadata.create_all(bind=engine)
    ```

- Al inciar el servidor, se muestra la tabla ya creada con las configuraciones previamente hechas.
    ![](https://i.imgur.com/45C8FIN.png)

## Registro de datos.

Al momento de importar la clase Movie del archivo models.movie, para que no haya confusión, es necesario cambiar de nombre la clase importada.

* Se cambia el nombre de la clase a "MovieModel" agregando *"as [NUEVO NOMBRE]"* de la siguiente manera:

    ```python
    from models.movie import Movie as MovieModel

    ```
* Se trae la siguiente ruta para insertar datos a la tabla previamente creada:
    ```python
    from config.database import Session, engine, Base
    from models.movie import Movie as MovieModel

    @app.post('/movies/', tags=['Movies'], response_model=dict, status_code=201)
    def create_movie(movie: Movie)-> dict:
        db = Session() # db va a hacer una instancia de Sessión
        new_movie = MovieModel(**movie.dict()) # Pasa los datos como un diccionario y agregando '**' para pasarlos como parámetros guardado en una variable.
        db.add(new_movie) # Agrega los nuevos datos a la base de datos con lo guardado en "new_movie".
        db.commit() # Actualiza y guarda los datos.
        # movies.append(movie) # Se puede eliminar esta línea.
        return JSONResponse(status_code=201, content={"Message": "Se ha registrado la película"})
    ```
## Consulta de datos.
De igual manera, agregaremos nuevas características a nuestro método GET para obtener alguna película mediante el uso de consultas a la base de datos.

* Importar desde la libreria "fastapi.encoders" la clase "jsonable_encoder".
```python
    from fastapi.encoders import jsonable_encoder
```
* Modificar el metodo get para aplicar los cambios.
    ```python
    @app.get('/movies', tags = ['Movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
    def get_movies()-> List[Movie]:
        db = Session() # Instancia de la sesion.
        result = db.query(MovieModel).all() # Se hace una consulta que obtiene todos los datos de ella con el metodo "all()" guardado en una variable llamada result.
        return JSONResponse(status_code=200, content=jsonable_encoder(result)) # [Eliminado = content=movies] Se cambia el contenido convertido.
    ```

### Consulta por filtrado ID.
Los cambios por filtrado ID se aplicaran sobre el método GET con ID.

* Se aplica lo siguiente:
    ```python
    @app.get('/movies/{id}', tags=['Movies'], response_model=Movie)
    def get_movie(id: int = Path(ge= 1, le=2000)) -> Movie:
        db = Session() # Instancia de la sesión
        result = db.query(MovieModel).filter(MovieModel.id == id).first() # Hace una consulta mediante un filtro, en el que busca el id del MovieModel (de la bd) con el que ingresa el usuario y regresa el primer resultado encontrado.
        if not result: # Si no hay resultados entonces:
            return JSONResponse(status_code=404, content={'message': "No encontrado"})
        # for item in movies:
        #     if item['id'] == id:
        #         return JSONResponse(content=item) # Se puede eliminar el filtrado anterior.
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    ```
* Ahora con la ruta de categorias:
    ```python
    @app.get('/movies/', tags=['Movies'], response_model=List[Movie])
    def get_movie_by_category_filter(category: str = Query(min_length= 5, max_length= 15)) -> List[Movie]:
        db = Session() # Instancia de la sesión
        result = db.query(MovieModel).filter(MovieModel.category == category).all() # Filtra por categoria.
        if not result:
            return JSONResponse(status_code=404, content={"message": "Category not found"}) # SI no encuentra nada, regresa un mensaje y un código de estatus.
        return JSONResponse(status_code=200, content=jsonable_encoder(result)) # Regresa la lista de películas.
    ```
## Modificación y eliminación de datos
Al saber cómo agregar nuevos elementos a la base de datos, ahora es fundamental eliminar y modificar datos en caso de tener cambios, para ello se aplicarán en las rutas PUT y DELETE.

* Ruta PUT:
    ```python
    @app.put('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
    def update_movie(id: int, movie: Movie)-> dict:
        db = Session()
        result = db.query(MovieModel).filter(MovieModel.id == id).first() # Filtra los resultados por ID y los guarda.
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        result.title = movie.title # Asigna los nuevos resultados a 'result.title' y así consecutivamente.
        result.overview = movie.overview
        result.year = movie.year
        result.rating = movie.rating
        result.category = movie.category
        db.commit() # Guarda y actualiza los cambios.
        return JSONResponse(status_code=404, content={"message": "No encontrado"})
    ```
* Ruta DELETE:
    ```python
    @app.delete('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
    def delete_movie(id: int)-> dict:
        db = Session()
        result = db.query(MovieModel).filter(MovieModel.id == id).first() # Filtra los resultados por ID y los guarda.
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        db.delete(result) # Elimina la película encontrada con el filtrado.
        db.commit() # Guarda y actualiza los cambios.
        return JSONResponse(status_code=200, content={'message': "Se ha eliminado la película exitosamente"})
    ```
## Manejo de errores
Es un Middleware que estará detectando si ocurre errores en la aplicación en general.
- Para implementarlo, se recomienda crear una carpeta que se llame "middleware" para crear las configuraciones específicas del módulo, en el que va a contener los siguientes archivos:
    ```shell
    middleware/__init__.py
    middleware/error_handler.py
    ```
* Para error se agregarán librerías para manejar los errores que puedan ocurrir en el sistema.
    ```python
    from starlette.middleware.base import BaseHTTPMiddleware, DispatchFunction, RequestResponseEndpoint
    from fastapi import FastAPI, Request, Response
    from fastapi.responses import JSONResponse

    class ErrorHandle(BaseHTTPMiddleware): # ErrorHandle hereda de BaseHTTPMiddleware
        def __init__(self, app: FastAPI) -> None: # Requiere una aplicación, en este caso de FastAPI.
            super().__init__(app)
        
        # Pide un Request, para acceder a las peticiones de la aplicación.
        async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response | JSONResponse: # Se ejectuta para estar detectando si hay errores en la aplicación (es un método asíncrono)
            try:
                return await call_next(request) # En caso de que no haya ningún error, retornará la siguiente llamada.
            except Exception as e:
                return JSONResponse(status_code=500, content={'error': str(e)}) # Regresa una excepción de tipo Exception con el detalle del error.
    ```
Para verificar si funciona, utilizamos de ejemplo el método GET para obtener una lista.
* Ejemplo:
    ```python
    @app.get('/movies/{id}', tags=['Movies'], response_model=Movie)
    def get_movie(id: int = Path(ge= 1, le=2000)) -> Movie:
        db = Session # Se eliminan los paréntesis para generar un error y mostrar sus resultados.
        result = db.query(MovieModel).filter(MovieModel.id == id).first()
        if not result:
            return JSONResponse(status_code=404, content={'message': "No encontrado"})
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    ```
* Arroja el siguiente error al momento de realizar una consulta: 
![](https://i.imgur.com/lwLTmR9.png)
> Error generado por los paréntesis faltantes, arroja un error de tipo "sessionmaker".

Para mejor organización, se recomienda mudar el código de la autenticación JWT a la carpeta'middleware', por lo que quedaría de la siguiente manera:

* Crear un archivo que se llame "jwt_beareer.py" que contenga lo siguiente:
    ```python
    from fastapi.security import HTTPBearer
    from fastapi import Request, HTTPException
    from jwt_manager import create_token, validate_token

    # Código extraído directamente del archivo main.py
    class JWTBearer(HTTPBearer):
        async def __call__(self, request: Request):
            auth = await super().__call__(request)
            data = validate_token(auth.credentials)
            if data['email'] != "admin@gmail.com":
                raise HTTPException(status_code=403, detail="Credenciales son inválidas")
    ```
* Y en el archivo "main.py" agregar la importación para que la aplicación siga funcionando con normalidad.
    ```python
    from middleware.jwt_bearer import JWTBearer
    ```

## Creación de routers.
Ayuda a la división de la aplicación por módulos utilizando routers, diviendo todo en diferentes archivos sin tener uno solo. Es necesario crear un directorio nuevo con el nombre 'routers' donde llevará los archivos ```__init__.py``` y ```movie.py```.

* En el archivo ```movie.py``` llevará el siguiente contenido.
```python
    from fastapi import APIRouter # Importar la clase APIRouter

    movie_router = APIRouter() # Contiene la instancia de APIRouter.

    # IMPORTAR TODAS LAS RUTAS QUE SEAN "/movie" AL ARCHIVO (incluido el BaseModel), EJEMPLO:
    # CONSULTA DE DATOS CON UN QUERY A BASE DE DATOS.
    # REEMPLAZAR "@app" por "movie_router".
    @movie_router.get('/movies', tags = ['Movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
    def get_movies()-> List[Movie]:
        db = Session() # Instancia de la sesion.
        result = db.query(MovieModel).all() # Se hace una consulta que obtiene todos los datos de ella con el metodo "all()" guardado en una variable llamada result.
        return JSONResponse(status_code=200, content=jsonable_encoder(result)) # [Eliminado = content=movies] Se cambia el contenido convertido de result.

    # FILTRADO DE DATOS HACIA BASE DE DATOS
    @movie_router.get('/movies/{id}', tags=['Movies'], response_model=Movie)
    def get_movie(id: int = Path(ge= 1, le=2000)) -> Movie:
        db = Session # Instancia de la sesión
        result = db.query(MovieModel).filter(MovieModel.id == id).first() # Hace una consulta mediante un filtro, en el que busca el id del MovieModel (de la bd) con el que ingresa el usuario y regresa el primer resultado encontrado.
        if not result: # Si no hay resultados entonces:
            return JSONResponse(status_code=404, content={'message': "No encontrado"})
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    # Etc..
```
Replicar lo mismo para la gestión de usuarios creando un nuevo archivo e importando el archivo al ```main.py```
```python
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from jwt_manager import create_token

user_router = APIRouter()

class User(BaseModel):
    email: str
    password: str
    
@user_router.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.model_dump())
        return JSONResponse(status_code=200, content=token)
```

* Y en el archivo ```main.py``` llamar el router 'movie' y 'user:
```python
    from routers.movie import movie_router
    from routers.user import user_router

    # Routers
    app.include_router(user_router)
    app.include_router(movie_router)
```


## Servicios para consultar datos
Los servicios apoyan a la separación de la lógica de los routers para comprender mejor el código de la app.
Se recomienda crear un nuevo directorio 'services' y sus respectivos archivos ```__init__.py``` y los archivos que acompañara el directorio (```movies.py```, ```user.py```).
* En el archivo ```movies.py``` del directorio previamente creado, crear un constructor que haga sesiones a la base de datos para hacer consultas y obtener la información requerida.
    ```python
    from models.movie import Movie as MovieModel # Exportar el modelo Movie para utilizarse en métodos.

    class MovieService():
        def __init__(self, db) -> None: # Cada vez que se llama este servicio, se envie una sesión a la base de datos.
            self.db = db # Se asigna lo que llega a la case de datos.
            
        def get_movies(self):
            result = self.db.query(MovieModel).all() # Hace una consulta a la base de datos con el modelo Movie.
            return result
    ``` 
* Ahora en el archivo "movie" del directorio "router" importar el servicio creado anteriormente.
    ```python
    from services.movie import MovieService

    # Y SOBRE LA RUTA GET, CAMBIAR CÓMO SE REALIZA LA CONSULTA CON LA NUEVA CLASE.
    @movie_router.get('/movies', tags = ['Movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
    def get_movies()-> List[Movie]:
        db = Session()
        # result = db.query(MovieModel).all() # ELIMINAR LA ANTERIOR CONSULTA
        result = MovieService(db).get_movies() # NUEVA CONSULTA, donde se llama la clase MovieService, con la sesión a la base de datos y con el método "get_movies" obtener los datos requeridos.
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    ```
### Filtrado con ID utilizando la clase MovieService.
Igual que el ejemplo anterior, se crea una nueva función que realice el filtrado de información por ID y llamar dicha función al router get con ID para realizar una búsqueda en especifico.
```python
    from models.movie import Movie as MovieModel

    def get_movie(self, id): # Pasa ID como parámetro.
        result = self.db.query(MovieModel).filter(id).all() # Se agrega el método "filter()" donde pasa como parámetro el ID y con "all()" trae todos los datos,
        return result
```
* Ahora en el archivo "Movie" del directorio 'routers', cambiar la lógica de búsqueda por la función creada previamente.
    ```python
        @movie_router.get('/movies/{id}', tags=['Movies'], response_model=Movie)
        def get_movie(id: int = Path(ge= 1, le=2000)) -> Movie:
            db = Session()
            # result = db.query(MovieModel).filter(MovieModel.id == id).first() # ELIMINAR LA ANTERIOR CONSULTA CON FILTRO.
            result = MovieService(db).get_movie(id) # NUEVA CONSULTA, DONDE PASA COMO PARÁMETRO EL ID PARA FILTRAR.
            if not result:
                return JSONResponse(status_code=404, content={'message': "No encontrado"})
            return JSONResponse(status_code=200, content=jsonable_encoder(result))
    ```
### Filtrado POR CATEGORÍA utilizando la clase MovieService.
Igual que el ejemplo anterior con ID, se crea otra nueva función que realice el filtrado de información utilizando texto para hacer una consulta a la base de datos.
```python
    from models.movie import Movie as MovieModel

    def get_movie_by_category(self, category): # Pasa el str(category) como parámetro.
        result = self.db.query(MovieModel).filter(MovieModel.category == category).all()
        return result
```
* Igual que con la función con ID, cambiar la lógica de búsqueda en el método GET con filtro.
    ```python
    @movie_router.get('/movies/', tags=['Movies'], response_model=List[Movie])
    def get_movie_by_category_filter(category: str = Query(min_length= 5, max_length= 15)) -> List[Movie]:
        db = Session()
        # result = db.query(MovieModel).filter(MovieModel.category == category).all() # ELIMINAR LA ANTERIOR CONSULTA CON FILTRO.
        result = MovieService(db).get_movie_by_category(category) # NUEVA CONSULTA, DONDE PASA COMO PARÁMETRO LA CATEGORÍA (category). 
        if not result:
            return JSONResponse(status_code=404, content={"message": "Category not found"})
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    ```
## Servicios para registrar y modificar datos.
Se crearán esquemas para la gestión de nuestros datos más ordenadas, para ello se crea una carpeta dedicada a los esquemas a utilizar, en el caso de esta app, se crea lo siguiente: directorio ```schemas/``` con sus archivos ```__init__.py```, ```movie.py```, ```user.py``` 

Será necesario mudar todos los modelos a los schemas, por lo que quedarán de la siguiente manera:
* ```movie.py:```
    ```python
    from pydantic import BaseModel, Field
    from typing import Optional

    ## Utilizando la clase "Config".
    class Movie(BaseModel):
        id: Optional[int] = None
        title: str = Field(min_length=5, max_length=15)
        overview: str = Field(min_length=15, max_length=50)
        year: int = Field(le=2022)
        rating: float = Field(ge=1, le=10)
        category: str = Field(min_length=5, max_length=15)

        model_config = {
            "json_schema_extra": {
                "examples": [
                    {
                        "id": 1,
                        "title": "Mi película",
                        "overview": "Descripción de la película",
                        "year": 2022,
                        "rating": 9.9,
                        "category": "Acción",
                    }
                ]
            }
        }
    ```
* Al tener el esquema listo de movies, será necesario crear una función para crear una película en servicios, por lo que se agregará el siguiente código en ```services/movie.py```:
    ```python
        from schemas.movie import Movie

        def create_movie(self, movie: Movie): # Parámetros de la película importado desde esquemas.
        new_movie = MovieModel(**movie.model_dump())
        self.db.add(new_movie)
        self.db.commit()
        return
    ```

* Después, se importa el esquema y se modificará el método 'create_movie' con la nueva lógica en ```routers/movie.py```:
    ```python
    from schemas.movie import Movie
    
    def create_movie(movie: Movie)-> dict:
    db = Session() # db va a hacer una instancia de Sessión 
    # new_movie = MovieModel(**movie.model_dump()) # SE PUEDE ELIMINAR.
    # db.add(new_movie) # SE PUEDE ELIMINAR.
    # db.commit() # SE PUEDE ELIMINAR
    MovieService(db).create_movie(movie) # Desde esquemas importa la lógica y así crea la película.
    return JSONResponse(status_code=201, content={"Message": "Se ha registrado la película"})
    ```
## Modificar datos
Definir un nuevo método en ```services/movie.py```:
```python
    def update_movie(self, id: int, data: Movie): # Pasa el ID para hacer match con la base de datos y 'data' guarda los datos encontrados para ser modificados.
        movie = self.db.query(MovieModel).filter(MovieModel.id == id).first() 
        movie.title = data.title
        movie.overview = data.overview
        movie.year = data.year
        movie.rating = data.rating
        movie.category = data.category
        self.db.commit() # Guarda y actualiza datos.
        return
```

Posteriormente, en el archivo ```routers/movie.py``` será necesario importar lo previamente creado, cambiando la lógica del método.
```python
    @movie_router.put('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
    def update_movie(id: int, movie: Movie)-> dict:
        db = Session()
        # result = db.query(MovieModel).filter(MovieModel.id == id).first() SE PUEDE ELIMINAR
        result = MovieService(db).get_movie
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        MovieService(db).update_movie(id, movie) # Pasa el ID y la data que se guarda en "movie: Movie".
        return JSONResponse(status_code=200, content={'message': "Se ha modificado la película exitosamente"})
```
* De igual manera para eliminar una película, es necesario crear otra función con el método de eliminar:
    ```python
    def delete_movie(self, id: int):
        result = self.get_movie(id)
        self.db.delete(result)
        self.db.commit()
        return
    ```
* Y cambiar la lógica en el archivo ```routers/movie.py```:
    ```python
    @movie_router.delete('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
    def delete_movie(id: int)-> dict:
        db = Session()
        # result = db.query(MovieModel).filter(MovieModel.id == id).first() # SE PUEDE ELIMINAR
        result = MovieService(db).get_movie(id)
        if not result:
            return JSONResponse(status_code=404, content={"message": "No encontrado"})
        # result.title = movie.title # SE PUEDE ELIMINAR
        # result.overview = movie.overview # SE PUEDE ELIMINAR
        # result.year = movie.year # SE PUEDE ELIMINAR
        # result.rating = movie.rating # SE PUEDE ELIMINAR
        # result.category = movie.category # SE PUEDE ELIMINAR
        # db.commit() # SE PUEDE ELIMINAR
        return JSONResponse(status_code=200, content={'message': "Se ha eliminado la película exitosamente"})
    ```
## Preparación del proyecto a producción
Se recomienda guardar el archivo ```jwt_manager.py``` a un nuevo directorio llamado ```utils```. Una vez que el archivo se encuentre en su nuevo directorio, será necesario excluir archivos antes de subir el proyecto a producción, como los archivos que guardan la caché, base de datos, entre otros.

* Para ello, se crea un archivo ```.gitignore``` agregando los archivos/carpeta que no se deseen subir a un repositorio. Se recomienda agregar archivos como: ```__pycache__```, ```venv/``` y ```database.sqlite``` (par evitar subir datos comprometidos de la base de datos).

Se creará un archivo que contendrá todos los módulos creados previamente para la aplicación a un nuevo archivo de requerimientos.
* Se hace lo siguiente:
    ```python
        pip freeze > requirements.txt
    ```
Al ejecutar el comando, se habrá creado un nuevo archivo con todo lo que se utilizó en el curso, el cual va a ser necesario de instalar para construir la aplicación.

![](https://i.imgur.com/FSHtKn1.png)
> Módulos requeridos para el levantamiento de la aplicación y versión compatible con ella.