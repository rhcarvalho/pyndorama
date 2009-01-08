<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
<head>
<title>Pyndorama :: Editando Aventura</title>
<style>
div {
    border: 1px dashed #F4F4F4;
    border-top: 0;
    border-right: 0;
    margin: 4px 0 16px 88px;
    padding: 0.2em;
}

th {
    text-align: right;
    color: #AAAAAA;
    font-size: smaller;
}

td {
    padding-left: 1em;
}
</style>
</head>
<body>

<div py:def="display_thing(container)">
    <table>
        <tr>
            <th>Nome:</th>
            <td py:content="container.get('nome')">Sem Nome</td>
        </tr>
        <tr>
            <th>Descri&ccedil;&atilde;o:</th>
            <td py:content="container.get('descricao')">Sem Descri&ccedil;&atilde;o</td>
        </tr>
    </table>
    <a href="item${0}" style="margin-left: 88px">editar</a>
    <div py:for="item in container.get('conteudo', [])" py:replace="display_thing(item)" />
</div>

<div py:replace="display_thing(mundo)" />

</body>
</html>
