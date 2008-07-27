/* Scripts para o template menu.kid */

/* Focar caixa de texto ao carregar a página  */
addLoadEvent(function () {
    var field = document.getElementById('btn_editar');

    if (field) {
        field.onclick = function () {
            var form = field.parentNode;
            while (form.tagName != 'FORM') {
                alert(form);
                form = form.parentNode;
            }

            form.action = '/edityaml';
            return form.submit();
        }
    }
});