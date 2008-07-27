from turbogears.database import PackageHub
from sqlobject import *

hub = PackageHub('pyndorama')
__connection__ = hub

# class YourDataClass(SQLObject):
#     pass

