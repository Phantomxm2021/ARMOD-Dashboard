var tagsOption = new Array()

function display_tag_manager() {
    $("#tag_manager_container").html('')
    $.ajax({
        url: `/dashboard/apps/appdetails/${app_uid}/tagmanager/`,
        type: 'GET',
        success: function (result) {
            switch (result.code) {
                case 200:
                    $("#tag_manager_container").append(result.data)
                    openTagManagerSideDrawer();
                    break;
                case 201:
                    new Notify('top', 'right', 'ni ni-bell-55', 'danger', 'ERROR!!!', result.message)
                    break;
            }
        },
    });
}


function deletetag(tagName) {
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();

    $.ajax({
        headers: {
            "X-CSRFToken": csrftoken
        },
        url: `/dashboard/apps/appdetails/${app_uid}/tagmanager/`,
        type: 'POST',
        data: { "method_type": "DeleteTag", "tag_name": tagName, "app_uid": app_uid },
        success: function (result) {
            switch (result.code) {
                case 200:
                    $("#tag_manager_container").html(result.data)

                    break;
                case 201:
                    new Notify('top', 'right', 'ni ni-bell-55', 'danger', 'ERROR!!!', result.message)
                    break;
            }
        },
    });
}

function createtag() {
    new_tag = $("#new_tag").val()
    if (new_tag == '' || new_tag == 'undefine') {
        new Notify('top', 'right', 'ni ni-bell-55', 'danger', 'ERROR!!!', 'You can not add empty tag!')
        return;
    }
    passData = {
        'method_type': 'CreateTag',
        'app_uid': app_uid,
        'tag_name': new_tag,
        'tag_weight': $("#tag_weight").val()
    }

    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    $.ajax({
        url: `/dashboard/apps/appdetails/${app_uid}/tagmanager/`,
        type: 'POST',
        data: passData,
        headers: {
            "X-CSRFToken": csrftoken
        },
        success: function (result) {
            switch (result.code) {
                case 200:
                    $("#new_tag").val(null)
                    $("#tag_weight").val(null)
                    new Notify('top', 'right', 'ni ni-bell-55', 'success', 'Success!!!', result.message)
                    $("#tag_manager_container").html(result.data)
                    $("#create-new-tags-modal").modal('hide')
                    break;
                case 201:
                    new Notify('top', 'right', 'ni ni-bell-55', 'danger', 'Error!!!', result.message)
                    break;
            }
        },
        error: function (_data) { console.log(_data); },
    })
}

function hideSelected(value) {
    if (value && !value.selected) {
        return $('<span>' + value.text + '</span>');
    }
}


var selector = null;

function loadtags(callback) {
    selector = $("#project_tags_display").select2({
        templateResult: hideSelected,
    });

    selector.val(null);
    selector.find('option').remove()

    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    $.ajax({
        url: `/dashboard/apps/appdetails/${app_uid}/tagmanager/`,
        type: 'POST',
        data: { "app_uid": app_uid, "method_type": "GetTags" },
        headers: {
            "X-CSRFToken": csrftoken
        },
        success: function (result) {
            switch (result.code) {
                case 200:
                   

                    for (var tag in result.data) {
                        newOption = new Option(result.data[tag].tag_name, result.data[tag].tag_name, false, false)
                       selector.append(newOption)
                    }
                    callback();

                    break;
                case 201:
                    new Notify('top', 'right', 'ni ni-bell-55', 'danger', 'ERROR!!!', result.message)
                    break;
            }
        }
    });
}

