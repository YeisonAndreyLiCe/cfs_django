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


export const addTask = (data, line, index) => {
  return(`
    <li id="ToDo-${index}" class="list-group-item artefact ${data.status=="complete" ? "done":"artefact"}">
      <div class="d-flex flex-wrap justify-content-between">
        <p class="ml-2" id="ToDo-info-${index}">${line}</p>
        <div class="d-flex flex-wrap justify-content-between align-items-center">
        <a href="/projects/delete/task/${index}/${data.id_project}" class="delete-task btn btn-block btn-danger btn-sm" onclick="deleteTasks()">
                Delete
        </a>
        </div>
      </div>
  </li>`
  );
};

export const addRequirement = (data, line, index) => {
  return(`
    <li id="requirement-${index}" class="list-group-item artefact">
      <div class="d-flex flex-wrap justify-content-between">
        <p class="ml-2" id="requirement-info-${index}">${line.split("--version")[0]}</p>
        <div class="d-flex flex-wrap justify-content-between align-items-center">
        <button class="btn btn-sm primary mx-2"> ${line.split("--version")[1]? "version" + line.split("--version")[1]: "last version"} </button>
        <a href="/projects/delete/requirement/${index}/${data.id_project}" class="delete-requirement btn btn-block btn-danger btn-sm" >
            Delete
        </a>
        </div>
      </div>
  </li>`
  );
};

export const addLi= (data, line, index) => {
  return(`
    <li id="${data.type}-${index}" class="list-group-item artefact ${data.status=="complete" ? "done":"artefact"}">
      <div class="d-flex flex-wrap justify-content-between">
        <p class="ml-2" id="${data.type}-info-${index}">${line}</p>
        <div class="d-flex flex-wrap justify-content-between">
        <a href="/projects/update_feature/${index}/${data.type}/Not Completed/${data.id_project}" class="update-feature btn btn-block" }
        </a>
        <a href="/projects/delete_feature/${index}/${data.type}/${data.id_project}" class="delete-task btn btn-block btn-danger btn-sm">
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
        <label for="input_${type}" class="h3 my-2">New ${type.split("_")[1]? "Requirements":"Tasks"}</label>
        <textarea name="${type}" class="form-control" id="input_${type}" rows="3" onkeydown="autoGrow(this)" onkeyup="autoGrow(this)"></textarea>
        </div>
        <input type="submit" value="Add" class="btn primary my-2">
    </form>`);
};

export const addTaskFieldInfo = ()=>{
  return(
  `<div class="form-group
    <label for="input_task" class="h3 my-2">New Task </label>
    <textarea name="tasks" class="form-control" id="input_task" rows="1" onkeydown="autoGrow(this)" onkeyup="autoGrow(this)"></textarea>
  </div>
  <input type="submit" value="Add" class="btn primary my-2">`
  );
};

export const addRequirementFieldInfo = ()=>{
  return(
  `<div class="form-group
    <label for="input_requirement" class="h3 my-2">New Requirement </label>
    <textarea name="requirements" class="form-control" id="input_requirement" rows="1" onkeydown="autoGrow(this)" onkeyup="autoGrow(this)"></textarea>
  </div>
  <input type="submit" value="Add" class="btn primary my-2">`
  );
};

export const addWireFrame = (token, user_id, project_id) =>{
  return( `
  <form action="projects/add_wireFrame" method="POST" enctype="multipart/form-data">
      <input type="hidden" name="csrfmiddlewaretoken" value=${token}>
      <input type="hidden" name="id_project" value="${project_id}">
      <label for="wireFrame" class="fw-bold">User Flow Image</label>
      <input type="file" name="wireFrame" id="wireFrame">
      <input type="submit" value="Add WireFrame" class="btn primary">
  </form>
`);
};