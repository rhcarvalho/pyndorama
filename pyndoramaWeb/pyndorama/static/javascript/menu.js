﻿/* Scripts para o template menu.kid */

var set_onclick = function (element, action) {
    element.onclick = function () {
        var form = document.getElementById('form_adv');
        if (form) {
            form.action = action;
            return form.submit();
        }
    }
};

addLoadEvent(function () {
    var field = document.getElementById('btn_editar');
    if (field) {
        set_onclick(field, '/editor/');
    }
    
    field = document.getElementById('btn_editar_yaml');
    if (field) {
        set_onclick(field, '/edityaml');
    }
});