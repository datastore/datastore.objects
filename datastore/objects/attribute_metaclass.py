from .attribute import Attribute



class DuplicateAttributeError(ValueError):
  pass



class AttributeMetaclass(type):
  '''Metaclass to initialize attributes in a class.

  It ensures that attributes do not clash,
  '''

  def __init__(cls, name, bases, attrs):
    super(AttributeMetaclass, cls).__init__(name, bases, attrs)
    cls._initialize_attributes(name, bases, attrs)


  def _initialize_attributes(cls, name, bases, attrs):
    '''This function initializes attributes (and handles name collisions).
    Attribute binding follows the model that property binding does in
    dronestore and in Google App Engine.
    '''

    cls._attributes = {}
    defined_attrs = {}

    def get_attr_source(cls, attr):
      '''walks the bases to find which class added the given attr.'''
      for src_cls  in cls.mro():
        if attr in src_cls.__dict__:
          return src_cls


    def verify_attr_source_match(attr_name, base, defined_attrs):
      '''ensures attr_name in base is the same as that in `defined_attrs`'''
      old_source = defined_attrs[attr_name]
      new_source = get_attr_source(base, attr_name)
      if old_source is not new_source:
        raise DuplicateAttributeError(
            'Duplicate attribute: %s is inherited from both %s and %s.' %
            (attr_name, old_source.__name__, new_source.__name__))


    def get_attrs_from_base(cls, base, defined_attrs):
      '''Gathers all the attributes from given `base`, in `defined_attrs`'''
      if not hasattr(base, '_attributes'):
        return

      keys = set(base._attributes.keys())
      attr_names = set(defined_attrs.keys()) & keys
      for attr_name in attr_names:
        verify_attr_source_match(attr_name, base, defined_attrs)

      keys -= attr_names
      if keys:
        defined_attrs.update(dict.fromkeys(keys, base))
        cls._attributes.update(base._attributes)


    def add_attr(cls, attr_name, attr, defined_attrs):
      '''Adds given `attr` to `cls._attributes`, checking for collissions.'''
      if not isinstance(attr, Attribute):
        return

      if attr_name in defined_attrs:
        raise DuplicateAttributeError(
          'Duplicate attribute: %s is already defined in %s' %
            (attr_name, defined_attrs[attr_name]))

      defined_attrs[attr_name] = cls
      cls._attributes[attr_name] = attr

      # configure attribute
      attr._attr_config(cls, attr_name)


    # Gather all the attributes from all the bases.
    for base in bases:
      get_attrs_from_base(cls, base, defined_attrs)

    # add the ds attributes from this class.
    for attr_name, attr in attrs.items():
      add_attr(cls, attr_name, attr, defined_attrs)
