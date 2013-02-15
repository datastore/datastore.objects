import unittest
import datastore

from ... import objects


class TestObjects(unittest.TestCase):

  def test_has_Key(self):
    self.assertTrue(hasattr(objects, 'Key'))

  def test_has_model(self):
    self.assertTrue(hasattr(objects, 'Model'))

  def test_has_object_datastore(self):
    self.assertTrue(hasattr(objects, 'ObjectDatastore'))

  def test_has_classproperty(self):
    self.assertTrue(hasattr(objects, 'classproperty'))

  def test_has_attribute(self):
    self.assertTrue(hasattr(objects, 'Attribute'))

  def test_has_attribute_metaclass(self):
    self.assertTrue(hasattr(objects, 'AttributeMetaclass'))

  def test_has_duplicate_attribute_error(self):
    self.assertTrue(hasattr(objects, 'DuplicateAttributeError'))

  def test_has_manager(self):
    self.assertTrue(hasattr(objects, 'Manager'))


if __name__ == '__main__':
  unittest.main()
