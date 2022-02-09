import sqlite3
from flask import *

def enregistrer_score(score, pseudo) :
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    parametres = (score, pseudo)
    requete_sql = """
    INSERT INTO bdd_scores(score, pseudo)
    VALUES (?, ?);
    """
    curseur.execute(requete_sql, parametres)
    connexion.commit()
    connexion.close()

def lire_scores() :
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    requete_sql = """SELECT * FROM bdd_scores"""
    resultat = curseur.execute(requete_sql)
    scores = resultat.fetchall()
    connexion.close()
    return scores

def meilleur_score() :
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    requete_sql = """
    SELECT MAX(score) FROM bdd_scores
    """
    resultat = curseur.execute(requete_sql)
    meilleur_score = resultat.fetchall()
    connexion.close()
    return meilleur_score


app = Flask(__name__)

@app.route("/")
def accueillir():
    scores=lire_scores()
    return render_template("index.html", scores = scores)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1660, debug=True)

print(meilleur_score())