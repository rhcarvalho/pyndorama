<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''" />
    <title>Pyndorama :: Editando Aventura '${title}'</title>
    <style type="text/css" media="screen">
    @import "${tg.url('/static/css/editor.css')}";
    </style>
</head>

<body class="pyndoeditor">
<div id="container">
    <div id="header">
        <div class="world">
            <div class="attributes">
                <h1>Mundo</h1>
            </div>
            <div class="content">
                <div class="place">
                        <div class="attributes">
                        <h1>Lugares</h1>
                    </div>
                    <div class="content">
                        <div class="object">
                            <div class="attributes">
                                <h1>Objetos</h1>
                            </div>
                            <div class="content">
                                <div class="verb">
                                    <div class="attributes">
                                        <h1>Verbos</h1>
                                    </div>
                                    <div class="content">
                                        <div class="action">
                                            <div class="attributes">
                                                <h1>Ações</h1>
                                            </div>
                                            <div class="content">
                                            </div>
                                            <br class="clearfloat" />
                                        </div>
                                    </div>
                                    <br class="clearfloat" />
                                </div>
                            </div>
                               <br class="clearfloat" />
                        </div>
                    </div>
                    <br class="clearfloat" />
                </div>
            </div>
            <br class="clearfloat" />
        </div>
    </div>
    <div class="world">
        <div class="attributes">
            <div class="item_actions">
                <ul>
                    <li><a href="#">+ local</a></li>
                </ul>
            </div>
            <div class="item_fields">
                <label for="nome">Nome</label>
                <input id="nome" name="nome" type="text" />
                <label for="descricao">Descrição</label>
                <input id="descricao" name="descricao" type="text" />
                <label for="imagem">Imagem</label>
                <input id="imagem" name="imagem" type="file" />
            </div>
        </div>
        <div class="content">
            <div class="place">
                <div class="attributes">
                    <div class="item_actions">
                        <ul>
                            <li><a href="#">- local</a></li>
                            <li><a href="#">+ objeto</a></li>
                        </ul>
                    </div>
                    <div class="item_fields">
                        <label for="nome">Nome</label>
                        <input id="nome" name="nome" type="text" />
                        <label for="descricao">Descrição</label>
                        <input id="descricao" name="descricao" type="text" />
                        <label for="imagem">Imagem</label>
                        <input id="imagem" name="imagem" type="file" />
                    </div>
                </div>
                <div class="content">
                    <div class="object">
                        <div class="attributes">
                            <div class="item_actions">
                                <ul>
                                    <li><a href="#">- objeto</a></li>
                                    <li><a href="#">+ verbo</a></li>
                                </ul>
                            </div>
                            <div class="item_fields">
                                <label for="nome">Nome</label>
                                <input id="nome" name="nome" type="text" />
                                <label for="descricao">Descrição</label>
                                <input id="descricao" name="descricao" type="text" />
                                <label for="imagem">Imagem</label>
                                <input id="imagem" name="imagem" type="file" />
                            </div>
                        </div>
                        <div class="content">
                            <div class="verb">
                                <div class="attributes">
                                    <div class="item_actions">
                                        <ul>
                                            <li><a href="#">- verbo</a></li>
                                            <li><a href="#">+ ação</a></li>
                                        </ul>
                                    </div>
                                    <div class="item_fields">
                                        <label for="nome">Nome</label>
                                        <input id="nome" name="nome" type="text" />
                                        <label for="descricao">Descrição</label>
                                        <input id="descricao" name="descricao" type="text" />
                                    </div>
                                </div>
                                <div class="content">
                                    <div class="action">
                                        <div class="attributes">
                                            <div class="item_actions">
                                                <ul>
                                                    <li><a href="#">- ação</a></li>
                                                </ul>
                                            </div>
                                            <div class="item_fields">
                                                <label for="nome">Nome</label>
                                                <select id="nome" name="nome">
                                                    <option value="M">Mover</option>
                                                    <option value="A">Ativar</option>
                                                    <option value="">Outro</option>
                                                </select>
                                                <label for="descricao">Descrição</label>
                                                <input id="descricao" name="descricao" type="text" />
                                                <label for="alvo">Alvo</label>
                                                <input id="alvo" name="alvo" type="text" />
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <br class="clearfloat" />
                        </div>
                    </div>
                    <br class="clearfloat" />
                    <div class="object">
                        <div class="attributes">
                            <div class="item_actions">
                                <ul>
                                    <li><a href="#">- objeto</a></li>
                                    <li><a href="#">+ verbo</a></li>
                                </ul>
                            </div>
                            <div class="item_fields">
                                <label for="nome">Nome</label>
                                <input id="nome" name="nome" type="text" />
                                <label for="descricao">Descrição</label>
                                <input id="descricao" name="descricao" type="text" />
                                <label for="imagem">Imagem</label>
                                <input id="imagem" name="imagem" type="file" />
                            </div>
                        </div>
                        <div class="content">
                            <div class="verb">
                                <div class="attributes">
                                    <div class="item_actions">
                                        <ul>
                                            <li><a href="#">- verbo</a></li>
                                            <li><a href="#">+ ação</a></li>
                                        </ul>
                                    </div>
                                    <div class="item_fields">
                                        <label for="nome">Nome</label>
                                        <input id="nome" name="nome" type="text" />
                                        <label for="descricao">Descrição</label>
                                        <input id="descricao" name="descricao" type="text" />
                                    </div>
                                </div>
                                <div class="content">
                                    <div class="action">
                                        <div class="attributes">
                                            <div class="item_actions">
                                                <ul>
                                                    <li><a href="#">- ação</a></li>
                                                </ul>
                                            </div>
                                            <div class="item_fields">
                                                <label for="nome">Nome</label>
                                                <select id="nome" name="nome">
                                                    <option value="M">Mover</option>
                                                    <option value="A">Ativar</option>
                                                    <option value="">Outro</option>
                                                </select>
                                                <label for="descricao">Descrição</label>
                                                <input id="descricao" name="descricao" type="text" />
                                                <label for="alvo">Alvo</label>
                                                <input id="alvo" name="alvo" type="text" />
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <br class="clearfloat" />
                        </div>
                    </div>
                    <br class="clearfloat" />
                </div>
            </div>
            <br class="clearfloat" />
            <div class="place">
                <div class="attributes">
                    <div class="item_actions">
                        <ul>
                            <li><a href="#">- local</a></li>
                            <li><a href="#">+ objeto</a></li>
                        </ul>
                    </div>
                    <div class="item_fields">
                        <label for="nome">Nome</label>
                        <input id="nome" name="nome" type="text" />
                        <label for="descricao">Descrição</label>
                        <input id="descricao" name="descricao" type="text" />
                        <label for="imagem">Imagem</label>
                        <input id="imagem" name="imagem" type="file" />
                    </div>
                </div>
                <div class="content">
                    <div class="object">
                        <div class="attributes">
                            <div class="item_actions">
                                <ul>
                                    <li><a href="#">- objeto</a></li>
                                    <li><a href="#">+ verbo</a></li>
                                </ul>
                            </div>
                            <div class="item_fields">
                                <label for="nome">Nome</label>
                                <input id="nome" name="nome" type="text" />
                                <label for="descricao">Descrição</label>
                                <input id="descricao" name="descricao" type="text" />
                                <label for="imagem">Imagem</label>
                                <input id="imagem" name="imagem" type="file" />
                            </div>
                        </div>
                        <div class="content">
                            <div class="verb">
                                <div class="attributes">
                                    <div class="item_actions">
                                        <ul>
                                            <li><a href="#">- verbo</a></li>
                                            <li><a href="#">+ ação</a></li>
                                        </ul>
                                    </div>
                                    <div class="item_fields">
                                        <label for="nome">Nome</label>
                                        <input id="nome" name="nome" type="text" />
                                        <label for="descricao">Descrição</label>
                                        <input id="descricao" name="descricao" type="text" />
                                    </div>
                                </div>
                                <div class="content">
                                    <div class="action">
                                        <div class="attributes">
                                            <div class="item_actions">
                                                <ul>
                                                    <li><a href="#">- ação</a></li>
                                                </ul>
                                            </div>
                                            <div class="item_fields">
                                                <label for="nome">Nome</label>
                                                <select id="nome" name="nome">
                                                    <option value="M">Mover</option>
                                                    <option value="A">Ativar</option>
                                                    <option value="">Outro</option>
                                                </select>
                                                <label for="descricao">Descrição</label>
                                                <input id="descricao" name="descricao" type="text" />
                                                <label for="alvo">Alvo</label>
                                                <input id="alvo" name="alvo" type="text" />
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <br class="clearfloat" />
                        </div>
                    </div>
                    <br class="clearfloat" />
                    <div class="object">
                        <div class="attributes">
                            <div class="item_actions">
                                <ul>
                                    <li><a href="#">- objeto</a></li>
                                    <li><a href="#">+ verbo</a></li>
                                </ul>
                            </div>
                            <div class="item_fields">
                                <label for="nome">Nome</label>
                                <input id="nome" name="nome" type="text" />
                                <label for="descricao">Descrição</label>
                                <input id="descricao" name="descricao" type="text" />
                                <label for="imagem">Imagem</label>
                                <input id="imagem" name="imagem" type="file" />
                            </div>
                        </div>
                        <div class="content">
                            <div class="verb">
                                <div class="attributes">
                                    <div class="item_actions">
                                        <ul>
                                            <li><a href="#">- verbo</a></li>
                                            <li><a href="#">+ ação</a></li>
                                        </ul>
                                    </div>
                                    <div class="item_fields">
                                        <label for="nome">Nome</label>
                                        <input id="nome" name="nome" type="text" />
                                        <label for="descricao">Descrição</label>
                                        <input id="descricao" name="descricao" type="text" />
                                    </div>
                                </div>
                                <div class="content">
                                    <div class="action">
                                        <div class="attributes">
                                            <div class="item_actions">
                                                <ul>
                                                    <li><a href="#">- ação</a></li>
                                                </ul>
                                            </div>
                                            <div class="item_fields">
                                                <label for="nome">Nome</label>
                                                <select id="nome" name="nome">
                                                    <option value="M">Mover</option>
                                                    <option value="A">Ativar</option>
                                                    <option value="">Outro</option>
                                                </select>
                                                <label for="descricao">Descrição</label>
                                                <input id="descricao" name="descricao" type="text" />
                                                <label for="alvo">Alvo</label>
                                                <input id="alvo" name="alvo" type="text" />
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <br class="clearfloat" />
                        </div>
                    </div>
                    <br class="clearfloat" />
                </div>
            </div>
            <br class="clearfloat" />
        </div>
    </div>
</div>
</body>

</html>
