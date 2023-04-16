const nom = document.getElementById('nom');
const espece = document.getElementById('espece');
const race = document.getElementById('race');
const age = document.getElementById('age');
const description = document.getElementById('description');
const courriel = document.getElementById('courriel');
const adr_civique = document.getElementById('adresse-civique')
const ville = document.getElementById('ville')
const cp = document.getElementById('cp')

/*
pour ne pas perdre les informations au rechargement de la page
 */

nom.value = localStorage.getItem('nom')
espece.value = localStorage.getItem('espece')
race.value = localStorage.getItem('race')
age.value = localStorage.getItem('age')
courriel.value = localStorage.getItem('courriel')
description.value = localStorage.getItem('description')
adr_civique.value = localStorage.getItem('adr_civique')
ville.value = localStorage.getItem('ville')
cp.value = localStorage.getItem('cp')


function contient_virgule(input_elem) {
    if (input_elem != null) return input_elem.indexOf(',') !== -1;
}


function valider_nom(input_elem) {

    let nom_animal = input_elem.value;

    if (nom_animal.length < 3 || input_elem.value.length > 30 || contient_virgule(nom_animal)) {
        input_elem.style.border = "2px solid red";
        document.getElementById('span-nom').style.visibility = "visible";
        localStorage.setItem('nom', "")

        return false;
    } else {
        document.getElementById('span-nom').style.visibility = "hidden";
        input_elem.style.border = "2px solid green";
        localStorage.setItem('nom', nom.value)

    }
    return true;
}

function valider_age(input_elem) {

    let age_animal = input_elem.value;

    if (age_animal == null || age_animal === "") {
        return false;
    }
    if (age_animal <= 0 || age_animal >= 30 || isNaN(age_animal)) {
        document.getElementById('span-age').style.visibility = "visible";
        input_elem.style.border = "2px solid red";
        localStorage.setItem('age', "")

    } else {
        document.getElementById('span-age').style.visibility = "hidden";
        input_elem.style.border = "2px solid green";
        localStorage.setItem('age', age.value)

        return true;
    }
    return false;
}


function plus_grand_varchar(input_elem, max) {
    let taille_input = input_elem.value.toString();
    return taille_input.length > max;
}


/*

Source reg-ex : https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/match

*/

function valider_courriel(input_elem) {

    let courriel = input_elem.value
    const regex = /^[A-Za-z0-9_!#$%&'*+\/=?`{|}~^.-]+@[A-Za-z0-9.-]+$/

    return regex.test(courriel)
}

nom.addEventListener('change', function () {
    valider_nom(nom)
})

espece.addEventListener('change', function () {

    if (contient_virgule(espece.value) || plus_grand_varchar(espece, 25)) {
        espece.style.border = "2px solid red";
        document.getElementById('span-espece').style.visibility = "visible";
        localStorage.setItem('espece', "")
    } else {
        espece.style.border = "2px solid green";
        document.getElementById('span-espece').style.visibility = "hidden";
        localStorage.setItem('espece', espece.value)

    }
})

race.addEventListener('change', function () {

    if (contient_virgule(race.value) || plus_grand_varchar(race, 25)) {
        race.style.border = "2px solid red";
        document.getElementById('span-race').style.visibility = "visible";
        localStorage.setItem('race', "")

    } else {
        race.style.border = "2px solid green";
        document.getElementById('span-race').style.visibility = "hidden";
        localStorage.setItem('race', race.value)

    }
})
courriel.addEventListener('change', function () {

    if (!valider_courriel(courriel)) {
        document.getElementById('span-courriel').style.visibility = "visible";
        courriel.style.border = "2px solid red";
        localStorage.setItem('courriel', "")

    } else {
        document.getElementById('span-courriel').style.visibility = "hidden";
        courriel.style.border = "2px solid green";
        localStorage.setItem('courriel', courriel.value)

    }

})
description.addEventListener('change', function () {
    if (contient_virgule(description.value) && !plus_grand_varchar(description, 500)) {
        document.getElementById('span-description').style.visibility = "visible";
        description.style.border = "2px solid red";
        localStorage.setItem('description', "")

    } else {
        document.getElementById('span-description').style.visibility = "hidden";
        description.style.border = "2px solid green";
        localStorage.setItem('description', description.value)

    }
})

age.addEventListener('change', function () {
    valider_age(age)
})


function valider_CP() {

    let valeur_civique = cp.value;
    let regex = /^[a-zA-Z]\d[a-zA-Z]\s?\d[a-zA-Z]\d$/


    if (cp.value == null || cp.value === "") {
        cp.style.border = "none"
        return false
    }

    if (!regex.test(valeur_civique)) {
        document.getElementById('span-adresse').style.visibility = "visible";
        cp.style.border = "2px solid red";
        localStorage.setItem('cp', "")

        return false;
    } else {
        document.getElementById('span-adresse').style.visibility = "hidden";
        cp.style.border = "2px solid green";
        localStorage.setItem('cp', cp.value)

    }

    return true

}

function valider_adresse_civique() {

    if (adr_civique.value == null || adr_civique.value === "") {
        adr_civique.style.border = "none"
        return false
    }

    if (contient_virgule(adr_civique.value) || plus_grand_varchar(adr_civique, 75)) {
        document.getElementById('span-adresse').style.visibility = "visible";
        adr_civique.style.border = "2px solid red";
        localStorage.setItem('adr_civique', "")

        return false;

    } else {
        document.getElementById('span-adresse').style.visibility = "hidden";
        adr_civique.style.border = "2px solid green";
        localStorage.setItem('adr_civique', adr_civique.value)

    }
    return true;
}


function valider_ville() {

    if (ville.value == null || ville.value === "") {
        ville.style.border = "none"
        return false
    }

    if (contient_virgule(ville.value) || plus_grand_varchar(adr_civique, 75)) {
        document.getElementById('span-adresse').style.visibility = "visible";
        ville.style.border = "2px solid red";
        localStorage.setItem('ville', "")

        return false;

    } else {
        document.getElementById('span-adresse').style.visibility = "hidden";
        ville.style.border = "2px solid green";
        localStorage.setItem('ville', ville.value)

    }

    return true;
}

document.getElementById('formulaire_adresse').addEventListener('change', function () {


    valider_adresse_civique();
    valider_ville()
    valider_CP()

})


document.getElementById('soumettre').addEventListener('click', function (e) {


    if (valider_nom(nom) && !contient_virgule(espece.value) && !contient_virgule(race.value)
        && valider_age(age) && valider_courriel(courriel) && valider_ville() && valider_adresse_civique()
        && valider_ville() && valider_CP() && !contient_virgule(description.value)) {
     //   localStorage.clear();
        document.getElementById('form').submit();
    }

})