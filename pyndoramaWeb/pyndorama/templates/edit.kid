<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Pyndorama :: Editando aventura '???'</title>
    <style type="text/css" media="screen">
    @import "${tg.url('/static/css/principal.css')}";
    </style>
</head>

<body>
    <div id="place_description">
        <span py:replace="''">Descrição do local</span>
        <textarea id="placedesc" name="placedesc" py:content="place.value" />
        <?python
            objects = [(key, place.contents[key].value) for key in place.contents.keys()]
        ?>
        <div py:if="objects" py:strip="">
            <br />Voc&ecirc; pode ver:
            <ul>
                <li py:for="key, value in objects">
                    <label for="${key}" py:content="'[%s]' % key" /><br />
                    <input type="text" id="${key}" name="${key}" value="${value}" />
                </li>
            </ul>
        </div>
    </div>
    <div id="place_img" py:if="image">
        <img src="${image}" alt="Lugar atual" />
    </div>
    <div id="command_prompt">
        <form action='${action}' method="post">
            <input type="text" name="query" id="query" value="" disabled="disabled" />
            <input type="submit" value="Ação!!!" disabled="disabled" />
        </form>
        <div id="all_actions" py:if="global_actions or local_actions">
            <span>Ações:</span>
            <span py:content="', '.join(global_actions + local_actions)">globais, locais.</span>
        </div>
    </div>
</body>
</html>
