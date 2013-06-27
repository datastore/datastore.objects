import copy
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

  def __init__(self, *args, **kwargs):
    model = kwargs.pop('model', None)
    if model:
      self.model = model

    super(ObjectDatastore, self).__init__(*args, **kwargs)


  def get(self, key):
    data = super(ObjectDatastore, self).get(key)
    if data and isinstance(data, dict) and 'key' in data:
      data = copy.deepcopy(data)
      return self.model.withData(data)
    return data


  def put(self, key, value):
    if isinstance(value, self.model):
      value = copy.deepcopy(value.data)
    super(ObjectDatastore, self).put(key, value)


  def query(self, query):
    '''disable query access'''
    results = super(ObjectDatastore, self).query(query)
    return self.model_instance_gen(results)


  def model_instance_gen(self, iterable):
    '''Yields model instances from an iterable of data'''
    for data in iterable:
      yield self.model.withData(data)
