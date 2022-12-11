import csrftoken from "./get_cookie.js"; 
import {addRequirement, addTask, addRequirementFieldInfo, addTaskFieldInfo} from "./project-features.js";

function deleteRequirements(){
  let requirements = document.getElementsByClassName("delete-requirement");
  for (let i = 0; i < requirements.length; i++) {
    requirements[i].onclick = (e)=> {
      e.preventDefault();
      let href = requirements[i].getAttribute("href");
      fetch(href, {method: "POST",headers: {"X-CSRFToken": csrftoken}})
      .then(response => response.json())
      .then(data => {
        $("#requirements-list").html("");
        data.lines.forEach((line, indexList ) => {
          $("#requirements-list").append(addRequirement(data, line, indexList ));
        });
      });
      return false;
    }
  }
};


function deleteTasks(){
  let tasks = document.getElementsByClassName("delete-task");
  for (let i = 0; i < tasks.length; i++) {
    tasks[i].onclick = (e)=> {
      e.preventDefault();
      let href = tasks[i].getAttribute("href");
      fetch(href, {method: "POST",headers: {"X-CSRFToken": csrftoken}})
      .then(response => response.json())
      .then(data => {
        document.getElementById("tasks-list").innerHTML = "";
        data.lines.forEach((line, indexList ) => {
          $("#tasks-list").append(addTask(data, line, indexList));
        });
      });
      return false;
    }
  }
};

/* deleteRequirements();
deleteTasks(); */

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
    //deleteTasks();
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
    //deleteRequirements();
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

