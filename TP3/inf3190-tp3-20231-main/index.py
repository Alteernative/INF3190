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

app = Flask(__name__, static_url_path="", static_folder="static")

nom = ""
espece = ""
race = ""
age = ""
courriel = ""
description = ""
adr_civique = ""
ville = ""
cp = ""


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
    return render_template('index.html', animaux=get_animaux_index())


@app.route('/recherche', methods=['POST'])
def donnees_recherche():
    resultat = []
    achercher = request.form['recherche']
    if len(achercher) == 0:
        return redirect('/')
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
    return render_template('ajouter_animal.html')


@app.route('/valider_formulaire', methods=['POST'])
def valider_form():
    nom = request.form['nom']
    espece = request.form['espece']
    race = request.form['race']
    age = request.form['age']
    courriel = request.form['courriel']
    description = request.form['description']
    adr_civique = request.form['adresse-civique']
    ville = request.form['ville']
    cp = request.form['cp']

    remplire_bd()

    return redirect('/remplir_BD')


def valider_nom():
    if "," not in nom and len(nom) < 25:
        return True
    return False


def valider_espece():
    if "," not in espece and len(espece) < 25:
        return True
    return False


def valider_race():
    if "," not in race and len(race) < 25:
        return True
    return False


def valider_age():
    if "," not in age and len(age) < 25 and type(age) == int and 0 < age < 29:
        return True
    return False


def valider_courriel():
    regex = re.compile("^[A-Za-z0-9_!#$%&'*+\/=?`{|}~^.-]+@[A-Za-z0-9.-]+$")
    if regex.match(courriel):
        return True
    else:
        return False


def valider_description():
    if "," not in description and len(description) < 500:
        return True
    else:
        return False


def valider_adresse():
    if "," in adr_civique or ville or cp:
        return False

    regex = re.compile("^[a-zA-Z]\d[a-zA-Z]\s?\d[a-zA-Z]\d$")
    if regex.match(cp):
        return True

    return False


def remplire_bd():
    if valider_nom(nom) and valider_espece(espece) and valider_race(race) and valider_age(age) \
            and valider_courriel(courriel) and valider_adresse(adr_civique, ville, cp):
        print('we gucci')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
