import datetime
import difflib
import pickle

from builtins import int
from collections import namedtuple
from collections.abc import Iterable, MutableMapping
from decimal import Decimal
from itertools import zip_longest

from fild.process.common import is_callable_with_strict_args


strings = (str, bytes)  # which are both basestring
numbers = (int, float, complex, datetime.datetime, datetime.date, Decimal)
items = 'items'  # pylint: disable=C0103
IndexedHash = namedtuple('IndexedHash', 'index item')


class ListItemRemovedOrAdded:

    """Class of conditions to be checked"""


INDEX_VS_ATTRIBUTE = ('[%s]', '.%s')


class DeepDiff(dict):
    """
    **DeepDiff v 1.1.0**

    Deep Difference of dictionaries, iterables, strings and almost any other
    object.
    It will recursively look for all the changes.

    **Parameters**

    t1 : A dictionary, list, string or any python object that has __dict__
        or __slots__
        This is the first item to be compared to the second item

    t2 : dictionary, list, string or almost any python object that has
        __dict__ or __slots__
        The second item is to be compared to the first one

    ignore_order : Boolean, defalt=False ignores orders for iterables.
        Note that if you have iterables contatining any unhashable,
        ignoring order can be expensive.
        Ignoring order for an iterable containing any unhashable
        will include duplicates if there are any in the iterable.
        Ignoring order for an iterable containing only hashables
        will not include duplicates in the iterable.

    **Returns**

        A DeepDiff object that has already calculated the difference of the 2
        items.

    **Supported data types**

    int, string, unicode, dictionary, list, tuple, set, frozenset, OrderedDict,
    NamedTuple and custom objects!

    **Examples**

    Importing
        >>> from deepdiff import DeepDiff
        >>> from pprint import pprint

    Same object returns empty
        >>> t1 = {1:1, 2:2, 3:3}
        >>> t2 = t1
        >>> print(DeepDiff(t1, t2))
        {}

    Type of an item has changed
        >>> t1 = {1:1, 2:2, 3:3}
        >>> t2 = {1:1, 2:"2", 3:3}
        >>> pprint(DeepDiff(t1, t2), indent=2)
        { 'type_changes': { 'root[2]': { 'new_type': <class 'str'>,
                                         'new_value': '2',
                                         'old_type': <class 'int'>,
                                         'old_value': 2}}}

    Value of an item has changed
        >>> t1 = {1:1, 2:2, 3:3}
        >>> t2 = {1:1, 2:4, 3:3}
        >>> pprint(DeepDiff(t1, t2), indent=2)
        {'values_changed': {'root[2]': {'new_value': 4, 'old_value': 2}}}

    Item added and/or removed
        >>> t1 = {1:1, 2:2, 3:3, 4:4}
        >>> t2 = {1:1, 2:4, 3:3, 5:5, 6:6}
        >>> ddiff = DeepDiff(t1, t2)
        >>> pprint (ddiff)
        {'dictionary_item_added': ['root[5]', 'root[6]'],
         'dictionary_item_removed': ['root[4]'],
         'values_changed': {'root[2]': {'new_value': 4, 'old_value': 2}}}

    String difference
        >>> t1 = {1:1, 2:2, 3:3, 4:{"a":"hello", "b":"world"}}
        >>> t2 = {1:1, 2:4, 3:3, 4:{"a":"hello", "b":"world!"}}
        >>> ddiff = DeepDiff(t1, t2)
        >>> pprint (ddiff, indent = 2)
        { 'values_changed': { 'root[2]': {'new_value': 4, 'old_value': 2},
                              "root[4]['b']": { 'new_value': 'world!',
                                                'old_value': 'world'}}}

    List difference
        >>> t1 = {1:1, 2:2, 3:3, 4:{"a":"hello", "b":[1, 2, 3, 4]}}
        >>> t2 = {1:1, 2:2, 3:3, 4:{"a":"hello", "b":[1, 2]}}
        >>> ddiff = DeepDiff(t1, t2)
        >>> pprint (ddiff, indent = 2)
        {'iterable_item_removed': {"root[4]['b'][2]": 3, "root[4]['b'][3]": 4}}

    List difference 2:
        >>> t1 = {1:1, 2:2, 3:3, 4:{"a":"hello", "b":[1, 2, 3]}}
        >>> t2 = {1:1, 2:2, 3:3, 4:{"a":"hello", "b":[1, 3, 2, 3]}}
        >>> ddiff = DeepDiff(t1, t2)
        >>> pprint (ddiff, indent = 2)
        {'iterable_item_added': {"root[4]['b'][1]": 3}}

    List difference ignoring order or duplicates: (with the same dictionaries as above)
        >>> t1 = {1:1, 2:2, 3:3, 4:{"a":"hello", "b":[1, 2, 3]}}
        >>> t2 = {1:1, 2:2, 3:3, 4:{"a":"hello", "b":[1, 3, 2, 3]}}
        >>> ddiff = DeepDiff(t1, t2, ignore_order=True)
        >>> print (ddiff)
        {}

    List that contains dictionary:
        >>> t1 = {1:1, 2:2, 3:3, 4:{"a":"hello", "b":[1, 2, {1:1, 2:2}]}}
        >>> t2 = {1:1, 2:2, 3:3, 4:{"a":"hello", "b":[1, 2, {1:3}]}}
        >>> ddiff = DeepDiff(t1, t2)
        >>> pprint (ddiff, indent = 2)
        { 'dictionary_item_removed': ["root[4]['b'][2][2]"],
          'values_changed': {"root[4]['b'][2][1]": {'new_value': 3, 'old_value': 1}}}


    Dictionary extended:
        >>> t1 = {1:1, 2:2}
        >>> t2 = {1:1, 2:2, 3:3}
        >>> ddiff = DeepDiff(t1, t2)
        >>> pprint (ddiff, indent = 2)
        {'dictionary_item_added': ['root[3]']}


    Named Tuples:
        >>> from collections import namedtuple
        >>> Point = namedtuple('Point', ['x', 'y'])
        >>> t1 = Point(x=11, y=22)
        >>> t2 = Point(x=11, y=23)
        >>> pprint (DeepDiff(t1, t2))
        {'values_changed': {'root.y': {'new_value': 23, 'old_value': 22}}}

    Custom objects:
        >>> class ClassA(object):
        ...     a = 1
        ...     def __init__(self, b):
        ...         self.b = b
        ...
        >>> t1 = ClassA(1)
        >>> t2 = ClassA(2)
        >>>
        >>> pprint(DeepDiff(t1, t2))
        {'values_changed': {'root.b': {'new_value': 2, 'old_value': 1}}}

    Object attribute added:
        >>> t2.c = "new attribute"
        >>> pprint(DeepDiff(t1, t2))
        {'attribute_added': ['root.c'],
         'values_changed': {'root.b': {'new_value': 2, 'old_value': 1}}}
    """

    def __init__(self, t1, t2, rules=None, ignore_order=False,
                 forbid_unapplied_rules=True):
        super().__init__()
        self.ignore_order = ignore_order
        self.forbid_unapplied_rules = forbid_unapplied_rules

        self.update({
            'type_changes': {},
            'dict_item_added': set([]),
            'dict_item_removed': set([]),
            'values_changed': {},
            'unprocessed': [],
            'iterable_item_added': {},
            'iterable_item_removed': {},
            'attribute_added': set([]),
            'attribute_removed': set([]),
            'set_item_removed': set([]),
            'set_item_added': set([]),
            'rules_violated': {},
            'unapplied_rules': {}
        })

        self.__diff(t1, t2, parents_ids=frozenset({id(t1)}), rules=rules)
        empty_keys = [k for k, v in getattr(self, items)() if not v]

        for k in empty_keys:
            del self[k]

    @staticmethod
    def __extend_result_list(keys, parent, result_obj, print_as_attribute=False):  # pylint: disable=unused-argument
        key_text = f'{INDEX_VS_ATTRIBUTE[print_as_attribute]}{{}}'

        for i in keys:
            i = f"'{i}'" if not print_as_attribute and isinstance(i, strings) else i
            result_obj.add(key_text % (i))

    def __diff_obj(self, t1, t2, parent, parents_ids=frozenset({})):
        """Difference of 2 objects"""
        try:
            t1 = t1.__dict__
            t2 = t2.__dict__
        except AttributeError:
            try:
                t1 = {i: getattr(t1, i) for i in t1.__slots__}
                t2 = {i: getattr(t2, i) for i in t2.__slots__}
            except AttributeError:
                self['unprocessed'].append(f'%{parent}: %{t1} and %{t2}')
                return

        self.__diff_dict(t1, t2, parent, parents_ids, print_as_attribute=True)

    def __diff_dict(self, t1, t2, parent, parents_ids=frozenset({}),
                    print_as_attribute=False, rules=None):
        """Difference of 2 dictionaries"""
        if print_as_attribute:
            item_added_key = 'attribute_added'
            item_removed_key = 'attribute_removed'
            parent_text = '%s.%s'
        else:
            item_added_key = 'dict_item_added'
            item_removed_key = 'dict_item_removed'
            parent_text = '%s[%s]'

        rules = rules or {}
        t1_keys = set(t1.keys())
        t2_keys = set(t2.keys())

        t_keys_intersect = t2_keys.intersection(t1_keys)

        t_keys_added = t2_keys - t_keys_intersect
        t_keys_removed = t1_keys - t_keys_intersect

        if self.forbid_unapplied_rules:
            for key, rule in rules.items():
                if key not in t1_keys and key not in t2_keys:
                    self['unapplied_rules'][f"{parent}['{key}']"] = str(rule)

        if t_keys_added:
            self.__extend_result_list(
                keys=t_keys_added,
                parent=parent,
                result_obj=self[item_added_key],
                print_as_attribute=print_as_attribute
            )

        if t_keys_removed:
            self.__extend_result_list(
                keys=t_keys_removed,
                parent=parent,
                result_obj=self[item_removed_key],
                print_as_attribute=print_as_attribute
            )

        self.__diff_common_children(
            t1, t2, t_keys_intersect, print_as_attribute, parents_ids, parent,
            parent_text, rules=rules
        )

    def __diff_common_children(
            self, t1, t2, t_keys_intersect, print_as_attribute, parents_ids,
            parent, parent_text, rules=None):
        """
        Difference between common attributes of objects or values of
        common keys of dictionaries
        """
        for item_key in t_keys_intersect:
            if not print_as_attribute and isinstance(item_key, strings):
                item_key_str = f"'{item_key}'"
            else:
                item_key_str = item_key

            t1_child = t1[item_key]
            t2_child = t2[item_key]
            rules_child = rules.get(item_key)

            item_id = id(t1_child)

            if parents_ids and item_id in parents_ids:
                continue

            parents_added = set(parents_ids)
            parents_added.add(item_id)
            parents_added = frozenset(parents_added)

            self.__diff(t1_child, t2_child, rules=rules_child,
                        parent=parent_text % (parent, item_key_str),
                        parents_ids=parents_added)

    def __diff_set(self, t1, t2, parent='root'):
        """Difference of sets"""
        items_added = list(t2 - t1)
        items_removed = list(t1 - t2)

        if items_removed:
            self.__extend_result_list(
                keys=items_removed,
                parent=parent,
                result_obj=self['set_item_removed']
            )

        if items_added:
            self.__extend_result_list(
                keys=items_added,
                parent=parent,
                result_obj=self['set_item_added']
            )

    def __diff_iterable(self, t1, t2, parent='root', parents_ids=frozenset({}),
                        rules=None):
        """Difference of iterables except dictionaries, sets and strings."""
        rules = rules or [None]
        items_removed = {}
        items_added = {}

        for i, (x, y) in enumerate(zip_longest(t1, t2, fillvalue=ListItemRemovedOrAdded)):
            key = f'{parent}[{i}]'
            if y is ListItemRemovedOrAdded:
                items_removed[key] = x
            elif x is ListItemRemovedOrAdded:
                items_added[key] = y
            else:
                self.__diff(x, y, key, parents_ids, rules=rules[0])

        self['iterable_item_removed'].update(items_removed)
        self['iterable_item_added'].update(items_added)

    def __diff_str(self, t1, t2, parent):
        """Compare strings"""
        if '\n' in t1 or '\n' in t2:
            diff = difflib.unified_diff(
                t1.splitlines(), t2.splitlines(), lineterm='')
            diff = list(diff)
            if diff:
                diff = '\n'.join(diff)
                self['values_changed'][parent] = {
                    'oldvalue': t1, 'newvalue': t2, 'diff': diff
                }
        elif t1 != t2:
            self['values_changed'][parent] = {'oldvalue': t1, 'newvalue': t2}

    def __diff_tuple(self, t1, t2, parent, parents_ids):
        # Checking to see if it has _fields. Which probably means it is a named
        # tuple.
        try:
            t1._fields
        # It must be a normal tuple
        except AttributeError:
            self.__diff_iterable(t1, t2, parent, parents_ids)
        # We assume it is a namedtuple then
        else:
            self.__diff_obj(t1, t2, parent, parents_ids)

    @staticmethod
    def __create_hashtable(t, parent):
        """Create hashtable of {item_hash: item}"""
        hashes = {}
        for (i, item) in enumerate(t):
            try:
                item_hash = hash(item)
            except TypeError:
                try:
                    item_hash = hash(pickle.dumps(item))
                except Exception as e:  # pylint: disable=W0703
                    print(
                        f'Warning: Can not produce a hash for {item} item '
                        f'in {parent} and thus not counting this object. {e}'
                    )
                else:
                    hashes[item_hash] = IndexedHash(i, item)
            else:
                hashes[item_hash] = IndexedHash(i, item)
        return hashes

    def __diff_unhashable_iterable(self, t1, t2, parent):
        """Diff of unhashable iterables. Only used when ignoring the order."""
        t1_hashtable = self.__create_hashtable(t1, parent)
        t2_hashtable = self.__create_hashtable(t2, parent)

        t1_hashes = set(t1_hashtable.keys())
        t2_hashes = set(t2_hashtable.keys())

        hashes_added = t2_hashes - t1_hashes
        hashes_removed = t1_hashes - t2_hashes

        items_added = {
            f'{parent}[{t2_hashtable[hash_value].index}]':
                t2_hashtable[hash_value].item for hash_value in hashes_added
        }

        items_removed = {
            f'{parent}[{t1_hashtable[hash_value].index}]':
                t1_hashtable[hash_value].item for hash_value in hashes_removed
        }

        self['iterable_item_removed'].update(items_removed)
        self['iterable_item_added'].update(items_added)

    def __diff(self, t1, t2, parent='root', parents_ids=frozenset({}),
               rules=None):
        """The main diff method"""
        if is_callable_with_strict_args(rules, args_count=2):
            if not rules(t1, t2):
                self['rules_violated'][parent] = {
                    'rule': str(rules), 'oldvalue': t1, 'newvalue': t2
                }

        elif t1 is t2:
            return

        elif not isinstance(t1, type(t2)):
            self['type_changes'][parent] = {
                'oldvalue': t1, 'newvalue': t2,
                'oldtype': type(t1), 'newtype': type(t2)
            }

        elif isinstance(t1, strings):
            if rules is not None:
                self['unapplied_rules'][parent] = str(rules)
            else:
                self.__diff_str(t1, t2, parent)

        elif isinstance(t1, numbers):
            if rules is not None:
                self['unapplied_rules'][parent] = str(rules)
            elif t1 != t2:
                self['values_changed'][parent] = {
                    'oldvalue': t1, 'newvalue': t2
                }

        elif isinstance(t1, MutableMapping):
            self.__diff_dict(t1, t2, parent, parents_ids, rules=rules)

        elif isinstance(t1, tuple):
            self.__diff_tuple(t1, t2, parent, parents_ids)

        elif isinstance(t1, (set, frozenset)):
            self.__diff_set(t1, t2, parent=parent)

        elif isinstance(t1, Iterable):
            if self.ignore_order:
                try:
                    t1 = set(t1)
                    t2 = set(t2)
                # When we can't make a set since the iterable has unhashable
                # items
                except TypeError:
                    self.__diff_unhashable_iterable(t1, t2, parent)
                else:
                    self.__diff_set(t1, t2, parent=parent)
            else:
                self.__diff_iterable(t1, t2, parent, parents_ids, rules=rules)

        else:
            self.__diff_obj(t1, t2, parent, parents_ids)

        return



if __name__ == '__main__':
    import doctest
    doctest.testmod()
