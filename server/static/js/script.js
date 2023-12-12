// script.js
var integerArray = [10,20,30,40,50];
function performAction() {
    $.ajax({
        url: "/get_list",
        type: "GET",
        success: function(data) {
            updateList(data);
        },
        error: function(error) {
            console.log("Error for getting the list in perform Action function:", error);
        }
    });
}
function test() {
    $.ajax({
        url: "/test",
        type: "GET",
        success: function(data) {
            updateList2(data);
        },
        error: function(error) {
            console.log("Error for getting the list in perform Action function:", error);
        }
    });
}

// script.js
function request_list() {
    //var user1_id = document.getElementById("variable1").value;
    //var user2_id = document.getElementById("variable2").value;
    var user1_id = "1"
    var user2_id = "2"
    var user1_id = parseInt(user1_id, 10);
    var user2_id = parseInt(user2_id, 10);
    $.ajax({
        url: "/combined_recommendations",
        type: "GET",
        data: {
            user1_id: user1_id,
            user2_id: user2_id
        },
        success: function (response) {
            // Creates a new sHTML-Code for the list
            var listHtml = "<ul class='movie-list'>";

            // Adding the ne results to the list
            for (var i = 0; i < response.top_recommendations.length; i++) {
                listHtml += "<li class='movie-list-item'>" + response.top_recommendations[i] + "</li>";
            }

            listHtml += "</ul>";

            // add the HTML code to the container
            var container = document.getElementById("resultContainer");
            container.innerHTML = listHtml;
        },
        error: function (error) {
            console.log("Error for getting the list in performAction2 function:", error);
        }

    });
}

function updateList(items) {
    console.log("test hello world")
    var testList = document.getElementById("testList");
    testList.innerHTML = ""; // Leeren Sie die Liste

    for (var i = 0; i < items.length; i++) {
        var listItem = document.createElement("li");
        listItem.textContent = items[i];
        testList.appendChild(listItem);
    }
}


document.addEventListener('DOMContentLoaded', function() {
    // Eventlistener für den Button hinzufügen
    var updateArrayButton = document.getElementById('updateArrayButton');

    if (updateArrayButton) { // Überprüfen, ob das Element existiert
        //console.log("Hello World");
        updateArrayButton.addEventListener('click', function() {
            // Hier kannst du die Variable aktualisieren
            var h1 = document.getElementById('hiddenIntegerArray');
            console.log(h1);
            
            var h2 = JSON.parse(h1.value);
            h2[5] = 1;
            h2[6] = 2;
            h2[7] = 3;
            h2[8] = 4;
            h2[9] = 5;
            // Beispiel: Füge eine neue Zahl hinzu
            console.log("2ter log: " + h2);
            
            // Aktualisiere den Wert des Hidden Inputs
            // Sende das aktualisierte Array an den Server
            fetch('/update_array', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ updatedArray: h2 })
            }).then(function(response) {
                console.log("then consolen output")
                if (response.ok) {
                    // Seite neu laden, wenn die Antwort erfolgreich ist
                    console.log("ok response")
                    window.location.href = '/hello?updatedArray=' + encodeURIComponent(JSON.stringify(h2));
                }
            });
        });
    } else {
        console.error('Element with id "updateArrayButton" not found.');
    }
});