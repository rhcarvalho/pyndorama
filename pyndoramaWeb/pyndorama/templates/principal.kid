<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Bem-vindo ao Pyndorama!</title>
    <style type="text/css" media="screen">
	@import "${tg.url('/static/css/principal.css')}";
	</style>
</head>

<body>
    <div id="book">
        <pre id="fabletext" py:content='text'>
        Texto relativo &agrave; aventura
        </pre>
        <img id="fableview" src='${image}' py:if='image' />
        <form action='${action}' method="POST">
            <div id="fableaction">
                <input type="text" name="query" value="" />
                <input type="submit" value="Ação!!!" />        
            </div>
        </form>
    </div>
    <div id="all_actions" py:if="global_actions or local_actions">
    	<span py:replace="">Lista de a&ccedil;&otilde;es dispon&iacute;veis</span>
        <div py:if="global_actions" py:strip="">
            <span>A&ccedil;&otilde;es dispon&iacute;veis durante toda a aventura:</span>
            <ul>
                <li py:for="someAction in global_actions" py:content="someAction">A&ccedil;&atilde;o global</li>
            </ul>
        </div>
        <div py:if="local_actions" py:strip="">
            <span>A&ccedil;&otilde;es adicionais dispon&iacute;veis aqui:</span>
            <ul>
                <li py:for="someAction in local_actions" py:content="someAction">A&ccedil;&atilde;o local</li>
            </ul>
        </div>
    </div>
</body>

</html>
