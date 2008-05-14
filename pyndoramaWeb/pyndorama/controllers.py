# -*- coding: utf-8 -*-
from codecs import open
import aventura
from cherrypy import session, request
from turbogears import controllers, expose, flash, redirect
# from model import *
import logging
log = logging.getLogger("pyndorama.controllers")

from util import getFullPath


class Root(controllers.RootController):
    @expose(template="pyndorama.templates.menu")
    def index(self, *args, **kwargs):
        aventuras = [('a_gralha_e_o_jarro.yaml', 'A gralha e o jarro (v2)'),
                     ('ave.yaml', 'A gralha e o jarro'),
                     ('labirinto.yaml', 'Labirinto'),
                     ('hominideo.yaml', u'Hominídeos'),
                     ('matematica.yaml', u'Matemática'),
                     ('aventuramix.yaml', 'Perdido numa cidade desconhecida')]
        log.debug("Happy TurboGears Controller Responding For Duty")
        return dict(aventuras=aventuras)

    @expose(template="pyndorama.templates.principal")
    def iniciar(self, adventure):
        # Session variable initialization
        path = getFullPath(__name__, 'static/aventura/%s' % adventure)
        pyndorama = aventura.Adventure(path).load()
        session['pyndorama'] = pyndorama
        pyndorama.finalizer = lambda self=self: self.finalizer()
        pyndorama.editor = lambda self=self: self.editor()
        # Variable assignment

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
    def edityaml(self, adventure='', aventurayaml=None):
        if aventurayaml is not None:
            pyndorama = aventura.Adventure(content=aventurayaml).load()
            session['pyndorama'] = pyndorama
            flash(u"Você editou a aventura, agora é hora de jogar! ")
            raise redirect('/acao')

        # Session variable initialization
        path = getFullPath(__name__, 'static/aventura/%s' % adventure)
        pyndorama = aventura.Adventure(path).load()
        yamlfile = open(path, 'rb', aventura.ENCODING, 'ignore')
        text = yamlfile.read()
        yamlfile.close()

        return dict(adventure=adventure, text=text, title=pyndorama.key)

    def finalizer(self):
        pass

    def editor(self):
        pass

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
    def default(self, url):
        flash(u'URL inválida: \"%s\".' % url)
        raise redirect('/')
