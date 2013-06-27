from datastore.core import SymlinkDatastore
from datastore.core import DirectoryDatastore

from .model import Model
from .model import Key


class Collection(object):
  '''Implements a simple persistent collection of objects.

  It uses symlink and directory datastores to keep track of the items.
  '''

  Model = Model

  def __init__(self, key, datastore, Model=None):
    self.key = key
    self.datastore = datastore
    self.symlink_datastore = SymlinkDatastore(datastore)
    self.directory_datastore = DirectoryDatastore(self.symlink_datastore)


  @property
  def keys(self):
    return self.directory_datastore.directoryRead(self.key)


  @property
  def instances(self):
    instances_data = self.instance_data_generator()
    for data in instances_data:
      yield self.Model.withData(data)


  def add(self, instance_key):
    if not isinstance(instance_key, Key):
      instance_key = instance_key.key

    collection_instance_key = self.key.instance(instance_key.name)

    # add symlink
    if instance_key != collection_instance_key:
      self.symlink_datastore.link(instance_key, collection_instance_key)

    # add to collection
    self.directory_datastore.directoryAdd(self.key, collection_instance_key)


  def remove(self, instance_key):
    if not isinstance(instance_key, Key):
      instance_key = instance_key.key

    collection_instance_key = self.key.instance(instance_key.name)

    # remove symlink/delete entry
    self.symlink_datastore.delete(collection_instance_key)

    # remove from collection list
    self.directory_datastore.directoryRemove(self.key, collection_instance_key)


  def instance_data_generator(self):
    '''
    Generator that returns all the data of all the instances.
    (Can override this to parallelize the access).
    '''
    for key in self.keys:
      yield self.directory_datastore.get(key)
