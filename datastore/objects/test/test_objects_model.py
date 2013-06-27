import unittest
import datastore

from .. import model
from ..model import Key
from ..model import Model
from ..attribute import Attribute
from ..attribute_metaclass import AttributeMetaclass

class TestKey(unittest.TestCase):

  def test_exists(self):
    self.assertTrue(hasattr(model, 'Key'))


  def test_is_datastore_key(self):
    self.assertEqual(Key, datastore.Key)



class TestModel(unittest.TestCase):

  def test_exists(self):
    self.assertTrue(hasattr(model, 'Model'))


  def test_is_class(self):
    self.assertTrue(isinstance(Model, type))


  # construction tests

  def test_construct_with_key(self):
    key = Key('/model:foo')
    self.assertEqual(Model(key).key, key)
    key = Key('/foo:bar/model:foo')
    self.assertEqual(Model(key).key, key)

    with self.assertRaises(TypeError):
      Model(Key('/foo:bar'))
      Model(Key('/model:foo/bar'))
      Model(Key('/model:foo/bar:biz'))

    # keys MUST be of type Key (not str)
    with self.assertRaises(AssertionError):
      Model('/foo:bar')


  def test_construct_with_name(self):
    self.assertEqual(Model('foo').key, Key('/model:foo'))
    self.assertEqual(Model('bar').key, Key('/model:bar'))


  def test_construct_without_key_or_name_fails(self):
    with self.assertRaises(TypeError):
      Model(1)
      Model({})
      Model([])


  # data tests

  def test_data_is_attr(self):
    self.assertTrue(hasattr(Model('foo'), 'data'))


  def test_data_is_dict(self):
    self.assertTrue(isinstance(Model('foo').data, dict))


  # Attribute tests

  def test_uses_attribute_metaclass(self):
    self.assertTrue(Model.__metaclass__ is AttributeMetaclass)


  def test_can_define_attributes(self):
    class Foo(Model):
      foo = Attribute()

    self.assertTrue('foo' in Foo._attributes)


  def test_attributes_get_from_data(self):
    class Foo(Model):
      foo = Attribute()

    f = Foo('foo')
    self.assertEqual(f.foo, None)
    f.data['foo'] = 'bar'
    self.assertEqual(f.foo, 'bar')


  def test_attributes_get_from_data_with_default(self):
    class Foo(Model):
      foo = Attribute(default='biz')

    f = Foo('foo')
    self.assertEqual(f.data['foo'], 'biz')
    self.assertEqual(f.foo, 'biz')
    f.data['foo'] = 'bar'
    self.assertEqual(f.foo, 'bar')


  def test_attributes_set_to_data(self):
    class Foo(Model):
      foo = Attribute()

    f = Foo('foo')
    self.assertEqual(f.data.get('foo'), None)
    f.foo = 'bar'
    self.assertEqual(f.data.get('foo'), 'bar')


  # key type tests

  def test_key_type_is_attr(self):
    self.assertTrue(hasattr(Model, 'key_type'))


  def test_key_type_defaults_to_lowercase_classname(self):
    self.assertEqual(Model.key_type, 'model')


  def test_key_type_value(self):
    Model.__key_type__ = 'foo'
    self.assertEqual(Model.key_type, 'foo')
    del Model.__key_type__


  def test_key_type_inheritance_default(self):
    class Foo(Model): pass
    class Bar(Foo): pass

    self.assertEqual(Foo.key_type, 'foo')
    self.assertEqual(Bar.key_type, 'bar')


  def test_key_type_inheritance_keeps_value(self):
    class Foo(Model):
      __key_type__ = 'foobar'
    class Bar(Foo): pass

    self.assertEqual(Foo.key_type, 'foobar')
    self.assertEqual(Bar.key_type, 'foobar')


  def test_key_type_inheritance_none_uses_default(self):
    class Foo(Model):
      __key_type__ = 'foobar'
    class Bar(Foo):
      __key_type__ = None
    class Biz(Bar): pass

    self.assertEqual(Foo.key_type, 'foobar')
    self.assertEqual(Bar.key_type, 'bar')
    self.assertEqual(Biz.key_type, 'biz')


  # key tests

  def test_key_is_attr(self):
    self.assertTrue(hasattr(Model, 'key'))


  def test_key_isinstance_Key(self):
    self.assertTrue(isinstance(Model.key, Key))
    self.assertTrue(isinstance(Model('foo').key, Key))


  def test_key_in_class_uses_key_type(self):
    self.assertTrue(Model.key, Key(Model.key_type))


  def test_key_in_instance_uses_attribute(self):
    self.assertTrue(Model('foo').key, Key(Model.key_type).instance('foo'))


  def test_key_validation(self):
    Model('foo')
    Model(Model.key.instance('foo'))
    Model(Key('/model:foo'))
    with self.assertRaises(TypeError):
      Model(Key('/Model:foo'))

  def test_key_validation_with_parent(self):
    Model(Key('/foo:bar/model:foo'))
    self.assertRaises(TypeError, Model, Key('/Foo:bar/Model:foo'))

  def test_key_inheritance(self):
    class Foo(Model): pass
    class Bar(Foo): pass

    self.assertEqual(Foo.key, Key('/foo'))
    self.assertEqual(Bar.key, Key('/bar'))


  def test_key_inheritance_key_type(self):
    class A(Model): __key_type__ = 'aaa'
    class B(A): pass
    class C(B): __key_type__ = None
    class D(C): pass

    self.assertEqual(A.key, Key('/aaa'))
    self.assertEqual(B.key, Key('/aaa'))
    self.assertEqual(C.key, Key('/c'))
    self.assertEqual(D.key, Key('/d'))

    self.assertEqual(A('a1').key, Key('/aaa:a1'))
    self.assertEqual(B('b1').key, Key('/aaa:b1'))
    self.assertEqual(C('c1').key, Key('/c:c1'))
    self.assertEqual(D('d1').key, Key('/d:d1'))


  # updateData tests

  def test_update_data_is_method(self):
    self.assertTrue(hasattr(Model, 'updateData'))
    self.assertTrue(callable(Model.updateData))

  def test_update_data_updates(self):
    data = {'key': '/model:foo', 'foo': 'bar'}
    instance = Model.withData(data)
    self.assertEqual(instance.data, data)

    data2 = {'foo': 'biz', 'bar': 'biz'}
    instance.updateData(data2)

    data.update(data2)
    self.assertEqual(instance.data, data)


  # updateAttributes tests

  def test_update_attributes_is_method(self):
    self.assertTrue(hasattr(Model, 'updateAttributes'))
    self.assertTrue(callable(Model.updateAttributes))

  def test_update_attributes_updates(self):

    class A(Model):
      foo = Attribute()
      bar = Attribute()

    key = '/a:foo'
    data = {'key': key, 'foo': 'bar'}
    instance = A.withData(data)
    self.assertEqual(instance.data, {'key': key, 'foo': 'bar', 'bar':None})

    data2 = {'foo': 'biz', 'bar': 'biz', 'biz': 'baz'}
    instance.updateAttributes(data2)
    self.assertEqual(instance.data, {'key': key, 'foo': 'biz', 'bar':'biz'})

    data3 = {'bar': 'baz', 'biz': 'foo'}
    instance.updateAttributes(data3)
    self.assertEqual(instance.data, {'key': key, 'foo': 'biz', 'bar':'baz'})


  # withData tests

  def test_with_data_is_classmethod(self):
    self.assertTrue(hasattr(Model, 'withData'))
    self.assertTrue(callable(Model.withData))


  def test_with_data_constructs_instance(self):
    instance = Model.withData({'key': '/model:foo'})
    self.assertTrue(isinstance(instance, Model))


  def test_with_data_respects_inheritance(self):
    class Foo(Model): pass
    class Bar(Foo): pass

    self.assertTrue(isinstance(Model.withData({'key': '/model:foo'}), Model))
    self.assertTrue(isinstance(Foo.withData({'key': '/foo:foo'}), Foo))
    self.assertTrue(isinstance(Bar.withData({'key': '/bar:foo'}), Bar))


  def test_with_data_uses_key_attr(self):
    for key in ['/model:foo', '/foo:bar/model:biz', '/a/model:biz']:
      instance = Model.withData({'key': key})
      self.assertEqual(instance.key, Key(key))

    self.assertRaises(TypeError, Model.withData, {'key': '/foo:bar'})
    self.assertRaises(TypeError, Model.withData, {'key': '/model:foo/foo'})
    self.assertRaises(TypeError, Model.withData, {'key': '/model:foo/foo:bar'})


  def test_with_data_uses_name_attr_for_key(self):
    instance = Model.withData({'key': '/model:bar'})
    self.assertEqual(instance.key, Key('/model:bar'))


  def test_with_data_requires_key_attr(self):
    with self.assertRaises(KeyError):
      Model.withData({'foo': 'bar'})


  def test_with_data_assigns_data_attr(self):
    data = {'key': '/model:foo', 'foo': 'bar'}
    instance = Model.withData(data)
    self.assertEqual(instance.data, data)


  # change key_attr

  def test_with_different_key_attr(self):
    class Foo(Model):
      key_attr = 'biz'

    instance = Foo.withData({'biz': '/foo:bar'})
    self.assertEqual(instance.key, Key('/foo:bar'))


  # str/repr tests

  def test_str(self):
    class Foo(Model): pass

    instance = Foo.withData({'key': '/foo:bar', 'foo': 'bar'})
    self.assertEqual(str(instance), '<Foo /foo:bar>')


  def test_repr(self):
    class Foo(Model): pass

    data = {'key': '/foo:bar', 'foo': 'bar'}
    instance = Foo.withData(data)
    self.assertEqual(repr(instance), 'Foo.withData(%s)' % data)





if __name__ == '__main__':
  unittest.main()
