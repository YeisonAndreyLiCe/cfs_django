document.onload = function() {
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


    var form = document.getElementById('form');
    form.onsubmit = function(e) {
        e.preventDefault();
        var formData = new FormData(form);
        fetch('/login_user',{'method': 'POST', 'body': formData})
        .then (response => response.json())
        .then (data => {
            if (data.message == 'success') {
                window.location.href = '/users/projects_templates';
            }
            else {
                alert(data['message']);
            }
        });
    }
}