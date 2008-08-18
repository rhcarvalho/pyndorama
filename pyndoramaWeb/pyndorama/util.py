# -*- coding: utf-8 -*-
import os, sys
import yaml

LATIN1_TO_ASCII = {u'¡': '!', u'¢': ''  , u'£': '' , u'¤': ''  , u'¥': '' , u'¦': '|',
                   u'§': '' , u'¨': ''  , u'©': '' , u'ª': ''  , u'«': '' , u'¬': '-',
                   u'­': '-', u'®': ''  , u'¯': '' , u'°': ''  , u'±': '' , u'²': '' ,
                   u'³': '' , u'´': ''  , u'µ': '' , u'¶': ''  , u'·': '' , u'¸': '' ,
                   u'¹': '' , u'º': ''  , u'»': '' , u'¼': ''  , u'½': '' , u'¾': '' ,
                   u'¿': '?', u'À': 'A' , u'Á': 'A', u'Â': 'A' , u'Ã': 'A', u'Ä': 'A',
                   u'Å': 'A', u'Æ': 'AE', u'Ç': 'C', u'È': 'E' , u'É': 'E', u'Ê': 'E',
                   u'Ë': 'E', u'Ì': 'I' , u'Í': 'I', u'Î': 'I' , u'Ï': 'I', u'Ð': 'D',
                   u'Ñ': 'N', u'Ò': 'O' , u'Ó': 'O', u'Ô': 'O' , u'Õ': 'O', u'Ö': 'O',
                   u'×': '*', u'Ø': 'O' , u'Ù': 'U', u'Ú': 'U' , u'Û': 'U', u'Ü': 'U',
                   u'Ý': 'Y', u'Þ': ''  , u'ß': 'B', u'à': 'a' , u'á': 'a', u'â': 'a',
                   u'ã': 'a', u'ä': 'a' , u'å': 'a', u'æ': 'ae', u'ç': 'c', u'è': 'e',
                   u'é': 'e', u'ê': 'e' , u'ë': 'e', u'ì': 'i' , u'í': 'i', u'î': 'i',
                   u'ï': 'i', u'ð': ''  , u'ñ': 'n', u'ò': 'o' , u'ó': 'o', u'ô': 'o',
                   u'õ': 'o', u'ö': 'o' , u'÷': '/', u'ø': 'o' , u'ù': 'u', u'ú': 'u',
                   u'û': 'u', u'ü': 'u' , u'ý': 'y', u'þ': ''  , u'ÿ': 'y'}


def getAbsParent(path):
    return os.path.abspath(os.path.dirname(path))


def getModulePath(module=__name__):
    path = getattr(sys.modules.get(module), '__file__', '')
    if os.path.exists(path):
        return path
    else:
        raise IOError, 'Could not find the path of module "%s"' % module


def getModuleDir(module=__name__):
    return getAbsParent(getModulePath(module))


def getFullPath(module, relative_path):
    return os.path.join(getModuleDir(module), os.path.normpath(relative_path))


def magicTranslate(string, mapping):
    """Replace substrings of a string using a dictionary."""
    for key, value in mapping.iteritems():
        string = string.replace(key, value)
    return string


def latin1_to_ascii(unicode_str):
    """This takes a UNICODE string and replaces Latin-1 characters with
    something equivalent in 7-bit ASCII. It returns a plain ASCII string.
    This function makes a best effort to convert Latin-1 characters into
    ASCII equivalents. It does not just strip out the Latin-1 characters.
    All characters in the standard 7-bit ASCII range are preserved.
    In the 8th bit range all the Latin-1 accented letters are converted
    to unaccented equivalents. Most symbol characters are converted to
    something meaningful. Anything not converted is deleted."""

##¡ ¢ £ ¤ ¥ ¦ § ¨ © ª « ¬ ­ ® ¯ ° ± ² ³ ´ µ ¶ · ¸ ¹ º » ¼ ½ ¾
##!         |           - -
##
##¿ À Á Â Ã Ä Å Æ Ç È É Ê Ë Ì Í Î Ï Ð Ñ Ò Ó Ô Õ Ö × Ø Ù Ú Û Ü Ý
##? A A A A A A AEC E E E E I I I I D N O O O O O * O U U U U Y
##
##Þ ß à á â ã ä å æ ç è é ê ë ì í î ï ð ñ ò ó ô õ ö ÷ ø ù ú û ü ý þ ÿ
##  B a a a a a a aec e e e e i i i i   n o o o o o / o u u u u y   y

    mapping = LATIN1_TO_ASCII
    ascii = magicTranslate(unicode_str, mapping)
    try:
        ascii = ascii.encode('ascii', 'strict')
    except UnicodeEncodeError:
        # append all other unicode chars (too time-consuming)
        mapping.update((unichr(i), '') for i in xrange(0x0100, 0xffde))
        ascii = magicTranslate(unicode_str, mapping)
        ascii = ascii.encode('ascii', 'replace')
    return ascii


def encode_to_xml_entities(text):
    return text.encode('ascii', 'xmlcharrefreplace')


def cria_lista_arquivos(path='./pyndorama/static/aventura/'):
    """Lê a pasta aventura e popula uma lista com os arquivos de aventuras e 
    seus respectivos nomes. Utiliza a classe ListaDeAventuras para filtrar as 
    aventuras que contenham nome"""
    arquivos = os.listdir(path)
    lista = []
    for arquivo in arquivos:
        if arquivo.endswith('.yaml'):
            try:
                arquivo_aberto = open(path + arquivo, 'r')
            except IOError:
                continue
            lista.append(arquivo_aberto)
    lista_aventuras = ListaDeAventuras()
    return lista_aventuras(lista)


class ListaDeAventuras:
    def _le_nome(self, dic):
        return dic['nome']

    def __call__(self, arquivos):
        lista = []
        
        for a in arquivos:
            caminho = a.name
            try:
                nome = self._le_nome(yaml.load(a.read()))
            except TypeError:
                continue
            finally:
                a.close()
            lista.append((caminho, nome))
        return lista


if __name__ == '__main__':
    from timeit import Timer

    time_latin1_str    = Timer(u"latin1_to_ascii(u'ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝßàáâãäåæçèéêëìíîïñòóôõö÷øùúûüýÿ')",
                                "from __main__ import latin1_to_ascii").timeit(100)

    time_nonlatin1_str = Timer(u"latin1_to_ascii(u'ĀHeālĂăĄląĆćoĈĉ WĊoċČrlčĎďd')",
                                "from __main__ import latin1_to_ascii").timeit(100)

    latin1_str    = u'ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝßàáâãäåæçèéêëìíîïñòóôõö÷øùúûüýÿ'
    nonlatin1_str = u'ĀHeālĂăĄląĆćoĈĉ WĊoċČrlčĎďd'

    print '\n'.join(('%-60s%10.5f\n%-70s\n%-70s\n%s',)*2) % \
          ('Latin-1 string'    , time_latin1_str   , latin1_str   , latin1_to_ascii(latin1_str)   , '-'*70,
           'Non-Latin 1 string', time_nonlatin1_str, nonlatin1_str, latin1_to_ascii(nonlatin1_str), '')



