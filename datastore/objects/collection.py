import datastore

from .model import Model


class ObjectDatastore(datastore.ShimDatastore):
  '''Implements a simple persistent collection of objects.

  It is a ShimDatastore to provide the datastore interface, and use a
  child_datastore to persist serialized object data.

  It is also heavily inspired by Backbone Model and Collection, in order to
  keep similar semantics in both backend and frontend.
  '''

  model = Model

  def get(self, key):
    data = super(Collection, self).get(key)
    return self.model.withData(data) if data else None

  def put(self, key, instance):
    super(Collection, self).put(instance.data)

  def query(self):
    '''disable query access'''
    raise NotImplemented
