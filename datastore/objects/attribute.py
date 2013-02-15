from datastore.core.serialize import NonSerializer



class Attribute(object):
  '''Implements a simple __get__ __set__ based attribute.

  An Attribute primarily defines a name and a data type.

  Attributes can have other options, including defining a default value, and
  validation for the data they hold.

  This is adapted from dronestore.attribute. See:
  https://github.com/jbenet/py-dronestore/blob/master/dronestore/attribute.py
  '''

  data_type = str


  def __init__(self, name=None, default=None, required=False, data_type=str,
      serializer=None):
    self.name = name
    self.default = default
    self.required = bool(required)
    self.data_type = data_type
    self.serializer = serializer if serializer else NonSerializer


  def _attr_raw_get(self, instance, name, default=None):
    '''gets the raw attribute value.'''
    if not name:
      raise AttributeError('attribute name is required')
    return getattr(instance, '_%s' % name, default)


  def _attr_raw_set(self, instance, name, value):
    '''Sets the raw attribute value.'''
    if not name:
      raise AttributeError('attribute name is required')
    setattr(instance, '_%s' % name, value)


  def _attr_config(self, model_class, attr_name):
    '''Configure attribute for a given model.

       This function is useful to be called when setting up attributes as
       members of a class, for example from a meta class.
    '''
    self.__model__ = model_class
    if self.name is None:
      self.name = attr_name


  def is_empty_value(self, value):
    '''Simple check to determine if value is empty.'''
    return value is None


  def default_value(self):
    '''The default value for a particular attribute.'''
    return self.default


  def type_coerced_value(self, value):
    '''Attempts to convert invalid value types to the proper type.'''
    if self.is_empty_value(value):
      return value

    if isinstance(value, self.data_type):
      return value

    try:
      return self.data_type(value)
    except:
      err = 'value for attribute %s is of incompatible type %s, must be %s'
      raise TypeError(err % (self.name, type(value), self.data_type))


  def validated_value(self, value):
    '''Asserts that provided value is compatible with this attribute.
       Returns a validated version of the value.
    '''
    if self.is_empty_value(value) and self.required:
      raise ValueError('Attribute %s is required.' % self.name)

    return value


  def __get__(self, instance, model_class):
    '''Descriptor to aid model instantiation.'''
    value = self._attr_raw_get(instance, self.name)

    if self.is_empty_value(value):
      value = self.default_value()

    return self.serializer.loads(value)


  def __set__(self, instance, value, validate=True):
    '''Validate and Set the attribute on the model instance.'''

    # coerce invalid value types
    value = self.type_coerced_value(value)

    if validate:
      value = self.validated_value(value)

    # serialized
    value = self.serializer.dumps(value)

    # set on the instance data
    self._attr_raw_set(instance, self.name, value)
