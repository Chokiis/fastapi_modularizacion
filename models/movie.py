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