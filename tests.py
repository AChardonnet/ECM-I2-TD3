import model
import controleur
from data_model import orm, Equipement, Animal

##Before running the tests, make sure to reset the database by running the following file: import_data_animalerie.py


def test_lit_etat():
    assert model.lit_etat("Tac") == "affamé"
    assert model.lit_etat("Bob") == None


@orm.db_session
def test_lit_lieu():
    assert model.lit_lieu("Tac") == Equipement["litière"]
    assert model.lit_lieu("Bob") == None


def test_verifie_disponibilite():
    assert model.verifie_disponibilite("litière") == "libre"
    assert model.verifie_disponibilite("mangeoire") == "occupé"
    assert model.verifie_disponibilite("nintendo") == None


@orm.db_session
def test_cherche_occupant():
    assert Animal["Totoro"] in model.cherche_occupant("mangeoire")
    assert Animal["Tac"] in model.cherche_occupant("litière")
    assert Animal["Tac"] not in model.cherche_occupant("mangeoire")
    assert model.cherche_occupant("nintendo") == []


def test_change_etat():
    model.change_etat("Totoro", "fatigué")
    assert model.lit_etat("Totoro") == "fatigué"  # 1
    model.change_etat("Totoro", "excité comme un pou")
    assert model.lit_etat("Totoro") == "fatigué"  # 2
    model.change_etat("Truc", "fatigué")
    assert model.lit_etat("Truc") == None  # 3


@orm.db_session
def test_change_lieu():
    model.change_lieu("Totoro", "roue")
    assert model.lit_lieu("Totoro") == Equipement["roue"]
    model.change_lieu("Totoro", "nid")
    assert model.lit_lieu("Totoro") == Equipement["roue"]
    model.change_lieu("Totoro", "nintendo")
    assert model.lit_lieu("Totoro") == Equipement["roue"]
    model.change_lieu("Muche", "litière")
    assert model.lit_lieu("Muche") == None


@orm.db_session
def test_nourrir():
    if (
        model.verifie_disponibilite("mangeoire") == "libre"
        and model.lit_etat("Tic") == "affamé"
    ):
        controleur.nourrir("Tic")
    assert model.verifie_disponibilite("mangeoire") == "occupé"
    assert model.lit_etat("Tic") == "repus"
    assert model.lit_lieu("Tic") == Equipement["mangeoire"]
    controleur.nourrir("Pocahontas")
    assert model.lit_etat("Pocahontas") == "endormi"
    assert model.lit_lieu("Pocahontas") == Equipement["nid"]
    controleur.nourrir("Tac")
    assert model.lit_etat("Tac") == "affamé"
    assert model.lit_lieu("Tac") == Equipement["litière"]
    controleur.nourrir("Bob")
    assert model.lit_etat("Bob") == None
    assert model.lit_lieu("Bob") == None
    assert model.verifie_disponibilite("mangeoire") == "occupé"
