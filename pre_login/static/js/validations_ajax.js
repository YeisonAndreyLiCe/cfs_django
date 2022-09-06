$(window).ready(function() {
    var form = document.getElementById('form');
    var FetchTo = document.getElementById('fetchTo').innerHTML;
    form.onsubmit = function(e) {
        e.preventDefault();
        var formData = new FormData(form);
        fetch(FetchTo,{'method': 'POST', 'body': formData})
        .then (response => response.json())
        .then (data => {
            if ('route' in data) {
                window.location.href = data.route;
            }
            else {
                var alertMessage = document.getElementById('alertMessage');
                alertMessage.innerHTML = "";
                for (var key in data) {
                    alertMessage.innerHTML += data[key] + '<br>';
                }
                //alertMessage.innerText = data.error;
                alertMessage.classList.add('alert');
                alertMessage.classList.add('alert-danger');
            }
        });
    }
});

