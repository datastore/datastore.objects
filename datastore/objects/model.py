from datastore import Key
from .util import classproperty
from .attribute_metaclass import AttributeMetaclass




class Model(object):
  '''Implements a basic model with keys. It uses a per-class (or per-instance)
  ObjectManager to save and fetch its values.
  '''

  __metaclass__ = AttributeMetaclass


  # name of the key attribute in model data
  key_attr = 'key'


  def __init__(self, keyOrName):
    self._set_data({})
    self._set_key(keyOrName)

    # set defaults into data

  def _set_data(self, data):
    '''Sets internal data, including defaults.'''
    self.data = data


    # update data with defaults
    attrs = self._attributes.values()
    defaults = [(attr.name, attr.default_value()) for attr in attrs]
    self.updateData(dict(defaults))


  def _set_key(self, keyOrName):
    '''validates keyOrName and sets internal key'''
    if isinstance(keyOrName, Key):
      key = keyOrName
    elif isinstance(keyOrName, basestring):
      key = self.__class__.key.instance(str(keyOrName))
    else:
      err = 'key must be of type %s, not %s'
      raise TypeError(err % (Key, keyOrName.__class__))

    if key.type != self.__class__.key.name:
      raise TypeError('key.type should be %s' % self.__class__.key.name)

    self._key = key
    self.data[self.key_attr] = str(key)


  def __getattr__(self, _name):
    '''Redirects Attribute._attr_raw_get to the `data` dictionary.'''

    # Attribute raw names start with _
    if not _name.startswith('_'):
      return super(Model, self).__getattribute__(_name)

    name = _name.lstrip('_')

    # if it's not an Attribute, proceed as normal.
    if name not in self._attributes:
      return super(Model, self).__getattribute__(_name)

    # it's an Attribute, set it to the `data` dictionary
    if name in self.data:
      return self.data[name]
    else:
      raise AttributeError


  def __setattr__(self, _name, value):
    '''Redirects Attribute._attr_raw_set to the `data` dictionary.'''

    # Attribute raw names start with _
    if not _name.startswith('_'):
      return super(Model, self).__setattr__(_name, value)

    name = _name.lstrip('_')

    # if it's not an Attribute, proceed as normal.
    if name not in self._attributes:
      return super(Model, self).__setattr__(_name, value)

    self.data[name] = value


  def __repr__(self):
    return '%s.withData(%s)' % (self.__class__.__name__, self.data)

  def __str__(self):
    return '<%s %s>' % (self.__class__.__name__, self.key)


  @classproperty
  def key_type(cls):
    '''The key type associated with this model/instance.
    This is a classproperty in order to have:

        >>> Model.key_type
        model
    '''
    # ensure cls is not instance (classproperty)
    if not isinstance(cls, type):
      cls = cls.__class__

    key_type = getattr(cls, '__key_type__', None)
    if not key_type:
      key_type = cls.__name__.lower()
    return key_type


  @classproperty
  def key(cls_or_self):
    '''The key associated with this model/instance.
    This is a classproperty in order to have:

        >>> Model.key
        Key('/Model')
        >>> Model('instance').key
        Key('/Model:instance)

    '''
    if isinstance(cls_or_self, type):
      return Key(cls_or_self.key_type)
    return cls_or_self._key


  def updateData(self, data):
    self.data.update(data)


  def updateAttributes(self, data):
    if self.key_attr in data:
      key = data[self.key_attr]
      self._set_key(key)

    for key in self._attributes.keys():
      if key in data:
        setattr(self, key, data[key])


  @classmethod
  def withData(cls, data):
    '''Constructs a version of this model with given data'''
    key = data[cls.key_attr]
    instance = cls(Key(key))
    instance.updateData(data)
    return instance
