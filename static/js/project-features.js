export const updateToDO = (data) => {
  $("#task-description-"+data.id).html(data.info);
  $("#task-description-"+data.id).toggleClass("task-done");
  $("#task-description-"+data.id).toggleClass("artefact");
  $(this).attr("href", `/projects/update_feature/${data.id}/${data.type}/${data.status}/${data.project_id}/`);
  $(this).toggleClass("primary");
  $(this).toggleClass("secondary");
  $(this).text(data.button);
};

export const updateRequirements = (data) => {
  $("#requirement-info-"+data.id).html(data.info);
  $("#description-"+data.id).toggleClass("done");
  $("#description-"+data.id).toggleClass("artefact");
  $(this).attr("href", `/projects/update_feature/${data.id}/${data.type}/${data.status}/${data.project_id}/`);
  $(this).toggleClass("primary");
  $(this).toggleClass("secondary");
  $(this).text(data.button);
};

export const addLi= (data, line, index) => {
  return(`
    <li id="${data.type}-${index}" class="list-group-item artefact ${data.status=="complete" ? "done":"artefact"}">
      <div class="d-flex flex-wrap justify-content-between">
        <p class="ml-2" id="${data.type}-info-${index}">${line}</p>
        <div class="d-flex flex-wrap justify-content-between">
        <a href="/projects/update_feature/${index}/${data.type}/${data.status}/${data.project_id}" class="update-feature btn btn-block ${ data.status == "Complete" ? "secondary" : "primary" } btn-sm">
                ${ data.status == "Completed" ? "Completed" : "Not Completed" }
        </a>
        <a href="/projects/delete_feature/${index}/${data.type}/${data.id_project}" class="delete-feature btn btn-block btn-danger btn-sm">
                Delete
        </a>
        </div>
      </div>
  </li>`
  );
};

export const showForm = (token, user_id, project_id, type)=>{
    return(
    `<form action="/projects/add_features/${type}" method="POST" class="form" id="add_${type}">
        <input type="hidden" name="csrfmiddlewaretoken" value=${token}>
        <input type="hidden" name="id_project" value="${project_id}">
        <input type="hidden" name="user_id" value="${user_id}">
        <div class="form-group">
        <label for="input_${type}">New ${type.split("_")[1]}</label>
        <textarea name="${type}" class="form-control" id="input_${type}" rows="3" onkeydown="autoGrow(this)" onkeyup="autoGrow(this)"></textarea>
        </div>
        <input type="submit" value="Add" class="btn primary my-2">
    </form>`);
};