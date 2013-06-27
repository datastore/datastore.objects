__author__ = 'Juan Batiz-Benet'
__email__ = 'juan@benet.ai'
__version__ = '0.2.3'
__doc__ = '''
`datastore-objects` is a simple *object mapper* on top of
[datastore](https://github.com/jbenet/datastore) (not relational). Thanks to
datastore's versatility, it makes it easy to (serialize and) persist custom
classes to any sort of data storage service.

Notice: please familiarize yourself with `datastore` first.
'''

import datastore.core

from .util import classproperty
from .attribute_metaclass import AttributeMetaclass
from .attribute_metaclass import DuplicateAttributeError
from .attribute import Attribute
from .model import Key
from .model import Model
from .manager import Manager
from .object_datastore import ObjectDatastore
