from .model import Key
from .manager import Manager
from .collection import Collection


class CollectionManager(Manager):
  '''Collection manager for model instances.'''


  # the collection class to use
  Collection = Collection


  def key(self, key_or_name):
    '''Overrides Manager.key'''
    if not isinstance(key_or_name, Key):
      return self.collection_key.instance(key_or_name)

    return key_or_name


  @property
  def collection_key(self):
    '''Returns the collection key that corresponds to this manager'''
    return self.model.key


  @property
  def collection(self):
    '''Returns the collection that corresponds to this manager.'''
    return self.Collection(self.collection_key, self.datastore)


  @property
  def instances(self):
    return self.collection.instances


  def put(self, instance):
    '''Stores given `instance` and adds it to the collection'''
    super(CollectionManager, self).put(instance)
    self.collection.add(instance)


  def delete(self, key):
    '''Deletes `instance` named by `key` and removes it from collection.'''
    self.collection.remove(key)
    super(CollectionManager, self).delete(key)
