# -*- coding: utf-8 -*-
import aventura
from cherrypy import session, request
from turbogears import controllers, expose, flash, redirect
from turbogears.widgets.forms import SingleSelectField, TableForm
# from model import *
import logging
log = logging.getLogger("pyndorama.controllers")

from util import getFullPath

def makeForm(campos):
    aventura = SingleSelectField("adventure", options=campos)
    return TableForm(fields=[aventura],
                     submit_text="Selecionar Aventura",
                     action="iniciar")


class Root(controllers.RootController):
    @expose(template="pyndorama.templates.menu")
    def index(self):
        aventuras = [('ave.yaml', 'A gralha e o jarro'),
                     ('labirinto.yaml', 'Labirinto'),
                     ('hominideo.yaml', 'Hominideos')]
        enviair_form = makeForm(aventuras)
        log.debug("Happy TurboGears Controller Responding For Duty")
        return dict(form=enviair_form)

    @expose(template="pyndorama.templates.principal")
    def iniciar(self, adventure):
        # Session variable initialization
        path = getFullPath(__name__, 'static/aventura/%s' % adventure)
        pyndorama = aventura.load(path)
        session['pyndorama'] = pyndorama
        pyndorama.finalizer = lambda self=self: self.finalizer()
        pyndorama.editor = lambda self=self: self.editor()
        # Variable assignment
        
        log.info(u"Nova sessão iniciada com a aventura '%s'" % adventure)
        
        actions = self.getActions(pyndorama)
        
        return dict(text=pyndorama.perform(''),
                    image=pyndorama.getImage(),
                    action='acao',
                    global_actions=actions.get('global_actions'),
                    local_actions=actions.get('local_actions'))

    @expose(template="pyndorama.templates.principal")
    def acao(self, query):
        pyndorama = session.get('pyndorama')
        if not pyndorama:
            flash(u"Para jogar o Pyndorama você deve habilitar os cookies de seu navegador.")
            raise redirect('/')

        actions = self.getActions(pyndorama)

        return dict(text=pyndorama.processaQuery(query),
                    image=pyndorama.getImage(),
                    action='acao',
                    global_actions=actions.get('global_actions'),
                    local_actions=actions.get('local_actions'))

    @expose(template="pyndorama.templates.edit")
    def edit(self):
        flash(u"A funcionalidade de edição ainda não foi implementada.")
        previous_url = request.headers.get("Referer", "/")
        raise redirect(previous_url)

    def finalizer(self, action='menu'):
        self.current_action = action

    def editor(self):
        self.current_action = 'edit'
        
    def getActions(self, Z):
        global_actions = Z.actions.keys() # Todas as ações de "Z"
        local_actions = []
        for obj in Z.currentPlace.contents.values(): # todas as ações de cada obj no local atual
            local_actions.extend(obj.contents.keys())
        # Método não eficiente de remover duplicatas!
        return dict(global_actions=global_actions, local_actions=sorted(list(set(local_actions))))

    @expose()
    def default(self, url):
        flash(u'URL inválida: \"%s\".' % url)
        raise redirect('/')
