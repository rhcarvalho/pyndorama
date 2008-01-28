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
    <div id="place_description">
    	<h2>Pyndorama</h2>
    	<p>Bem vindo ao Pyndorama! Selecione uma aventura abaixo.</p>
		<span py:content="form()" py:strip="">Formul&aacute;rio de sele&ccedil;&atilde;o de aventura</span>
    </div>
</body>

</html>
