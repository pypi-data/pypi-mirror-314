LAZR Lifecycle Events
=====================

lazr.lifecycle defines common lifecycle events. They are extensions of the
base Z3 lifecycle events.


    >>> from lazr.lifecycle.interfaces import (
    ...     IObjectCreatedEvent, IObjectModifiedEvent,
    ...     IObjectDeletedEvent)
    >>> from lazr.lifecycle.event import (
    ...     ObjectCreatedEvent, ObjectDeletedEvent, ObjectModifiedEvent)

    >>> from zope.interface.verify import verifyObject

    >>> class Fnord:
    ...     "A Fnort sighting."""
    ...
    ...     def __init__(self, who, where):
    ...         self.who = who
    ...         self.where = where

The module defines three lifecycle events:

    * ObjectCreatedEvent - Used when an object has been created.

    * ObjectModifiedEvent - Used then an object has been modified, it
      provides meta data explaining what was modified.

    * ObjectDeletedEvent - Used when the object was deleted.

All events expose the user responsible for the change in the user
attribute. By default, if not specified when constructing the event,
this will be the principal associated with the interaction. (Only one
principal is currently supported)

    >>> from zope.security.management import (
    ...     newInteraction, endInteraction)

    >>> class MyParticipation:
    ...     def __init__(self, who):
    ...         self.principal = who
    ...         self.interaction = None

    >>> newInteraction(MyParticipation('the user'))

    >>> fnord = Fnord('me', 'the_bridge')
    >>> created_event = ObjectCreatedEvent(fnord)
    >>> verifyObject(IObjectCreatedEvent, created_event)
    True

    >>> print(created_event.user)
    the user

The object attribute contains the object that was created:

    >>> created_event.object is fnord
    True

The ObjectModifiedEvent holds the names of the modified fields in the
'edited_fields' attribute and the state of the object before the
modifications in 'object_before_modification' attribute. (See
snapshot.txt for a way to manage that easily).

    >>> snapshot = Fnord('me', 'the_bridge')
    >>> fnord.who = 'someone else'

    >>> modified_event = ObjectModifiedEvent(fnord, snapshot, ['who'])

    >>> verifyObject(IObjectModifiedEvent, modified_event)
    True

    >>> modified_event.edited_fields
    ['who']
    >>> modified_event.object is fnord
    True
    >>> print(modified_event.object_before_modification.who)
    me
    >>> print(modified_event.user)
    the user

The ObjectDeletedEvent is used to broadcast the deletion of the object.

    >>> deleted_event = ObjectDeletedEvent(fnord, user='the_censor')

    >>> verifyObject(IObjectDeletedEvent, deleted_event)
    True

    >>> deleted_event.object is fnord
    True
    >>> print(deleted_event.user)
    the_censor
