// L'endroit où placer le code du front-end.


document.getElementById('adopter').addEventListener('click', function () {
    window.location.href="/ajouter_animal"
    }
)

function valider(inputElem) {
    console.log(inputElem.value.length);
    if (inputElem.value.length < 3 || inputElem.value.length > 30) {
        inputElem.style.border = "2px solid red";
    }
    else {
         inputElem.style.border = "2px solid green";
    }
}

const nom = document.getElementById('nom');
nom.addEventListener('change', function() {
    valider(nom);
});