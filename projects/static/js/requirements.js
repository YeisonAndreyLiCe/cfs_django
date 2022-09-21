jQuery(window).ready(
    function() {
        $('.form').each(index => {
            var form = $('.form')[index];
            var FetchTo = form.getAttribute('action');
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
                        var alertMessage = $('.alertMessage')[index];
                        alertMessage.innerHTML = "";
                        for (var key in data) {
                            alertMessage.innerHTML += data[key] + '<br>';
                        }
                        alertMessage.classList.add('alert');
                        alertMessage.classList.add('alert-danger');
                    }
                });
            };
        });
    }
);
