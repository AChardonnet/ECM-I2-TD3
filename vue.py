from appJar import gui
import model
import controleur


def initGui():
    app.addLabel("en-tête", "Bienvenue à l'animalerie!", colspan=2)
    app.setLabelBg("en-tête", "salmon")
    app.setLabelFg("en-tête", "white")

    app.addLabel("tableau de bord", "Tableau de bord", colspan=2)
    app.setLabelBg("tableau de bord", "gray")

    colors = ["lavender", None]
    for animal in animals:
        row = app.getRow()
        app.addLabel(animal, f"{animal}", row, 0)
        app.addLabel(
            animal + "_info",
            f"{model.lit_etat(animal)}, {model.lit_lieu(animal).nom_equipement}",
            row,
            1,
        )
        app.setLabelAlign(animal, "left")
        app.setLabelAlign(animal + "_info", "left")
        app.setLabelBg(animal, colors[row % 2])
        app.setLabelBg(animal + "_info", colors[row % 2])

    app.addLabel("actions", "Actions", colspan=2)
    app.setLabelBg("actions", "gray")

    row = app.getRow()

    app.addLabel("animal", "Animal", row, 0)
    app.setLabelBg("animal", "lightgray")

    for i in range(len(animals)):
        app.addRadioButton("id_animal", animals[i], row + i + 1, 0)

    app.addLabel("action", "Action", row, 1)
    app.setLabelBg("action", "lightgray")

    for i in range(len(etats)):
        app.addRadioButton("etat", etats[i], row + i + 1, 1)

    app.addButton("go", press, row + max(len(animals), len(etats)) + 1, colspan=2)

    app.go()


def updateGui():
    for animal in animals:
        app.setLabel(
            animal + "_info",
            f"{model.lit_etat(animal)}, {model.lit_lieu(animal).nom_equipement}",
        )


def press(act):
    action = app.getRadioButton("etat")
    animal = app.getRadioButton("id_animal")
    result = None
    match action:
        case "nourrir":
            result = controleur.nourrir(animal)
        case "divertir":
            result = controleur.divertir(animal)
        case "coucher":
            result = controleur.coucher(animal)
        case "reveiller":
            result = controleur.reveiller(animal)
    updateGui()
    if result != True:
        app.warningBox("Erreur !", result)


animals = ["Tic", "Tac", "Totoro", "Patrick", "Pocahontas"]
etats = ["nourrir", "divertir", "coucher", "reveiller"]
app = gui()

initGui()
