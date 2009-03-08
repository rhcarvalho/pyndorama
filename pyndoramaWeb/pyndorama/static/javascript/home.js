$(function () {
    var setaction = function (action) {
        return function () {
            $("#form_adv").attr({action: action}).submit();
        };
    };

    $("#btn_editar").click(setaction('/editor/'));
    $("#btn_editar_yaml").click(setaction('/edityaml'));
    $("#btn_iniciar").click(setaction('/iniciar'));
});
