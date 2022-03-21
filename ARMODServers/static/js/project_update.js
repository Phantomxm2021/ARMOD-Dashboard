var preview_image_list = new Array();

//Remove the image after apply
var will_remove_preview_image_list = new Array()

$("#project_icon_image").change(function () {
    draw_preview("project_icon_image_display", $("#project_icon_image")[0].files);
});


$("#project_preview_image").change(function () {
    seleted_files = $("#project_preview_image")[0].files;
    children = $("#project_preview_image_display_area").children();
    child_count = children.length;

    if (child_count >= 6) {
        new Notify('top', 'left', 'ni ni-bell-55', 'danger', 'ERROR!!!', 'Up to 6 preview images!');
        return;
    }

    if (seleted_files.length < 2) {
        //single
        if (child_count == 0)
            generate_preview_image(child_count, seleted_files[0]);
        else {
            var last_idx = $(children[child_count - 1]).attr('id').split('_')[2];
            generate_preview_image(1 + parseInt(last_idx), seleted_files[0]);
        }

    } else {
        for (var idx = 0; idx < seleted_files.length; idx++) {

            if (idx + child_count >= 6 || child_count >= 6) {
                new Notify('top', 'left', 'ni ni-bell-55', 'danger', 'ERROR!!!', 'Up to 6 preview images!');
                return;
            }
            generate_preview_image(idx + child_count, seleted_files[idx]);
        }
    }

});


$("#project_banner_image").change(function () {
    draw_single_preview('project_header_image_display', $("#project_banner_image")[0].files[0]);
});

function wsaAssetsSelected() {
    var wsa_files = $('#WSA')[0].files
    uploadAssets('WSA', wsa_files)
}

function iosAssetsSelected() {
    var ios_files = $('#iOS')[0].files
    uploadAssets('iOS', ios_files)
}

function androidAssetsSelected() {
    var android_files = $('#Android')[0].files
    uploadAssets('Android', android_files)
}

function uploadAssets(platform, files) {
    $("#asseturl-" + platform).attr("Style", "display:none;");
    $("#spinner-" + platform).attr("Style", "display:block;");
    var data = new FormData();
    data.append('app_uid', app_uid)
    data.append('project_id', $("#project_id_display").text())
    data.append("project_name", $("#project_name_display").text());
    data.append("platform", platform);
    data.append("method_type", "UploadARResources");

    data.append(files[0].name.split('.').pop().toLowerCase(), files[0])
    data.append(files[1].name.split('.').pop().toLowerCase(), files[1])

    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    $.ajax({
        xhr: function () {
            var xhr = new window.XMLHttpRequest();
            xhr.upload.addEventListener("progress", function (evt) {
                if (evt.lengthComputable) {
                    var percentComplete = (evt.loaded / evt.total) * 100;
                    // Place upload progress bar visibility code here
                }
            }, false);
            return xhr;
        },
        url: "/dashboard/apps/updateproject/",
        type: 'POST',
        data: data,
        headers: {
            "X-CSRFToken": csrftoken
        },
        success: function (result) {
            switch (result.code) {
                case 200:
                    data = result.data;
                    var elements = data.json_url.split('/');
                    JsonFileName = elements[elements.length - 1];
                    var bundleFileElements = data.bundle_url.split('/')
                    bundleFileName = bundleFileElements[bundleFileElements.length - 1]


                    switch (data.platform_type) {
                        case "iOS":
                            $("#ios-json").text(JsonFileName)
                            $("#ios-bundle").text(bundleFileName)
                            break;
                        case "Android":
                            $("#android-json").text(JsonFileName)
                            $("#android-bundle").text(bundleFileName)
                            break;
                        case "WSA":
                            $("#wsa-json").text(JsonFileName)
                            $("#wsa-bundle").text(bundleFileName)
                            break;
                    }

                    $("#asseturl-" + platform).attr("Style", "display:block;");
                    $("#spinner-" + platform).attr("Style", "display:none;");

                    new Notify('top', 'right', 'ni ni-bell-55', 'success', 'Success!!!', result.message)

                    break;
                case 201:
                    new Notify('top', 'right', 'ni ni-bell-55', 'danger', 'Error!!!', result.message)

                    break;
            }

            $('#iOS').val(null)
            $('#Android').val(null)
        },
        error: function (_data) {
            new Notify('top', 'right', 'ni ni-bell-55', 'danger', 'Error!!!', result.message)
        },
        contentType: false,
        processData: false,
    })
}


function generate_preview_image(idx, file) {
    element = `<div id='preview_wrap_${idx}' class="scroller-image_wrap"><span role='button' class='delete-button' tabindex='0' id='project_preview_image_delete_btn_${idx}' onclick='delete_preview_element(this)'></span><img class='scroller-item' id='project_preview_image_display_${idx}' src='' /></div>`;
    $("#project_preview_image_display_area").append(element);
    draw_single_preview(`project_preview_image_display_${idx}`, file);
    preview_image_list.push(file);
    update_preview_image_count_display();
}

function generate_preview_image_by_url(idx, url) {
    element = `<div id='preview_wrap_${idx}' class="scroller-image_wrap"><span role='button' class='delete-button' tabindex='0' id='project_preview_image_delete_btn_${idx}' onclick='delete_preview_element(this)'></span><img class='scroller-item' id='project_preview_image_display_${idx}' src='' /></div>`;
    $("#project_preview_image_display_area").append(element);
    draw_single_preview_by_url(`project_preview_image_display_${idx}`, url)
    update_preview_image_count_display();
}

function delete_preview_element(element) {
    var tmp_WillRemoveNodeId = $(element).parent().attr('id');
    var tmp_WillRemoveFileId = tmp_WillRemoveNodeId.split('_')[2];
    will_remove_preview_image_list.push(parseInt(tmp_WillRemoveFileId));
    $(`#${tmp_WillRemoveNodeId}`).remove();
    update_preview_image_count_display();
}


function update_preview_image_count_display() {
    $("#preview_image_count_display").text(`(${$("#project_preview_image_display_area").children().length}/6)`);
}

function getFileFromInput(nodeId) {
    var tmp_Files = $(`#${nodeId}`)[0].files
    return tmp_Files.length > 0 ? tmp_Files[0] : null;
}

$("#project_detail_apply_btn").click(function () {
    //Clean removed image from the array
    for (var idx = 0; idx < will_remove_preview_image_list.length; idx++) {
        preview_image_list.splice(will_remove_preview_image_list[idx], 1);
    }


    var data = new FormData();
    data.append('method_type', 'UpdateProject')
    data.append('app_uid', app_uid)
    data.append('project_id', $("#project_id_display").text())
    data.append('project_name', $("#project_name_display").val())
    data.append('project_description', $("#project_description_display").val())
    data.append('project_support_url', $("#project_support_url_display").val())
    data.append('project_brief', $("#project_brief_display").val())
    data.append('project_weight', $("#project_weight_display").val())
    data.append('project_preview_count', preview_image_list.length);
    data.append('project_preview_delete_id', JSON.stringify(will_remove_preview_image_list));
    data.append('project_tags', JSON.stringify($('#project_tags_display').val()));

    for (var idx = 0; idx < preview_image_list.length; idx++) {
        data.append(`project_preview_${idx}`, preview_image_list[idx]);
    }

    project_icon_file = getFileFromInput("project_icon_image");
    data.append('project_icon', project_icon_file);

    project_banner_file = getFileFromInput("project_banner_image");
    data.append('project_header', project_banner_file);

    data.append('project_permission', $("#project_permission_checker").prop('checked') == true ? 1 : 0);
    data.append('project_status', $("#project_publish_checker").prop('checked') == true ? 1 : 0);
    data.append('project_recommend', $("#project_recommend_checker").prop('checked') == true ? 1 : 0);


    will_remove_preview_image_list = new Array();

    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    $.ajax({
        xhr: function () {
            var xhr = new window.XMLHttpRequest();
            xhr.upload.addEventListener("progress", function (evt) {
                if (evt.lengthComputable) {
                    var percentComplete = (evt.loaded / evt.total) * 100;
                    // Place upload progress bar visibility code here
                }
            }, false);
            return xhr;
        },
        url: `/dashboard/apps/updateproject/`,
        type: 'POST',
        data: data,
        headers: {
            "X-CSRFToken": csrftoken
        },
        success: function (result) {
            switch (result.code) {
                case 200:
                    // $("#project_name_display").val(result.data.project_name)
                    // var create_time = new Date(result.data.create_time).Format("yyyy-MM-dd hh:mm:ss");
                    // var update_time = new Date(result.data.update_time).Format("yyyy-MM-dd hh:mm:ss");;
                    // $("#project-create-time").html(create_time)
                    // $("#project-update-time").html(update_time)
                    seleted_tags = new Array();
                    new Notify('top', 'right', 'ni ni-bell-55', 'success', 'Success!!!', result.message)
                    break;
                case 201:
                    new Notify('top', 'right', 'ni ni-bell-55', 'danger', 'ERROR!!!', result.message)
                    break;
            }
        },
        contentType: false,
        processData: false,
    });
});


function deleteproject() {
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    data = { 'project_id': $("#project_id_display").text(), 'app_uid': app_uid, "method_type": "DeleteProject" };

    $.ajax({
        url: `/dashboard/apps/appdetails/${app_uid}/`,
        type: 'POST',
        data: data,
        headers: {
            "X-CSRFToken": csrftoken
        },
        success: function (result) {
            switch (result.code) {
                case 200:
                    window.location.reload()
                    break;
                case 201:
                    new Notify('top', 'right', 'ni ni-bell-55', 'danger', 'ERROR!!!', result.message)
                    break;
            }
        }
    });
}
