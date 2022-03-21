function draw_preview(node, file) {
    if (file == null) return;
    var freader = new FileReader();
    freader.readAsDataURL(file[0]);
    freader.onload = function (e) {
        $("#" + node).attr('src', e.target.result);
    }
}


function draw_single_preview(node, file) {
    if (file == null) return;
    var freader = new FileReader();
    freader.readAsDataURL(file);
    freader.onload = function (e) {
        $("#" + node).attr('src', e.target.result);
    }
}



function draw_single_preview_by_url(node, url) {
    if (url == 'null') return;
    $("#" + node).attr('src', url);
}