import csrftoken from "./get_cookie.js"; 
import {updateToDO, updateRequirements, addLi, showForm, addRequirement, addTask, addRequirementFieldInfo, addTaskFieldInfo} from "./project-features.js";

function deleteRequirements(){
  $(".delete-requirement").each((index, element)=> {
    $(element).on("click", (e)=> {
      e.preventDefault();
      let href = $(element).attr("href");
      $.ajax({
        url: href,
        success: function(data) {
          $("#requirements-list").html("");
          data.lines.forEach((line, index) => {
            $("#requirements-list").append(addRequirement(data, line, index));
          });
        }
      });
      addFeatures();
      return false;
    });
  });
};


function deleteTasks(){
  $(".delete-task").each((index, element)=> {
    $(element).on("click", (e)=> {
      e.preventDefault();
      let href = $(element).attr("href");
      $.ajax({
        url: href,
        success: function(data) {
          $("#tasks-list").html("");
          data.lines.forEach((line, index) => {
            $("#tasks-list").append(addTask(data, line, index));
          });
        }
      });
      addFeatures();
      return false;
    });
  });
}
//tasks form
function addTasks(){
  let formTasks = document.getElementById("formAddTasks");
  formTasks.onsubmit = (e)=> {
    e.preventDefault();
    var formData = new FormData(formTasks);
    let FetchTo = formTasks.getAttribute("action");
    fetch(FetchTo, {method: "POST",body: formData,headers: {"X-CSRFToken": csrftoken}})
    .then(response => response.json())
    .then(data => {
      if(data.status == "success"){
        let num = parseInt(data.num_lines_before);
        data.lines.forEach((line, index) => {
          $("#tasks-list").append(addTask(data, line, num+index));
        });
      };
    });
    formTasks.innerHTML = "";
    addTaskButton.style.visibility = "visible";
  }
    return false;
}

//requirements form
function addRequirements(){
  let formRequirements = document.getElementById("formAddRequirements");
  formRequirements.onsubmit = (e)=> {
    e.preventDefault();
    var formData = new FormData(formRequirements);
    let FetchTo = formRequirements.getAttribute("action");
    fetch(FetchTo, {method: "POST",body: formData,headers: {"X-CSRFToken": csrftoken}})
    .then(response => response.json())
    .then(data => {
      if(data.status == "success"){
        let num = parseInt(data.num_lines_before);
        data.lines.forEach((line, index) => {
          $("#requirements-list").append(addRequirement(data, line, num+index));
        });
      };
    });
    formRequirements.innerHTML = "";
    addRequirementsButton.style.visibility = "visible";
  }
  return false;
}

addRequirements();
addTasks();



let addRequirementsButton = document.getElementById("addRequirementsButton");
let addTaskButton = document.getElementById("addTasksButton");

addRequirementsButton.onclick = ()=> {
  let form = document.getElementById("formAddRequirements");
  form.innerHTML= addRequirementFieldInfo();
  addRequirements();
  addRequirementsButton.style.visibility = "hidden";
  return false;
}

addTaskButton.onclick = ()=> {
  let form = document.getElementById("formAddTasks");
  form.innerHTML = addTaskFieldInfo();
  addTaskButton.style.visibility= "hidden";
  addTasks();
  return false;
}
