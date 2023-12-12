// test.js
var loadButton = document.getElementById("loadRecommendationsButton");

loadButton.addEventListener("click", function() {
    fetch('/test')

        /*
        .then(response => response.json())
        .then(data => {
            console.log('Received data:', data);  // Konsolenausgabe hinzugefügt

            var recommendations = data.top_recommendations;
            var tableBody = document.getElementById("recommendationTableBody");

            // Tabelle leeren
            tableBody.innerHTML = "";

            // Empfehlungen in die Tabelle einfügen
            recommendations.forEach(function(filmID) {
                var filmInfo = getFilmInfo(filmID);

                var newRow = tableBody.insertRow(-1);

                var cell1 = newRow.insertCell(0);
                cell1.innerHTML = '<img src="' + filmInfo.image + '" alt="' + filmInfo.item_id + '" class="limited-dimensions">';

                var cell2 = newRow.insertCell(1);
                cell2.innerHTML = filmInfo.Title;

                var cell3 = newRow.insertCell(2);
                cell3.innerHTML = filmInfo.Genres;

                var cell4 = newRow.insertCell(3);
                cell4.innerHTML = filmInfo.Year;

                var cell5 = newRow.insertCell(4);
                cell5.innerHTML = '9.0';  // Hier kann der echte Bewertungswert eingefügt werden
            });
        })
        .catch(error => console.error('Error:', error));
    */
});

function getFilmInfo(filmID) {
    // Hier implementierst du die Logik, um Filminformationen basierend auf der Film-ID abzurufen
    // Dies könnte eine Fetch-Anfrage oder eine andere Methode sein, um auf deine Filmdaten zuzugreifen
    // Hier ist eine vereinfachte Beispiellogik:
    var filmData = {
        1: {'item_id': 1, 'Title': 'Movie 1', 'Genres': 'Action', 'Year': '2022', 'image': 'path/to/image1.jpg'},
        2: {'item_id': 2, 'Title': 'Movie 2', 'Genres': 'Drama', 'Year': '2023', 'image': 'path/to/image2.jpg'},
        // ...
    };

    // Hier wird die Filminformation basierend auf der Film-ID zurückgegeben
    return filmData[filmID];
}
