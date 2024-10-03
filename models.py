#from flask_sqlalchemy import SQLAlchemy
#from app import db
from extensions import db

#db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(80), nullable=False)
    fitness_level = db.Column(db.String(80), nullable=False)
    goals = db.Column(db.String(80), nullable=False)
    equipment = db.Column(db.String(80), nullable=False)
    availability = db.Column(db.String(80), nullable=False)
    health_limitations = db.Column(db.String(80), nullable=True)

    # reszta definicji klasy
