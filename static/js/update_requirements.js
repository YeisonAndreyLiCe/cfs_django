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

    function updateFeatures(){$('.form-update-requirements').each(function() {
        $(this).on('submit', function(e) {
            e.preventDefault();
            var form = $(this);
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
    })}
    function deleteRequirement(){$('.form-delete-requirement').each(function() {
        $(this).on('submit', function(e) {
            e.preventDefault();
            var form = $(this);
            $.ajax({
                url: form.attr('action'),
                type: 'POST',
                data: form.serialize(),
                headers: {'X-CSRFToken': csrftoken},
                success: function(data) {
                    $("#description-"+data.id).remove();
                    $("#requirements-list").html(``);
                    var lines = data.lines;
                    for (var i = 0; i < lines.length; i++) {
                        $("#requirements-list").append(
                            `<li class="list-group-item artefact" id="description-${i}">
                            <div class="d-flex flex-wrap justify-content-between">
                                <div>
                                    <p class="ml-2" id="requirement-info-${i}">${lines[i]}</p>
                                </div>
                                <div class="d-flex flex-wrap justify-content-between">
                                    <form action="/projects/requirement_completed" id="form-${i}" method="POST" class="form-update-requirements m-1">
                                        <input type="hidden" name="csrfmiddlewaretoken" value=${csrftoken}>
                                        <input type="hidden" name="id_project" value="${data.id_project}">
                                        <input type="hidden" name="id_requirement" value="${i}">
                                        <button type="submit" class="btn btn-block primary btn-sm" id="update-requirement-submit-${i}">Not Completed</button>
                                    </form>
                                    <form action="/projects/delete_requirement" id="delete-${i}" method="POST" class="form-delete-requirement m-1">
                                        <input type="hidden" name="csrfmiddlewaretoken" value=${csrftoken}>
                                        <input type="hidden" name="id_project" value="${data.id_project}">
                                        <input type="hidden" name="id_requirement" value="${i}">
                                        <button type="submit" class="btn btn-block btn-danger btn-sm">Delete</button>
                                    </form>
                                </div>
                            </div>`);
                    };
                updateFeatures();
                deleteRequirement();
                addRequirements();
                }
            });
        });
    })}

    function deleteTask(){$('.delete-task').each(function() {
        $(this).on('submit', function(e) {
            e.preventDefault();
            var form = $(this);
            $.ajax({
                url: form.attr('action'),
                type: 'POST',
                data: form.serialize(),
                headers: {'X-CSRFToken': csrftoken},
                success: function(data) {
                    /* $("#task-description-"+data.id).remove(); */
                    $("#to_dos-list").html(``);
                    var lines = data.lines;
                    for (var i = 0; i < lines.length; i++) {
                        $("#to_dos-list").append(
                            `<li class="list-group-item artefact" id="description-${i}">
                            <div class="d-flex flex-wrap justify-content-between">
                                <div>
                                    <p class="ml-2" id="description-task-${i}">${lines[i]}</p>
                                </div>
                                <div class="d-flex flex-wrap justify-content-between">
                                    <form action="/projects/todo_task_completed" id="formTask-${i}" method="POST" class="form-update-to-do m-1">
                                        <input type="hidden" name="csrfmiddlewaretoken" value=${csrftoken}>
                                        <input type="hidden" name="id_project" value="${data.id_project}">
                                        <input type="hidden" name="id_task" value="${i}">
                                        <button type="submit" class="btn btn-block primary btn-sm" id="update-requirement-submit-${i}">Not Completed</button>
                                    </form>
                                    <form action="/projects/delete_todo_task" id="delete-task-${i}" method="POST" class="delete-task m-1">
                                        <input type="hidden" name="csrfmiddlewaretoken" value=${csrftoken}>
                                        <input type="hidden" name="id_project" value="${data.id_project}">
                                        <input type="hidden" name="id_task" value="${i}">
                                        <button type="submit" class="btn btn-block btn-danger btn-sm">Delete</button>
                                    </form>
                                </div>
                            </div>`);
                    };
                updateFeatures();
                deleteRequirement();
                addRequirements();
                deleteTask();
                }
            });
        });
    })}

    $('.form-update-to-do').each(function() {
        $(this).on('submit', function(e) {
            e.preventDefault();
            var form = $(this);
            $.ajax({
                url: form.attr('action'),
                type: 'POST',
                data: form.serialize(),
                headers: {'X-CSRFToken': csrftoken},
                success: function(data) { 
                    $("#description-task-"+data.id).html(data.info);
                    $("#task-description-"+data.id).toggleClass("task-done");
                    $("#task-description-"+data.id).toggleClass("artefact");
                    form.attr("action", "/projects/"+data.route);
                    $("#update-todo-submit-"+data.id).toggleClass("primary");
                    $("#update-todo-submit-"+data.id).toggleClass("secondary");
                    $("#update-todo-submit-"+data.id).text(data.button);
                }
            });
        });
    });
    function addRequirements(){
        $("#add-requirements-button").click(function() {
            var id_project = $("#id_project").val();
            var user_id = $("#user_id").val();
            $('#form-add-requirements').html(`
            <form action="/projects/add_requirements" method="POST" class="form" id="add-requirements">
                <input type="hidden" name="csrfmiddlewaretoken" value=${csrftoken}>
                <input type="hidden" name="id_project" value="${id_project}">
                <input type="hidden" name="user_id" value="${user_id}}">
                <div class="form-group">
                    <label for="new_requirements">New Requirements</label>
                    <textarea name="new_requirements" class="form-control" id="new_requirements" rows="3" onkeydown="autoGrow(this)" onkeyup="autoGrow(this)"></textarea>
                </div>
                <input type="submit" value="Add" class="btn primary my-2">
            </form>
            `);
        $("#add-requirements").submit(function(e) {
            e.preventDefault();
            var form = $(this);
            $("#form-add-requirements").html(`<button class="btn primary" id="add-requirements-button"> Add Requirements </button>`);
            $.ajax({
                url: form.attr('action'),
                type: 'POST',
                data: form.serialize(),
                headers: {'X-CSRFToken': csrftoken},
                success: function(data) { 
                    var new_requirements = data.new_requirements.split("\r\n");
                    var id_requirement = parseInt(data.num_lines_before);
                    for (var i = 0; i < new_requirements.length; i++) {
                        if (new_requirements[i] != "") {
                            $("#requirements-list").append(
                                `<li class="list-group-item artefact" id="description-${id_requirement}">
                                <div class="d-flex flex-wrap justify-content-between">
                                    <div>
                                        <p class="ml-2" id="requirement-info-${id_requirement}">${new_requirements[i]}</p>
                                    </div>
                                    <div class="d-flex flex-wrap justify-content-between">
                                        <form action="/projects/requirement_completed" id="form-${id_requirement}" method="POST" class="form-update-requirements m-1">
                                            <input type="hidden" name="csrfmiddlewaretoken" value=${csrftoken}>
                                            <input type="hidden" name="id_project" value="${data.id_project}">
                                            <input type="hidden" name="id_requirement" value="${id_requirement}">
                                            <button type="submit" class="btn btn-block primary btn-sm" id="update-requirement-submit-${id_requirement}">Not Completed</button>
                                        </form>
                                        <form action="/projects/delete_requirement" id="delete-${id_requirement}" method="POST" class="form-delete-requirement m-1">
                                            <input type="hidden" name="csrfmiddlewaretoken" value=${csrftoken}>
                                            <input type="hidden" name="id_project" value="${data.id_project}">
                                            <input type="hidden" name="id_requirement" value="${id_requirement}">
                                            <button type="submit" class="btn btn-block btn-danger btn-sm">Delete</button>
                                        </form>
                                    </div>
                                </div>`);
                            id_requirement++;
                        }
                    }
                updateFeatures();
                deleteRequirement();
                addRequirements();
                deleteTask();
                addTask();
                }
                });
            });
        });
    }

    function addTask(){
        $("#addTasks").click(function() {
            var id_project = $("#id_project").val();
            var user_id = $("#user_id").val();
            $('#form-add-to_dos').html(`
            <form action="/projects/add_todo_task" method="POST" id="add-to_dos">
                <input type="hidden" name="csrfmiddlewaretoken" value=${csrftoken}>
                <input type="hidden" name="id_project" value="${id_project}">
                <input type="hidden" name="user_id" value="${user_id}">
                <div class="form-group">
                    <label for="new_requirements">New Requirements</label>
                    <textarea name="new_tasks" class="form-control" id="new_tasks" rows="3" onkeydown="autoGrow(this)" onkeyup="autoGrow(this)"></textarea>
                </div>
                <button type="submit" class="btn primary my-2">Add</button>
            </form>
        `);
        $("#add-to_dos").submit(function(e) {
            e.preventDefault();
            var form = $(this);
            $("#form-add-to_dos").html(`<button class="btn primary mt-2" id="add-requirements-button"> Add Tasks</button>`);
            $.ajax({
                url: form.attr('action'),
                type: 'POST',
                data: form.serialize(),
                headers: {'X-CSRFToken': csrftoken},
                success: function(data) { 
                    var new_to_dos = data.new_to_dos.split("\r\n");
                    var id_task = parseInt(data.num_lines_before);
                    for (var i = 0; i < new_to_dos.length; i++) {
                        if (new_to_dos[i] != "") {
                            $("#to_dos-list").append(
                                `<li class="list-group-item artefact" id="description-${id_task}">
                                <div class="d-flex flex-wrap justify-content-between">
                                    <div>
                                        <p class="ml-2" id="requirement-info-${id_task}">${new_to_dos[i]}</p>
                                    </div>
                                    <div class="d-flex flex-wrap justify-content-between">
                                        <form action="/projects/todo_task_completed" id="form-${id_task}" method="POST" class="form-update-requirements m-1">
                                            <input type="hidden" name="csrfmiddlewaretoken" value=${csrftoken}>
                                            <input type="hidden" name="id_project" value="${data.id_project}">
                                            <input type="hidden" name="id_task" value="${id_task}">
                                            <button type="submit" class="btn btn-block primary btn-sm" id="update-todo-submit--${id_task}">Not Completed</button>
                                        </form>
                                        <form action="/projects/delete_todo_task" id="delete-${id_task}" method="POST" class="form-delete-requirement m-1">
                                            <input type="hidden" name="csrfmiddlewaretoken" value=${csrftoken}>
                                            <input type="hidden" name="id_project" value="${data.id_project}">
                                            <input type="hidden" name="id_task" value="${id_task}">
                                            <button type="submit" class="btn btn-block btn-danger btn-sm">Delete</button>
                                        </form>
                                    </div>
                                </div>`);
                            id_task++;
                        }
                    }
                updateFeatures();
                deleteRequirement();
                addRequirements();
                deleteTask();
                addTask();
                }
                });
            });
        });
    };
    updateFeatures();
    deleteRequirement();
    addRequirements();
    deleteTask();
    addTask();
});







