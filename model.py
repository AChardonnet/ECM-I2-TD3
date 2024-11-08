from pony import orm
from data_model import Equipement, Animal, db

liste_etats = ["affamé", "fatigué", "repus", "endormi"]

db.bind(provider="sqlite", filename="animalerie.db")
db.generate_mapping()


def lit_etat(id_animal):
    with orm.db_session:
        try:
            return Animal[id_animal].etat_animal
        except:
            return None


def lit_lieu(id_animal):
    with orm.db_session:
        try:
            return Animal[id_animal].lieu_animal
        except:
            return None


def verifie_disponibilite(id_équipement):
    with orm.db_session:
        try:
            return Equipement[id_équipement].disponibilite
        except:
            return None


def cherche_occupant(id_équipement):
    with orm.db_session:
        try:
            return list(Equipement[id_équipement].animal)
        except:
            return []


def change_etat(id_animal, etat):
    etats_autorises = ["affamé", "fatigué", "repus", "endormi"]
    if etat not in etats_autorises:
        return
    with orm.db_session:
        try:
            Animal[id_animal].etat_animal = etat
        except:
            pass


def change_lieu(id_animal, id_équipement):
    equipements_autorises = ["litière", "mangeoire", "roue", "nid"]
    if id_équipement not in equipements_autorises:
        return
    if verifie_disponibilite(id_équipement) == "libre":
        with orm.db_session:
            try:
                Equipement[lit_lieu(id_animal).nom_equipement].disponibilite = "libre"
                if id_équipement != "litière":
                    print(f"not litière : {id_équipement}")
                    Equipement[id_équipement].disponibilite = "occupé"
                    orm.commit()
                Animal[id_animal].lieu_animal = Equipement[id_équipement]
                orm.commit()
            except Exception as e:
                print(e)
