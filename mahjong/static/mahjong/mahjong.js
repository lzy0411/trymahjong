function getCSRFToken() {
    let cookies = document.cookie.split(";")
    
    for (let i = 0; i < cookies.length; i++) {
        let c = cookies[i].trim()
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length)
        }
    }
     return "unknown"
}

function selectTile(pk, gameId, request_user) {
                                
    $("#discard_tile_id_discard").remove();
    $("#request_user_discard").remove();
    $("#game_id_discard").remove();
    $("#id_discard").remove();
    $("#discard").append('<input ' + 'type="hidden" ' + 'name="discard_tile_id' + '" id="discard_tile_id_discard" value = ' + pk + '>')
    $("#discard").append('<input ' + 'type="hidden" ' + 'name="request_user' + '" id="request_user_discard" value = ' + request_user + '>')
    $("#discard").append('<input type="hidden" ' + 'name="game_id' + '" id="game_id_discard" value = ' + gameId + '>')
    $("#discard").append('<button type="submit' + '" ' + 'id="id_discard' + '" ' + 'class="submitButton' + '">Discard</button>')


    var tile1_element = document.getElementById("eat_1")
    var tile2_element = document.getElementById("eat_2")
    
    if(tile1_element == null){
        $("#eat").append('<input ' + 'type="hidden" ' + 'name="eat_tile_1_id" id="eat_1"' + ' value = ' + pk + '>')
    }

    else if(tile2_element == null){
        $("#eat").append('<input ' + 'type="hidden" ' + 'name="eat_tile_2_id" id="eat_2"' + ' value = ' + pk + '>')
    }

    else {
        $("#eat_1").remove();
        document.getElementById("eat_2").name = "eat_tile_1_id"
        document.getElementById("eat_2").id = "eat_1"                                    
        $("#eat").append('<input ' + 'type="hidden" ' + 'name="eat_tile_2_id" id="eat_2"' + ' value = ' + pk + '>')
    }
}