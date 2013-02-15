import json
import pickle
import unittest

from datastore.core.serialize import NonSerializer

from .. import attribute
from ..attribute import Attribute


class Object(object):
  '''Need to subclass object to be able to add attributes'''


class TestAttribute(unittest.TestCase):

  def test_exists(self):
    self.assertTrue(hasattr(attribute, 'Attribute'))


  def test_is_class(self):
    self.assertTrue(isinstance(Attribute, type))


  # construction tests

  def test_construct_bare(self):
    a = Attribute()
    self.assertEqual(a.name, None)
    self.assertEqual(a.default, None)
    self.assertEqual(a.required, False)
    self.assertEqual(a.data_type, str)
    self.assertEqual(a.serializer, NonSerializer)

  def test_construct_with_values(self):
    a = Attribute(name='foo', default='bar', required='yay', data_type=int,
      serializer=json)
    self.assertEqual(a.name, 'foo')
    self.assertEqual(a.default, 'bar')
    self.assertEqual(a.required, True)
    self.assertEqual(a.data_type, int)
    self.assertEqual(a.serializer, json)


  # attr raw get/set

  def test_attr_raw_get_default(self):
    m = Object()
    a = Attribute()
    self.assertEqual(a._attr_raw_get(m, 'foo'), None)
    self.assertEqual(a._attr_raw_get(m, 'foo', 'biz'), 'biz')

  def test_attr_raw_get_value(self):
    m = Object()
    a = Attribute()
    m._foo = 'bar'
    self.assertEqual(a._attr_raw_get(m, 'foo'), 'bar')
    self.assertEqual(a._attr_raw_get(m, 'foo', 'biz'), 'bar')

  def test_attr_raw_set_value(self):
    m = Object()
    a = Attribute()
    a._attr_raw_set(m, 'foo', 'bar')
    self.assertEqual(m._foo, 'bar')


  # attr raw get/set as class members

  def test_attr_raw_get_default(self):
    class Foo(object):
      foo = Attribute(name='foo')

    m = Foo()
    a = m.__class__.__dict__['foo']
    self.assertEqual(a._attr_raw_get(m, 'foo'), None)
    self.assertEqual(a._attr_raw_get(m, 'foo', 'biz'), 'biz')

  def test_attr_raw_get_value(self):
    class Foo(object):
      foo = Attribute(name='foo')

    m = Foo()
    m._foo = 'bar'
    a = m.__class__.__dict__['foo']
    self.assertEqual(a._attr_raw_get(m, 'foo'), 'bar')
    self.assertEqual(a._attr_raw_get(m, 'foo', 'biz'), 'bar')

  def test_attr_raw_set_value(self):
    class Foo(object):
      foo = Attribute(name='foo')

    m = Foo()
    a = m.__class__.__dict__['foo']
    a._attr_raw_set(m, 'foo', 'bar')
    self.assertEqual(m._foo, 'bar')


  # attr config

  def test_attr_config_defines_model(self):
    a = Attribute()
    a._attr_config(Object, 'foo')
    self.assertTrue(a.__model__ is Object)

  def test_attr_config_sets_name_if_none(self):
    a = Attribute()
    a._attr_config(Object, 'foo')
    self.assertEqual(a.name, 'foo')

  def test_attr_config_respects_given_name(self):
    a = Attribute(name='bar')
    a._attr_config(Object, 'foo')
    self.assertEqual(a.name, 'bar')


  # value helpers

  def test_is_empty_value(self):
    a = Attribute()
    self.assertTrue(a.is_empty_value(None))
    self.assertFalse(a.is_empty_value(0))
    self.assertFalse(a.is_empty_value(5))
    self.assertFalse(a.is_empty_value(''))
    self.assertFalse(a.is_empty_value('Foo'))


  def test_default_value(self):
    self.assertEqual(Attribute().default_value(), None)
    self.assertEqual(Attribute(default=0).default_value(), 0)
    self.assertEqual(Attribute(default='').default_value(), '')
    self.assertEqual(Attribute(default='Foo').default_value(), 'Foo')


  def test_type_coerced_value_str(self):
    a = Attribute(data_type=str)
    self.assertEqual(a.data_type, str)
    self.assertEqual(a.type_coerced_value('foo'), 'foo')
    self.assertEqual(a.type_coerced_value(1), '1')
    self.assertEqual(a.type_coerced_value([]), '[]')
    self.assertEqual(a.type_coerced_value({}), '{}')


  def test_type_coerced_value_int(self):
    a = Attribute(data_type=int)
    self.assertEqual(a.data_type, int)
    self.assertEqual(a.type_coerced_value('1'), 1)
    self.assertEqual(a.type_coerced_value(1), 1)


  def test_type_coerced_value_list(self):
    a = Attribute(data_type=list)
    self.assertEqual(a.data_type, list)
    self.assertEqual(a.type_coerced_value('foo'), list('foo'))
    self.assertEqual(a.type_coerced_value([]), [])
    self.assertEqual(a.type_coerced_value({}), [])


  def test_type_coerced_value_ignores_empty_value(self):
    a = Attribute()
    self.assertEqual(a.data_type, str)
    self.assertEqual(a.type_coerced_value(None), None)


  def test_validated_value(self):
    self.assertEqual(Attribute().validated_value('foo'), 'foo')
    self.assertEqual(Attribute(required=True).validated_value('foo'), 'foo')

  def test_validated_value_allows_empty_values(self):
    self.assertEqual(Attribute().validated_value(None), None)

  def test_validated_value_rejects_empty_values_if_required(self):
    with self.assertRaises(ValueError):
      Attribute(required=True).validated_value(None)


  # descriptor __get__ direct

  def test_get_fails_without_name(self):
    with self.assertRaises(AttributeError):
      Attribute().__get__(Object(), Object)


  def test_get_direct(self):
    m = Object()
    a = Attribute(name='foo')
    self.assertEqual(a.__get__(m, Object), None)
    m._foo = 'bar'
    self.assertEqual(a.__get__(m, Object), 'bar')

  def test_get_direct_default(self):
    m = Object()
    a = Attribute(name='foo', default='biz')
    self.assertEqual(a.__get__(m, Object), 'biz')
    m._foo = 'bar'
    self.assertEqual(a.__get__(m, Object), 'bar')

  def test_get_direct_serializer(self):
    m = Object()
    a = Attribute(name='foo', serializer=json)
    m._foo = '"bar"'
    self.assertEqual(a.__get__(m, Object), 'bar')


  # descriptor __get__ cls member

  def test_get_cls_member(self):
    class Foo(object):
      foo = Attribute(name='foo')

    m = Foo()
    self.assertEqual(m.foo, None)
    m._foo = 'bar'
    self.assertEqual(m.foo, 'bar')

  def test_get_cls_member_default(self):
    class Foo(object):
      foo = Attribute(name='foo', default='biz')

    m = Foo()
    self.assertEqual(m.foo, 'biz')
    m._foo = 'bar'
    self.assertEqual(m.foo, 'bar')

  def test_get_cls_member_serializer(self):
    class Foo(object):
      foo = Attribute(name='foo', serializer=json)

    m = Foo()
    m._foo = '"bar"'
    self.assertEqual(m.foo, 'bar')


  # descriptor __set__ direct

  def test_set_fails_without_name(self):
    with self.assertRaises(AttributeError):
      Attribute().__set__(Object(), Object, 'foo')


  def test_set_direct(self):
    m = Object()
    a = Attribute(name='foo')
    a.__set__(m, 'bar')
    self.assertEqual(m._foo, 'bar')

  def test_set_direct_default(self):
    m = Object()
    a = Attribute(name='foo', default='biz')
    a.__set__(m, 'bar')
    self.assertEqual(m._foo, 'bar')

  def test_set_direct_serializer(self):
    m = Object()
    a = Attribute(name='foo', serializer=json)
    a.__set__(m, 'bar')
    self.assertEqual(m._foo, '"bar"')

  def test_set_direct_type_coercion(self):
    m = Object()
    a = Attribute(name='foo')
    a.__set__(m, 5)
    self.assertEqual(m._foo, '5')

  def test_set_direct_type_not_required(self):
    m = Object()
    a = Attribute(name='foo', required=False)
    a.__set__(m, 'bar')
    self.assertEqual(m._foo, 'bar')
    a.__set__(m, None)
    self.assertEqual(m._foo, None)

  def test_set_direct_type_required(self):
    m = Object()
    a = Attribute(name='foo', required=True)
    a.__set__(m, 'bar')
    self.assertEqual(m._foo, 'bar')
    with self.assertRaises(ValueError):
      a.__set__(m, None)


  # descriptor __set__ cls member

  def test_set_cls_member(self):
    class Foo(object):
      foo = Attribute(name='foo')

    m = Foo()
    m.foo = 'bar'
    self.assertEqual(m._foo, 'bar')

  def test_set_cls_member_default(self):
    class Foo(object):
      foo = Attribute(name='foo', default='biz')

    m = Foo()
    m.foo = 'bar'
    self.assertEqual(m._foo, 'bar')

  def test_set_cls_member_serializer(self):
    class Foo(object):
      foo = Attribute(name='foo', serializer=json)

    m = Foo()
    m.foo = 'bar'
    self.assertEqual(m._foo, '"bar"')

  def test_set_cls_member_type_coercion(self):
    class Foo(object):
      foo = Attribute(name='foo')

    m = Foo()
    m.foo = 5
    self.assertEqual(m._foo, '5')

  def test_set_cls_member_type_not_required(self):
    class Foo(object):
      foo = Attribute(name='foo', required=False)

    m = Foo()
    m.foo = 'bar'
    self.assertEqual(m._foo, 'bar')
    m.foo = None
    self.assertEqual(m._foo, None)

  def test_set_cls_member_type_required(self):
    class Foo(object):
      foo = Attribute(name='foo', required=True)

    m = Foo()
    m.foo = 'bar'
    self.assertEqual(m._foo, 'bar')
    with self.assertRaises(ValueError):
      m.foo = None



if __name__ == '__main__':
  unittest.main()
