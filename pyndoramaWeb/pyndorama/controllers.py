# -*- coding: utf-8 -*-
import aventura
from cherrypy import session, request
from turbogears import controllers, expose, flash, redirect
from turbogears.widgets.forms import SingleSelectField, TableForm
# from model import *
import logging
log = logging.getLogger("pyndorama.controllers")

from util import getFullPath

def make_select_form(options):
    select = SingleSelectField('adventure', options=options)
    return TableForm(fields=[select],
                     submit_text='Selecionar Aventura',
                     action='iniciar')


class Root(controllers.RootController):
    @expose(template="pyndorama.templates.menu")
    def index(self):
        adventures = [('ave.yaml', 'A gralha e o jarro'),
                      ('labirinto.yaml', 'Labirinto'),
                      ('hominideo.yaml', 'Hominideos')]
        adv_selection_form = make_select_form(adventures)
        log.debug("Happy TurboGears Controller Responding For Duty")
        return dict(form=adv_selection_form)

    @expose(template="pyndorama.templates.principal")
    def iniciar(self, adventure):
        # Session variable initialization
        path = getFullPath(__name__, 'static/aventura/%s' % adventure)
        pyndorama = aventura.load(path)
        session['pyndorama'] = pyndorama
        pyndorama.finalizer = lambda self = self: self.finalizer()
        pyndorama.editor = lambda self = self: self.editor()
        # Variable assignment
        
        log.info(u"Nova sessão iniciada com a aventura '%s'" % adventure)
        
        actions = self.getActions(pyndorama)
        place = pyndorama.currentPlace
        
        return dict(text=pyndorama.perform(''),
                    image=pyndorama.getImage(),
                    action='acao',
                    global_actions=actions.get('global_actions'),
                    local_actions=actions.get('local_actions'),
                    place=place)

    @expose(template="pyndorama.templates.principal")
    def acao(self, query):
        pyndorama = session.get('pyndorama')
        if not pyndorama:
            flash(u"Para jogar o Pyndorama você deve habilitar os cookies de "\
                  u"seu navegador.")
            raise redirect('/')

        text = pyndorama.processaQuery(query)
        actions = self.getActions(pyndorama)

        place = pyndorama.currentPlace
        
        
        IN_DEBUG_MODE = 0
        if IN_DEBUG_MODE:
            from xml.sax.saxutils import escape
            def meandmyattr(obj, attr):
                return escape("%10s | %s" % (attr, getattr(place, attr, '')))
            debug = '\n'.join(meandmyattr(place, attr) for attr in dir(place) \
                              if not attr.startswith('__'))
        else:
            debug = ''
                          
        if aventura.YOU_CAN_SEE not in text:
            notice = text
        else:
            notice = ''

        return dict(text=text,
                    image=pyndorama.getImage(),
                    action='acao',
                    global_actions=actions.get('global_actions'),
                    local_actions=actions.get('local_actions'),
                    place=place,
                    debug=debug,
                    notice=notice)

    @expose(template="pyndorama.templates.edit")
    def edit(self):
        flash(u"A funcionalidade de edição ainda não foi implementada.")
        previous_url = request.headers.get('Referer', '/')
        raise redirect(previous_url)

    def finalizer(self, action='menu'):
        self.current_action = action

    def editor(self):
        self.current_action = 'edit'
        
    def getActions(self, Z):
        global_actions = Z.actions.keys() # Todas as ações de "Z"
        local_actions = []
        for obj in Z.currentPlace.contents.values():
            # todas as ações de cada obj no local atual
            local_actions.extend(obj.contents.keys())
        # Método não eficiente de remover duplicatas!
        local_actions = sorted(list(set(local_actions)))
        return dict(global_actions=global_actions, local_actions=local_actions)

    @expose()
    def default(self, url):
        flash(u'URL inválida: \"%s\".' % url)
        raise redirect('/')
