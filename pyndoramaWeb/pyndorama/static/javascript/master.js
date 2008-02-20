/* Scripts para o template master.kid */

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