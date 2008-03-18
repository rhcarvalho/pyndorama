#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""\
Pyndorama: An adventure trip around the world.
Pyndorama: Uma viagem de aventura ao redor do mundo
===================================================

A text based adventure that can be programmed.
Uma aventura baseada em texto que pode se programada.

Copyright (c) 2002-2007
Carlo E.T. Oliveira et all
(see U{http://labase.nce.ufrj.br/info/equipe.html})

This software is licensed as described in the file LICENSE.txt,
which you should have received as part of this distribution.
"""

import sys
from codecs import open

import yaml

import util

__author__  = "Carlo E. T. Oliveira (cetoli@yahoo.com.br) $Author: carlo $"
__version__ = "1.0 $Revision: 1.18 $"[10:-1]
__date__    = "2006/04/24 $Date: 30/06/2006 16:18:46 $"

ENCODING = 'utf-8'
FIRST_PLACE = 0
MAPA_MUNDI = {}
CANNOT_FIND_OBJECT = u'Não vejo necas de %s aqui!'
CANNOT_PERFORM_ACTION = u'Não deu certo essa de %s!'
ACTION_IS_USELESS = u'Nada acontece caso você %s.'
YOU_CAN_SEE = u'Você pode ver:'


class UselessAction(Exception):
    pass


class Thing(object):
    """Anything whatsoever - Uma coisa qualquer."""
    def __init__(self, value, *args):
        if len(value) < 2:
            value.append('')
        self.key = value[0] and self.normalize(value[0]) or value[0]
        self.value = value[-1]
        self.following = None
        self.finalizer = lambda: None
        self.editor = lambda: None

    def set_next(self, next):
        self.following = next

    def additself(self, target):
        """Double-dispatch response during initialization
        -- Resposta do double dispatch de inicializacao."""
        target.append(self)

    def perform(self, statement, place=None):
        return self.value + '\n' + self.following.perform(statement, place)

    def invoke_finalizer_hook_from_outer_application(self):
        self.finalizer()

    def normalize(self, key):
        """converte unicode, limita tamanho e muda para caixa alta."""
        return util.latin1_to_ascii(key[:4].upper())


class Things(Thing):
    """Coletivos."""
    def __init__(self, value, *args):
        Thing.__init__(self, value, args)
        self.contents = {}
        self.args = args[:][0]
        if len(self.args) and isinstance(self.args[0], list):
            self.args = self.args[0]
        self.active = False
        for coisa in self.args:
            coisa.additself(self)

    def append(self, athing):
        """adiciona na colecao"""
        if isinstance(athing.key, list):
            for key in athing.key:
                self.contents[key] = athing
        else:
            self.contents[athing.key] = athing

    def pop(self, athing):
        """remove da colecao"""
        self.contents.pop(athing.key)

    def find(self, key):
        """procura na colecao"""
        return self.contents[self.normalize(key)]

    def has(self, key):
        """verifica se tem na colecao"""
        return self.contents.has_key(self.normalize(key))

    def __repr__(self):
        return '<%s>' % self.key

    def parse(self, statement, place):
        if not (statement[0:] and statement[0]):
            return self.show()
        for noum in statement:
            if self.has(noum):
                statement.pop(statement.index(noum))
                return self.find(noum).perform(statement, place)
        return None

    def show(self):
        """mostra o conteudo da localizacao"""
        return self.value


class Chain(Thing):
    """O conteudo eh uma Chain of Responsibility."""
    def __init__(self, value, *args):
        Thing.__init__(self, value, args)
        arguments = args[:][0]
        if len(arguments) and isinstance(arguments[0], list):
            arguments = arguments[0]
        self.contents = CHAIN_END
        for item in arguments:
            self.contents, self.contents.following = item, self.contents


class ChainEnd(Thing):
    """Objeto nulo para fechar o fim da chain"""
    def perform(self, statement, place=None):
        return ''


CHAIN_END = ChainEnd(['END'])


class Local(Things):
    """Representa um Inventario com varios objetos."""
    def __init__(self, value, *args):
        Things.__init__(self, value, args)
        MAPA_MUNDI[self.key] = self

    def perform(self, statement, place):
        return self.parse(statement, place)

    def show(self):
        """mostra o conteudo da localizacao"""
        response = [self.value, YOU_CAN_SEE]
        if self.contents.values():
            response.extend('\t' + item.value
                            for item in self.contents.itervalues()
                            if item.value)
        else:
            response.append('\tnada aqui')
        return '\n'.join(response)


class I(Thing):
    """Descreve a tela inicial."""
    def __init__(self, value):
        self.key = value[0]


class D(Thing):
    """Descreve uma coisa."""
    def __init__(self, value):
        self.key = value[0]
        self.value = value[1]

    def additself(self, target):
        target.value += '\n' + self.value


class L(Local):
    """Representa um Lugar com varios objetos."""
    def __init__(self, value, *args):
        Things.__init__(self, value, args)
        MAPA_MUNDI[self.key] = self

    def perform(self, statement, place):
        question = statement[:]
        try:
            found = inventario.perform(statement, place)
            if found:
                return found
            found = self.parse(statement, place)
            if found:
                return found
            if statement[1:]:
                return CANNOT_FIND_OBJECT % statement[-1]
            raise KeyError
        except KeyError:
            return CANNOT_PERFORM_ACTION % (' '.join(question))
        except UselessAction:
            return ACTION_IS_USELESS % (' '.join(question))

    def find(self, key):
        """procura na colecao"""
        if inventario.has(key):
            return inventario.find(key)
        return self.contents[self.normalize(key)]


inventario = Local(['inventario', u'Você examina o seu inventário.'])
playadventure = True


class Z(Things):
    """Representa o mundo."""
    def __init__(self, value, *args):
        Things.__init__(self, value, args)
        self.current_place = self.args[FIRST_PLACE]
        #print self.current_place
        self.response = self.perform([])
        self.can = True
        self.prompt = '\nO que devo fazer agora?\n'
        self.actions = {'QUIT': lambda self = self: self.dismiss(),
                        'INVE': lambda self = self: self.report(),
                        'OLHE': lambda self = self: self.show(),
                        'XYZZ': lambda self = self: self.edit_adventure()}

    def edit_adventure(self):
        """finaliza aventura"""
        global playadventure
        playadventure = False
        self.response = 'XXX --- A AVENTURA SERA EDITADA!!! --- XXX'
        self.editor()
        return self.response

    def play(self):
        """Continua a aventura enquanto pode."""
        #print 'Aventura'
        while playadventure:
            self.perform(self.question(self.for_situation()))
        print self.response

    def for_situation(self):
        """Concatena a resposta com uma nova pergunta"""
        return self.response + self.prompt

    def question(self, query):
        """Imprime a resposta e pede o novo comando"""
        try:
            query = query.encode(sys.stdout.encoding, 'replace')
        except AttributeError:
            pass
        return raw_input(query).split(' ')

    def get_image(self):
        return '/static/images/' + self.current_place.key + '.gif'

    def dismiss(self):
        """finaliza aventura"""
        global playadventure
        playadventure = False
        self.response = 'XXX --- ACABOU A SUA AVENTURA !!! --- XXX'
        self.invoke_finalizer_hook_from_outer_application()
        return self.response

    def report(self):
        return inventario.show()

    def show(self):
        self.response = self.current_place.show()
        return self.response

    def perform(self, statement, place=None):
        here = self.current_place
        self.response = self.parse(statement, self)
        if not self.response:
            self.response = here.perform(statement, self)
        return self.response

    def parse(self, statement, place):
        verb = ''
        if not (statement[0:] and statement[0]):
            return self.show()
        verb = self.normalize(statement[0])
        if statement[1:]:
            return None
        try:
            return self.actions[verb]()
        except KeyError:
            return None

    def pop(self, athing):
        """remove da colecao"""
        if not inventario.has(athing.key):
            return
        self.current_place.append(athing)
        inventario.pop(athing)

    def push(self, athing):
        """remove da colecao"""
        if not self.current_place.has(athing.key):
            return
        self.current_place.pop(athing)
        inventario.append(athing)

    def finish(self):
        """finaliza aventura"""
        self.can = False

    def goto(self, place):
        """move para um lugar"""
        location = MAPA_MUNDI[self.normalize(place)]
        self.current_place = location
        return self.current_place

    def find(self, key):
        """procura na colecao"""
        if inventario.has(key):
            return inventario.find(key)
        return self.current_place.find(key)


class O(Things):
    """Representa um Objeto que suporta varias acoes"""
    def __init__(self, value, *args):
        Things.__init__(self, value, args)

    def perform(self, statement, place=None):
        found = self.parse(statement, place)
        if found:
            return found
        if statement.count('olhe'):
            return self.value
        raise UselessAction


class V(Chain):
    """Representa um verbo com variantes de acoes sobre objetos"""
    def __init__(self, value, *args):
        Chain.__init__(self, value, args)

    def perform(self, statement, place=None):
        try:
            if self.value:
                return self.value + '\n' + self.contents.perform(statement, place)
            return self.contents.perform(statement, place)
        except KeyError:
            return CANNOT_PERFORM_ACTION % (' '.join(statement)) + ' ...'


class P(Thing):
    """Pega objeto e poe no inventario"""
    def __init__(self, value, *args):
        Thing.__init__(self, value, args)

    def perform(self, statement, place=None):
        obj = place.find(self.key)
        try:
            place.push(obj)
            return self.value + '\n' + self.following.perform(statement, place)
        except KeyError:
            return CANNOT_PERFORM_ACTION % (' '.join(statement)) + ' ...'


class T(Thing):
    """Pega objeto e tira do inventario"""
    def __init__(self, value, *args):
        Thing.__init__(self, value, args)

    def perform(self, statement, place=None):
        obj = place.find(self.key)
        try:
            place.pop(obj)
            return self.value + '\n' + self.following.perform(statement, place)
        except KeyError:
            return CANNOT_PERFORM_ACTION % (' '.join(statement)) + ' ...'


class A(Thing):
    """Ativa objeto"""
    def perform(self, statement, place=None):
        obj = place.find(self.key)
        obj.active = True
        return self.value + '\n' + self.following.perform(statement, place)


class B(Thing):
    """Bloqueia objeto"""
    def perform(self, statement, place=None):
        obj = place.find(self.key)
        obj.active = False
        return self.value + '\n' + self.following.perform(statement, place)


class E(Thing):
    """Ativa objeto, trocando a sua descricao"""
    def perform(self, statement, place=None):
        obj = place.find(self.key)
        obj.active = True
        obj.value = self.value
        return self.following.perform(statement, place)


class U(Thing):
    """Bloqueia objeto, trocando a sua descricao"""
    def perform(self, statement, place=None):
        obj = place.find(self.key)
        obj.active = False
        obj.value = self.value
        return self.following.perform(statement, place)


class S(Thing):
    """testa se objeto estah ativo"""
    def perform(self, statement, place=None):
        try:
            obj = place.find(self.key)
            if not obj.active:
                return self.value
            else:
                return self.following.perform(statement, place)
        except KeyError:
            return self.value


class R(Thing):
    """testa se objeto estah bloqueado"""
    def perform(self, statement, place=None):
        try:
            obj = place.find(self.key)
            if obj.active:
                return self.value
            else:
                return self.following.perform(statement, place)
        except KeyError:
            return self.value


class M(Thing):
    """Move para o lugar"""
    def perform(self, statement, place=None):
        return (self.value + '\n' + place.goto(self.key).show()
                + '\n' + self.following.perform(statement, place))
##        return self.value + '\n' + place.goto(self.key).show()


class F(Thing):
    """Finaliza a aventura"""
    def perform(self, statement, place=None):
        return self.value + '\n' + place.dismiss()


class Adventure(object):
    g = globals()
    for t in range(ord('A'), ord('Z')):
        if chr(t) not in g.keys():
            g[chr(t)] = type(chr(t), (Thing,), {})

    def __init__(self, filename=None, content=None):
        if filename is not None:
            adventure_file = open(filename, 'rb', ENCODING, 'ignore')
            self.world_mapping = yaml.load(adventure_file)
            adventure_file.close()
        elif content is not None:
            self.world_mapping = yaml.load(content)
        else:
            # Should never happen!
            raise TypeError, '__init__() takes at least 2 arguments (1 given)'

    def load(self):
        global FIRST_PLACE
        try:
            FIRST_PLACE = -1
            return self.load_letters_and_lists(self.world_mapping[0])
        except KeyError:
            FIRST_PLACE = 0
            return self.load_nested_mappings()

    def load_nested_mappings(self, mapping=None, level=0):
        if mapping is None:
            mapping = self.world_mapping
##        print '-' * 80
##        print level, mapping
        classes = [Z, L, O, V]
        try:
            theclass = classes[level]
            thename = mapping.get('nome', '')
            thecontent = [self.load_nested_mappings(sibiling, level + 1)
                          for sibiling in mapping.get('conteudo', [])]
        except IndexError:
            theclass = Adventure.g[mapping.get('nome')]
            try:
                thename = mapping.get('conteudo', [])[0].get('nome', '')
            except IndexError:
                thename = ''
            thecontent = []
        thedescription = mapping.get('descricao', '')
        if thecontent:
            return theclass([thename, thedescription], thecontent)
        else:
            return theclass([thename, thedescription])

    def load_letters_and_lists(self, thing):
        thing_name = thing.keys()[0]
        thing_definition = thing.pop(thing_name)
        thing_value = thing_definition[0]
        thing_contents = [self.load_letters_and_lists(athing)
                          for athing in thing_definition[1:]]
##        print thing_name, ' > ', thing_contents
        if thing_contents:
            return Adventure.g[thing_name](thing_value, thing_contents)
        else:
            return Adventure.g[thing_name](thing_value)


if __name__ == '__main__':
    try:
        Adventure('static/aventura/a_gralha_e_o_jarro.yaml').load().play()
##        Adventure('static/aventura/ave.yaml').load().play()
    except Exception:
        import traceback
        traceback.print_exc()
