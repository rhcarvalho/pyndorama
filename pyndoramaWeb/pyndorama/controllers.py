import aventura
import cherrypy
from turbogears import controllers, expose, flash
from turbogears.widgets.forms import SingleSelectField, TableForm
# from model import *
import logging
log = logging.getLogger("pyndorama.controllers")


def makeForm(campos):
    adventure = SingleSelectField("adventure", options=campos[0])
    return TableForm(fields=[adventure],
                     submit_text="Selecionar Aventura",
                     action="iniciar")


class Root(controllers.RootController):
    @expose(template="pyndorama.templates.menu")
    def index(self):
        aventuras = [('ave.yaml','A gralha e o jarro'),('labirinto.yaml','Labirinto')]
        enviair_form = makeForm([aventuras])
        log.debug("Happy TurboGears Controller Responding For Duty")
        return dict(form=enviair_form)

    @expose(template="pyndorama.templates.principal")
    def iniciar(self, adventure):
        # Session variable initialization (or recall if exists)
        pindorama = aventura.load('pyndorama/static/aventura/%s' % adventure)
        cherrypy.session['pindorama'] = pindorama
        pindorama.finalizer = lambda self=self :self.finalizer()
        pindorama.editor = lambda self=self :self.editor()
        # Variable assignment
        log.debug("Happy TurboGears Controller Responding For Duty")
        #pyndorama=aventura.load()
        return dict(text=pindorama.perform(''),
            image=pindorama.getImage(), action='acao')

    @expose(template="pyndorama.templates.menu")
    def menu(self, query):
        aventuras = [('ave.yaml','A gralha e o jarro'),('labirinto.yaml','Labirinto')]
        enviair_form = makeForm([aventuras])
        log.debug("Happy TurboGears Controller Responding For Duty")
        return dict(form=enviair_form)

    @expose(template="pyndorama.templates.principal")
    def acao(self,query):
        #return dict(text=pyndorama.perform(''))
        pyndorama= cherrypy.session['pindorama']
        self.current_action = "acao"
        return dict(text=pyndorama.processaQuery(query),
            image=pyndorama.getImage(), action=self.current_action)

    @expose(template="pyndorama.templates.edit")
    def edit(self,query):
        pyndorama= cherrypy.session['pindorama']
        self.current_action = "acao"
        return dict(text=pyndorama.processaQuery(query),
            image=pyndorama.getImage(), action=self.current_action)

    def finalizer(self, action='menu'):
        self.current_action = "menu"

    def editor(self):
        self.current_action = "edit"
