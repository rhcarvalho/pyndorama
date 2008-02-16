# -*- coding: utf-8 -*-
import unittest
import re
from pyndorama.util import *


class TestGlobalFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testgetAbsParent(self):
        self.assertEqual(getAbsParent('/home/joe/pyndorama/pyndorama/controllers.py'),
                         os.path.abspath('/home/joe/pyndorama/pyndorama/'))

    def testgetModulePath(self):
        self.assertTrue(re.match('.*(util.py).?$', getModulePath()),
                        'Failed to match util.py')
        for name, arg in [('test_util.py', __name__),
                          ('unittest.py', 'unittest')]:
            self.assertTrue(re.match('.*(%s).?$' % name, getModulePath(arg)),
                            'Failed to match %s' % name)
        self.assertRaises(IOError, getModulePath, 'someDummyModule')

    def testgetModuleDir(self):
        self.assertRaises(IOError, getModuleDir, 'someDummyModule')

    def testgetFullPath(self):
        self.assertRaises(IOError, getFullPath, 'someDummyModule', 'some/dir/adventure.yaml')

        path = getFullPath(__name__, 'some/dir/adventure.yaml')
        self.assertTrue(path.endswith(os.path.normpath('some/dir/adventure.yaml')))

    def testmagicTranslate(self):
        mydict = {
        "Larry Wall" : "Guido van Rossum",
        "creator" : "Benevolent Dictator for Life",
        "Perl" : "Python",
        }

        tests = [(mydict, "Larry Wall is the creator of Perl",
                   'Guido van Rossum is the Benevolent Dictator for Life of Python'),
                 (LATIN1_TO_ASCII, u'João é ágil. Luz, câmera e AÇÃO!',
                   'Joao e agil. Luz, camera e ACAO!')]

        for mapping, text, answer in tests:
            self.assertEqual(answer, magicTranslate(text, mapping))

    def testlatin1_to_ascii(self):
        latin1 = u'ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝßàáâãäåæçèéêëìíîïñòóôõö÷øùúûüýÿ'
        ascii = 'AAAAAAAECEEEEIIIIDNOOOOO*OUUUUYBaaaaaaaeceeeeiiiinooooo/ouuuuyy'

        self.assertEqual(ascii, latin1_to_ascii(latin1))

        # generic unicode chars (non Latin-1)
        non_latin1 = ''.join(unichr(i) for i in xrange(0x0100, 0xfffe, 1000))
        self.assertEqual('', latin1_to_ascii(non_latin1))

        mixed_text = u'ĀHeālĂăĄląĆćoĈĉ WĊoċČrlčĎďd'
        self.assertEqual('Hello World', latin1_to_ascii(mixed_text))

    def testencode_to_xml_entities(self):
        text = u'<html><body>&#169; Pyndorama não é difícil.&nbsp;Alô! ©</body></html>'
        answer = '<html><body>&#169; Pyndorama n&#227;o &#233; dif&#237;cil.&nbsp;Al&#244;! &#169;</body></html>'
        self.assertEqual(answer, encode_to_xml_entities(text))


if __name__ == '__main__':
    unittest.main()