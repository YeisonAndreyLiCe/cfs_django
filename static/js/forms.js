$(window).ready(
    function getForm(id) {
        var form = document.getElementById(id);
        var FetchTo = form.getAttribute('action');
        form.onsubmit = function(e) {
            e.preventDefault();
            var formData = new FormData(form);
            fetch(FetchTo,{'method': 'POST', 'body': formData})
            .then (response => response.json())
            .then (data => {
                window.location.href = data.route;
            });
        };
    }
);

$(window).ready(
    function addListener() {
        $('button[submit]').click(function() {
            console.log('clicked');
            var id = $(this).attr('id');
            getForm(id);
        });
    }
);



