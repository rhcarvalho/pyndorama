<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <title>Bem-vindo ao Pyndorama!</title>
    <style type="text/css" media="screen">
    @import "${tg.url('/static/css/home.css')}";
    </style>
    <script type="text/javascript" src="${tg.url('/static/javascript/home.js')}"></script>
</head>

<body>
    <div class="clearfix box rounded">
		<div class="left_column">
            <p>Bem vindo ao Pyndorama!</p>
            <p>O Pyndorama é um ambiente para a construção de aventuras textuais.
            Ele foi criado para permitir que qualquer pessoa na Internet possa
            produzir um jogo.
            Se você quer produzir uma aventura, basta clicar no botão "Criar nova aventura" ou
            se quer jogar, selecione uma aventura e jogue!
            Você também pode usar as aventuras já prontas para criar novos desafios.</p>
        </div>
        <div>
            <form action="${tg.url('/iniciar')}" id="form_adv" method="post">
                <fieldset>
                <legend>Aventuras</legend>
                    
                    <p><a href="/editor/nova" class="rounded {transparent} button">Criar nova aventura</a></p>
                    <select id="adventure" name="adventure" size="5" class="rounded button">
                        <option py:for="caminho, nome in aventuras" title="$nome" value="${caminho}" py:content="nome">Nome da Aventura</option>
                    </select>
                    <input type="button" id="btn_editar" value="Editar" class="rounded {transparent} button" />
                    <input type="button" id="btn_editar_yaml" value="Editar YAML" class="rounded {transparent} button" />
                    <input type="submit" id="btn_iniciar" value="Jogar!" class="rounded {transparent} button" />
                </fieldset>
            </form>
        </div>
    </div>
</body>

</html>
