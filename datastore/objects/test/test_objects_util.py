import json
import pickle
import unittest

from .. import util
from ..util import classproperty


class TestUtilClassproperty(unittest.TestCase):

  def test_exists(self):
    self.assertTrue(hasattr(util, 'classproperty'))


  def test_is_class(self):
    self.assertTrue(isinstance(classproperty, type))


  def test_stores_getter_function(self):
    foo = lambda: 'foo'
    cp = classproperty(foo)
    self.assertEqual(cp.getter(), foo())
    self.assertEqual(cp.getter, foo)


  def test_get_without_instance(self):
    class Foo(object):
      pass

    bar = lambda x: x

    cp = classproperty(bar)
    self.assertTrue(cp.__get__(None, Foo), bar(Foo))
    self.assertTrue(cp.__get__(None, Foo), Foo)


  def test_get_with_instance(self):
    class Foo(object):
      pass

    bar = lambda x: x

    cp = classproperty(bar)
    foo = Foo()
    self.assertTrue(cp.__get__(foo, Foo), bar(foo))
    self.assertTrue(cp.__get__(foo, Foo), foo)


  def test_method_use(self):

    class Foo(object):
      bar = lambda cls_or_self: cls_or_self
      bar = classproperty(bar)

    foo = Foo()
    self.assertTrue(Foo.bar, Foo)
    self.assertTrue(foo.bar, foo)


  def test_decorator_use(self):

    class Foo(object):
      @classproperty
      def bar(cls_or_self):
        return cls_or_self

    foo = Foo()
    self.assertTrue(Foo.bar, Foo)
    self.assertTrue(foo.bar, foo)


if __name__ == '__main__':
  unittest.main()
