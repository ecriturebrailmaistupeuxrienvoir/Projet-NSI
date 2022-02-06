import sqlite3
from flask import *

def enregistrer_score(score) :
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    requete_sql = """
    INSERT INTO bdd_scores(score)
    VALUES (?);
    """
    parametre = (score,)
    curseur.execute(requete_sql, parametre)
    connexion.commit()
    connexion.close()

def lire_scores() :
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    requete_sql = """
    SELECT * FROM bdd_scores
    """
    resultat = curseur.execute(requete_sql)
    scores = resultat.fetchall()
    connexion.close()
    return scores

app = Flask(__name__)

@app.route("/")
def accueillir():
    scores=lire_scores()
    return render_template("index.html", scores = scores)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1660, debug=True)