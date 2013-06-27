import unittest
import logging
import datastore

from datastore.core import DictDatastore

from .. import collection
from ..model import Key
from ..model import Model
from ..collection import Collection
from ..object_datastore import ObjectDatastore


class TestCollection(unittest.TestCase):

  def test_exists(self):
    self.assertTrue(hasattr(collection, 'Collection'))


  def test_is_class(self):
    self.assertTrue(isinstance(Collection, type))


  def test_has_datastore(self):
    ds = DictDatastore()
    coll = Collection(Key('Foo'), ds)
    self.assertTrue(coll.datastore is ds)


  def test_has_symlink_datastore(self):
    from datastore.core import SymlinkDatastore
    ds = DictDatastore()
    coll = Collection(Key('Foo'), ds)
    self.assertTrue(isinstance(coll.symlink_datastore, SymlinkDatastore))


  def test_has_directory_datastore(self):
    from datastore.core import DirectoryDatastore
    ds = DictDatastore()
    coll = Collection(Key('Foo'), ds)
    self.assertTrue(isinstance(coll.directory_datastore, DirectoryDatastore))


  def test_keys_property(self):
    coll = Collection(Key('Foo'), DictDatastore())
    ds = ObjectDatastore(coll.directory_datastore)

    bar = Model('bar')
    baz = Model('baz')
    ds.put(bar.key, bar)
    ds.put(baz.key, baz)
    coll.add(bar)
    coll.add(baz)
    bar_ckey = Key('/Foo:bar')
    baz_ckey = Key('/Foo:baz')

    keys = list(coll.keys)
    self.assertEqual(keys, [bar_ckey, baz_ckey])


  def test_instances_property(self):
    coll = Collection(Key('Foo'), DictDatastore())
    ds = ObjectDatastore(coll.directory_datastore)

    bar = Model('bar')
    baz = Model('baz')
    ds.put(bar.key, bar)
    ds.put(baz.key, baz)
    coll.add(bar)
    coll.add(baz)

    instances = list(coll.instances)
    self.assertEqual(instances[0].data, bar.data)
    self.assertEqual(instances[1].data, baz.data)


  def test_instance_data_generator(self):
    coll = Collection(Key('Foo'), DictDatastore())
    ds = ObjectDatastore(coll.directory_datastore)

    bar = Model('bar')
    baz = Model('baz')
    ds.put(bar.key, bar)
    ds.put(baz.key, baz)
    coll.add(bar)
    coll.add(baz)

    data = list(coll.instance_data_generator())
    self.assertEqual(data[0], bar.data)
    self.assertEqual(data[1], baz.data)


  def test_add(self):
    coll = Collection(Key('Foo'), DictDatastore())
    ds = ObjectDatastore(coll.directory_datastore)

    bar = Model('bar')
    baz = Model('baz')
    ds.put(bar.key, bar)
    ds.put(baz.key, baz)
    bar_ckey = Key('/Foo:bar')
    baz_ckey = Key('/Foo:baz')

    self.assertIsNone(ds.get(bar_ckey))
    self.assertEqual(list(coll.keys), [])
    coll.add(bar)
    self.assertEqual(ds.get(bar_ckey).data, bar.data)
    self.assertEqual(list(coll.keys), [bar_ckey])

    self.assertIsNone(ds.get(baz_ckey))
    self.assertEqual(list(coll.keys), [bar_ckey])
    coll.add(baz)
    self.assertEqual(ds.get(baz_ckey).data, baz.data)
    self.assertEqual(list(coll.keys), [bar_ckey, baz_ckey])


  def test_remove(self):
    coll = Collection(Key('Foo'), DictDatastore())
    ds = ObjectDatastore(coll.directory_datastore)

    bar = Model('bar')
    baz = Model('baz')
    ds.put(bar.key, bar)
    ds.put(baz.key, baz)
    bar_ckey = Key('/Foo:bar')
    baz_ckey = Key('/Foo:baz')

    coll.add(bar)
    coll.add(baz)
    self.assertEqual(list(coll.keys), [bar_ckey, baz_ckey])


    self.assertEqual(ds.get(bar_ckey).data, bar.data)
    self.assertEqual(list(coll.keys), [bar_ckey, baz_ckey])
    coll.remove(bar)
    self.assertIsNone(ds.get(bar_ckey))
    self.assertEqual(list(coll.keys), [baz_ckey])

    self.assertEqual(ds.get(baz_ckey).data, baz.data)
    self.assertEqual(list(coll.keys), [baz_ckey])
    coll.remove(baz)
    self.assertIsNone(ds.get(baz_ckey))
    self.assertEqual(list(coll.keys), [])



if __name__ == '__main__':
  unittest.main()
