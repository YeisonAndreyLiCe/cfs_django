$(window).ready(function() {
    var form = document.getElementById('form');
    var FetchTo = document.getElementById('fetchTo').innerHTML;
    form.onsubmit = function(e) {
        e.preventDefault();
        var formData = new FormData(form);
        fetch(FetchTo,{'method': 'POST', 'body': formData})
        .then (response => response.json())
        .then (data => {
            if ('user_id' in data) {
                window.location.href = '/users/' + data.user_id + data.route;
            }
            else {
                var alertMessage = document.getElementById('alertMessage');
                alertMessage.innerHTML = "";
                if (FetchTo == '/register_user/' ){
                    for (var key in data) {
                        alertMessage.innerHTML += data[key] + '<br>';
                    }
                }else {
                    alertMessage.innerText = data.error;
                }
                alertMessage.classList.add('alert');
                alertMessage.classList.add('alert-danger');
            }
        });
    }
});

