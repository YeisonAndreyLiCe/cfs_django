$(document).ready(function() {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    $('.form-update').each(function() {
        $(this).on('submit', function(e) {
            e.preventDefault();
            var form = $(this);
            console.log(form);
            console.log(form.attr('action'));
            $.ajax({
                url: form.attr('action'),
                type: 'POST',
                data: form.serialize(),
                headers: {'X-CSRFToken': csrftoken},
                success: function(data) {       
                    $("#requirement-info-"+data.id).html(data.info);
                    $("#description-"+data.id).toggleClass("done");
                    $("#description-"+data.id).toggleClass("artefact");
                    form.attr("action", "/projects/"+data.route);
                    $("#update-requirement-submit-"+data.id).toggleClass("primary");
                    $("#update-requirement-submit-"+data.id).toggleClass("secondary");
                    $("#update-requirement-submit-"+data.id).text(data.button);
                }
            });
        });
    });
});


