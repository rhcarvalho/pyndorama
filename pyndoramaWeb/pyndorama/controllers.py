import aventura
import cherrypy
from turbogears import controllers, expose, flash, redirect
from turbogears.widgets.forms import SingleSelectField, TableForm
# from model import *
import logging
log = logging.getLogger("pyndorama.controllers")


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
        # Session variable initialization (or recall if exists)
        pyndorama = aventura.load('pyndorama/static/aventura/%s' % adventure)
        cherrypy.session['pyndorama'] = pyndorama
        pyndorama.finalizer = lambda self=self: self.finalizer()
        pyndorama.editor = lambda self=self: self.editor()
        # Variable assignment
        
        log.debug("Happy TurboGears Controller Responding For Duty")
        
        actions = self.getActions(pyndorama)
        
        return dict(text=pyndorama.perform(''),
                    image=pyndorama.getImage(),
                    action='acao',
                    global_actions=actions.get('global_actions'),
                    local_actions=actions.get('local_actions'))

    @expose(template="pyndorama.templates.principal")
    def acao(self,query):
        pyndorama = cherrypy.session.get('pyndorama')
        if not pyndorama:
            flash("Para jogar o Pyndorama voce deve habilitar os cookies de seu navegador.")
            raise redirect('/')
        
        self.current_action = "acao"
        actions = self.getActions(pyndorama)
        
        return dict(text=pyndorama.processaQuery(query),
                    image=pyndorama.getImage(),
                    action=self.current_action,
                    global_actions=actions.get('global_actions'),
                    local_actions=actions.get('local_actions'))

    @expose(template="pyndorama.templates.edit")
    def edit(self,query):
        pyndorama = cherrypy.session.get('pyndorama')
        if not pyndorama:
            flash("Para jogar o Pyndorama voce deve habilitar os cookies de seu navegador.")
            raise redirect('/')
        
        self.current_action = "acao"
        
        return dict(text=pyndorama.processaQuery(query),
                    image=pyndorama.getImage(),
                    action=self.current_action)

    def finalizer(self, action='menu'):
        self.current_action = "menu"

    def editor(self):
        self.current_action = "edit"
        
    def getActions(self, Z):
        global_actions = Z.actions.keys() # Todas as acoes de "Z"
        local_actions = []
        for obj in Z.currentPlace.contents.values(): # todas as acoes de cada obj no local atual
            local_actions.extend(obj.contents.keys())
        # Metodo nao eficiente de remover duplicatas!
        return dict(global_actions=global_actions, local_actions=sorted(list(set(local_actions))))

    @expose()
    def default(self, url):
        flash('URL invalida: \"%s\".' % url)
        raise redirect('/')
