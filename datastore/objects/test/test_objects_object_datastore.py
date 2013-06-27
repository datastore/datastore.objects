import unittest
import datastore

from .. import object_datastore
from ..model import Key
from ..model import Model
from ..object_datastore import ObjectDatastore


class TestObjectDatastore(unittest.TestCase):

  def test_exists(self):
    self.assertTrue(hasattr(object_datastore, 'ObjectDatastore'))


  def test_is_class(self):
    self.assertTrue(isinstance(ObjectDatastore, type))


  def test_is_shim_datastore(self):
    self.assertTrue(issubclass(ObjectDatastore, datastore.ShimDatastore))


  def test_model_is_attribute(self):
    self.assertTrue(hasattr(ObjectDatastore, 'model'))


  def test_construct_with_model_option(self):
    class Foo(Model): pass

    dds = datastore.DictDatastore()
    ods = ObjectDatastore(dds, model=Foo)
    self.assertTrue(ods.model is Foo)


  def test_get_constructs_model(self):
    dds = datastore.DictDatastore()
    ods = ObjectDatastore(dds)
    key = Key('/model:foo')
    dds.put(key, {'key': str(key), 'foo': 'bar'})
    instance = ods.get(key)
    self.assertTrue(isinstance(instance, ObjectDatastore.model))


  def test_get_constructs_model_option(self):
    class Foo(Model): pass

    dds = datastore.DictDatastore()
    ods = ObjectDatastore(dds, model=Foo)
    key = Key('/foo:foo')
    dds.put(key, {'key': str(key), 'foo': 'bar'})
    instance = ods.get(key)
    self.assertTrue(isinstance(instance, ObjectDatastore.model))
    self.assertTrue(isinstance(instance, Foo))


  def test_get_constructs_model_with_data_attr(self):
    dds = datastore.DictDatastore()
    ods = ObjectDatastore(dds)
    key = Key('/model:foo')
    data = {'key': str(key), 'foo': 'bar'}
    dds.put(key, data)
    instance = ods.get(key)
    self.assertEqual(instance.data, data)
    self.assertFalse(instance.data is data)


  def test_get_constructs_model(self):
    dds = datastore.DictDatastore()
    ods = ObjectDatastore(dds)
    key = Key('/model:foo')
    dds.put(key, {'key': str(key), 'foo': 'bar'})
    instance = ods.get(key)
    self.assertTrue(isinstance(instance, ObjectDatastore.model))


  def test_put_stores_model_data_copy(self):
    dds = datastore.DictDatastore()
    ods = ObjectDatastore(dds)
    key = Key('/model:foo')
    instance = Model.withData({'key': str(key), 'foo': 'bar'})
    ods.put(key, instance)
    data = dds.get(key)
    self.assertEqual(instance.data, data)
    self.assertFalse(instance.data is data)


  def test_put_stores_model_data_with_key(self):
    dds = datastore.DictDatastore()
    ods = ObjectDatastore(dds)
    key = Key('/model:foo')
    data = {'key': str(key), 'foo': 'bar'}
    instance = Model.withData(data)
    self.assertTrue('key' in data)
    self.assertTrue('key' in instance.data)

    ods.put(key, instance)
    data = dds.get(key)
    self.assertTrue('key' in data)
    self.assertEqual(data['key'], '/model:foo')


  def test_delete_and_contains_work(self):
    dds = datastore.DictDatastore()
    ods = ObjectDatastore(dds)
    key = Key('/model:foo')
    data = {'key': str(key), 'foo': 'bar'}
    instance = Model.withData(data)

    # put in ods, delete from ods
    ods.put(key, instance)
    self.assertTrue(ods.contains(key))
    self.assertTrue(dds.contains(key))

    ods.delete(key)
    self.assertFalse(ods.contains(key))
    self.assertFalse(dds.contains(key))

    # put in ods, delete from dds
    ods.put(key, instance)
    self.assertTrue(ods.contains(key))
    self.assertTrue(dds.contains(key))

    dds.delete(key)
    self.assertFalse(ods.contains(key))
    self.assertFalse(dds.contains(key))

    # put in dds, delete from ods
    dds.put(key, data)
    self.assertTrue(ods.contains(key))
    self.assertTrue(dds.contains(key))

    ods.delete(key)
    self.assertFalse(ods.contains(key))
    self.assertFalse(dds.contains(key))

    # put in dds, delete from dds
    dds.put(key, data)
    self.assertTrue(ods.contains(key))
    self.assertTrue(dds.contains(key))

    dds.delete(key)
    self.assertFalse(ods.contains(key))
    self.assertFalse(dds.contains(key))


  def test_query_is_implemented(self):
    dds = datastore.DictDatastore()
    ods = ObjectDatastore(dds)
    ods.query(datastore.Query(Key('/model')))


  def test_query_returns_instances(self):
    dds = datastore.DictDatastore()
    ods = ObjectDatastore(dds)

    key = Key('/model:foo')
    instance = Model.withData({'key': str(key), 'foo': 'bar'})
    ods.put(key, instance)

    key = Key('/model:bar')
    instance = Model.withData({'key': str(key), 'foo': 'bar'})
    ods.put(key, instance)

    query = datastore.Query(Key('/model'))
    query.order('-key')
    results = list(ods.query(query))
    self.assertEqual(len(results), 2)
    self.assertTrue(isinstance(results[0], Model))
    self.assertTrue(isinstance(results[1], Model))
    self.assertEqual(results[0].key, Key('/model:foo'))
    self.assertEqual(results[1].key, Key('/model:bar'))



if __name__ == '__main__':
  unittest.main()
