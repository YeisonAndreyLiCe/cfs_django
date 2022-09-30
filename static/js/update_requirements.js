"use strict";
import csrftoken from "./get_cookie.js";
/* eslint-disable */
$(document).ready(() => {
  function updateFeatures(){$(".update-feature").each(function() {
    $(this).on("submit", function(e) {
      e.preventDefault();
      var href = $(this).attr("href");
      $.ajax({
        url: href,
        headers: {"X-CSRFToken": csrftoken},
        success: function(data) {
          if (data.type == "requirements") {
            $("#requirement-info-"+data.id).html(data.info);
            $("#description-"+data.id).toggleClass("done");
            $("#description-"+data.id).toggleClass("artefact");
            $(this).attr("href", `/projects/update_feature/${data.id}/${data.type}/${data.status}/${data.project_id}/`);
            $(this).toggleClass("primary");
            $(this).toggleClass("secondary");
            $(this).text(data.button);
          }else{
            $("#task-description-"+data.id).html(data.info);
            $("#task-description-"+data.id).toggleClass("task-done");
            $("#task-description-"+data.id).toggleClass("artefact");
            $(this).attr("href", `/projects/update_feature/${data.id}/${data.type}/${data.status}/${data.project_id}/`);
            $(this).toggleClass("primary");
            $(this).toggleClass("secondary");
            $(this).text(data.button);
          }
        },
      });
    });
  });}
  function deleteFeature(){$(".delete-feature").each(function() {
    $(this).on("submit", function(e) {
      e.preventDefault();
      var href = $(this).attr("href");
      $.ajax({
        url: href,
        success: function(data) {
          if (data.type == "requirements") {
            $("#requirements-list").html("");
            var lines = data.lines;
            for (var i = 0; i < lines.length; i++) {
              $("#requirements-list").append(`
                            <li class="list-group-item artefact ${data.status=="complete" ? "done":"artefact"} id="requirement-${i}}">
                                <div class="d-flex flex-wrap justify-content-between">
                                    <p class="ml-2" id="requirement-info-${i}}">${data.info}</p>
                                    <div class="d-flex flex-wrap justify-content-between">
                                        <a href="/update_feature/${i}/${data.type}/${data.status}/${data.project_id}" class="update-feature btn btn-block ${ data.status == "Complete" ? "secondary" : "primary" } btn-sm">${ data.status == "Completed" ? "Completed" : "Not Completed" }</a>
                                        <a href="/delete_feature/${i}/${data.type}/${data.id_project}" class="delete-feature btn btn-block btn-danger btn-sm">Delete</a>
                                    </div>
                                </div>
                            </li>`
              );
            }
          }
        }
      });
    });
  });}


  function addFeatures(){
    $(".add-feature").each(function() {
      $(this).click(function() {
        var id_project = $("#id_project").val();
        var user_id = $("#user_id").val();
        var type = $(this).attr("id");
        $(this).parent().html(`
                <form action="/projects/add_features/new_requirements" method="POST" class="form" id="add_new_requirements">
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
        addFeaturesSubmit(type);
      });
    });
  }

  function addFeaturesSubmit(type){
    $("#add_"+type).submit(function(e) {
      e.preventDefault();
      var form = $(this);
      console.log(form);
      console.log(form.serialize());
      $(this).parent().html(`<button class="add-feature btn primary my-2" id=${type}> Add ${type.split("_")[1]} </button>`);
      $.ajax({
        url: form.attr("action"),
        type: "POST",
        data: form.serialize(),
        headers: {"X-CSRFToken": csrftoken},
        success: function(data) {
          if(data.status == "success"){
            var info = data.info.split("\r\n");
            var id_feature = parseInt(data.num_lines_before);
            $("#"+type.split("_")[0]+"-list").html("");
            for (var i = parseInt(data.num_lines_before); i < info.length; i++) {
              $("#"+type.split("_")[0]+"-list").append(`
                                <li class="list-group-item artefact ${data.status=="complete" ? "done":"artefact"} id="requirement-${id_feature}}">
                                    <div class="d-flex flex-wrap justify-content-between">
                                        <p class="ml-2" id="requirement-info-${id_feature}}">${data.info}</p>
                                        <div class="d-flex flex-wrap justify-content-between">
                                            <a href="/update_feature/${id_feature}/${data.type}/${data.status}/${data.id_project}" class="update-feature btn btn-block ${ data.status == "Complete" ? "secondary" : "primary" } btn-sm">${ data.status == "Completed" ? "Completed" : "Not Completed" }</a>
                                            <a href="/delete_feature/${id_feature}/${data.type}/${data.id_project}" class="delete-feature btn btn-block btn-danger btn-sm">Delete</a>
                                        </div>
                                    </div>
                                </li>`
              );
            }
            id_feature++;
          } 
        }
      });
    });
  }
    

  addFeatures();
  updateFeatures();
  deleteFeature();
  addFeatures();
});
