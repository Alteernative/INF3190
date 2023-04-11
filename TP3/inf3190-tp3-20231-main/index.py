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
from database import Database

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


@app.route('/form')
def afficher():
    return render_template('recherche.html')


@app.route('/<nom_animal>')
def adopter_animal(nom_animal):

    for animal in get_liste_animaux():
        if nom_animal == animal.get('nom'):
            return render_template('animal.html', animal=animal)

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
