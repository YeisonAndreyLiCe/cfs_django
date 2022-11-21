import csrftoken from "./get_cookie.js"; 
import {updateToDO, updateRequirements, addLi, showForm} from "./project-features.js";

function updateFeatures(){
  $(".update-feature").each((index, element)=> {
    console.log('element :>> ', element);
    $(element).on("click", (e)=> {
      e.preventDefault();
      const href = $(element).attr("href");
      $.ajax({
        url: href,
        headers: {"X-CSRFToken": csrftoken},
        success: (data)=> {
          $(element).parent().siblings().html(data.info);
          $(element).parent().parent().toggleClass("done");
          $(element).parent().parent().toggleClass("artefact");
          $(element).attr("href", `/projects/update_feature/${data.id}/${data.type}/${data.status}/${data.project_id}/`);
          $(element).toggleClass("primary");
          $(element).toggleClass("secondary");
          $(element).text(data.button);
        }
      });
      return false;
    });
  });
};

function deleteFeature(){
  $(".delete-feature").each((index, element)=> {
    $(element).on("click", (e) => {
      e.preventDefault();
      let href = $(element).attr("href");
      $.ajax({
        url: href,
        success: function(data) {
          if (data.type == "requirements") {
            $("#requirements-list").html("");
            data.lines.forEach((line, index) => {
              $("#requirements-list").append(addLi(data,line, index));
            });
          }else{
            $("#tasks-list").html("");
            data.lines.forEach((line, index) => {
              $("#tasks-list").append(addLi(data, line, index));
            });
          };
        }
      });
      return false;
    });
  });
};

function addFeatures(){
  $("button.add-feature").each((index, element)=>{
    $(element).click(()=> {
      let project_id = $("#id_project").val();
      let user_id = $("#user_id").val();
      let type = $(element).attr("id");
      let parent = $(element).parent();
      $(parent).html(showForm(csrftoken, user_id, project_id, type));
      $(parent).children().submit((e)=> {
        e.preventDefault();
        let form = $(parent).children();
        $.ajax({
          url: form.attr("action"),
          type: "POST",
          data: form.serialize(),
          headers: {"X-CSRFToken": csrftoken},
          success: function(data) {
            if(data.status == "success"){
              let num = parseInt(data.num_lines_before);//-1?
              data.lines.forEach((line, index) => {
                if (data.type == "new_requirements") {
                  $("#requirements-list").append(addLi(data, line, num+index));
                }else{
                  $("#tasks-list").append(addLi(data, line, num+index));
                };
              });
            };
          }
        });
        $(parent).children().html(`<button class="add-feature btn primary my-2" id=${type}> Add ${type.split("_")[1]} </button>`);
        return false;
      });
    });
  });
}


$(document).ready(() => {
  updateFeatures();
  deleteFeature();
  addFeatures();

  const observer = new MutationObserver(()=> {
    updateFeatures();
    deleteFeature();
    addFeatures();
  });

  const targetNode1 = document.getElementById("tasks-list");
  observer.observe(targetNode1, {childList: true});
  const targetNode2 = document.getElementById("requirements-list");
  observer.observe(targetNode2, {childList: true});
});