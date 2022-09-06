$(window).ready(function() {
    // Set up the form to submit when the user clicks the button
    $("#edit").click(function() {
        var form = $("#main");
        
    });

    // Set up the form to submit when the user presses enter
    $("#edit_project_form").keypress(function(e) {
        if (e.which == 13) {
            $("#edit_project_form").submit();
        }
    });
});