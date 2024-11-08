import json
import os

from pony import orm
from data_model import Equipement, Animal, db


def create_db():
    db.bind(provider="sqlite", filename="animalerie.db", create_db=True)
    db.generate_mapping(create_tables=True)

    équipement_data = r"orig\equipment.json"
    with open(équipement_data, "r") as f:
        equipement_dict = json.load(f)
        for nom_equipement in equipement_dict:
            disponibilite = equipement_dict[nom_equipement]["DISPONIBILITÉ"]
            with orm.db_session:
                try:
                    Equipement(
                        nom_equipement=nom_equipement, disponibilite=disponibilite
                    )
                    orm.commit()
                except:
                    print(nom_equipement, "already exists in database")
                    pass

    animal_data = r"orig\animal.json"
    with open(animal_data, "r") as f:
        animal_dict = json.load(f)
        for id_animal in animal_dict:
            etat = animal_dict[id_animal]["ETAT"]
            type = animal_dict[id_animal]["TYPE"]
            race = animal_dict[id_animal]["RACE"]
            lieu = animal_dict[id_animal]["LIEU"]
            with orm.db_session:
                try:
                    Animal(
                        nom_animal=id_animal,
                        etat_animal=etat,
                        type_animal=type,
                        race_animal=race,
                        lieu_animal=Equipement[lieu],
                    )
                    orm.commit()
                except:
                    print(id_animal, "already exists in database")
                    pass


if os.path.isfile("animalerie.db"):
    os.remove("animalerie.db")
create_db()
