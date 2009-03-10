class Field(object):
    """Fields implement constraints on ConfigObj instances, and rigidly define
    what is and is not exposed to an application. In almost every case, a Field
    will be entirely transparent to an application.
    
    A ConfigObj class shares one instance of a Field among all its instances,
    as well as from the class itself. The ConfigObj is responsible for setting
    the values of _name and _owner, so trying to use a Field instance that
    hasn't been bound to a ConfigObj class will usually fail.
    
    >>> class C1(ConfigObj):
    ...     field = Field()
    ...
    >>> str(C1.field) 
    "C1.field <class 'Field'>"
    >>> c1 = C1()

    Fields are initialized to None, but by default will not allow you to set
    them back to None - or to an empty string, for that matter.
    >>> c1.field
    >>> c1.field = None
    Traceback (most recent call last):
        ...
    ValueError: C1.field <class 'Field'> cannot be null.
    >>> c1.field = ''
    Traceback (most recent call last):
        ...
    ValueError: C1.field <class 'Field'> cannot be blank.

    Of course, that behavior is configurable:
    >>> class C2(ConfigObj):
    ...    field = Field(default = 'hi', blank = True, null = True)
    ...
    >>> c2 = C2()
    >>> c2.field
    'hi'
    >>> c2.field = ''
    >>> c2.field = None

    Defaults should be validated, too.
    >>> class C3(ConfigObj):
    ...     field = Field(default = '', blank = False)
    ...
    Traceback (most recent call last):
        ...
    ValueError: C3.field <class 'Field'> cannot be blank.
    """

    def __init__(self, blank = False, null = False, default = None):
        """Creates a Field instance. Subclasses may extend this method."""

        self._blank = blank
        self._null = null
        self._default = default
                
        # The name of the field in the owning ConfigObj.
        self._name = None
        # A reference to the owning ConfigObj class.
        self._owner = None

    # Make Field.default read-only
    @property
    def default(self):
        return self._default

    def _postinit(self, name, owner):
        """Called by the ConfigObj class to which this instance is bound. We
        defer default validation until here, but this all happens behind the
        __init__ method, so the user doesn't know the difference."""
        self._name = name
        self._owner = owner
        if self._default is not None:
            self._default = self.validate(self._default)

    def __get__(self, instance, owner):
        if not issubclass(owner, self._owner):
            raise AttributeError('Fields must be bound to ConfigObj classes.')

        # Follow the pattern documented in ConfigObj class 
        if instance is None:
            return self
        else:
            return instance.__dict__[self._name]

    def __set__(self, instance, value):
        if not self._owner:
            raise AttributeError('Fields must be bound to ConfigObj classes.')

        instance.__dict__[self._name] = self.validate(value)

    def validate(self, value):
        """Takes a value and ensures it meets some characteristic. This is
        called immediately upon variable assignment. This method should only
        validate the immediate value, and should not attempt to do
        introspection against the ConfigObj which owns the Field instance.
        
        Returns the validated value. Conversion to a new type is permissible,
        as long as the returned value and validate(str(value)) are equivalent."""

        if value is None and not self._null:
            raise ValueError('%s cannot be null.'  % (str(self)))
        if value is '' and not self._blank:
            raise ValueError('%s cannot be blank.' % (str(self)))

        return value

    def _serialize(self, instance, owner):
        """Returns a canonical representation of the contents. In most cases
        this will be simply the string representation of 'value', but in some
        cases more complex types are justified. Keep it JSON-compatible."""
        val = instance.__dict__[self._name]
        if val is None: return None
        return str(val)
        
    def __str__(self):
        return "%s.%s <class '%s" % (self._owner.__name__, self._name, 
                                     str(type(self)).split('.')[-1])

class EnumField(Field):
    """Validates that the input is equal to one of the items in an iterable.
    
    Please note that blank=True is not supported for this method.

    >>> class C1(ConfigObj):
    ...     type_choices = ('a', 'b', 'c')
    ...     type = EnumField(type_choices)
    ...
    >>> c1 = C1()
    >>> c1.type = C1.type_choices[1]
    >>> c1.type = 'b'
    >>> c1.type = 'd'
    Traceback (most recent call last):
        ...
    ValueError: Given value not equal to any valid choice.
    >>> c1.type
    'b'
    >>> c1.type = None
    Traceback (most recent call last):
        ...
    ValueError: C1.type <class 'EnumField'> cannot be null.

    >>> class C2(ConfigObj):
    ...     type = EnumField( [1, 2, 3], blank = True)
    ...
    Traceback (most recent call last):
        ...
    ValueError: EnumField with blank = True not supported.


    >>> class C3(ConfigObj):
    ...     type = EnumField( [1, 2, 3], null = True)
    ...
    >>> c3 = C3()
    >>> c3.type
    >>> c3.type = 1
    >>> c3.type
    1
    >>> c3.type = None
    >>> c3.type

    >>> class C4(ConfigObj):
    ...     type = EnumField( () )
    ...
    Traceback (most recent call last):
        ...
    ValueError: Value of 'choices' cannot be zero-length.

    >>> class C5(ConfigObj):
    ...     type = EnumField(6)
    ...
    Traceback (most recent call last):
        ...
    TypeError: Value of 'choices' must be iterable.

    """

    def __init__(self, choices, **kwargs):
        if kwargs.get('blank'):
            raise ValueError('EnumField with blank = True not supported.')

        try:
            if len(choices) == 0:
                raise ValueError("Value of 'choices' cannot be zero-length.")
        except TypeError:
            raise TypeError("Value of 'choices' must be iterable.")

        self.choices = choices
        super(EnumField, self).__init__(**kwargs)

    def validate(self, value):
        value = super(EnumField, self).validate(value)
        if value is None: return None

        if value not in self.choices: 
            raise ValueError("Given value not equal to any valid choice.")
        return value

class ForeignObjField(Field):
    """References an instance of a ConfigObj class.
    
    >>> class C1(ConfigObj): # generic example class 
    ...     field = Field()
    ...
    >>> c1a = C1()
    >>> c1a.field = 'C1 A'
    >>> c1b = C1()
    >>> c1b.field = 'C1 B'

    Works pretty much like you'd expect.
    >>> class C2(ConfigObj): 
    ...     ref = ForeignObjField(C1) 
    >>> c2 = C2()
    >>> c2.ref = c1a
    >>> c2.ref.field
    'C1 A'
    >>> c2.ref = c1b
    >>> c2.ref.field
    'C1 B'
    >>> c2.ref = c2
    Traceback (most recent call last):
        ...
    TypeError: <...C2 object at ...> is not an instance of <class '...C1'>.

    Of course, this will only store instances of a type:
    >>> c2.ref = C1
    Traceback (most recent call last):
        ...
    TypeError: <class '...C1'> is not an instance of <class '...C1'>.
    
    Inheritance works how you'd expect, as well:
    >>> class C1Child(C1): pass
    >>> c1c = C1Child()
    >>> c1c.field = 'C1 Child'
    >>> c2.ref = c1c
    >>> c2.ref.field
    'C1 Child'

    It's possible to do self-reference, too; for now, this has no form of
    cycle-checking, so you can have unbounded recursion on serialization. Avoid
    cycles for now; a cycle-checker may be added in the future and it will
    default to 'on'. 
    
    Note that to do self-reference, you must pass the class name in as a
    string. This defers lookup until validation, which means that the class
    being refered to has to be in the namespace when the validator is used for
    the first time. Making this work proved harder than I thought, and I'm
    deferring support for this until after a workable version ships.
    """
    # TODO: re=add this doctest, and make it work
    #>>> class C3(ConfigObj):
    #...     self_ref = ForeignObjField('C3')
    #...
    #>>> c3 = C3()
    #>>> c3.self_ref = c3
    #>>> c3.serialize() # Don't do this.
    
    def __init__(self, foreign_class, **kwargs):

        if isinstance(foreign_class, str):
            self.fc_name = foreign_class
            self.foreign_class = None
        elif issubclass(foreign_class, ConfigObj):
            self.foreign_class = foreign_class
        else:
            raise TypeError('foreign_class must be a ConfigObj class.')
    
        super(ForeignObjField, self).__init__(**kwargs)

    def validate(self, value):
        value = super(ForeignObjField, self).validate(value)
        if value is None: return None
        
        if not self.foreign_class:
            try:
                fc = eval(self.fc_name, globals())
            except:
                raise #TypeError("Could not resolve '%s'." % self.fc_name)
            if not issubclass(fc, ConfigObj):
                raise TypeError("'%s' does not resolve to a ConfigObj class." %
                                self.fc_name)
            self.foreign_class = fc
        
        if not isinstance(value, self.foreign_class):
            raise TypeError('%s is not an instance of %s.' % 
                            (value, self.foreign_class))
        
        return value

    def _serialize(self, instance, owner):
        inst = self.__dict__[self._name]
        if inst is None: return None
        return inst.serialize()

#class TupleFieldMixIn(object):
#    """Allows a field to store a tuple of the underlying types. Validator args
#    are those of the underlying validator; the MixIn reads an extra arg called
#    'empty' which defines whether zero-length tuples are allowed.

#    >>> class TupleField(Field, TupleFieldMixIn): pass
#    >>> class C(ConfigObj):
#    ...     field = TupleField(blank = True)
#    ...
#    >>> c = C()
#    >>> c.fleid = ('tuple', 'values')
#    >>> c.field 

#    Of course, validators still work. This passes, because we set 
#    'blank = True' in the field declaration:
#    >>> c.field = ('validators', 'still', 'work', '')
#    >>> c.field
#    
#    This doesn't, because null is still at False (the default):
#    >>> c.field = ('and still throw', None)
#    >>> c.field = ['works', 'over', 'any', 'iterable']
#    
#    Bonus: works over any iterable (although always *returns* a tuple).
#    >>> c.field = ['shallow', 'copies', 'into', 'a', 'tuple']
#    >>> c.field

#    Zero-length values are distinct from None. While zero-length tuples can be
#    allowed via... define later
#    >>> c.field = None
#    >>> c.field = ()
#    >>> class C2(ConfigObj):
#    ...     field = TupleField(empty = True)
#    ...
#    >>> c2 = C2()
#    >>> c2.field = ()
#    >>> c2.field

#    TODO: finish, obviously.
#    """
#    pass
    

class ConfigObj:
    """This class provides the framework for obtaining and saving information
    about a running system and its static configuration.

    At this time, ConfigObj will not 

    """
    
    class __metaclass__(type):
        def __new__(mcs, name, bases, dict):
            # Scan for bound Field instances, and run _postinit on them. Extra
            # instrospection could happen here, but probably doesn't need to.
            class_inst = type.__new__(mcs, name, bases, dict)
            for (k, v) in dict.items():
                if isinstance(v, Field):
                    v._postinit(k, class_inst)
                    dict[k] = v
            return class_inst
    
    @property
    def _fields(self):
        return ( (k, v) for k, v in type(self).__dict__.items() \
                        if isinstance(v, Field) )

    def __init__(self, **kwargs):
        """Creates an object. Initializes all field values to the default value
        of the field.
        
        TODO: Currently, unused kwargs are discarded. When all optional kwargs
        have been decided on, come back and make unrecognized ones fail."""

        for (k, v) in self._fields:
            if k in kwargs:
                self.__dict__[k] = v.validate(kwargs[k])
            self.__dict__[k] = v.default

    def serialize(self):
        """Serializes the object to a dict. 
        
        Note that this method does not do any kind of cycle detection, even
        1-level. It's generally sensible to avoid cycles with ConfigObj,
        though.""" 
                
        ret = {}

        for (name, field) in inst._fields:
            ret[name] = field.serialze(self, type(self))

        return ret

    
    # Subclasses must also implement get() and save() for now.

if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags = doctest.ELLIPSIS |
                                  doctest.REPORT_ONLY_FIRST_FAILURE)

