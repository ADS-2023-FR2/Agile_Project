// script.js
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
    var resultList = document.getElementById("resultList");
    resultList.innerHTML = ""; // Leeren Sie die Liste

    for (var i = 0; i < items.length; i++) {
        var listItem = document.createElement("li");
        listItem.textContent = items[i];
        resultList.appendChild(listItem);
    }
}
