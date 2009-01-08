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
<div py:if="mundo">
    <table>
        <tr>
            <th>Nome:</th>
            <td py:content="mundo.get('nome')">Sem Nome</td>
        </tr>
        <tr>
            <th>Descri&ccedil;&atilde;o:</th>
            <td py:content="mundo.get('descricao')">Sem Descri&ccedil;&atilde;o</td>
        </tr>
    </table>
    <a href="#" style="margin-left: 88px">+local</a>
    <div py:for="local in mundo.get('conteudo', [])">
        <table>
            <tr>
                <th>Nome:</th>
                <td py:content="local.get('nome')">Sem Nome</td>
            </tr>
            <tr>
                <th>Descri&ccedil;&atilde;o:</th>
                <td py:content="local.get('descricao')">Sem Descri&ccedil;&atilde;o</td>
            </tr>
        </table>
        <div py:for="objeto in local.get('conteudo', [])">
            <table>
                <tr>
                    <th>Nome:</th>
                    <td py:content="objeto.get('nome')">Sem Nome</td>
                </tr>
                <tr>
                    <th>Descri&ccedil;&atilde;o:</th>
                    <td py:content="objeto.get('descricao')">Sem Descri&ccedil;&atilde;o</td>
                </tr>
            </table>
            <div py:for="verbo in objeto.get('conteudo', [])">
                <table>
                    <tr>
                        <th>Nome:</th>
                        <td py:content="verbo.get('nome')">Sem Nome</td>
                    </tr>
                    <tr>
                        <th>Descri&ccedil;&atilde;o:</th>
                        <td py:content="verbo.get('descricao')">Sem Descri&ccedil;&atilde;o</td>
                    </tr>
                </table>
                <div py:for="acao in verbo.get('conteudo', [])">
                    <table>
                        <tr>
                            <th>Nome:</th>
                            <td py:content="acao.get('nome')">Sem Nome</td>
                        </tr>
                        <tr>
                            <th>Descri&ccedil;&atilde;o:</th>
                            <td py:content="acao.get('descricao')">Sem Descri&ccedil;&atilde;o</td>
                        </tr>
                    </table>
                </div>
            </div>
        </div>
    </div>
</div>
</body>
</html>
