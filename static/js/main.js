
$("#btn_search").click(function () {
    var tk_select = $("#tk_select label.active input"),
        result_block = $("#result-block"),
        response,
        tk_id;

    if (tk_select.length>0) {
        tk_id = tk_select[0].id
    }
    else {
        tk_id = null
    }

    $.ajax({
        url: "http://localhost:5000/search/", data: {"track_id": $("#search_text").val(), "tk_id": tk_id}, success: function (result) {
            response = JSON.parse(result);

            if (result=='{}') {
                check_result(tk_id, $("#search_text").val());
                result_block.html('<div class="progress">' +
                    '<div class="progress-bar progress-bar-striped active" role="progressbar"' +
                    'aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width:100%">' +
                    '</div>' +
                    '</div>')
            }
            else  if (response.success != undefined) {
                show_result(response.message, response.success)
            }
            else if (response.choose_tk == true) {
                result_block.html('<div class="alert alert-warning" role="alert">Выберите транспортную компанию</div>');
                tk_select.show();
            }
        }
    });
});


function check_result(tk_id, track_id) {
    var response;
    $.ajax({
        url: "http://localhost:5000/check/", data: {"track_id": track_id, "tk_id": tk_id}, success: function (result) {
            response = JSON.parse(result);
            if (result=='{}') {
                setTimeout(function(){check_result(tk_id, track_id)}, 1000)
            }
            else {
                show_result(response.message, response.success)
            }
        }
    });
}

function show_result(message, success) {
    var result_block = $("#result-block"),
        type_message = '';
    if (success==true) {
        type_message = 'alert-success';
    }
    else {
        type_message = 'alert-danger';
    }
    result_block.html('<div class="alert ' + type_message + '" role="alert">' + message + '</div>')
}