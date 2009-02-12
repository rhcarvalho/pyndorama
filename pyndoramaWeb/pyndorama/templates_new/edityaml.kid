<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''" />
    <title>Pyndorama :: Editando aventura '${title}'</title>
    <style type="text/css" media="screen">
    @import "${tg.url('/static/css/principal.css')}";
    @import "${tg.url('/static/css/edityaml.css')}";
    </style>
</head>

<body>
    <div id="place_description">
        <form action="/iniciar" method="post">
            <input type="hidden" id="adventure" name="adventure" value="${adventure}" />
            <textarea id="aventurayaml" name="aventurayaml" py:content="text" />
            <input type="reset" value="Reverter" />
            <input type="submit" value="Salvar" />
        </form>
    </div>
</body>
</html>
