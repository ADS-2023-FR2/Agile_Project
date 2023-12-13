// script.js

function getDataFromTest() {
    fetch('/test', {
        method: 'GET',
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(jsonData => {
        // Hier können Sie die Logik zum Konvertieren des JSON-Arrays in ein Integer-Array einfügen
        const integerArray = jsonData.map(item => parseInt(item, 10));
        console.log('Integer Array:', integerArray);
        return integerArray
    })
    .catch(error => {
        console.error('Error fetching test data:', error);
    });
}


//combined_recomendations = [21,22,23,24,25]

document.addEventListener('DOMContentLoaded', function() {

    var searchForm = document.getElementById('searchForm');
    if (searchForm)  { // Überprüfen, ob das Element existiert
        searchForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Verhindert das standardmäßige Absenden des Formulars

            var h1 = document.getElementById('hiddenIntegerArray');
            var h2;
            var user1_id = 1;
            var user2_id;
            user2_id = user2_id = parseInt(searchForm.querySelector('.search-bar').value, 10);
        
            console.log('User2 ID:', user2_id);


        fetch('/test?user1_id=' + user1_id + '&user2_id=' + user2_id, {
            method: 'GET',
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(jsonData => {
                // Hier können Sie die Logik zum Konvertieren des JSON-Arrays in ein Integer-Array einfügen
                const integerArray = jsonData.map(item => parseInt(item, 10));
                console.log('Integer Array:', integerArray);
                combined_Recomendations = integerArray;
                console.log('combined_Recomendations: ', combined_Recomendations);
                console.log(h1);
            
                h2 = JSON.parse(h1.value);
                for (var i = 0; i <5; i++) { 
                    h2[i+5] = combined_Recomendations[i];
                }
                // Beispiel: Füge eine neue Zahl hinzu
                console.log("2ter log: " + h2);

                return fetch('/update_array', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ updatedArray: h2 })
                });
            })

            .then(function(response) {
                console.log("then consolen output")
                if (response.ok) {
                    // Seite neu laden, wenn die Antwort erfolgreich ist
                    console.log("ok response")
                    window.location.href = '/hello?updatedArray=' + encodeURIComponent(JSON.stringify(h2));
                }
            })

            .catch(error => {
                console.error('Error fetching test data:', error);
            });
        });
        
    }else {
        console.error('Element with id "searchForm" not found.');
    }
       
}); 
