# datastore.objects

[`datastore.objects`](https://github.com/datastore/datastore.objects) is a
simple *object mapper* on top of
[`datastore`](https://github.com/jbenet/datastore) (not relational). Thanks to
datastore's versatility, it makes it easy to (serialize and) persist custom
classes to any sort of data storage service.

Notice: please familiarize yourself with `datastore` first.

## Install


    pip install datastore.objects


## Interface

### Key

`datastore.objects` uses the default `datastore.Key`, making significant use
of the `type` and `instance` fragments.

```python
>>> from datastore.objects import Key, Model
>>> class Scientist(Model):
>>>   pass
>>> Scientist.key
Key('/Scientist')
>>> Scientist('Tesla').key
Key('/Scientist:Tesla')
```


### Model

`datastore.objects` provides a class that you inherit from to define your
models. datastore.objects.Model handles the datastore serializing and
deserializing, attribute validation, etc.

```python
>>> from datastore.objects import Model
>>> class Scientist(Model):
>>>   pass
```


### Attribute

`datastore.objects` uses descriptor Attributes to track the properties you wish
to store. This is heavily based on how other python ORMs (django, app engine)
do it. In short, you define model attributes like this:


```python
>>> from datastore.objects import Attribute, Model
>>> class Scientist(Model):
>>>   name = Attribute(required=True)
>>>   field = Attribute(default='Physics')
>>> tesla = Scientist('Tesla')
>>> tesla.name = 'Nicola Tesla'
>>> tesla.field
'Physics'
>>> tesla.field = 'Electrical Engineering'
>>> tesla.data
{'name': 'Nicola Tesla', 'field': 'Electrical Engineering'}
```

### ObjectDatastore

`datastore.objects` provides a `ShimDatastore` that wraps any other datastore.
Thus you can use any of the various datastores to persist your objects.
`ObjectDatastore` makes sure to serialize (on put) and deserialize (on get)
data properly, and construct your classes.

```python
>>> import datastore
>>> from datastore.objects import Attribute, Model, ObjectDatastore
>>>
>>> class Scientist(Model):
>>>   name = Attribute(required=True)
>>>   field = Attribute(default='Physics')
>>>
>>> tesla = Scientist('Tesla')
>>> tesla.name = 'Tesla'
>>> tesla.field = 'Electrical Engineering'
>>>
>>> dds = datastore.DictDatastore()
>>> ods = ObjectDatastore(dds, model=Scientist)
>>> ods.put(tesla.key, tesla)
>>> dds.get(tesla.key)
{'name': 'Tesla', 'field': 'Electrical Engineering'}
>>> ods.get(tesla.key)
<Model /Scientist:Tesla>
```


## About

#### Author

`datastore.objects` is written by [Juan Batiz-Benet](https://github.com/jbenet),
of [Athena](http://athena.ai).

#### License

It is free open-source software, available under
the MIT License.

#### Contact

Project webpage: https://github.com/datastore/datastore.objects.
Issues: https://github.com/jbenet/object-datastore/issues
