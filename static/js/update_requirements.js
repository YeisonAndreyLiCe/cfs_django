import csrftoken from "./get_cookie.js"; 
import {updateToDO, updateRequirements, addLi, showForm} from "./project-features.js";
$(document).ready(() => {
  function updateFeatures(){$(".update-feature").each(function() {
    $(this).on("submit", (e)=> {
      e.preventDefault();
      const href = $(this).attr("href");
      $.ajax({
        url: href,
        headers: {"X-CSRFToken": csrftoken},
        success: (data)=> {
          data = JSON.parse(data);
          if (data.type == "requirements") {
            updateRequirements(data);
          }else{
            updateToDO(data);
          }
        },
      });
    });
  });}

  function deleteFeature(){$(".delete-feature").each((index, element)=> {
    $(element).on("click", (e) => {
      e.preventDefault();
      let href = $(element).attr("href");
      $.ajax({
        url: href,
        success: function(data) {
          if (data.type == "new_requirements") {
            $("#requirements-list").html("");
            data.lines.forEach((line, index) => {
              $("#requirements-list").append(addLi(data,line, index));
            });
          }else{
            $("#tasks-list").html("");
            data.lines.forEach((line, index) => {
              $("#tasks-list").append(addLi(data, line, index));
            });
          }
          updateFeatures();
          deleteFeature();
        }
      });
    });
  });}

  function addFeatures(){
    $("button.add-feature").each((index, element)=>{
      $(element).click(()=> {
        let project_id = $("#id_project").val();
        let user_id = $("#user_id").val();
        let type = $(element).attr("id");
        let parent = $(element).parent();
        $(parent).html(showForm(csrftoken, user_id, project_id, type));
        addFeaturesSubmit(type);
      });
    });
  }

  function addFeaturesSubmit(type){
    $("#add_"+type).submit(function(e) {
      e.preventDefault();
      let form = $(this);
      $(this).parent().html(`<button class="add-feature btn primary my-2" id=${type}> Add ${type.split("_")[1]} </button>`);
      $.ajax({
        url: form.attr("action"),
        type: "POST",
        data: form.serialize(),
        headers: {"X-CSRFToken": csrftoken},
        success: function(data) {
          if(data.status == "success"){
            let num = parseInt(data.num_lines_before)-1;
            data.lines.forEach((line, index) => {
              if (type == "new_requirements") {
                console.log(addLi(data, line, num));
                $("#requirements-list").append(addLi(data, line, num+index));
              }else{
                $("#tasks-list").append(addLi(data, line, num+index));
              }
            });
          };
        }
      });
      addFeatures();
      updateFeatures();
      deleteFeature();
    });
  }
  addFeatures();
  updateFeatures();
  deleteFeature();
});