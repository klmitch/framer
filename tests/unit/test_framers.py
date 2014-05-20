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

import unittest

import mock

from framer import exc
from framer import framers


class FramerStateTest(unittest.TestCase):
    def test_init(self):
        state = framers.FramerState()

        self.assertEqual(state._data, {})

    def test_getattr_available(self):
        state = framers.FramerState()
        state._data['test'] = 'value'

        self.assertEqual(state.test, 'value')

    def test_getattr_unavailable(self):
        state = framers.FramerState()
        state._data['test'] = 'value'

        self.assertRaises(AttributeError, lambda: state.other)

    def test_getitem_available(self):
        state = framers.FramerState()
        state._data['test'] = 'value'

        self.assertEqual(state['test'], 'value')

    def test_getitem_unavailable(self):
        state = framers.FramerState()
        state._data['test'] = 'value'

        self.assertRaises(KeyError, lambda: state['other'])

    def test_setattr_internal(self):
        state = framers.FramerState()

        state._attr = 'value'

        self.assertFalse('_attr' in state._data)
        self.assertTrue('_attr' in state.__dict__)
        self.assertEqual(state.__dict__['_attr'], 'value')

    def test_setattr_normal(self):
        state = framers.FramerState()

        state.attr = 'value'

        self.assertTrue('attr' in state._data)
        self.assertEqual(state._data, {'attr': 'value'})
        self.assertFalse('attr' in state.__dict__)

    def test_setitem_internal(self):
        state = framers.FramerState()

        def setter():
            state['_attr'] = 'value'

        self.assertRaises(KeyError, setter)
        self.assertFalse('_attr' in state.__dict__)
        self.assertFalse('_attr' in state._data)

    def test_setitem_normal(self):
        state = framers.FramerState()

        state['attr'] = 'value'

        self.assertEqual(state._data, {'attr': 'value'})

    def test_delattr_internal(self):
        state = framers.FramerState()
        state._attr = 'value'

        del state._attr

        self.assertFalse('_attr' in state.__dict__)

    def test_delattr_exists(self):
        state = framers.FramerState()
        state._data['attr'] = 'value'

        del state.attr

        self.assertEqual(state._data, {})

    def test_delattr_missing(self):
        state = framers.FramerState()

        def deleter():
            del state.attr

        self.assertRaises(AttributeError, deleter)

    def test_delitem_internal(self):
        state = framers.FramerState()
        state._data['_attr'] = 'value'

        def deleter():
            del state['_attr']

        self.assertRaises(KeyError, deleter)

    def test_delitem_exists(self):
        state = framers.FramerState()
        state._data['attr'] = 'value'

        del state['attr']

        self.assertEqual(state._data, {})

    def test_delitem_missing(self):
        state = framers.FramerState()

        def deleter():
            del state['attr']

        self.assertRaises(KeyError, deleter)

    def test_iter(self):
        state = framers.FramerState()
        state._data = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 4,
        }

        result = set(iter(state))

        self.assertEqual(result, set('abcd'))

    def test_len(self):
        state = framers.FramerState()
        state._data = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 4,
        }

        self.assertEqual(len(state), 4)
