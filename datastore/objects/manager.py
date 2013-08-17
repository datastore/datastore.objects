from .model import Key
from .model import Model
from datastore import Query
from .object_datastore import ObjectDatastore


class Manager(object):
  '''Simplified manager for model instances.'''

  model = Model

  def __init__(self, datastore, model=None):
    if model:
      self.model = model

    self.datastore = ObjectDatastore(datastore, model=self.model)


  def key(self, key_or_name):
    '''Coerces `key_or_name` to be a proper model Key'''
    if not isinstance(key_or_name, Key):
      return self.model.key.instance(key_or_name)

    if key_or_name.type != self.model.key.name:
      err = 'key %s must have key type %s'
      raise TypeError(err % (key_or_name, self.model.key.name))

    return key_or_name


  # simplified datastore api

  def contains(self, key):
    '''Returns whether manager contains instance named by `key_or_name`.'''
    return self.datastore.contains(self.key(key))


  def get(self, key):
    '''Retrieves instance named by `key_or_name`.'''
    return self.datastore.get(self.key(key))


  def put(self, instance):
    '''Stores given `instance`.'''
    if not isinstance(instance, self.model):
      raise TypeError('%s must be of type %s' % (instance, self.model))

    self.datastore.put(instance.key, instance)


  def delete(self, key_or_name):
    '''Deletes instance named by `key_or_name`.'''
    self.datastore.delete(self.key(key_or_name))


  def init_query(self):
    '''Initiates a Query object for the model'''
    if not self.model:
      raise Exception('Can not query when no model is set on the manager')
    return Query(Key('/' + self.model.key_type))


  def query(self, query):
    '''Execute a query on the underlying datastore'''
    return self.datastore.query(query)


  def remove_all_items(self):
    '''Removes all items from the datastore'''
    for obj in self.query(self.init_query()):
      self.delete(obj.key)