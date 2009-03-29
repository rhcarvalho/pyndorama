<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python
from base64 import urlsafe_b64encode as b64encode
classes = ('mundo', 'local', 'objeto', 'verbo', 'acao', 'alvo_acao')

import os
from cherrypy import session
from pyndorama.util import latin1_to_ascii, path_to_adventure

def exists(imagename):
    adventure = session.get('_adventure')
    for ext in 'gif jpg png'.split():
        filename = '%s.%s' % (latin1_to_ascii(imagename), ext)
        if os.path.isfile(path_to_adventure(adventure, 'images', filename)):
            return '[já possui imagem]'
    return ''
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'../master.kid'">

<head>
    <title>Pyndorama :: Editando Aventura</title>
    <style type="text/css" media="screen">
    @import "${tg.url('/static/css/editor/full.css')}";
    </style>
    <script type="text/javascript" src="${tg.url('/static/javascript/editor/full.js')}"></script>
</head>

<body>
    <div class="box rounded">
        <div><a href="desfazer">Desfazer</a></div>
        <div py:def="display_thing(container, id)" py:strip="">
            <?python
            level = id.count('.')
            show_add = show_remove_content = level < 5
            show_remove = level > 0
            show_add_image = level in (0, 1)
            ?>
            <div class="editor-box ${classes[level]} rounded">
                <div class="editor-menu rounded {top}">
                    <a href="item/${b64encode(id)}">editar</a>
                    <span py:if="show_remove" py:strip=""> |
                    <a href="remover/${b64encode(id)}">remover</a></span>
                    <span py:if="show_add" py:strip=""> |
                    <a href="adicionar/${b64encode(id)}">adicionar conte&uacute;do</a></span>
                    <span py:if="show_add_image" py:strip=""> | 
                    <span class="image_status" py:content="exists(container.get('nome'))">Tem imagem?</span>
                    <a href="#" class="img_upload">adicionar imagem</a></span>
                    <span py:if="show_remove_content" py:strip=""> |
                    <a href="remover_tudo/${b64encode(id)}">remover conte&uacute;do</a></span>
                    <form class="form_salvar_imagem"
                          action="upload_imagem" method="post"
                          enctype="multipart/form-data"
                          py:if="show_add_image">
                        <input type="hidden" id="b64id" name="b64id" value="${b64encode(id)}" />
                        <input type="file" id="imagem" name="imagem" />
                        <input type="submit" value="salvar" />
                    </form>
                </div>
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
                <div py:for="index, item in enumerate(container.get('conteudo', []))"
                     py:replace="display_thing(item, '%s.%s' % (id, index))" />
            </div>
        </div>
        <div py:replace="display_thing(mundo, '0')" />
        <form action="salvar" method="post">
            <input type="submit" value="Salvar" />
        </form>
        <table id="actionlist">
            <tr><th colspan="2">Nomes das a&ccedil;&otilde;es:</th></tr>
            <tr><td>M</td><td>Move para o lugar informado</td></tr>
            <tr><td>P</td><td>P&otilde;e o objeto no invent&aacute;rio do jogador</td></tr>
            <tr><td>T</td><td>Retira o objeto do invent&aacute;rio do jogador</td></tr>
            <tr><td>A</td><td>Ativa o objeto</td></tr>
            <tr><td>B</td><td>Bloqueia o objeto</td></tr>
            <tr><td>S</td><td>Testa se o objeto est&aacute; ativo</td></tr>
            <tr><td>R</td><td>Testa se o objeto est&aacute; bloqueado</td></tr>
            <tr><td>F</td><td>Finaliza a aventura</td></tr>
        </table>
    </div>
</body>

</html>
