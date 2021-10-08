
var Notify = (function (placement, align, icon, type, title, message) {
    notify(placement, align, icon, type, title, message);
    function notify(placement, align, icon, type, title, message) {
        $.notify({
            // options
            icon: icon,
            title: title,
            message: message,
        }, {
            element: 'body',
            type: type,
            allow_dismiss: true,
            placement: {
                from: placement,
                align: align
            },
            offset: {
                x: 15, // Keep this as default
                y: 15 // Unless there'll be alignment issues as this value is targeted in CSS
            },
            spacing: 10,
            z_index: 1080,
            delay: 1500,
            timer: 1000,
            url_target: '_blank',
            mouse_over: false,
            animate: {
                enter: 'animated fadeInDown',
                exit: 'animated fadeOutUp'
            },
            template: '<div data-notify="container" class="alert alert-dismissible alert-{0} alert-notify" role="alert">' +
                '<span class="alert-icon" data-notify="icon"></span> ' +
                '<div class="alert-text"</div> ' +
                '<span class="alert-title" data-notify="title">{1}</span> ' +
                '<span data-notify="message">{2}</span>' +
                '</div>' +
                '<button type="button" class="close" data-notify="dismiss" aria-label="Close"><span aria-hidden="true">&times;</span></button>' +
                '</div>'
        })
    }
})


