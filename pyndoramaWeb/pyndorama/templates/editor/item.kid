<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../master.kid'">

<head>
    <title>Pyndorama :: Editando Aventura</title>
    <style type="text/css" media="screen">
    @import "${tg.url('/static/css/editor/item.css')}";
    </style>
    <script type="text/javascript" src="${tg.url('/static/javascript/editor/item.js')}"></script>
</head>

<body>
    <div class="box rounded">
        <form action="${action}" method="post">
            <input type="hidden" id="b64id" name="b64id" value="${b64id}" />
            <table>
                <tr>
                    <th>Nome:</th>
                    <td><input type="text" id="nome" name="nome" value="${item.get('nome')}" /></td>
                </tr>
                <tr>
                    <th>Descri&ccedil;&atilde;o:</th>
                    <td><textarea id="descricao" name="descricao" py:content="item.get('descricao')" /></td>
                </tr>
            </table>
            <input type="submit" value="Salvar" />
        </form>
    </div>
</body>

</html>
