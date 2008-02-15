/* Scripts para o template principal.kid */

addLoadEvent = function (func) {
    var oldLoadEvent = window.onload;
    if (typeof oldLoadEvent == 'function')
    {
        window.onload = function () {
            oldLoadEvent();
            func();
        }
    }
    else
    {
        window.onload = func;
    }
}

/* Focar caixa de texto ao carregar a página  */
addLoadEvent(function () {
    var fields = document.getElementsByTagName('input');

    for (var i = 0; i <= fields.length; i++)
    {
        var field = fields[i];
        if (field.type == 'text')
        {
            field.focus();
            break;
        }
    }
});