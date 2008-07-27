# -*- coding: utf-8 -*-
import unittest
from pyndorama.aventura import (Thing, Things, Chain, ChainEnd, Local,
                                I, D, L, Z, O, V, Action, P, T, A, B, E, U, S,
                                R, M, F)
from pyndorama.util import latin1_to_ascii


class TestThing(unittest.TestCase):

    def setUp(self):
        self.baselist = ['Coisa qualquer', 'Coisa para teste']
        self.thing = Thing(self.baselist)

    def tearDown(self):
        self.baselist = self.thing = None

    def test__init__(self):
        self.assertEqual(self.thing.key,
                         latin1_to_ascii(self.baselist[0]),
                         'Nome incorreto')
        self.assertEqual(self.thing.value, self.baselist[1],
                         'Descrição incorreta')

    def testset_next(self):
        nextthing = Thing(['Outra coisa', 'Coisa diferente'])
        self.thing.set_next(nextthing)
        self.assertEqual(self.thing.following, nextthing,
                         'Erro ao definir proxima coisa')

    def testadditself(self): # TODO Look this up on wikipedia: Visitor Pattern
        thethings = Things(['Grupo 1', 'Um bando de coisas'], [])
        self.thing.additself(thethings)
        self.assertEqual(thethings.contents[self.thing.key], self.thing)

    def testperform(self):
        pass

    def testinvoke_finalizer_hook_from_outer_application(self):
        pass

    def testnormalize(self):
        pass

    def testto_primitive_type(self):
        self.assertEqual(self.thing.to_primitive_type(),
                         dict(nome=self.baselist[0],
                              descricao=self.baselist[1]),
                         'Tipo primitivo errado')

class TestThings(unittest.TestCase):

    def setUp(self):
        self.baselist = [['Grupo 1', 'Um bando de coisas'],
                         [Thing(['1 Coisa', 'Uma coisa 1']),
                         Thing(['2 Coisa', 'Uma coisa 2'])]]
        self.things = Things(*self.baselist)

    def tearDown(self):
        self.baselist = self.thing = None

    def test__init__(self):
        self.assertEqual(self.things.key,
                         latin1_to_ascii(self.baselist[0][0]),
                         'Nome incorreto')
        self.assertEqual(self.things.value, self.baselist[0][1],
                         'Descrição incorreta')
        self.assertEqual(len(self.things.contents), 2,
                         'Conteúdo incorreto')

    def testappend(self): # FIXME Check whether both flows are ever executed in the if branch
        thething = Thing(['3 Coisa', 'Uma coisa 3'])
        self.things.append(thething)
        self.assertEqual(len(self.things.contents), 3,
                         'Número errado de coisas')

    def testpop(self):
        self.things.pop(self.baselist[1][0])
        self.assertEqual(len(self.things.contents), 1,
                         'Número errado de coisas')

    def testfind(self):
        self.assertEqual(self.things.find('2 Coisa'), self.baselist[1][1],
                         'Coisa errada')

    def testhas(self):
        self.assertTrue(self.things.has('2 Coisa'),
                        'Tem coisa 2')
        self.assertFalse(self.things.has('3 Coisa'),
                         'Não tem coisa 3')

    def testparse(self):
        pass

    def testshow(self):
        pass

    def testto_primitive_type(self):
        self.assertEqual(self.things.to_primitive_type(),
                         dict(nome=self.baselist[0][0],
                              descricao=self.baselist[0][1],
                              conteudo=[item.to_primitive_type()
                                        for item in self.baselist[1]]),
                         'Tipo primitivo errado')

class TestChain(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test__init__(self):
        pass

class TestChainEnd(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testperform(self):
        pass

class TestLocal(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test__init__(self):
        pass

    def testperform(self):
        pass

    def testshow(self):
        pass

class TestI(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test__init__(self):
        pass

class TestD(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test__init__(self):
        pass

    def testadditself(self):
        pass

class TestL(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test__init__(self):
        pass

    def testperform(self):
        pass

    def testfind(self):
        pass

class TestZ(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test__init__(self):
        pass

    def testedit_adventure(self):
        pass

    def testplay(self):
        pass

    def testfor_situation(self):
        pass

    def testquestion(self):
        pass

    def testget_image(self):
        pass

    def testdismiss(self):
        pass

    def testreport(self):
        pass

    def testshow(self):
        pass

    def testperform(self):
        pass

    def testparse(self):
        pass

    def testpop(self):
        pass

    def testpush(self):
        pass

    def testfinish(self):
        pass

    def testgoto(self):
        pass

    def testfind(self):
        pass

class TestO(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test__init__(self):
        pass

    def testperform(self):
        pass

class TestV(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test__init__(self):
        pass

    def testperform(self):
        pass


class TestActions(unittest.TestCase):

    def setUp(self):
        self.baselist = ['cachorro', u'Você pegou o cachorrinho!']
        self.action = Action(self.baselist)
        self.p = P(self.baselist)

    def tearDown(self):
        self.action = None

    def _assertion(self, obj, nome):
        self.assertEqual(obj.to_primitive_type(),
                         dict(nome=nome, descricao=self.baselist[1],
                              conteudo=dict(nome=self.baselist[0])),
                         'Tipo primitivo errado')

    def testto_primitive_type(self):
        self._assertion(self.action, 'Action')
        self._assertion(self.p, 'P')


class TestP(unittest.TestCase):

    def setUp(self):
        self.baselist = ['cachorro', u'Você pegou o cachorrinho!']
        self.p = P(self.baselist)

    def tearDown(self):
        pass

    def test__init__(self):
        pass

    def testperform(self):
        pass

    def testto_primitive_type(self):
        self.assertEqual(self.p.to_primitive_type(),
                         dict(nome='P', descricao=self.baselist[1],
                              conteudo=dict(nome=self.baselist[0])),
                         'Tipo primitivo errado')

class TestT(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test__init__(self):
        pass

    def testperform(self):
        pass

class TestA(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testperform(self):
        pass

class TestB(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testperform(self):
        pass

class TestE(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testperform(self):
        pass

class TestU(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testperform(self):
        pass

class TestS(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testperform(self):
        pass

class TestR(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testperform(self):
        pass

class TestM(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testperform(self):
        pass

class TestF(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testperform(self):
        pass

class TestGlobalFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testload(self):
        pass

    def testload_yaml(self):
        pass

if __name__ == '__main__':
    unittest.main()
