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
    "C1.field <class '...Field'>"
    >>> c1 = C1()

    Fields are initialized to None, but by default will not allow you to set
    them back to None - or to an empty string, for that matter.
    >>> c1.field
    >>> c1.field = None
    Traceback (most recent call last):
        ...
    ValueError: C1.field <class '...Field'> cannot be null.
    >>> c1.field = ''
    Traceback (most recent call last):
        ...
    ValueError: C1.field <class '...Field'> cannot be blank.

    Of course, that behavior is configurable:
    >>> class C2(ConfigObj):
    ...    field = Field(default = 'hi', blank = True, null = True)
    ...
    >>> c2 = C2()
    >>> c2.field
    'hi'
    >>> c2.field = ''
    >>> c2.field = None
    """

    def __init__(self, blank = False, null = False, default = None):
        """Creates a Field instance. Subclasses may extend this method, and may
        add extra kwargs, but may _not_ add extra positional args."""
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
        """Called by the ConfigObj class to which this instance is bound."""
        self._name = name
        self._owner = owner

    def __get__(self, instance, owner):
        if owner is not self._owner:
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
        
    def __str__(self):
        return '%s.%s %s' % (self._owner.__name__, self._name, str(type(self)))
    
# ConfigObj uses more Python-Fu than I'm normally comfortable allowing, but it
# follows the same design pattern used by most ORMs, so it must be right.
#
# ...right?

class ConfigObj:
    """This class provides the framework for obtaining and saving information
    about a running system and its static configuration.

    TODO: doctests. Most current code is covered by Field's doctests."""
    
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
    def __fields(self):
        # *might* allow this to be public, it depends
        return ( (k, v) for k, v in type(self).__dict__.items() \
                        if isinstance(v, Field) )

    def __init__(self, **kwargs):
        """Creates an object. Initializes all field values to the default value
        of the field.
        
        TODO: Currently, unused kwargs are discarded. When all optional kwargs
        have been decided on, come back and make unrecognized ones fail."""

        for (k, v) in self.__fields:
            if k in kwargs:
                self.__dict__[k] = v.validate(kwargs[k])
            self.__dict__[k] = v.default

class ConfigObjBackend(object):
    """This base class will be inherited by the code which actually loads and
    saves ConfigObj systems.

    In the interests of checking something in, I'm just going to pass here"""
    pass

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags = doctest.ELLIPSIS)

# These classes and comments are from an old version, I'm leaving them in here
# for purposes of explaining my *original* thinking for this first check-in.
# It's changed somewhat, I did the fruitless 'document an idea' rather than
# 'document your code' which I am notorious for (at least in my own head) and
# it didn't get me any farther than it ever has, but the concept shines
# through.
#
# Everything below this comment, inclusive, should be gone in one or two
# check-ins, replaced by real code. 
#
# GAAH there I go again PLANNING IN MY COMMENTS

"""This module provides a mapper between a system's configuration, its state,
and Python objects.

The design is modeled after existing object-relational mappers, most notably
Django's. However, objects which represent information in a relational database
have the benefit of rigidly-defined lifecycles and datatypes. Representations
of a configuration on a running system under user control, however, have no
implicit guarantees about concurrent access. This ORM thus provides only a mild
level of abstraction at the top level, and explicitly exposes the potentially
dynamic nature of the underlying data in a sane way. On the other hand, it does
not take a fully D-BUS-like approach, where objects register callbacks to
receive state-change notifications, because it's designed for a web backend.
"""

class ConfigObjContextManager (object):
    """This class is, at this point, a rather stupid singleton-pattern wrapper
    around a dict which stores another dict. Upon detecting that the stored
    information might be out of sync with the original source of the
    information, the class calls the _load classmethod on its client classes,
    which then refresh the information in their object.

    If real concurrency is ever necessary, or if a more advanced change
    detection method is ever required, this should offer a much simpler path to
    accomplishing the change.

    Did I mention that this was a stupid idea?"""

    _data = {}

    def __init__(self, klass):
        """Call with a class or instance of a class with a _load method before
        you need data from that class."""
        pass
        
class OldConfigObj (object):
    """This class implements a simple mapping resembling an ORM.

    The ConfigObj system isn't intended to be overly complex, or completely
    hide the task of configuring a system; since at this point most of the
    backends will be contributed by the same people who are writing the
    frontends, the main point is to simply provide a clear internal structure
    to what otherwise might become a morass of divergent code.
    """

    @classmethod
    def _load(klass):
        """Here's where all the metaprogramming kicks in. Or would, if we ever
        needed it. For now, this method remains as a reminder that I need to
        make a decision about this."""
        pass

    def __init__(self):
        """Creates a new ConfigObj instance.
        
        This method has no side effects within the system, but unlike most ORMs,
        it may well have side effects within the calling application, such as
        causing an object to be ref'd by an internal table. I'm still working
        on that bit."""

        self._id = None
    
    @property
    def id(self):     
        """The primary distinction between ConfigObj and a real ORM, aside from
        not necessarily having strict relational types, is the fact that the
        information a ConfigObj represents may represent a *current*
        configuration, rather than a saved configuration. In Django's ORM, for
        instance, it is an error to attempt to associate an object by ID with
        another object until the first object is saved in the database,
        whereupon it is given a primary key.  Naturally we don't want to save
        dynamic configuration information just to read it.

        ConfigObj instances must have an 'id' property. If an instance
        represents a persistent configuration that has been saved on the
        system, the 'id' property can be any unique key, but if the instance
        represents information that is read dynamically, 'id' must be None.
        'id' should only be set programmatically at save time or upon reading
        the object from an existing configuration file, and should remain fixed
        across the lifetime of a particular configuration.
        
        It's a compromise; we're aware of that.
        """

        return _id
    
    def save(self):
        """Saves a configuration to the system, whatever that means.

        Although configurations will be read from multiple sources, usually
        only one backend will implement saving a configuration. It is implied
        that saving a configuration makes it ready to use, but it is not
        necessarily true that it makes it active. I'm leaving it up to the
        implementer (probably me) how that is handled for now; it'll be
        standardized on the next pass through the code."""
        
        raise NotImplementedError, \
              '%s does not know how to save itself.' %  type(self)

    def get(self):
        """Gets all instances of a ConfigObj."""

        raise NotImplementedError, \
              '%s is a useless bum of a class.' % type(self)

    def get_by_id(self, id):
        """Gets a particular instance of a ConfigObj."""
        
        if id is None:
            raise ValueError, \
                  "id *can't* be None here, that's kind of the point"

        raise NotImplementedError, \
              '%s is a useless bum of a class.' % type(self)
   

    def delete(self):
        """Deletes an instance of a ConfigObj from the system.  This also means
        rewriting the associated configuration file. No guarantee is made to
        clean up stale references.""" 
        pass


