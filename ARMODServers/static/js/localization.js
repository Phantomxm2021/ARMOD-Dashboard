// The default language is English
var lang = getLanguageKey();

function getLanguageKey() {
    var lang = (navigator.language || navigator.userLanguage).toLowerCase();
    if (lang.indexOf('zh') == -1) {
        lang = 'en';
    }

    if (lang === 'zh') {
        lang = 'zh-cn';
    }
    return lang;
}


// Check for localStorage support
if ('localStorage' in window) {
    var usrLang = localStorage.getItem('uiLang');
    if (usrLang) {
        lang = usrLang
    }

}


$(document).ready(function () {

    $(".lang").each(function (index, element) {
        if ($(this).attr("data-content") != null) {
            $(this).attr("data-content",arrLang[lang][$(this).attr("key")])
        }
        else {
            $(this).text(arrLang[lang][$(this).attr("key")]);
        }
    });

    // // update localStorage key
    // if ('localStorage' in window) {
    //     localStorage.setItem('uiLang', lang);
    //     console.log(localStorage.getItem('uiLang'));
    // }

    // $(".lang").each(function (index, element) {
    //     if ($(this).attr("data-content") != null) {
    //         // $(this).data("data-content",arrLang[lang][$(this).attr("key")])
    //     }
    //     else {
    //         // $(this).text(arrLang[lang][$(this).attr("key")]);
    //     }
    // });
});