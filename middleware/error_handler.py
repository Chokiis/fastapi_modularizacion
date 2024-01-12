from starlette.middleware.base import BaseHTTPMiddleware, DispatchFunction, RequestResponseEndpoint
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

class ErrorHandler(BaseHTTPMiddleware): # ErrorHandle hereda de BaseHTTPMiddleware
    def __init__(self, app: FastAPI) -> None: # Requiere una aplicación, en este caso de FastAPI.
        super().__init__(app)
    
    # Pide un Request, para acceder a las peticiones de la aplicación.
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response | JSONResponse: # Se ejectuta para estar detectando si hay errores en la aplicación (es un método asíncrono)
        try:
            return await call_next(request) # En caso de que no haya ningún error, retornará la siguiente llamada.
        except Exception as e:
            return JSONResponse(status_code=500, content={'error': str(e)}) # Regresa una excepción de tipo Exception con el detalle del error.