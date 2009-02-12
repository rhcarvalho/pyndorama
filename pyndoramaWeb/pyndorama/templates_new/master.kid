<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python import sitetemplate ?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="sitetemplate">

<head py:match="item.tag=='{http://www.w3.org/1999/xhtml}head'" py:attrs="item.items()">
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" />
    <title py:replace="''">Pyndorama</title>
    <style type="text/css" media="screen">
    @import "${tg.url('/static/css/master.css')}";
    </style>
    <script type="text/javascript" src="${tg.url('/static/javascript/jquery-1.3.1.min.js')}"></script>
    <script type="text/javascript" src="${tg.url('/static/javascript/jquery.corners.min.js')}"></script>
    <script type="text/javascript" src="${tg.url('/static/javascript/master.js')}"></script>
    <script type="text/javascript">
	$(function(){
		$(".rounded").corners("10px");
	});
	</script>
    <meta py:replace="item[:]" />
</head>

<body py:match="item.tag=='{http://www.w3.org/1999/xhtml}body'" py:attrs="item.items()">
    <div py:if="tg.config('identity.on') and not defined('logging_in')" id="pageLogin">
        <span py:if="tg.identity.anonymous">
            <a href="${tg.url('/login')}">Login</a>
        </span>
        <span py:if="not tg.identity.anonymous">
            Welcome ${tg.identity.user.display_name}.
            <a href="${tg.url('/logout')}">Logout</a>
        </span>
    </div>
<div id="container" class="clearfix">
    <div id="header" class="box rounded">
    	<img src="${tg.url('/static/images/header.png')}" />
    </div>
    <div id="status_block" class="rounded" py:if="value_of('tg_flash', None)" py:content="tg_flash"></div>
    <div id="main_menu" class="box rounded">
        <ul>
            <li><a href="${tg.url('/')}">Página Inicial</a></li>
            <li><a href="http://labase.nce.ufrj.br/pyndorama/">Labase</a></li>
            <li><a href="http://code.google.com/p/pyndorama/">Repositório no Google Code</a></li>
        </ul>
    </div>
    <div id="content">
        <div py:replace="[item.text]+item[:]" />
    </div>
</div>
</body>

</html>
