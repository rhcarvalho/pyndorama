<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Bem-vindo ao Pyndorama!</title>
    <style type="text/css" media="screen">
	@import "${tg.url('/static/css/principal.css')}";
	</style>
    <script type="text/javascript" src="${tg.url('/static/javascript/principal.js')}"></script>
</head>

<body>
	<pre style="position: absolute; top: -15px; right: 10px; width: 400px; background: #EEEEEE;" py:if="defined('debug') and debug">
		<!-- DEBUG INFO -->
        <div py:content="XML(debug)">
        	Informações sobre métodos e propriedades de 'place'
        </div>
        <div py:content="text">
            Texto relativo &agrave; aventura
        </div>
    </pre>

    <div id="place_description">
        <h2 py:content="'--' if not defined('place') else place.key">Nome do local</h2>
        <p>
        	<span py:content="'--' if not defined('place') else place.value">Descrição do local</span>
        	<br />Voc&ecirc; pode ver:
        </p>
        <ul py:if="defined('place')">
            <li py:for="obj in place.contents.values()" py:content="obj.value" py:if="obj.value">Lista de itens no local atual</li>
        </ul>
        <div class="notice" py:if="defined('notice') and notice" py:content="value_of('notice', '')">Mensagem ao jogador</div>
    </div>
    <div id="place_img" py:if="image">
    	<img src="${image}" alt="Lugar atual" />
    </div>
    <div id="command_prompt">
        <form action='${action}' method="post">
            <input type="text" name="query" id="query" value="" />
            <input type="submit" value="Ação!!!" />
        </form>
        <div id="all_actions" py:if="global_actions or local_actions">
            <span>Ações:</span>
            <span py:content="', '.join(global_actions + local_actions)">globais, locais.</span>
        </div>
    </div>
</body>

</html>
