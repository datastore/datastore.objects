import unittest
import datastore

from .. import collection_manager
from ..model import Key
from ..model import Model
from ..manager import Manager
from ..collection import Collection
from ..collection_manager import CollectionManager
from ..object_datastore import ObjectDatastore


class TestCollectionManager(unittest.TestCase):

  def test_exists(self):
    self.assertTrue(hasattr(collection_manager, 'CollectionManager'))


  def test_is_class(self):
    self.assertTrue(isinstance(CollectionManager, type))


  def test_collection_is_attribute(self):
    self.assertTrue(hasattr(CollectionManager, 'Collection'))


  def test_collection_key(self):
    class Foo(Model): pass

    ds = datastore.DictDatastore()
    mgr = CollectionManager(ds)
    mgr.model = Foo
    self.assertEqual(mgr.collection_key, Key('/foo'))


  def test_key(self):
    class Foo(Model): pass

    ds = datastore.DictDatastore()
    mgr = CollectionManager(ds)
    mgr.model = Foo
    self.assertEqual(mgr.key('bar'), Key('/foo:bar'))


  def test_collection(self):
    ds = datastore.DictDatastore()
    mgr = CollectionManager(ds)
    self.assertTrue(isinstance(mgr.collection, Collection))
    self.assertEqual(mgr.collection.key, Key('/model'))


  def test_put_adds_to_collection(self):
    ds = datastore.DictDatastore()
    mgr = CollectionManager(ds)
    key = Key('/model:bar')
    instance = Model.withData({'key': str(key), 'foo': 'bar'})
    self.assertEqual(list(mgr.collection.keys), [])

    mgr.put(instance)
    self.assertEqual(list(mgr.collection.keys), [instance.key])

  def test_delete_removes_from_collection(self):
    ds = datastore.DictDatastore()
    mgr = CollectionManager(ds)
    key = Key('/model:bar')
    instance = Model.withData({'key': str(key), 'foo': 'bar'})
    self.assertEqual(list(mgr.collection.keys), [])

    mgr.put(instance)
    self.assertEqual(list(mgr.collection.keys), [instance.key])

    mgr.delete(instance.key)
    self.assertEqual(list(mgr.collection.keys), [])


if __name__ == '__main__':
  unittest.main()
