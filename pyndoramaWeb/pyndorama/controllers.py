# -*- coding: utf-8 -*-
from codecs import open
from base64 import urlsafe_b64encode as b64encode
from base64 import urlsafe_b64decode as b64decode
import os
import shutil
import yaml
from datetime import datetime
import aventura
from cherrypy import session, request
from turbogears import controllers, expose, flash, redirect
# from model import *
import logging
log = logging.getLogger("pyndorama.controllers")

from util import (latin1_to_ascii, list_adventures,
                  path_to_adventure, path_to_adventure_yaml)


def keep_backup(func):
    def new_func(*args, **kwargs):
        session['pyndo_editor_backup'] = yaml.dump(session.get('pyndo_editor', {}))
        return func(*args, **kwargs)
    return new_func


class Editor(controllers.Controller):
    def get_mundo(self):
        u"""Retorna o mundo (dict) armazenado na session ou redireciona para
            a raiz da aplicação exibindo uma mensagem"""
        mundo = session.get('pyndo_editor')
        if mundo is None:
            flash(u"Para jogar o Pyndorama você deve habilitar os cookies de "
                  u"seu navegador.")
            raise redirect('/')
        return mundo

    def get_element(self, b64id, with_parent=False):
        u"""Retorna o elemento do mundo com o id codificado por b64id.
            Caso with_parent seja True, retorna uma tupla com o pai do
            elemento e o próprio"""
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
        if adventure is not None:
            path = path_to_adventure_yaml(adventure)
            mapping = aventura.Adventure(path).world_mapping
            # Protege contra aventuras no formato antigo
            if not isinstance(mapping, dict):
                flash(u"Aventura incompatível com o editor.")
                raise redirect('/')
            session['pyndo_editor'] = mapping
            
            # copia a aventura atual e edita a recem-criada
            new_name = datetime.now().strftime("%Y%m%d%H%M%S")
            
            old_filename, new_filename = map(path_to_adventure_yaml, (adventure, new_name))
            old_basedir, new_basedir = map(path_to_adventure, (adventure, new_name))
            shutil.copytree(old_basedir, new_basedir)
            os.rename(os.path.join(new_basedir, os.path.basename(old_filename)), new_filename)
            
            session['_adventure'] = new_name
        mundo = self.get_mundo()
        return dict(mundo=mundo)

    @expose()
    def nova(self):
        mapping = {}
        new_name = datetime.now().strftime("%Y%m%d%H%M%S")
        basedir = path_to_adventure(new_name)
        os.mkdir(basedir)
        filename = path_to_adventure_yaml(new_name)
        
        session['pyndo_editor'] = mapping
        session['_adventure'] = new_name
        raise redirect('./')

    @expose(template="pyndorama.templates.editor.item")
    def item(self, b64id, **kwargs):
        u"""GET  (sem kwargs) - Exibe um elemento (Mundo, Lugar, Objeto, ...)
                                para edição
            POST (com kwargs) - Edita um elemento alterando seus atributos"""
        element = self.get_element(b64id)
        if kwargs:
            self.salvar_item(element, **kwargs)
            raise redirect('./')
        return dict(action="../item", b64id=b64id, item=element)

    @expose(template="pyndorama.templates.editor.item")
    def adicionar(self, b64id, **kwargs):
        u"""GET  (sem kwargs) - Cria um novo elemento e vai para sua tela
                                de edição
            POST (com kwargs) - Adiciona um novo elemento ao conteúdo do pai
                                do elemento identificado por b64id"""
        parent = self.get_element(b64id)
        parent.setdefault('conteudo', [])
        element = {'nome': 'sem_nome%s' % len(parent['conteudo'])}
        if kwargs:
            self.salvar_item(element, parent, **kwargs)
            raise redirect('./')
        return dict(action="../adicionar", b64id=b64id, item=element)

    @keep_backup
    def salvar_item(self, element, parent=None, **kwargs):
        for key in ('nome', 'descricao'):
            try:
                element[key] = kwargs[key]
            except KeyError:
                pass
        # adicionando conteúdo
        if parent is not None:
            parent['conteudo'].append(element)

    @expose()
    @keep_backup
    def remover(self, b64id):
        u"""Remove o elemento identificado por b64id e todo seu conteúdo"""
        parent, element = self.get_element(b64id, with_parent=True)
        parent['conteudo'].remove(element)
        raise redirect('../')

    @expose()
    @keep_backup
    def remover_tudo(self, b64id):
        u"""Remove o conteúdo do elemento identificado por b64id"""
        element = self.get_element(b64id)
        del element['conteudo'][:]
        raise redirect('../')

    @expose()
    def salvar(self):
        mundo = self.get_mundo()
        aventurayaml = yaml.dump(mundo)
        filename = path_to_adventure_yaml(session['_adventure'])
        aventura.Adventure(content=aventurayaml).save(filename)
        raise redirect('/iniciar', adventure='', aventurayaml=aventurayaml)

    @expose()
    def desfazer(self):
        backup = session.get('pyndo_editor_backup')
        if backup is not None:
            session['pyndo_editor'] = yaml.load(backup)
        raise redirect('./')

    @expose()
    def upload_imagem(self, b64id, imagem):
        acceptable_image_types = {'image/gif': 'gif',
                                  'image/jpeg': 'jpg',
                                  'image/png': 'png'}
        if imagem.type not in acceptable_image_types:
            flash(u"Você só pode carregar imagens no formato GIF, JPEG ou PNG")
        else:
            basedir = path_to_adventure(session['_adventure'])
            images_path = path_to_adventure(session['_adventure'], 'images')
            if os.path.isdir(basedir) and not os.path.isdir(images_path):
                os.mkdir(images_path)
            filesize, method = 'unknown', 'none'
            try:
                filesize = os.fstat(imagem.file.fileno())[6]/1024.
            except:
                try:
                    imagem.file.seek(0, 2)
                    filesize = imagem.file.tell()/1024.
                except:
                    pass
            try:
                name = self.get_element(b64id)['nome']
                filename = "%s.%s" % (latin1_to_ascii(name),
                                      acceptable_image_types[imagem.type])
            except KeyError:
                flash(u"Não foi possível salvar a imagem: elemento sem nome")
            else:
                savedimage = open(os.path.join(images_path, filename), 'wb')
                savedimage.write(imagem.file.read())
                savedimage.close()
                flash(u"Imagem salva '%s' (%.2f KB)" % (filename, filesize))
        raise redirect('./')

    @expose(template="pyndorama.templates.editor")
    def concept(self, *args, **kwargs):
        u"""Exibe o conceito antigo de editor de aventuras"""
        return dict(title="Untitled")


class Root(controllers.RootController):
    editor = Editor()
    @expose(template="pyndorama.templates.home")
    def index(self, *args, **kwargs):
        aventuras = list_adventures()
        log.debug("Happy TurboGears Controller Responding For Duty")
        return dict(aventuras=aventuras)

    @expose(template="pyndorama.templates.play")
    def iniciar(self, adventure, aventurayaml=None):
        if aventurayaml is not None:
            pyndorama = aventura.Adventure(content=aventurayaml).load()
            flash(u"Você editou a aventura, agora é hora de jogar! ")
        else:
            path = path_to_adventure_yaml(adventure)
            pyndorama = aventura.Adventure(path).load()
            session['_adventure'] = adventure
        session['pyndorama'] = pyndorama

        log.info(u"Nova sessão iniciada com a aventura '%s'" % adventure)

        actions = self.get_actions(pyndorama)
        place = pyndorama

        return dict(text=pyndorama.perform(''),
                    image=pyndorama.get_image(adventure=session['_adventure'], place=place),
                    action='/acao',
                    global_actions=[],
                    local_actions=[],
                    title=pyndorama.key,
                    place=place,
                    show=False)

    @expose(template="pyndorama.templates.play")
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
            place = pyndorama.inventario
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

        if pyndorama.playadventure:
            action = '/acao'
        else:
            action = '/'

        return dict(text=text,
                    image=pyndorama.get_image(adventure=session['_adventure']),
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

        return dict(image=pyndorama.get_image(adventure=session['_adventure']),
                    action='/acao',
                    global_actions=actions.get('global_actions'),
                    local_actions=actions.get('local_actions'),
                    title=pyndorama.key,
                    place=place)

    @expose(template="pyndorama.templates.edityaml")
    def edityaml(self, adventure):
        path = path_to_adventure_yaml(adventure)
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
