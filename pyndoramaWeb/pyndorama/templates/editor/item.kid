<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../master.kid'">
<head>
<title>Pyndorama :: Editando Aventura</title>
<style>
form {
    margin: auto;
    padding: 0.2em;
    width: 50%;
}

th {
    text-align: right;
    color: #AAAAAA;
    font-size: smaller;
    width: 6em;
}

td {
    padding-left: 1em;
}

table, input[type="text"], textarea {
    width: 100%;
}

textarea {
    height: 8em;
}

input[type="submit"] {
    margin-left: 7em;
}
</style>
<script>
window.onload = function () {
    if (location.href.match(/.*\/adicionar\//))
    {
        document.forms[0].elements[1].select();
    }
};
</script>
</head>
<body>
<div class="box rounded">
    <form action="${action}" method="post">
        <input type="hidden" name="b64id" value="${b64id}" />
        <table>
            <tr>
                <th>Nome:</th>
                <td><input type="text" name="nome" value="${item.get('nome')}" /></td>
            </tr>
            <tr>
                <th>Descri&ccedil;&atilde;o:</th>
                <td><textarea name="descricao" py:content="item.get('descricao')" /></td>
            </tr>
        </table>
        <input type="submit" value="Salvar" />
    </form>
</div>
</body>
</html>
