<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <title>Pyndorama :: Aventura '${title}'</title>
    <style type="text/css" media="screen">
    @import "${tg.url('/static/css/play.css')}";
    </style>
    <script type="text/javascript" src="${tg.url('/static/javascript/play.js')}"></script>
</head>

<body>
    <div class="box rounded" style="background: #000000; color: #4E9A06; overflow: auto;" py:if="defined('debug') and debug">
        <!-- DEBUG INFO -->
        <pre py:content="XML(debug)">
            Informações sobre métodos e propriedades de 'place'
        </pre>
        <pre py:content="text">
            Texto relativo à aventura
        </pre>
    </div>
    
    <div class="right_column box rounded">
        <div id="place_img" py:if="image">
            <img src="${image}" alt="Lugar atual" />
        </div>
    </div>

    <div class="left_column box rounded justified">
        <div class="notice" py:if="defined('notice') and notice" py:content="value_of('notice', '')">Mensagem ao jogador</div>
        <div id="place_description">
            <span py:content="place.value">Descrição do local</span>
            <?python
                objects = [obj for obj in place.contents.values() if obj.value]
            ?>
            <div py:if="(not defined('show') or show) and objects or defined('inve') and inve" py:strip="">
                <br />Você pode ver:
                <ul>
                    <li py:for="obj in objects" py:content="obj.value">Lista de itens no local atual</li>
                    <li py:if="not objects">nada aqui</li>
                </ul>
            </div>
        </div>
        <div id="command_prompt">
            <form action='${action}' method="post">
                <span py:if="not defined('show') or show" py:strip="">
                <input type="text" name="query" id="query" value="" />
                </span>
                <input type="submit" value="Ação!!!" />
            </form>
            <div id="all_actions" py:if="global_actions or local_actions">
                <span>Comandos disponíveis:</span>
                <span py:content="', '.join(global_actions + local_actions)">globais, locais.</span>
            </div>
        </div>
    </div>
</body>

</html>
