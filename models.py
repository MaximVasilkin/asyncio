import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class SwapiPerson(Base):
    __tablename__ = 'StarWarsPersons'

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=False)
    birth_year = sq.Column(sq.String(length=20), nullable=False)
    eye_color = sq.Column(sq.String(length=30), nullable=False)
    films = sq.Column(sq.String(length=500), nullable=False)
    gender = sq.Column(sq.String(length=20), nullable=False)
    hair_color = sq.Column(sq.String(length=30), nullable=False)
    height = sq.Column(sq.String(length=10), nullable=False)
    homeworld = sq.Column(sq.String(length=100), nullable=False)
    mass = sq.Column(sq.String(length=10), nullable=False)
    name = sq.Column(sq.String(length=100), nullable=False)
    skin_color = sq.Column(sq.String(length=25), nullable=False)
    species = sq.Column(sq.String(length=500), nullable=True)
    starships = sq.Column(sq.String(length=500), nullable=True)
    vehicles = sq.Column(sq.String(length=500), nullable=True)
