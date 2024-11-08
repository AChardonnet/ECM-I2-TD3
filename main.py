from pony import orm
import numpy as np
import pandas
import os
import shutil

db = orm.Database()


class Client(db.Entity):
    id_client = orm.PrimaryKey(str)
    telephone = orm.Required(str)
    ville = orm.Required(str)
    pays = orm.Required(str)
    achats = orm.Set("Commande")


class Produit(db.Entity):
    code_produit = orm.PrimaryKey(str)
    type_produit = orm.Required(str)
    prix_unitaire = orm.Required(float)
    ventes = orm.Set("Commande")


class Commande(db.Entity):
    num_commande = orm.Required(int)
    code_produit = orm.Required(str)
    orm.PrimaryKey(num_commande, code_produit)
    quantité = orm.Required(int)
    montant = orm.Required(float)
    mois = orm.Required(int)
    année = orm.Required(int)
    client = orm.Required(Client)
    produit = orm.Required(Produit)


def reset_produits():
    produits = data[["CODE_PRODUIT", "TYPE_PRODUIT", "PRIX_UNITAIRE"]].drop_duplicates()
    with orm.db_session:
        for p in produits.values:
            try:
                Produit(code_produit=p[0], type_produit=p[1], prix_unitaire=p[2])
                orm.commit()
            except Exception as e:
                print("*** ERREUR DE TRANSACTION :", e, "***")


def reset_client():
    clients = data[["CLIENT", "TELEPHONE", "VILLE", "PAYS"]].drop_duplicates()
    with orm.db_session:
        for c in clients.values:
            try:
                Client(id_client=c[0], telephone=c[1], ville=c[2], pays=c[3])
                orm.commit()
            except Exception as e:
                print("*** ERREUR DE TRANSACTION :", e, "***")


def resetVentes():
    ventes = data[
        [
            "NUM_COMMANDE",
            "QUANTITE",
            "MONTANT",
            "MOIS",
            "ANNEE",
            "CLIENT",
            "CODE_PRODUIT",
        ]
    ].drop_duplicates()
    with orm.db_session:
        for v in ventes.values:
            try:
                client = Client[v[5]]
                produit = Produit[v[6]]
                Commande(
                    num_commande=int(v[0]),
                    code_produit=v[6],
                    quantité=int(v[1]),
                    montant=float(v[2]),
                    mois=int(v[3]),
                    année=int(v[4]),
                    client=client,
                    produit=produit,
                )
                orm.commit()
            except Exception as e:
                print("*** ERREUR DE TRANSACTION :", e, "***")


def reset_all():
    os.remove("ventes.db")
    shutil.copy("orig/ventes_new.csv", "ventes_new.csv")
    db.bind(provider="sqlite", filename="ventes.db", create_db=True)
    orm.set_sql_debug(True)
    db.generate_mapping(create_tables=True)
    reset_produits()
    reset_client()
    resetVentes()


db.bind(provider="sqlite", filename="ventes.db", create_db=True)
orm.set_sql_debug(True)
db.generate_mapping(create_tables=True)


with open("ventes_new.csv", encoding="utf-8") as f:
    data = pandas.read_csv(f)
print(data)


with orm.db_session:
    Client.select().show()

    print(Client["Land of Toys Inc."])
    print(Client["Land of Toys Inc."].id_client)
    print(Client["Land of Toys Inc."].ville)
    print(Client["Land of Toys Inc."].pays)
    print(Client["Land of Toys Inc."].achats)

    requête = Client.select(lambda c: c.pays == "France")
    requête.show()

    for c in requête:
        print(c.id_client, c.ville, c.pays)

with orm.db_session:
    Produit.select().show()
    print("=====================================")
    orm.show(Produit.select()[:10])
    print("=====================================")
    print(Produit["S10_1678"])
    print(Produit["S10_1678"].type_produit)
    print(Produit["S10_1678"].prix_unitaire)
    print(Produit["S10_1678"].ventes)


with orm.db_session:
    Commande.select().show()
    print(Commande[10118, "S700_3505"])
    print("Montant :", Commande[10118, "S700_3505"].montant)
    print("Quantité :", Commande[10118, "S700_3505"].quantité)
    print("Année :", Commande[10118, "S700_3505"].année)
    print("Mois :", Commande[10118, "S700_3505"].mois)
    print("Client :", Commande[10118, "S700_3505"].client)
    print("Produit :", Commande[10118, "S700_3505"].produit)

    requête = Commande.select(lambda c: c.montant > 10000)
    for r in requête:
        print(
            f"{r.num_commande}, {r.quantité}, {r.mois}, {r.année}, {r.client}, {r.produit}"
        )
    print("=====================================")
    requête.show()


with orm.db_session:
    Produit.select(lambda p: p.code_produit == "S12_1108").show()
    Produit["S12_1108"].prix_unitaire = 100
    orm.commit()
    Produit.select(lambda p: p.code_produit == "S12_1108").show()
    Produit["S12_1108"].delete()
    orm.commit()
    Produit.select(lambda p: p.code_produit == "S12_1108").show()
