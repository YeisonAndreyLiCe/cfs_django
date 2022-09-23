$(window).ready(function() {
    var form = document.getElementById('accept-cookies');
    var FetchTo = form.getAttribute('action');
    form.onsubmit = function(e) {
        e.preventDefault();
        var formData = new FormData(form);
        fetch(FetchTo,{'method': 'POST', 'body': formData})
        .then (response => response.json())
        .then (data => {
            console.log(data);
            fetch('http://api.ipstack.com/167.0.161.63?access_key='+data.key)
            .then (response => response.json())
            .then (data => {
                console.log(data);
            });
        });
    }
});