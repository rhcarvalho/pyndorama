$(function () {
    $(".form_salvar_imagem").hide()
                            .find("input[type=submit]").hide().end()
                            .find("input[type=file]").change(function () {
        $(this).parent(".form_salvar_imagem").hide().submit();
        return false;
    });
    $(".img_upload").click(function () {
        $(this).parent().find(".form_salvar_imagem:first").show();
        return false;
    });
});
