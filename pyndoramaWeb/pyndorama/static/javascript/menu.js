/* Scripts para o template menu.kid */

var set_onclick = function (element, action) {
    element.onclick = function () {
        var form = document.getElementById('form_adv');
        if (form) {
            form.action = action;
            return form.submit();
        }
    }
};

$(function () {
    var field = document.getElementById('btn_editar');
    if (field) {
        set_onclick(field, '/editor/');
    }
    
    field = document.getElementById('btn_editar_yaml');
    if (field) {
        set_onclick(field, '/edityaml');
    }
    
    field = document.getElementById('btn_iniciar');
    if (field) {
        set_onclick(field, '/iniciar');
    }
});

/* jQuery version

$(function(){
    $("btn_editar").click(function(){
        alert("god");
        $("form_adv").action = '/editor/';
    });
    
    $("btn_editar_yaml").click(function(){
        $("form_adv").action = '/edityaml';
    });
    
    $("btn_iniciar").click(function(){
        $("form_adv").action = '/iniciar';
    });
});

*/
