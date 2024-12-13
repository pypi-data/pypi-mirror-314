# -*- coding: utf-8 -*-
# This file is part of the 'astrophysix' Python package.
#
# Copyright © Commissariat a l'Energie Atomique et aux Energies Alternatives (CEA)
#
#  FREE SOFTWARE LICENCING
#  -----------------------
# This software is governed by the CeCILL license under French law and abiding by the rules of distribution of free
# software. You can use, modify and/or redistribute the software under the terms of the CeCILL license as circulated by
# CEA, CNRS and INRIA at the following URL: "http://www.cecill.info". As a counterpart to the access to the source code
# and rights to copy, modify and redistribute granted by the license, users are provided only with a limited warranty
# and the software's author, the holder of the economic rights, and the successive licensors have only limited
# liability. In this respect, the user's attention is drawn to the risks associated with loading, using, modifying
# and/or developing or reproducing the software by the user in light of its specific status of free software, that may
# mean that it is complicated to manipulate, and that also therefore means that it is reserved for developers and
# experienced professionals having in-depth computer knowledge. Users are therefore encouraged to load and test the
# software's suitability as regards their requirements in conditions enabling the security of their systems and/or data
# to be ensured and, more generally, to use and operate it in the same conditions as regards security. The fact that
# you are presently reading this means that you have had knowledge of the CeCILL license and that you accept its terms.
#
#
# COMMERCIAL SOFTWARE LICENCING
# -----------------------------
# You can obtain this software from CEA under other licencing terms for commercial purposes. For this you will need to
# negotiate a specific contract with a legal representative of CEA.
#
"""
Datatype enum
-------------

.. autoclass:: astrophysix.simdm.utils.DataType
    :members:
    :undoc-members:


Object lists
------------

.. autoclass:: astrophysix.simdm.utils.ObjectList
   :members:
   :no-special-members: __call__
   :exclude-members: add_deletion_handler

"""
from __future__ import unicode_literals  # Python 2 and 3 compatibility
from future.builtins import str, list
import enum
import re
import logging
import numpy as N

from astrophysix.utils import Stringifiable

log = logging.getLogger("astrophysix.simdm")


class DataType(enum.Enum):
    """
    Value data type enum

    Example
    -------
    >>> dt = DataType.INTEGER
    >>> dt.name
    "Integer number"

    """
    BOOLEAN = ('bool', "Boolean")
    COMPLEX = ('comp', "Complex number")
    DATETIME = ('time', "Datetime")
    REAL = ('real', "Real number")
    INTEGER = ('int', "Integer number")
    RATIONAL = ('rat', "Rational number")
    STRING = ('str', "String")

    def __init__(self, key, name):
        self._key = key
        self._name = name

    @property
    def key(self):
        """Data type index key"""
        return self._key

    @property
    def name(self):
        """Data type verbose name"""
        return self._name

    @classmethod
    def from_key(cls, k):
        """
        Parameters
        ----------
        key: :obj:`string`
            data type key

        Returns
        -------
        t: :class:`~astrophysix.simdm.utils.DataType`
            Physics matching the requested key.

        Raises
        ------
        ValueError
            if requested key does not match any physics.

        Example
        -------
            >>> dt = DataType.from_key("rat")
            >>> dt.name
            "Rational number"
            >>> dt2 = DataType.from_key("MY_UNKNOWN_DTYPE")
            ValuerError: No DataType defined with the key 'MY_UNKNOWN_DTYPE'.
        """
        for dt in cls:
            if dt.key == k:
                return dt
        raise ValueError("No DataType defined with the key '{key:s}'.".format(key=k))


class GalacticaValidityCheckMixin(object):
    INVALID_ALIAS_ERROR_MESSAGE = "The alias can contain capital letters, digits and \'_\' only. It must start with " \
                                  "a capital letter and cannot end with a \'_\'."
    VALID_ALIAS_REGEX = re.compile("""^[A-Z]        # First character must be a capital letter
                                      ([A-Z0-9_]*   # Then any capital letter, digit or '_'
                                      [A-Z0-9])?$   # Must ends with a capital letter or a digit""", re.VERBOSE)

    def galactica_validity_check(self, **kwargs):
        """
        Perform validity checks on this instance and eventually log warning messages.

        Parameters
        ----------
        kwargs: :obj:`dict`
            keyword arguments (optional)
        """
        pass

    def galactica_valid_alias(self, alias_value):
        if self.VALID_ALIAS_REGEX.match(alias_value) is None:
            return self.INVALID_ALIAS_ERROR_MESSAGE
        return None


class ObjectList(GalacticaValidityCheckMixin, Stringifiable):
    """
    Generic object list container class

    Parameters
    ----------
    obj_class: :obj:`type`
        base class of the objects that can be added to the list
    index_prop_name: :obj:`string`
        object property name used as a list index
    object_addition_vcheck: :obj:`tuple` (:obj:`callable` validity check method, :obj:`string` added object list property name)
        validity check method to install into an object's object list upon object addition into the list. Default None.
    object_addition_delhandler: :obj:`tuple` (:obj:`callable` deletion handler, :obj:`string` added object list property name)
        deletion handler to install into an object's object list upon object addition into the list. Default None.

    Examples
    --------
        >>> run1 = Simulation(simu_code=arepo, name="Pure-hydro run (isolated galaxy)")
        >>> run2 = Simulation(simu_code=arepo, name="MHD run")
        >>> run3 = project.simulation.add(Simulation(simu_code=arepo, name="Hydro run with BH feedback")
        >>> run4 = Simulation(simu_code=arepo, name="MHD run with BH feedback")
        >>> project.simulation.add(run1)
        >>> project.simulation.add(run2)
        >>> project.simulation.add(run3)
        >>> project.simulation.add(run4, insert_pos=2)  # Insert at position 2, not appendend at the end of the list
        >>> len(project.simulations)
        4
        >>> print(str(project.simulations))
        Simulation list :
        +---+-----------------------------------+-----------------------------------------------+
        | # |              Index                |                          Item                 |
        +---+-----------------------------------+-----------------------------------------------+
        | 0 | Pure-hydro run (isolated galaxy)  | 'Pure-hydro run (isolated galaxy)' simulation |
        +---+-----------------------------------+-----------------------------------------------+
        | 1 | MHD run                           | 'MHD run' simulation                          |
        +---+-----------------------------------+-----------------------------------------------+
        | 2 | MHD run with BH feedback          | 'MHD run with BH feedback' simulation         |
        +---+-----------------------------------+-----------------------------------------------+
        | 3 | Hydro run with BH feedback        | 'Hydro run with BH feedback' simulation       |
        +---+-----------------------------------+-----------------------------------------------+
        >>> run3 is project.simulations[3]  # Search by item position
        True
        >>> project.simulations["MHD run"]  # Search by item index value
        'MHD run' simulation
        >>> del project.simulations[0]
        >>> del project.simulations["MHD run"]
        >>> del project.simulations[run4]
        >>> print(str(project.simulations))
        Simulation list :
        +---+-----------------------------------+-----------------------------------------------+
        | # |              Index                |                          Item                 |
        +---+-----------------------------------+-----------------------------------------------+
        | 0 | Hydro run with BH feedback        | 'Hydro run with BH feedback' simulation       |
        +---+-----------------------------------+-----------------------------------------------+
    """
    def __init__(self, obj_class, index_prop_name, object_addition_vcheck=None, object_addition_delhandler=None):
        super(ObjectList, self).__init__()
        self._list = list()
        self._obj_class = obj_class
        self._index_prop_name = index_prop_name
        self._validity_check_methods = [self._index_unicity_validity_check]
        self._deletion_handlers = []
        if object_addition_vcheck is not None:
            self._propag_obj_add_vc_method, self._added_obj_list_prop_name = object_addition_vcheck
        else:
            self._propag_obj_add_vc_method = None
            self._added_obj_list_prop_name = ""
        if object_addition_delhandler is not None:
            self._propag_obj_add_delhandler, self._added_obj_list_prop_name_dh = object_addition_delhandler
        else:
            self._propag_obj_add_delhandler = None
            self._added_obj_list_prop_name_dh = ""

    def __eq__(self, other):
        """
        Object list comparison method

        Parameters
        ----------
        other: :class:`~astrophysix.simdm.utils.ObjectList`
            other object list to compare to
        """
        # Object classes differ => not equal
        if self._obj_class != other.object_class:
            return False

        # Indexing property differ => not equal
        if self._index_prop_name != other.index_attribute_name:
            return False

        # List lengths differ => not equal
        if len(other) != len(self._list):
            return False

        # Check each object equality (both lists DO have the same length here)
        for iobj, o in enumerate(other):
            if o != self._list[iobj]:
                return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __len__(self):
        """Size of the object list"""
        return len(self._list)

    @property
    def index_attribute_name(self):
        """
        Name of the object property used as an index in this object list
        """
        return self._index_prop_name

    @property
    def object_class(self):
        """
        Type of object that can be added into the list
        """
        return self._obj_class

    def _index_unicity_validity_check(self, obj):
        # Check unicity of object with this given index attribute value within the list
        index_val = getattr(obj, self._index_prop_name, None)
        if index_val is not None and self.__contains__(index_val):
            err_msg = "Cannot add {cname:s} object with index '{iv!s}' in this list, another item with that index " \
                      "value already exists.".format(cname=self._obj_class.__name__, iv=index_val)
            log.error(err_msg)
            raise AttributeError(err_msg)

    def add_validity_check_method(self, can_add_meth):
        """
        Add an object addition validity check method to the list of addition validity check methods

        Parameters
        ----------
        can_add_meth: ``Callable``
            object addition validity check method
        """
        # Add addition validity check method to the list of object list addition validity check methods
        if can_add_meth not in self._validity_check_methods:  # Warning here method __eq__() comparison method will be called
            self._validity_check_methods.append(can_add_meth)

    def _can_add_object(self, obj):
        if not isinstance(obj, self._obj_class):
            err_msg = "Added object is not a valid '{cname:s}' instance.".format(cname=self._obj_class.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

        # ---------------------------------------- Validity check methods ------------------------------------------- #
        # Call validity check methods, if any is defined
        for validity_check_meth in self._validity_check_methods:
            validity_check_meth(obj)

    def add_deletion_handler(self, can_delete_meth):
        """
        Add an object deletion handling method to the list of deletion handlers

        Parameters
        ----------
        can_delete_meth: :obj:`callable`
            object deletion handling method
        """
        # Add deletion handling method to the list of object list deletion handlers
        if can_delete_meth not in self._deletion_handlers:  # Warning here hendling instance __eq__() comparison method will be called
            self._deletion_handlers.append(can_delete_meth)

    def __getitem__(self, index):
        """
        Get an object from the list.

        Parameters
        ----------
        item: :obj:`int` or :obj:`string`
            object position in the list (:obj:`int`) or index property value (:obj:`string`) of the object
            to fetch from the list.

        Returns
        -------
        o: :obj:`object` of type self.object_class
            Found object in the list. None if none were found.

        Raises
        ------
        AttributeError
            if the search index type is neither an :obj:`int` nor a :obj:`string`.
        IndexError
            if the :obj:`int` search index value is lower than 0 or larger than the length of the list - 1.
        """
        if Stringifiable.is_type_string(index):
            sindex = Stringifiable.cast_string(index)
            for item in self._list:
                index_val = getattr(item, self._index_prop_name, None)
                if index_val is not None and index_val == sindex:
                    return item

            log.warning("Cannot find '{idx!s}' {cln:s} instance in list !".format(idx=sindex,
                                                                                  cln=self._obj_class.__name__))
            return None
        elif type(index) == int:
            if index >= 0 and index < len(self._list):
                return self._list[index]
            err_msg = "Object list index out of range (len={l:d}).".format(l=len(self._list))
            log.error(err_msg)
            raise IndexError(err_msg)
        else:
            err_msg = "'{it:s}' is not a valid search index. Valid types are 'str' and " \
                      "'int'.".format(it=str(index), cln=self._obj_class.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

    def __contains__(self, item):
        if Stringifiable.is_type_string(item):  # Check instance index is in list
            sitem = Stringifiable.cast_string(item)
            for obj in self._list:
                index_val = getattr(obj, self._index_prop_name, None)
                if index_val is not None and index_val == sitem:
                    return True
            return False
        elif isinstance(item, self._obj_class):  # Check instance is in list
            if item in self._list:
                return True
            return False
        else:
            err_msg = "'{it!s}' is not a valid search index. Valid types are 'str' and '{cln:s}' " \
                      "objects.".format(it=item, cln=self._obj_class.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

    def add(self, obj, insert_pos=-1):
        """
        Adds a instance to the list at a given position

        Parameters
        ----------
        obj: :obj:`object`
            instance to insert in the list
        insert_pos: :obj:`int`
            insertion position in the simulation list. Default -1 (last).
        """
        self._can_add_object(obj)

        if insert_pos == -1:
            self._list.append(obj)
        else:
            self._list.insert(insert_pos, obj)

        # Propagate validity check method into the added object's internal object list
        if self._propag_obj_add_vc_method is not None and hasattr(obj, self._added_obj_list_prop_name):
            obj_list = getattr(obj, self._added_obj_list_prop_name)
            obj_list.add_validity_check_method(self._propag_obj_add_vc_method)

        # Propagate deletion handler into the added object's internal object list
        if self._propag_obj_add_delhandler is not None:
            if isinstance(self._added_obj_list_prop_name_dh, list):
                target = None
                for prop in self._added_obj_list_prop_name_dh:
                    if target is None and hasattr(obj, prop):
                        target = getattr(obj, prop)
                    elif target is not None and hasattr(target, prop):
                        target = getattr(target, prop)
            elif hasattr(obj, self._added_obj_list_prop_name_dh):
                target = getattr(obj, self._added_obj_list_prop_name_dh)

            obj_list = target
            obj_list.add_deletion_handler(self._propag_obj_add_delhandler)

        return obj

    def find_by_uid(self, uid):
        """
        Find an object in the list with a matching UUID

        Parameters
        ----------
        uid: :obj:`UUID` or :obj:`string`
            UUID or UUID string representation of the object to search for.

        Returns
        -------
        o: Matching object with corresponding UUID,if any. Otherwise returns None
        """
        suid = str(uid)
        if getattr(self._obj_class, "uid", None) is None:
            err_msg = "{cname} objects do not have a 'uid' property.".format(cname=self._obj_class.__name__)
            log.error(err_msg)
            raise TypeError(err_msg)

        for o in self._list:
            if str(o.uid) == suid:
                return o
        return None

    def galactica_validity_check(self, **kwargs):
        """
        Perform validity checks on this  instance and eventually log warning messages.

        Parameters
        ----------
        kwargs: :obj:`dict`
            keyword arguments (optional)
        """
        # Perform Galactica validity check on list items
        if issubclass(self._obj_class, GalacticaValidityCheckMixin):
            for item in self._list:
                item.galactica_validity_check(**kwargs)

        # Check unicity of object with this given index attribute value within the list
        index_dict = {}
        for item in self._list:
            index_val = getattr(item, self._index_prop_name, None)
            if index_val is not None:
                if index_val in index_dict:
                    log.warning("{o1!s} and {o2!s} share the same '{p:s}' index value in this "
                                "list.".format(o1=item, o2=index_dict[index_val], p=self._index_prop_name))
                else:
                    index_dict[index_val] = item

    def __unicode__(self):
        """
        String representation of the instance
        """
        # Empty object list
        if len(self._list) == 0:
            return "{obj_cname:s} list : empty".format(obj_cname=self._obj_class.__name__)

        # Display object list in a pretty-formatted table
        strrep = "{obj_cname:s} list :\n".format(obj_cname=self._obj_class.__name__)
        obj_slist = list([str(obj) for obj in self])
        index_slist = list([getattr(obj, self._index_prop_name, "") for obj in self])
        npos = int(N.log10(len(obj_slist))) + 1
        nind = N.max([len(ind) for ind in index_slist])
        ind_header = "Index"
        nind = len(ind_header) if nind < len(ind_header) else nind
        nstr = N.max([len(sobj) for sobj in obj_slist])
        item_header = "Item"
        nstr = len(item_header) if nstr < len(item_header) else nstr
        interline = "+-{npos:s}-+-{nind:s}-+-{nstr:s}-+".format(npos="-"*npos, nind=nind*"-", nstr=nstr*"-")
        strrep += interline + "\n| {d:^{npos}s} | {ind:^{nind}s} | " \
                              "{s:^{nstr}s} |\n".format(npos=npos, d="#", nind=nind, ind=ind_header, nstr=nstr,
                                                        s=item_header)
        for i in range(len(obj_slist)):
            strrep += interline + "\n"
            strrep += "| {i:>{npos}d} | {ind:<{nind}s} | {s:<{nstr}s} |\n".format(npos=npos, i=i, nind=nind,
                                                                                  ind=index_slist[i], nstr=nstr, s=obj_slist[i])
        strrep += interline

        return strrep

    def __iter__(self):
        """Basic object list iterator"""
        return iter(self._list)

    def __call__(self, *args, **kwargs):
        return self.__iter__()

    def __delitem__(self, item):
        """
        Delete an object from the list.

        Parameters
        ----------
        item: :obj:`object` or :obj:`int` or :obj:`string`
            instance to delete, object position in the list (:obj:`int`) or index property value (:obj:`string`) of the
            object to remove from the list.
        """
        found_obj = None
        if isinstance(item, self._obj_class):  # item is a corresponding instance of the list object class
            if item in self._list:
                found_obj = item
            else:
                err_msg = "'{o!s}' does not belong to this '{cln:s}' list.".format(o=item, cln=self._obj_class.__name__)
                log.error(err_msg)
                raise KeyError(err_msg)
        elif type(item) == int:
            if item >= 0 and item < len(self._list):
                found_obj = self._list[item]
            else:
                err_msg = "Object list index out of range (len={l:d}).".format(l=len(self._list))
                log.error(err_msg)
                raise IndexError(err_msg)
        elif Stringifiable.is_type_string(item):  # item is a string => search for an object in the list
            sitem = Stringifiable.cast_string(item)
            for obj in self._list:
                index_val = getattr(obj, self._index_prop_name, None)
                if index_val is not None and index_val == sitem:
                    found_obj = obj
                    break

            if found_obj is None:
                # Not found
                err_msg = "Cannot find '{it!s}' {cln:s} instance in list !".format(it=sitem, cln=self._obj_class.__name__)
                log.error(err_msg)
                raise KeyError(err_msg)
        else:
            # Invalid item value
            err_msg = "'{it!s}' is not a valid deletion index. Valid types are 'str' and '{cln:s}' " \
                      "objects.".format(it=item, cln=self._obj_class.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

        # ------------------------------------------ Checks dependencies --------------------------------------------- #
        # Call object deletion handlers, if any is defined
        depend_list = []
        for del_handler in self._deletion_handlers:
            depend_obj = del_handler(found_obj)
            if depend_obj is not None:
                if isinstance(depend_obj, list):
                    depend_list += depend_obj
                else:
                    depend_list.append(depend_obj)

        # If deleted object has any dependency, prevent its deletion
        if len(depend_list) > 0:
            err_msg = "'{o!s}' cannot be deleted, the following items depend on it (try to delete them first) : " \
                      "[{dl:s}].".format(o=found_obj, dl=", ".join(depend_list))
            log.warning(err_msg)
            raise AttributeError(err_msg)

        self._list.remove(found_obj)

    def clear(self):
        """Clear the object list"""
        for i in range(len(self._list)):
            del self[0]


__all__ = ["ObjectList", "DataType", "GalacticaValidityCheckMixin"]
