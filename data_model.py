from pony import orm
import numpy as np
import pandas

db = orm.Database()


class Equipement(db.Entity):
    nom_equipement = orm.PrimaryKey(str)
    disponibilite = orm.Required(str)
    animal = orm.Set("Animal")


class Animal(db.Entity):
    nom_animal = orm.PrimaryKey(str)
    race_animal = orm.Required(str)
    type_animal = orm.Required(str)
    etat_animal = orm.Required(str)
    lieu_animal = orm.Required("Equipement")
