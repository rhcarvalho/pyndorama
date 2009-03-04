<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python
from base64 import urlsafe_b64encode as b64encode
classes = ('mundo', 'local', 'objeto', 'verbo', 'acao', 'alvo_acao')
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../master.kid'">
<head>
<title>Pyndorama :: Editando Aventura</title>
<style>
body {
    background: #e9e9e9;
}

div {
    border: 1px dashed #F4F4F4;
    border-top: 0;
    border-right: 0;
    margin: 4px 0 16px 88px;
    padding: 0.2em;
}

div.box > div, div.box > form > div, div.box {
    margin-left: 0 !important;
}

th {
    text-align: right;
    color: #AAAAAA;
    font-size: smaller;
}

td {
    padding-left: 1em;
}

.mundo {
    background: #ccccff;
}

.local {
    background: #ccffff;
}

.objeto {
    background: #99ffcc;
}

.verbo {
    background: #ffffaa;
}

.acao {
    background: #ffcc99;
}

.alvo_acao {
    background: #ffcccc;
}
</style>
<script>
$(function () {
    $("input[type=file]").css({display: 'none'});
    $(".img_upload").click(function () {
        $("input[type=file]").css({display: 'block'});
    });
});
</script>
</head>
<body>
<div class="box rounded">
    <div><a href="desfazer">Desfazer</a></div>
    <div py:def="display_thing(container, id)">
        <?python
        level = id.count('.')
        show_add = show_remove_content = level < 5
        show_remove = level > 0
        show_add_image = level in (0, 1)
        ?>
        <table class="${classes[level]}">
            <tr>
                <th>Nome:</th>
                <td py:content="container.get('nome')">Sem Nome</td>
            </tr>
            <tr>
                <th>Descri&ccedil;&atilde;o:</th>
                <td py:content="container.get('descricao')">Sem Descri&ccedil;&atilde;o</td>
            </tr>
        </table>
        <a href="item/${b64encode(id)}" style="margin-left: 88px">editar</a>
        <span py:if="show_remove" py:strip=""> |
        <a href="remover/${b64encode(id)}">remover</a></span>
        <span py:if="show_add" py:strip=""> |
        <a href="adicionar/${b64encode(id)}">adicionar conte&uacute;do</a></span>
        <span py:if="show_add_image" py:strip=""> |
        <a href="#" class="img_upload">adicionar imagem</a></span>
        <span py:if="show_remove_content" py:strip=""> |
        <a href="remover_tudo/${b64encode(id)}">remover conte&uacute;do</a></span>
        <input type="file" id="img_upload_${b64encode(id)}"
               name="img_upload_${b64encode(id)}" />
        <div py:for="index, item in enumerate(container.get('conteudo', []))"
             py:replace="display_thing(item, '%s.%s' % (id, index))" />
    </div>
    <form action="salvar" method="post">
	    <div py:replace="display_thing(mundo, '0')" />
        <input type="submit" value="Salvar" />
    </form>
    <div>
        <p>Nomes das a&ccedil;&otilde;es:</p>
        <p>M - Move para o lugar informado</p>
        <p>P - P&otilde;e o objeto no invent&aacute;rio do jogador</p>
        <p>T - Retira o objeto do invent&aacute;rio do jogador</p>
        <p>A - Ativa o objeto</p>
        <p>B - Bloqueia o objeto</p>
        <p>S - Testa se o objeto est&aacute; ativo</p>
        <p>R - Testa se o objeto est&aacute; bloqueado</p>
        <p>F - Finaliza a aventura</p>
    </div>
</div>
</body>
</html>
