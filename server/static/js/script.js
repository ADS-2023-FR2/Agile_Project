
document.addEventListener('DOMContentLoaded', function() {

    var searchForm = document.getElementById('searchForm');
    if (searchForm)  { // Checks, wheater searachForm exist in the file
        searchForm.addEventListener('submit', function(event) {
            event.preventDefault();

            var recomendation_array_input = document.getElementById('hiddenIntegerArray'); //contains old recomendation values
            var recomendation_array; 
            var hiddenIntegerField = document.getElementById('hidden_ownuserid_int');
            var own_user_id;
            var friend_user_id;
            own_user_id = hiddenIntegerField.value;
            //the next line, uses the search bar and interpretets the input as integer number. Maybe we need to some code to converte the names to the corect intger ids.
            friend_user_id = parseInt(searchForm.querySelector('.search-bar').value, 10);
        
            //console.log('User2 ID:', friend_user_id);

        //now take both user ids and call the new recomendation to watch together with a friend.
        //as return I expect the combinded recomendation function. 
        //I obtain the own_user_id form a hidden variable in the hello.html file. and the friend_user_id from the search bar.
        fetch('/combined_recommendations?own_user_id=' + own_user_id + '&friend_user_id=' + friend_user_id, {
            method: 'GET',
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(jsonData => {
    
                const integerArray = jsonData.map(item => parseInt(item, 10)); //integer Array contains the updated recomendation values
                console.log('Integer Array with new recomendation values:', integerArray);
                //combined_Recomendations = integerArray;
                //console.log('combined_Recomendations: ', combined_Recomendations);
                //console.log(recomendation_array_input);
            
                //gives recomendation array the lenth and the values of the old recomendation array
                recomendation_array = JSON.parse(recomendation_array_input.value); 
                for (var i = 0; i <5; i++) { //updates the watch together values in recomendation_array with the new recomendation values
                    recomendation_array[i+5] = integerArray[i];
                }
                // Beispiel: Füge eine neue Zahl hinzu
                console.log("updated recomendation array" + recomendation_array);


                //this sends the new recomendation data --> so the page can be reloaded with the updated recomendation values.
                return fetch('/update_array', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ updatedArray: recomendation_array })
                });
            })

            .then(function(response) {
                console.log("then consolen output")
                if (response.ok) {
                    //the hello page will be reloaded, if the response was received.
                    //console.log("ok response")
                    window.location.href = '/hello?updatedArray=' + encodeURIComponent(JSON.stringify(recomendation_array)); //this reload finaly the recomendation array
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
