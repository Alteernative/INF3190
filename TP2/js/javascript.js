function afficherProchain(elem) {
    document.getElementById(elem).style.visibility = "visible"
}

function cacherElements(elem) {
    document.getElementById(elem).style.visibility = "hidden"
}

document.getElementById('genre').style.visibility = 'visible'

document.getElementById('genre').addEventListener('change', function () {
    if (!verifierDonnees()) {
        return;
    }
    afficherProchain('age')
})

document.getElementById('age').addEventListener('change', function () {

    const age = document.getElementById('age-input').value;
    if (!verifierDonnees()) {
        return;
    }
    if (age > 0) {
        afficherProchain('vehicule');
    }
    if (age < 0) {
        document.getElementById('age-input').value = 0;
        cacherElements('vehicule')

    }

})

document.getElementById('vehicule').addEventListener('change', function () {
    if (!verifierDonnees()) {
        return;
    }
    const valeur = document.getElementById('valeur-vehicule').value;

    if (valeur > 0) {
        afficherProchain('fabrication');
    }

    if (valeur < 0) {
        document.getElementById('valeur-vehicule').value = 0;
        cacherElements('fabrication')

    }
})

document.getElementById('annee-fabrication').addEventListener('keypress', function (event) {
    event.preventDefault();

})

document.getElementById('fabrication').addEventListener('change', function () {
    if (this.onkeydown)
        return;

    afficherProchain('reclamation');
    afficherProchain('text-reclamation');
    afficherProchain('input-oui');
    afficherProchain('input-non');
})

document.getElementById('reclamation-non').addEventListener('change', function () {
    cacherElements('chiffre-reclamation')
    cacherElements('reclamations-montant')
    cacherElements('buttons')
    document.getElementById('reclamations-montant').innerHTML = "";
    document.getElementById('reclamations').value = 0;
})

document.getElementById('reclamation-oui').addEventListener('change', function () {

    if (!verifierDonnees()) {
        return;
    }
    afficherProchain('chiffre-reclamation');

})


document.getElementById('reclamations').addEventListener('change', () => {

    let chiffreReclamation;

    document.getElementById('reclamations-montant').innerHTML = "";
    document.getElementById('reclamations-montant').style.display = "flex";
    chiffreReclamation = document.getElementById('reclamations').value;

    if (chiffreReclamation < 0) {
        document.getElementById('reclamations').value = 0;
    }
    if (chiffreReclamation > 4) {
        return;
    }
    afficherProchain('reclamations-montant');
    for (let i = 0; i < chiffreReclamation; i++) {

        let idDiv = "input" + i;
        let idInput = "reclamationNr" + i;

        document.getElementById('reclamations-montant').innerHTML +=
            '<div class="input"' + " id=" + idDiv + ">" +
            '<label>Montant de la reclamation numero ' + (i + 1) + ' : ' + '</label>' +
            '<input type="number"' + ' id=' + idInput + ' value="0">' + '</div>'


        afficherProchain('input' + i);
    }
    afficherProchain('calcule');
})


document.getElementById('button-reset').addEventListener('click', function () {

    cacherElements('age');
    cacherElements('vehicule');
    cacherElements('fabrication');
    cacherElements('reclamation');
    cacherElements('text-reclamation');
    cacherElements('input-oui');
    cacherElements('input-non');
    cacherElements('chiffre-reclamation');
    cacherElements('reclamations-montant');
    cacherElements('calcule');
    document.getElementById('reclamations-montant').style.display = "none"

})

let sexe;
let age;
let valeurAchat;
let date;
let dateFabrication;
let dateAjd;
let nombreReclamations;
let prixTotaleReclamations;

function verifierDonnees() {

    sexe = document.getElementById('options').value;
    age = parseInt(document.getElementById('age-input').value);
    valeurAchat = parseInt(document.getElementById('valeur-vehicule').value);
    date = document.getElementById('annee-fabrication').value.split('-');
    dateFabrication = new Date(date[0], date[1] - 1, date[2])
    dateAjd = new Date();
    nombreReclamations = parseInt(document.getElementById('reclamations').value);
    prixTotaleReclamations = 0;

    if (sexe === "") {
        return false;
    }
    if (sexe === 'femme' && age < 16) {
        return false;
    }
    if (sexe === 'homme' || sexe === 'non-binaire') {
        if (age < 18) {
            return false;
        }
    }
    if (age < 0 || age > 100) {
        return false;
    }
    if(valeurAchat < 0 || valeurAchat > 100000){
        return false;
    }

    if ((dateAjd.getFullYear() - dateFabrication.getFullYear()) >= 25) {
        return false;
    }

    if (nombreReclamations > 4) {
        return false;
    }
    for (let i = 0; i < nombreReclamations; i++) {
        let id = 'reclamationNr' + i;
        prixTotaleReclamations += parseInt(document.getElementById(id).value);
    }
    if (prixTotaleReclamations > 35000) {
        return false;
    }

    return true;
}

document.getElementById('formulaire').addEventListener('change', function () {

    if (!verifierDonnees()) {
        return alert("Désolé, nous n'avons aucun produit à offrir pour ce profil de client");
    }
})

document.getElementById('calcule').addEventListener('click', function () {

    let montantAssurance;
    let montantBase;
    let penalite = 0;
    let etat = verifierDonnees();


    if (!etat) {
        return alert("Désolé, nous n'avons aucun produit à offrir pour ce profil de client");
    }
    
    montantBase = valeurAchat * 0.02;

    if (sexe === 'homme' || sexe === 'non-binaire') {
        if (age < 25) {
            montantBase = valeurAchat * 0.05;
        }
    }

    if (age >= 75) {
        montantBase = valeurAchat * 0.04
    }

    if (prixTotaleReclamations > 25000) {
        penalite = 500;
    }

    montantAssurance = montantBase + (350 * nombreReclamations) + penalite;


    document.getElementById('prix-par-annee').innerHTML = montantAssurance.toFixed(2) + " $";
    document.getElementById('prix-par-mois').innerHTML = (montantAssurance / 12).toFixed(2) + " $";

    document.getElementById('formulaire').style.display = "none";
    cacherElements('text-principal')
    afficherProchain('resultat')

})

function initialiserValeurs() {

    document.getElementById('options').value = null;
    document.getElementById('age-input').value = null;
    document.getElementById('valeur-vehicule').value = null;
    document.getElementById('annee-fabrication').value = null;
    document.getElementById('reclamations').value = null;
    document.getElementsByName('reclamation-six-mois')[0].checked = false;
    document.getElementsByName('reclamation-six-mois')[1].checked = false;
}

document.getElementById('button-reset').addEventListener('click', function () {

    document.getElementById('formulaire').style.display = "flex";
    cacherElements('resultat');
    initialiserValeurs();

    afficherProchain('text-principal');
    afficherProchain('genre');
})


