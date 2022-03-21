$("#app_icon_image").change(function () {
    draw_preview("app_icon_image_display", $("#app_icon_image")[0].files)
});



$("#createapp").click(function () {
    $("#packageid").change()
    $("#app_name").change()
    $("#description").change()

    app_icon_image = $("#app_icon_image")[0].files[0];
    app_name = $("#app_name").val();
    packageid = $("#packageid").val();
    project_description = $("#description").val();

    var packageidPatten = pattern = /^(com)(.\w+){2,}/;
    if (!packageidPatten.test(packageid) || app_name == '') return;

    if (app_name == '') return;
    var data = new FormData();
    data.append("app_name", app_name);
    data.append("method_type", 'CreateApp');
    data.append("packageid", packageid);
    data.append("project_description", project_description);
    data.append("app_icon_image", app_icon_image)

    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    $.ajax({
        url: "/dashboard/apps/",
        type: 'POST',
        data: data,
        headers: {
            "X-CSRFToken": csrftoken
        },
        success: function (result) {
            console.log(result)
            switch (result.code) {
                case 200:
                    window.location.reload();
                    break;
                case 201:
                    new Notify('top', 'right', 'ni ni-bell-55', 'danger', 'ERROR!!!', result.message)
                    break;
            }
        },
        error: function (_data) { console.log(_data); },
        contentType: false,
        processData: false,
    })

});
