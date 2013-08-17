import unittest
import datastore

from .. import manager
from ..manager import Manager
from ..model import Key
from ..model import Model
from ..object_datastore import ObjectDatastore


class TestManager(unittest.TestCase):

  def test_exists(self):
    self.assertTrue(hasattr(manager, 'Manager'))


  def test_is_class(self):
    self.assertTrue(isinstance(Manager, type))


  def test_model_is_attribute(self):
    self.assertTrue(hasattr(Manager, 'model'))

  def test_construct_with_model_option(self):
    class Foo(Model): pass

    ds = datastore.DictDatastore()
    mgr = Manager(ds, model=Foo)
    self.assertTrue(mgr.model is Foo)


  def test_get_constructs_model(self):
    ds = datastore.DictDatastore()
    mgr = Manager(ds)
    key = Key('/model:bar')
    data = {'key': str(key), 'foo': 'bar'}
    ds.put(key, data)
    instance = mgr.get('bar')
    self.assertTrue(isinstance(instance, Manager.model))
    self.assertEqual(instance.data, data)


  def test_get_constructs_model_with_model(self):
    class Foo(Model): pass

    ds = datastore.DictDatastore()
    mgr = Manager(ds, model=Foo)
    key = Key('/foo:bar')
    data = {'key': str(key), 'foo': 'bar'}
    ds.put(key, data)
    instance = mgr.get('bar')
    self.assertTrue(isinstance(instance, Manager.model))
    self.assertEqual(instance.data, data)


  def test_put_stores_model_data_copy(self):
    ds = datastore.DictDatastore()
    mgr = Manager(ds)
    key = Key('/model:bar')
    instance = Model.withData({'key': str(key), 'foo': 'bar'})
    mgr.put(instance)
    data = ds.get(key)
    self.assertFalse(instance.data is data)
    self.assertEqual(instance.data, data)

  def test_put_stores_model_data_copy_with_model(self):
    class Foo(Model): pass

    ds = datastore.DictDatastore()
    mgr = Manager(ds, model=Foo)
    key = Key('/foo:bar')
    instance = Foo.withData({'key': str(key), 'foo': 'bar'})
    mgr.put(instance)
    data = ds.get(key)
    self.assertFalse(instance.data is data)
    self.assertEqual(instance.data, data)

  def test_delete_and_contains_work(self):
    ds = datastore.DictDatastore()
    mgr = Manager(ds)
    key = Key('/model:bar')
    data = {'key': str(key), 'foo': 'bar'}
    instance = Model.withData(data)

    # put in mgr, delete from mgr
    mgr.put(instance)
    self.assertTrue(mgr.contains(key))
    self.assertTrue(ds.contains(key))

    mgr.delete(key)
    self.assertFalse(mgr.contains(key))
    self.assertFalse(ds.contains(key))

    # put in mgr, delete from ds
    mgr.put(instance)
    self.assertTrue(mgr.contains(key))
    self.assertTrue(ds.contains(key))

    ds.delete(key)
    self.assertFalse(mgr.contains(key))
    self.assertFalse(ds.contains(key))

    # put in ds, delete from mgr
    ds.put(key, data)
    self.assertTrue(mgr.contains(key))
    self.assertTrue(ds.contains(key))

    mgr.delete(key)
    self.assertFalse(mgr.contains(key))
    self.assertFalse(ds.contains(key))

    # put in ds, delete from mgr
    ds.put(key, data)
    self.assertTrue(mgr.contains(key))
    self.assertTrue(ds.contains(key))

    ds.delete(key)
    self.assertFalse(mgr.contains(key))
    self.assertFalse(ds.contains(key))

  def test_query_returns_results(self):
    class Foo(Model):
        def __eq__(self, other):
            return self.data == other.data

    ds = datastore.DictDatastore()
    mgr = Manager(ds, model=Foo)

    instance1 = Foo.withData({'key': '/foo:bar1', 'foo': 'bar1'})
    instance2 = Foo.withData({'key': '/foo:bar2', 'foo': 'bar2'})

    mgr.put(instance1)
    mgr.put(instance2)

    q = mgr.init_query()
    self.assertFalse(q is None)
    results = list(mgr.query(q))
    self.assertEqual(len(results), 2)

    results = list(mgr.query(mgr.init_query().filter('foo','=','bar1')))
    self.assertEqual(len(results), 1)
    self.assertEqual(results[0], instance1)

    results = list(mgr.query(mgr.init_query().filter('foo','=','bar2')))
    self.assertEqual(len(results), 1)
    self.assertEqual(results[0], instance2)

  def test_remove_all_items(self):
    class Foo(Model): pass

    ds = datastore.DictDatastore()
    mgr = Manager(ds, model=Foo)
    key1 = Key('/foo:bar1')
    key2 = Key('/foo:bar2')
    instance1 = Foo.withData({'key': str(key1), 'foo': 'bar1'})
    instance2 = Foo.withData({'key': str(key2), 'foo': 'bar2'})

    # put in mgr
    mgr.put(instance1)
    mgr.put(instance2)
    self.assertTrue(mgr.contains(key1))
    self.assertTrue(ds.contains(key1))
    self.assertTrue(mgr.contains(key2))
    self.assertTrue(ds.contains(key2))

    # delete all
    mgr.remove_all_items()
    self.assertFalse(mgr.contains(key1))
    self.assertFalse(ds.contains(key1))
    self.assertFalse(mgr.contains(key2))
    self.assertFalse(ds.contains(key2))




if __name__ == '__main__':
  unittest.main()
