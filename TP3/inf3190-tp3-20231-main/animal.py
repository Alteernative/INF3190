class Animal:

    def __init__(self, nom, espece, race, age, description, courriel, adresse, ville, cp):
        self._nom = nom
        self._espece = espece
        self._race = race
        self._age = age
        self._description = description
        self._courriel = courriel
        self._adresse = adresse
        self._ville = ville
        self._cp = cp

    @property
    def animal_nom(self):
        return self._nom

    @animal_nom.setter
    def animal_nom(self, nom):
        self._nom = nom

    @property
    def animal_espece(self):
        return self._espece

    @animal_espece.setter
    def animal_espece(self, espece):
        self._espece = espece

    @property
    def animal_race(self):
        return self._race

    @animal_race.setter
    def animal_race(self, race):
        self._race = race

    @property
    def animal_age(self):
        return self._age

    @animal_age.setter
    def animal_age(self, age):
        self._age = age

    @property
    def animal_description(self):
        return self._description

    @animal_description.setter
    def animal_description(self, description):
        self._description = description

    @property
    def animal_courriel(self):
        return self._courriel

    @animal_courriel.setter
    def animal_courriel(self, courriel):
        self._courriel = courriel

    @property
    def animal_adresse(self):
        return self._adresse

    @animal_adresse.setter
    def animal_adresse(self, adresse):
        self._adresse = adresse

    @property
    def animal_ville(self):
        return self._ville

    @animal_ville.setter
    def animal_ville(self, ville):
        self._ville = ville

    @property
    def animal_cp(self):
        return self._cp

    @animal_cp.setter
    def animal_cp(self, cp):
        self._cp = cp
