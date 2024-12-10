LAZR lifecycle
**************

This package defines three "lifecycle" events that notify about object
creation, modification and deletion. The events include information about the
user responsible for the changes.

The modification event also includes information about the state of the object
before the changes.

The module also contains snapshot support to save the state of an object for
notification, and to compute deltas between version of objects.
