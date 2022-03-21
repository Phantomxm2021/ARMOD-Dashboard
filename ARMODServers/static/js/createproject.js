$("#app_icon_image").change(function () {
    draw_preview("app_icon_image_display", $("#app_icon_image")[0].files)
});

$("#create_project_btn").click(function () {
    project_name = $("#project_name").val()
    description = $("#description").val()
    if (project_name == '') return;

    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    data = {
        'app_uid': app_uid,
        'project_name': project_name,
        'project_description': description,
        'method_type': "CreateProject"
    }
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
});

$("#update_app_detail").click(function () {
    var app_icon_image = $("#app_icon_image")[0].files[0];


    var data = new FormData();
    data.append("app_uid", app_uid)
    data.append("method_type", "UpdateApp");
    data.append("app_icon_image", app_icon_image);
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
        },
        error: function (_data) { console.error(_data); },
        contentType: false,
        processData: false,
    });
})

function getprojectdetail(app_uid, arexperience_uid, projectname) {
    loadtags(function () {
        $("#project_preview_image_display_area").empty();
        //onselected(app_uid, arexperience_uid, projectname)
        var csrftoken = $("[name=csrfmiddlewaretoken]").val();
        $.ajax({
            url: `/dashboard/apps/appdetails/${app_uid}/projectdetails/${arexperience_uid}`,
            type: 'GET',
            headers: {
                "X-CSRFToken": csrftoken
            },
            success: function (result) {
                switch (result.code) {
                    case 200:
                        openSideDrawer()
                        $("#project_name_display").val(result.data.project_name)
                        $("#project_id_display").text(result.data.project_id)
                        $("#project_description_display").val(result.data.project_description)
                        $("#project_brief_display").val(result.data.project_brief)
                        $("#project_support_url_display").val(result.data.project_support_url)
                        $("#project_permission_checker").prop("checked", result.data.project_permission == 1);
                        $("#project_publish_checker").prop("checked", result.data.project_status == 1);
                        $("#project_recommend_checker").prop("checked", result.data.project_recommend == 1);

                        $("#project_weight_display").val(result.data.project_weight)



                        $("#project_header_image_display").attr('src', result.data.project_header)
                        $("#app_detail_icon_image").attr('src', result.data.project_icon)
                        $("#project_icon_image_display").attr('src', result.data.project_icon)

                        selector.val(result.data.project_tags).trigger('change')

                        if (result.data.project_preview != '') {
                            preview_images = JSON.parse(result.data.project_preview)
                            for (var idx = 0; idx < preview_images.length; idx++) {
                                generate_preview_image_by_url(idx, preview_images[idx]);
                            }
                        } else {
                            $("#project_preview_image_display_area").empty();
                        }


                        for (var idx = 0; idx < result.data.resources.length; idx++) {

                            var elements = result.data.resources[idx].json_url.split('/');
                            JsonFileName = elements[elements.length - 1];
                            var bundleFileElements = result.data.resources[idx].bundle_url.split('/')
                            bundleFileName = bundleFileElements[bundleFileElements.length - 1]

                           
                            switch (result.data.resources[idx].platform_type) {
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
                        }



                        break;
                    case 201:
                        new Notify('top', 'right', 'ni ni-bell-55', 'danger', 'ERROR!!!', result.message)
                        break;
                }
            }
        });
    });
}

$("#delete-app-btn").click(function () {
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    data = { 'app_uid': app_uid, 'method_type': "DeleteApp" };

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
                    window.location.href = "/dashboard/apps/"
                    break;
                case 201:
                    new Notify('top', 'right', 'ni ni-bell-55', 'danger', 'ERROR!!!', result.message)
                    break;
            }
        }
    });
});