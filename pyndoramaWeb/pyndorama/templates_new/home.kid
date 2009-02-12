<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''" />
    <title>Bem-vindo ao Pyndorama!</title>
    <script type="text/javascript" src="${tg.url('/static/javascript/menu.js')}"></script>
</head>

<body>
    <div class="clearfix box rounded">
		<div class="left_column">
            <p>Bem vindo ao Pyndorama!</p>
            <p>O Pyndorama é um conjunto de jogos de aventuras textuais... Lorem ipsum dolor sit amet,
            consectetur adipiscing elit. Proin sodales. Nunc fermentum. Proin convallis vestibulum dui.
            Phasellus feugiat fringilla nibh. Nulla volutpat augue accumsan leo. Fusce sem lectus,
            facilisis et, elementum sit amet, dignissim eu, diam. Vestibulum leo sapien, lobortis vitae,
            blandit sit amet, elementum pulvinar, erat. Cras pulvinar rutrum erat. Ut at est et orci
            fringilla tempus.</p>
        </div>
        <div>
            <form action="${tg.url('/iniciar')}" id="form_adv" method="post">
                <fieldset>
                <legend>Aventuras</legend>
                    
                    <p><a href="/editor/nova">Criar Nova Aventura</a></p>
                    
                    <label for="adventure">Aventura:</label>
                    <select id="adventure" name="adventure">
                        <option py:for="caminho, nome in aventuras" value="${caminho}" py:content="nome">Nome da Aventura</option>
                    </select>
                    <input type="button" id="btn_editar" value="Editar" />
                    <input type="button" id="btn_editar_yaml" value="Editar YAML" />
                    <input type="submit" id="btn_iniciar" value="Jogar!" />
                </fieldset>
            </form>
        </div>
    </div>
</body>

</html>
