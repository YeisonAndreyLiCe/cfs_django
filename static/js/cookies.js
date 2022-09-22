$(document).ready(function() {
    $('#accept-cookies').submit(function(e) {
        e.preventDefault();
        ip = $('#ip').val();
        $.ajax({
            url: '/accept-cookies',
            type: 'POST',
            data: {accept: true, csrf_token: '{{ csrf_token() }}'},
            success: function(data) {
                $('#cookie-banner').hide();
            }
        });        
    });
});