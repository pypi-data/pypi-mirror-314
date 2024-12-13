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
from __future__ import print_function, unicode_literals, division, absolute_import  # Python 2 and 3 compatibility
from future.builtins import str
import pytest
import logging

from astrophysix.simdm.utils import ObjectList, GalacticaValidityCheckMixin

log = logging.getLogger("astrophysix.simdm")


class DummyA(GalacticaValidityCheckMixin):
    def __init__(self, my_param, alt=None):
        self._p = my_param
        self._a = alt

    @property
    def p(self):
        return self._p

    @property
    def alternative(self):
        return self._a

    @alternative.setter
    def alternative(self, new_alt):
        self._a = new_alt

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        if other.__class__ != DummyA:
            return False

        if self._p != other.p:
            return False

        if self._a != other.alternative:
            return False

        return True

    def __str__(self):
        s = "[DummyA] p={p:s}".format(p=self._p)
        if self._a is not None:
            s += " ; alternative={alt:s}".format(alt=self._a)
        return s

    def __repr__(self):
        return self.__str__()

    def galactica_validity_check(self, **kwargs):
        """
        Perform validity checks on this  instance and eventually log warning messages.

        Parameters
        ----------
        kwargs: `dict`
            keyword arguments (optional)
        """
        if self._p.startswith("a"):
            log.warning("'{s!s}' starts with 'a'.".format(s=self))


class DummyB(DummyA):
    def __init__(self, *args, **kwargs):
        super(DummyB, self).__init__(*args, **kwargs)
        self._alist = ObjectList(DummyA, 'p')

    @property
    def uid(self):
        return self._p

    @property
    def alist(self):
        return self._alist


class DummyC(DummyA):
    def __init__(self, *args, **kwargs):
        super(DummyC, self).__init__(*args, **kwargs)
        self._alist = ObjectList(DummyA, 'p')
        self._b = DummyB(3.14, alt="Pi")

    @property
    def my_prop(self):
        return "property: {p:s}".format(p=self._p)

    @property
    def b(self):
        return self._b

    @property
    def alist(self):
        return self._alist


class TestObjectList(object):
    def test_init_object_list(self):
        """
        Tests ObjectList instance initialisation
        """
        ol = ObjectList(DummyA, "p")
        a1 = ol.add(DummyA("f"))
        a2 = ol.add(DummyA("g"))
        a10 = ol.add(DummyA("Q", alt="x"))

        assert len(ol) == 3
        assert ol.index_attribute_name == "p"
        assert ol.object_class == DummyA
        assert a10.alternative == "x"
        assert list(ol) == [a1, a2, a10]

    def test_object_list_equality(self):
        """
        Tests ObjectList comparison method
        """
        ol = ObjectList(DummyA, "p")

        ol_alt = ObjectList(DummyA, 'alternative')
        assert ol != ol_alt  # Different index attribute names

        olb = ObjectList(DummyB, "p")
        assert ol != olb  # Different object class

        a1 = DummyA("f")
        a2 = DummyA("g")
        a10 = DummyA("Q", alt="x")
        ol.add(a1)
        ol.add(a2)
        ol.add(a10)

        # Object lists of different lengths
        ol2 = ObjectList(DummyA, "p")
        print(len(ol), len(ol2))  # 3 0
        assert ol != ol2  # Different length

        sa1 = ol2.add(DummyA("f"))
        sa2 = ol2.add(DummyA("g"))
        sa10 = ol2.add(DummyA("Q", alt="y"))

        assert ol != ol2  # 3rd item differ
        sa10.alternative = "x"
        assert ol == ol2  # => Ok, all items are equals

    def test_object_list_add_exception(self):
        """
        Tests ObjectList.add() method + raised exceptions
        """
        ol = ObjectList(DummyA, "p")

        # Tests adding a dict in a DummyA object list
        with pytest.raises(AttributeError) as e:
            ol.add({"a": 1.45})
        assert str(e.value) == "Added object is not a valid 'DummyA' instance."

        # Tests adding 2 objects with same index value in list
        with pytest.raises(AttributeError) as e:
            a1 = ol.add(DummyA("P"))
            a2 = ol.add(DummyA("P"))
        assert str(e.value) == "Cannot add DummyA object with index 'P' in this list, another item with that index " \
                               "value already exists."

        # Tests insert position
        a11 = DummyA("Y")
        assert a11 == ol.add(a11)
        a12 = ol.add(DummyA("W"))
        a13 = ol.add(DummyA("S"))
        ains = ol.add(DummyA("insert"), insert_pos=2)
        assert ains is ol[2]

        # Tests validity check function
        def vc_func(obj):
            if obj.alternative != "x":
                raise ValueError("alt != 'x")

        olvc = ObjectList(DummyA, "p")
        olvc.add_validity_check_method(vc_func)
        a10 = olvc.add(DummyA("Q", alt="x"))  # OK => should not raise an error
        with pytest.raises(ValueError) as e:
            af = olvc.add(DummyA("F"))
        assert str(e.value) == "alt != 'x"

    def test_object_list_getitem(self, caplog):
        """
        Tests ObjectList.__getitem() method + ObjectList.__contains__() method

        caplog: captured log PyTest fixture
        """
        # Item not found warning message and None returned value
        ol = ObjectList(DummyA, "p")
        a = ol.add(DummyA("K", alt='s'))
        assert ol["K"] is a  # Ok => should get item with key "K"
        b = ol.add(DummyA("U", alt='s'))
        assert ol[1] is b  # Ok => should get
        c = ol.add(DummyA("D", alt="x"))
        a = ol["my_index"]
        assert a is None and caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                                          "Cannot find 'my_index' DummyA instance in list !")

        # Tests invalid int index value exception
        with pytest.raises(IndexError)as e:
            item = ol[3]
        assert str(e.value) == "Object list index out of range (len=3)."

        # Tests invalid index type exception
        with pytest.raises(AttributeError) as e:
            key = {103: -3.14159}
            o = ol[key]
        assert str(e.value) == "'{103: -3.14159}' is not a valid search index. Valid types are 'str' and 'int'."

        # ---------------------------------------------- __contains__ tests ------------------------------------------ #
        assert "unknown_param" not in ol
        assert c.p in ol
        assert c in ol
        del ol[b.p]  # b DummyA instance is removed
        assert b.p not in ol
        assert b not in ol

        # Tries to test if integer value is contained in list
        exc_msg = "'{103: -3.14159}' is not a valid search index. Valid types are 'str' and 'DummyA' objects."
        with pytest.raises(AttributeError, match=exc_msg):
            is_in_list = {103: -3.14159} in ol
        # ------------------------------------------------------------------------------------------------------------ #

    def test_object_list_item_deletion(self):
        """
        Tests object list item deletion
        """
        ol = ObjectList(DummyA, "p")
        a12 = ol.add(DummyA("W"))
        a13 = ol.add(DummyA("S"))
        a14 = ol.add(DummyA("Q"))

        del ol[a12]  # Deletion should be ok

        # Tests invalid deletion index type
        with pytest.raises(AttributeError, match="'{102: 1.4509e-06}' is not a valid deletion index. Valid types are "
                                                 "'str' and 'DummyA' objects."):
            key = {102: 1.4509E-6}
            del ol[key]

        # Item not in list => should raise a KeyError
        not_in_ol = DummyA("test")
        exc_msg = "'\\[DummyA\\] p=test' does not belong to this 'DummyA' list."
        with pytest.raises(KeyError, match=exc_msg):
            del ol[not_in_ol]
        with pytest.raises(KeyError, match="Cannot find 'test' DummyA instance in list !"):
            del ol["test"]

        # Tests invalid int deletion index value exception
        with pytest.raises(IndexError, match="Object list index out of range \\(len=2\\)."):
            del ol[2]

        def can_delete_dummya(a):
            """
            Checks if a DummyA instance can be safely deleted from list. Returns None if it can be deleted, otherwise
            returns a string.
            """
            if a in ol:
                return "{a!s}".format(a=a)
            return None

        # Deletion with a dependency => should raise an error
        ol2 = ObjectList(DummyA, "p")
        ol2.add_deletion_handler(can_delete_dummya)
        ol2.add(a13)
        exc_msg = "'\\[DummyA\\] p=S' cannot be deleted, the following items depend on it \\(try to delete " \
                  "them first\\) : \\[\\[DummyA\\] p=S\\]"
        with pytest.raises(AttributeError, match=exc_msg):
            del ol2[a13]

        def can_delete_a_in_c(a_obj):
            if a_obj.p == "Q":
                raise AttributeError("Not possible")

        ocl = ObjectList(DummyC, 'my_prop', object_addition_vcheck=(can_delete_a_in_c, 'alist'))
        c1 = DummyC('alpha')
        ocl.add(c1)
        with pytest.raises(AttributeError, match="Not possible"):
            a15 = c1.alist.add(DummyA("Q"))

        # Test if on can delete an object in a list, the list being a property of another object, property of
        #  an object list item
        def can_delete_a_in_cb(a_obj):
            if a_obj.p == "Q":
                raise AttributeError("No can do ! Not possible.")
        ocl = ObjectList(DummyC, 'my_prop', object_addition_delhandler=(can_delete_a_in_cb, ['b', 'alist']))
        c1 = DummyC('alpha')
        ocl.add(c1)
        Aq = c1.b.alist.add(DummyA("Q"))
        Ap = c1.b.alist.add(DummyA("P"))
        del c1.b.alist[Ap]  # => Should be ok
        with pytest.raises(AttributeError, match="No can do ! Not possible."):
            del c1.b.alist[Aq]

    def test_object_list_clear(self):
        """Test object list cleanup method"""
        ol = ObjectList(DummyA, "p")
        a12 = ol.add(DummyA("W"))
        a13 = ol.add(DummyA("S"))
        a14 = ol.add(DummyA("Q"))
        assert len(ol) == 3
        ol.clear()
        assert len(ol) == 0

    def test_object_list_find_by_uid(self):
        """
        Tests finding a object instance in the list by its uid property
        """
        ol = ObjectList(DummyA, "p")
        with pytest.raises(TypeError, match="DummyA objects do not have a 'uid' property."):
            o = ol.find_by_uid("abcd")

        # Find DummyB object instance by its 'uid' property value
        olb = ObjectList(DummyB, "p")
        b = olb.add(DummyB("abcd1234", alt="x"))
        assert b is olb.find_by_uid("abcd1234")

        o = olb.find_by_uid("unknown_uid")
        assert o is None

    def test_object_list_galactica_validity_checks(self, caplog):
        """
        Tests project Galactica validity checks

        Parameters
        ----------
        caplog: captured log PyTest fixture
        """
        ol = ObjectList(DummyA, "p")
        d = ol.add(DummyA("Damien", alt="Genius"))
        a = ol.add(DummyA("Damien2", alt="Awesome genius"))
        a._p = d.p

        # Index unicity
        ol.galactica_validity_check()
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "[DummyA] p=Damien ; alternative=Awesome genius and [DummyA] p=Damien ; "
                                            "alternative=Genius share the same 'p' index value in this list.")

        # Bad alias starting with an 'a'
        a._p = "alexandre"
        ol.galactica_validity_check()
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "'[DummyA] p=alexandre ; alternative=Awesome genius' starts with 'a'.")


__all__ = ["TestObjectList"]
