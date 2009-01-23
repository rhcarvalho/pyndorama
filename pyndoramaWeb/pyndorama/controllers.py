# -*- coding: utf-8 -*-
from codecs import open
from base64 import urlsafe_b64encode as b64encode
from base64 import urlsafe_b64decode as b64decode
from yaml import dump
from datetime import datetime
import aventura
from cherrypy import session, request
from turbogears import controllers, expose, flash, redirect
# from model import *
import logging
log = logging.getLogger("pyndorama.controllers")

from util import getFullPath
from util import cria_lista_arquivos


class Editor(controllers.Controller):
    def get_mundo(self):
        mundo = session.get('pyndo_editor')
        if mundo is None:
            flash(u"Para jogar o Pyndorama você deve habilitar os cookies de "
                  u"seu navegador.")
            raise redirect('/')
        return mundo

    def get_element(self, b64id, with_parent=False):
        mundo = self.get_mundo()
        indexes = (int(i) for i in b64decode(b64id.encode()).split('.'))
        parent, element = None, mundo
        indexes.next()
        for i in indexes:
            parent, element = element, element['conteudo'][i]
        if with_parent:
            return parent, element
        return element

    @expose(template="pyndorama.templates.editor.full")
    def index(self, adventure=None):
        if adventure is None:
            mapping = {}
        else:
            mapping = aventura.Adventure(adventure).world_mapping
        session['pyndo_editor'] = mapping
        mundo = self.get_mundo()
        return dict(mundo=mundo)

    @expose(template="pyndorama.templates.editor.item")
    def item(self, b64id, **kwargs):
        element = self.get_element(b64id)
        if kwargs:
            for key in ('nome', 'descricao'):
                try:
                    element[key] = kwargs[key]
                except KeyError:
                    pass
            raise redirect('./')
        return dict(b64id=b64id, item=element)

    @expose(template="pyndorama.templates.editor.item")
    def adicionar(self, b64id):
        element = self.get_element(b64id)
        element.setdefault('conteudo', [])
        child = {'nome': 'sem_nome%s' % len(element['conteudo'])}
        element['conteudo'].append(child)

        id = b64decode(b64id.encode())
        index = element['conteudo'].index(child)
        child_b64id = b64encode('%s.%s' % (id, index))
        return dict(b64id=child_b64id, item=child)

    @expose()
    def remover(self, b64id):
        parent, element = self.get_element(b64id, with_parent=True)
        parent['conteudo'].remove(element)
        raise redirect('../')

    @expose()
    def remover_tudo(self, b64id):
        element = self.get_element(b64id)
        del element['conteudo'][:]
        raise redirect('../')

    @expose()
    def salvar(self):
        mundo = self.get_mundo()
        aventurayaml = dump(mundo)
        filename = "pyndorama/static/aventura/%s.yaml" % \
                   datetime.now().strftime("%Y%m%d%H%M%S")
        aventura.Adventure(content=aventurayaml).save(filename)
        raise redirect('/iniciar', adventure='', aventurayaml=aventurayaml)

    @expose(template="pyndorama.templates.editor")
    def concept(self, *args, **kwargs):
        return dict(title="Untitled")


class Root(controllers.RootController):
    editor = Editor()
    @expose(template="pyndorama.templates.menu")
    def index(self, *args, **kwargs):
        aventuras = cria_lista_arquivos()
        log.debug("Happy TurboGears Controller Responding For Duty")
        return dict(aventuras=aventuras)

    @expose(template="pyndorama.templates.principal")
    def iniciar(self, adventure, aventurayaml=None):
        if aventurayaml is not None:
            pyndorama = aventura.Adventure(content=aventurayaml).load()
            flash(u"Você editou a aventura, agora é hora de jogar! ")
        else:
            path = adventure
            pyndorama = aventura.Adventure(path).load()
        session['pyndorama'] = pyndorama
        pyndorama.finalizer = lambda self=self: self.finalizer()
        pyndorama.editor = lambda self=self: self.editor()

        log.info(u"Nova sessão iniciada com a aventura '%s'" % adventure)

        actions = self.get_actions(pyndorama)
        place = pyndorama

        return dict(text=pyndorama.perform(''),
                    image=pyndorama.get_image(pyndorama),
                    action='/acao',
                    global_actions=[],
                    local_actions=[],
                    title=pyndorama.key,
                    place=place,
                    show=False)

    @expose(template="pyndorama.templates.principal")
    def acao(self, query=''):
        if query.lower() == 'xyzz':
            raise redirect('/edit')

        pyndorama = session.get('pyndorama')
        if not pyndorama:
            flash(u"Para jogar o Pyndorama você deve habilitar os cookies de "
                  u"seu navegador.")
            raise redirect('/')

        text = pyndorama.perform(query.split(' ')).strip()
        actions = self.get_actions(pyndorama)

        place = pyndorama.current_place

        if aventura.YOU_CHECK_YOUR_INVENTORY in text:
            place = aventura.inventario
            inve = True
        else:
            inve = False

        IN_DEBUG_MODE = 0
        if IN_DEBUG_MODE:
            from xml.sax.saxutils import escape
            def meandmyattr(obj, attr):
                return escape("%10s | %s" % (attr, getattr(place, attr, '')))
            debug = '\n'.join(meandmyattr(place, attr) for attr in dir(place)
                              if not attr.startswith('__'))
        else:
            debug = ''

        pos = text.find(place.value)
        if pos == 0:
            notice = ''
        elif pos == -1:
            notice = text
        else:
            notice = text[:pos]

        if aventura.playadventure:
            action = '/acao'
        else:
            action = '/'

        return dict(text=text,
                    image=pyndorama.get_image(),
                    action=action,
                    global_actions=actions.get('global_actions'),
                    local_actions=actions.get('local_actions'),
                    place=place,
                    debug=debug,
                    title=pyndorama.key,
                    notice=notice,
                    inve=inve)

    @expose(template="pyndorama.templates.edit")
    def edit(self, placedesc=None, **kwargs):
        pyndorama = session.get('pyndorama')
        if not pyndorama:
            flash(u"Para jogar o Pyndorama você deve habilitar os cookies de "
                  u"seu navegador.")
            raise redirect('/')

        actions = self.get_actions(pyndorama)
        place = pyndorama.current_place

        if placedesc is not None:
            place.value = placedesc
            for obj, desc in kwargs.iteritems():
                try:
                    place.contents[obj].value = desc
                except KeyError:
                    pass
            raise redirect('/acao')

        return dict(image=pyndorama.get_image(),
                    action='/acao',
                    global_actions=actions.get('global_actions'),
                    local_actions=actions.get('local_actions'),
                    title=pyndorama.key,
                    place=place)

    @expose(template="pyndorama.templates.edityaml")
    def edityaml(self, adventure):
        path = adventure
        pyndorama = aventura.Adventure(path).load()
        yamlfile = open(path, 'rb', aventura.ENCODING, 'ignore')
        text = yamlfile.read()
        yamlfile.close()

        return dict(adventure=adventure, text=text, title=pyndorama.key)

    def get_actions(self, Z):
        global_actions = Z.actions.keys() # Todas as ações de "Z"
        local_actions = []
        for obj in Z.current_place.contents.values():
            # todas as ações de cada obj no local atual
            local_actions.extend(obj.contents.keys())
        # Método não eficiente de remover duplicatas!
        local_actions = sorted(list(set(local_actions)))
        return dict(global_actions=global_actions, local_actions=local_actions)

    @expose()
    def default(self, *args, **kwargs):
        url = request.browser_url
        flash(u'URL inválida: \"%s\".' % url)
        raise redirect('/')
