# Copyright (C) 2014 by Kevin L. Mitchell <klmitch@mit.edu>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see
# <http://www.gnu.org/licenses/>.

import abc
import sys

import six

# Need the MutableMapping class from collections for FramerState
if sys.version_info >= (3, 3):
    from collections.abc import MutableMapping
else:
    from collections import MutableMapping


@six.add_metaclass(abc.ABCMeta)
class Framer(object):
    """
    An abstract base class for framers.  Framers are responsible for
    transforming between streams of bytes and individual frames,
    through the ``to_frame()`` and ``to_bytes()`` methods.  These
    methods receive an instance of ``FramerState``, which will be
    initialized by a call to the ``initialize_state()`` method.
    """

    def initialize_state(self, state):
        """
        Initialize a ``FramerState`` object.  This state will be
        passed in to the ``to_frame()`` and ``to_bytes()`` methods,
        and may be used for processing partial frames or cross-frame
        information.  The default implementation does nothing.

        :param state: The state to initialize.
        """

        pass

    @abc.abstractmethod
    def to_frame(self, data, state):
        """
        Extract a single frame from the data buffer.  The consumed
        data should be removed from the buffer.  If no complete frame
        can be read, must raise a ``NoFrames`` exception.

        :param data: A ``bytearray`` instance containing the data so
                     far read.
        :param state: An instance of ``FramerState``.  If the buffer
                      contains a partial frame, this object can be
                      used to store state information to allow the
                      remainder of the frame to be read.

        :returns: A frame.  The frame may be any object.  The stock
                  framers always return ``bytes`` objects.
        """

        pass

    @abc.abstractmethod
    def to_bytes(self, frame, state):
        """
        Convert a single frame into bytes that can be transmitted on
        the stream.

        :param frame: The frame to convert.  Should be the same type
                      of object returned by ``to_frame()``.
        :param state: An instance of ``FramerState``.  This object may
                      be used to track information across calls to the
                      method.

        :returns: Bytes that may be transmitted on the stream.
        """

        pass


class FramerState(MutableMapping):
    """
    Maintains state for framers.  This object may be used to store
    relevant data when a framer has consumed a part of a frame from
    the receive buffer.  It may also be used, if desired, for the
    send-side framer.  Data is stored as attributes; attribute names
    beginning with '_' are reserved.
    """

    def __init__(self):
        """
        Initialize a ``FramerState`` object.
        """

        self._data = {}

    def __getattr__(self, name):
        """
        Retrieve a state attribute.

        :param name: The name of the attribute to retrieve.

        :returns: The value of the state attribute.
        """

        # Get the data from the data dictionary
        try:
            return self._data[name]
        except KeyError:
            raise AttributeError("'%s' object has no attribute '%s'" %
                                 (self.__class__.__name__, name))

    def __getitem__(self, name):
        """
        Retrieve a state attribute by item access.

        :param name: The name of the attribute to retrieve.

        :returns: The value of the state attribute.
        """

        # Retrieve the data from the data dictionary
        return self._data[name]

    def __setattr__(self, name, value):
        """
        Set a state attribute.

        :param name: The name of the attribute to set.
        :param value: The desired value of the attribute.
        """

        # Attributes with a leading '_' are normal attributes
        if name[0] == '_':
            return super(FramerState, self).__setattr__(name, value)

        self._data[name] = value

    def __setitem__(self, name, value):
        """
        Set a state attribute by item access.

        :param name: The name of the attribute to set.
        :param value: The desired value of the attribute.
        """

        # Attributes with a leading '_' are special
        if name[0] == '_':
            raise KeyError(name)

        self._data[name] = value

    def __delattr__(self, name):
        """
        Delete a state attribute.

        :param name: The name of the attribute to delete.
        """

        # Attributes with a leading '_' are normal attributes
        if name[0] == '_':
            return super(FramerState, self).__delattr__(name)

        try:
            del self._data[name]
        except KeyError:
            raise AttributeError("'%s' object has no attribute '%s'" %
                                 (self.__class__.__name__, name))

    def __delitem__(self, name):
        """
        Delete a state attribute by item access.

        :param name: The name of the attribute to delete.
        """

        # Attributes with a leading '_' are special
        if name[0] == '_':
            raise KeyError(name)

        del self._data[name]

    def __iter__(self):
        """
        Obtain an iterator over all declared state attributes.

        :returns: An iterator over the state attribute names.
        """

        return six.iterkeys(self._data)

    def __len__(self):
        """
        Obtain the length of the state--that is, the number of
        declared state attributes.

        :returns: The number of state attributes.
        """

        return len(self._data)
