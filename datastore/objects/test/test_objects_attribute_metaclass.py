import json
import pickle
import unittest

from .. import attribute_metaclass
from ..attribute_metaclass import AttributeMetaclass
from ..attribute_metaclass import DuplicateAttributeError
from ..attribute import Attribute




class TestAttributeMetaclass(unittest.TestCase):

  def test_exists(self):
    self.assertTrue(hasattr(attribute_metaclass, 'AttributeMetaclass'))


  def test_duplicate_attribute_error_exists(self):
    self.assertTrue(hasattr(attribute_metaclass, 'DuplicateAttributeError'))
    self.assertTrue(issubclass(DuplicateAttributeError, ValueError))


  def test_is_class(self):
    self.assertTrue(isinstance(AttributeMetaclass, type))


  def test_is_type(self):
    self.assertTrue(issubclass(AttributeMetaclass, type))


  def test_model1_has_empty_attributes_map(self):
    class Model(object):
      __metaclass__ = AttributeMetaclass

    self.assertTrue(hasattr(Model, '_attributes'))
    self.assertTrue(isinstance(Model._attributes, dict))
    self.assertTrue(len(Model._attributes) is 0)

  def test_cls_has_attribute(self):
    class Model(object):
      __metaclass__ = AttributeMetaclass
      foo = Attribute()

    self.assertTrue(len(Model._attributes) is 1)
    self.assertTrue(isinstance(Model._attributes['foo'], Attribute))

  def test_sets_attribute_name_if_none(self):
    class Model(object):
      __metaclass__ = AttributeMetaclass
      foo = Attribute()

    self.assertEqual(Model._attributes['foo'].name, 'foo')

  def test_respects_attr_name_if_not_none(self):
    class Model(object):
      __metaclass__ = AttributeMetaclass
      foo = Attribute(name='bar')

    self.assertEqual(Model._attributes['foo'].name, 'bar')


  def test_cls_inherits_attributes(self):
    class Model1(object):
      __metaclass__ = AttributeMetaclass
      foo = Attribute()

    class Model2(Model1):
      pass

    self.assertEqual(Model1._attributes, Model2._attributes)


  def test_cls_inheriting_and_defining_attributes(self):
    class Model1(object):
      __metaclass__ = AttributeMetaclass
      foo = Attribute()

    class Model2(Model1):
      bar = Attribute()

    self.assertTrue('foo' in Model2._attributes)
    self.assertTrue('bar' in Model2._attributes)


  def test_detects_inheritance_name_clash(self):
    class Model1(object):
      __metaclass__ = AttributeMetaclass
      foo = Attribute()

    with self.assertRaises(DuplicateAttributeError):
      class Model2(Model1):
        foo = Attribute()

  def test_detects_inheritance_name_clash_across_long_chain(self):
    class Model1(object):
      __metaclass__ = AttributeMetaclass
      foo = Attribute()

    class Model2(Model1): pass
    class Model3(object): pass
    class Model4(Model3, Model2): pass

    with self.assertRaises(DuplicateAttributeError):
      class Model5(Model4):
        foo = Attribute()

  def test_detects_inheritance_name_clash_in_different_parents(self):
    class Model1(object):
      __metaclass__ = AttributeMetaclass
      foo = Attribute()

    class Model2(object):
      __metaclass__ = AttributeMetaclass
      foo = Attribute()

    with self.assertRaises(DuplicateAttributeError):
      class Model3(Model1, Model2): pass




if __name__ == '__main__':
  unittest.main()
