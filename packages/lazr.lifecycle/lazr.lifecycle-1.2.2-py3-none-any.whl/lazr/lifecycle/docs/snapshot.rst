Get a Snapshot of an Object
---------------------------

The lazr.lifecycle.event.ObjectModifiedEvent has an attribute giving the
initial state of the object before the modifications. The Snapshot class can
be used to easily represent such states:

    >>> from zope.interface import Attribute, Interface, implementer
    >>> from zope.schema import List, TextLine, Text
    >>> from lazr.lifecycle.snapshot import doNotSnapshot, Snapshot

    >>> class IFoo(Interface):
    ...     title = TextLine(title=u'My Title')
    ...     description = Text(title=u'Description')
    ...     remotes = List(title=u'remotes')
    ...     totals = Attribute('totals')
    ...     ignore_me = doNotSnapshot(Attribute('ignored attribute'))

    >>> @implementer(IFoo)
    ... class Foo:
    ...     remotes = ["OK"]
    ...
    ...     @property
    ...     def totals(self):
    ...         return "NOT"
    >>> foo = Foo()
    >>> foo.title = 'Some Title'
    >>> foo.description = 'bla bla bla'

A snapshot can be created by specifying the names of the attribute you want to
snapshot:

    >>> snapshot = Snapshot(foo, names=['title'])

Only the given attributes will be assigned to the snapshot:

    >>> snapshot.title == foo.title
    True
    >>> hasattr(snapshot, 'description')
    False

The snapshot won't provide the same interface as foo, though:

    >>> IFoo.providedBy(snapshot)
    False

If we want the snapshot to provide some interface, we have to specify
that explicitly:

    >>> snapshot = Snapshot(foo, names=['title'], providing=IFoo)
    >>> snapshot.title == foo.title
    True
    >>> hasattr(snapshot, 'description')
    False
    >>> IFoo.providedBy(snapshot)
    True

The API requires you to specify either 'names' or 'providing':

    >>> snapshot = Snapshot(foo) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    SnapshotCreationError

If no names argument is supplied, the snapshot will contain all
IFields of the specified interface(s).

    >>> snapshot = Snapshot(foo, providing=IFoo)
    >>> snapshot.title == foo.title
    True
    >>> hasattr(snapshot, 'description')
    True

Totals is not a Fields so isn't copied over.

    >>> hasattr(snapshot, 'totals')
    False
    >>> hasattr(snapshot, 'remotes')
    True
    >>> snapshot.remotes == ["OK"]
    True

Fields can be explicitly ignored if they provide the IDoNotSnapshot
interface.

    >>> hasattr(snapshot, 'ignore_me')
    False

We can also give more than one interface to provide as an iterable. If
we don't specify any names, all the names in the given interfaces will
be copied:

    >>> from zope.interface import providedBy
    >>> snapshot = Snapshot(foo, providing=providedBy(foo))
    >>> snapshot.title == foo.title
    True
    >>> snapshot.description == foo.description
    True
    >>> IFoo.providedBy(snapshot)
    True

    >>> class IBar(Interface):
    ...     name = Text(title=u'Name')

    >>> foo.name = "barbie"

    >>> snapshot = Snapshot(foo, providing=[IFoo, IBar])
    >>> IFoo.providedBy(snapshot)
    True
    >>> IBar.providedBy(snapshot)
    True

    >>> snapshot.title == foo.title
    True
    >>> snapshot.name == "barbie"
    True
    >>> snapshot.description == foo.description
    True
    >>> IFoo.providedBy(snapshot)
    True
    >>> IBar.providedBy(snapshot)
    True


ISnapshotValueFactory
---------------------

For some fields, assigning the existing value to the snapshot object
isn't appropriate. For these case, one can provide a factory registered
as an adapter for the value to ISnapshotValueFactory. The result of the
adaptation lookup will be stored in the snapshot attribute.

    >>> from zope.interface import implementer, Interface
    >>> from zope.component import adapter, getSiteManager

    >>> class IIterable(Interface):
    ...     """Marker for a value that needs a special snapshot."""

    >>> @implementer(IIterable)
    ... class EvenOrOddIterable:
    ...     """An object that will be snapshotted specially."""
    ...     even = True
    ...     max = 10
    ...
    ...     def __iter__(self):
    ...         for i in range(self.max):
    ...             if i % 2  == 0 and self.even:
    ...                 yield i
    ...             elif i % 2  == 1 and not self.even:
    ...                 yield i
    ...             else:
    ...                 continue

    >>> from lazr.lifecycle.interfaces import ISnapshotValueFactory
    >>> @implementer(ISnapshotValueFactory)
    ... @adapter(IIterable)
    ... def snapshot_iterable(value):
    ...     return list(value)
    >>> getSiteManager().registerAdapter(snapshot_iterable)

    >>> foo = Foo()
    >>> foo.title = 'Even'
    >>> foo.description = 'Generates even number below 10.'
    >>> foo.remotes = EvenOrOddIterable()

    >>> snapshot = Snapshot(foo, providing=IFoo)
    >>> snapshot.remotes == list(foo.remotes)
    True

    >>> getSiteManager().unregisterAdapter(snapshot_iterable)
    True
