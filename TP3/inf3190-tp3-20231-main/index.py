# Copyright 2022 <Votre nom et code permanent>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import random
import re
from flask import Flask
from flask import render_template
from flask import g
from flask import request
from flask import redirect
from werkzeug.exceptions import abort
from database import Database
from animal import Animal

erreur = {}
champs_valides = {}

app = Flask(__name__, static_url_path="", static_folder="static")


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


def get_liste_animaux():
    return get_db().get_animaux()


def get_animaux_index():
    animaux = get_liste_animaux()
    random.shuffle(animaux)
    animaux = animaux[:5]
    return animaux


@app.route('/')
def index():
    erreur.clear()
    return render_template('index.html', animaux=get_animaux_index())


@app.route('/recherche', methods=['POST'])
def donnees_recherche():
    resultat = []
    achercher = request.form['recherche']
    if len(achercher) == 0:
        return '', 204
    reg = re.compile(achercher, re.IGNORECASE)
    for animal in get_db().get_animaux():
        if re.search(reg, animal.get('nom')) or re.findall(reg, animal.get('espece')) \
                or re.findall(reg, animal.get('race')) or re.findall(reg, animal.get('description')):
            resultat.append(animal)

    if len(resultat) == 0:
        return render_template('animal-introuvable.html', animals=get_liste_animaux()[:2])

    return render_template('recherche.html', resultat=resultat)


@app.route('/animal', methods=['POST'])
def adopter():
    animal_a_adopter = request.form.get('animal')
    return redirect('/{}'.format(animal_a_adopter))


@app.route('/<nom_animal>')
def afficher_animal(nom_animal):
    for animal in get_liste_animaux():
        if nom_animal == animal.get('nom'):
            return render_template('animal.html', animal=animal)

    return abort(404)


@app.route('/ajouter_animal')
def ajouter_animal():
    print('erreur : ', erreur)
    print('valide :', champs_valides)
    return render_template('ajouter_animal.html', erreurs=erreur, champs_valides=champs_valides)


@app.route('/valider_formulaire', methods=['POST'])
def valider_form():
    nom = request.form['nom']
    espece = request.form['espece']
    race = request.form['race']
    age = request.form['age']
    courriel = request.form['courriel']
    description = request.form['description']
    adresse = request.form['adresse-civique']
    ville = request.form['ville']
    cp = request.form['cp']

    animal = Animal(nom, espece, race, age, description, courriel, adresse, ville, cp)

    if remplire_bd(animal):
        erreur.clear()
        champs_valides.clear()
        return redirect('/{}'.format(animal.animal_nom))

    return redirect('/ajouter_animal')


def valider_nom(nom):
    print(len(nom))

    if "," not in nom and 3 < len(nom) < 20:
        champs_valides['nom'] = nom
        return True

    erreur["nom"] = "Entrez un nom valide"

    return False


def valider_espece(espece):
    if "," not in espece and 0 < len(espece) < 25:
        champs_valides['espece'] = espece
        return True

    erreur["espece"] = "Entrez une espece valide"

    return False


def valider_race(race):
    if "," not in race and 0 < len(race) < 25:
        champs_valides['race'] = race
        return True

    erreur["race"] = "Entrez une race valide"
    return False


def valider_age(age):
    if age.isdigit():
        age = int(age)
        if 0 <= age <= 30:
            champs_valides['age'] = age
            return True

    erreur["age"] = "Entrez un age valide"
    return False


def valider_courriel(courriel):
    regex = re.compile("^[A-Za-z0-9_!#$%&'*+\/=?`{|}~^.-]+@[A-Za-z0-9.-]+$")
    if regex.match(courriel):
        champs_valides['courriel'] = courriel
        return True
    else:
        erreur["courriel"] = "Entrez un courriel valide"
        return False


def valider_description(description):
    if "," not in description and 0 < len(description) < 500:
        champs_valides['description'] = description
        return True
    else:
        erreur["description"] = "Entrez une description valide"

        return False


def valider_adresse(adr_civique, ville, cp):
    if ',' in adr_civique or ',' in ville or ',' in cp:
        return False

    regex = re.compile("^[a-zA-Z]\d[a-zA-Z]\s?\d[a-zA-Z]\d$")
    if regex.match(cp):
        champs_valides['adr_civique'] = adr_civique
        champs_valides['ville'] = ville
        champs_valides['cp'] = cp
        return True

    erreur["adresse"] = "Entrez une adresse valide"
    return False


def verifier_donnes(animal):
    if valider_nom(animal.animal_nom) & valider_espece(animal.animal_espece) & valider_race(animal.animal_race) \
            & valider_age(animal.animal_age) & valider_description(animal.animal_description) \
            & valider_courriel(animal.animal_courriel) \
            & valider_adresse(animal.animal_adresse, animal.animal_ville, animal.animal_cp):
        return True
    return False


def remplire_bd(animal):
    erreur.clear()
    champs_valides.clear()
    if verifier_donnes(animal):
        get_db().add_animal(animal.animal_nom, animal.animal_espece, animal.animal_race, animal.animal_age,
                            animal.animal_description, animal.animal_courriel, animal.animal_adresse,
                            animal.animal_adresse, animal.animal_cp)

        return True
    return False


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
