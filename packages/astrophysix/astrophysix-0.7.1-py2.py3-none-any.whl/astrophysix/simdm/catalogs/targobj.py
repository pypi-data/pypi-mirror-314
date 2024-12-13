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
import uuid
from enum import Enum
from future.builtins import str, list, int
import logging

from astrophysix.simdm.utils import ObjectList, GalacticaValidityCheckMixin, DataType
from astrophysix.utils.persistency import Hdf5StudyPersistent
from astrophysix.utils.strings import Stringifiable
from astrophysix import units as U


log = logging.getLogger("astrophysix.simdm")


class PropertyFilterFlag(Enum):
    NO_FILTER = ("no_filter", "Not used in filters")
    BASIC_FILTER = ("basic_filter", "Filter in basic form")
    ADVANCED_FILTER = ("advanced_filter", "Filter in advanced form")

    def __init__(self, filter_flag, display_name):
        self._flag = filter_flag
        self._disp_name = display_name

    @property
    def flag(self):
        """Object property filter flag value"""
        return self._flag

    @property
    def displayed_flag(self):
        """Object property filter flag displayed name"""
        return self._disp_name

    @classmethod
    def from_flag(cls, flag):
        """
        Parameters
        ----------
        flag: :obj:`string`
            property filter flag value

        Returns
        -------
        t: :class:`~astrophysix.simdm.catalogs.targobj.PropertyFilterFlag`
            Property filter flag matching the requested flag value.

        Raises
        ------
        ValueError
            if requested flag value does not match any property filter flag.

        Example
        -------
            >>> flag = PropertyFilterFlag.from_flag("no_filter")
            >>> flag.displayed_flag
            "Not used in filters"
            >>> flag2 = PropertyFilterFlag.from_flag("MY_UNKNOWN_FLAG")
            ValuerError: No PropertyFilterFlag defined with the flag 'MY_UNKNOWN_FLAG'.
        """
        for fflag in cls:
            if fflag.flag == flag:
                return fflag
        raise ValueError("No PropertyFilterFlag defined with the flag '{f:s}'".format(f=flag))


class PropertySortFlag(Enum):
    NO_SORT = ("no_sort", "Not used for sorting")
    BASIC_SORT = ("basic_sort", "Sort in basic form")
    ADVANCED_SORT = ("advanced_sort", "Sort in advanced form")

    def __init__(self, sort_flag, display_name):
        self._flag = sort_flag
        self._disp_name = display_name

    @property
    def flag(self):
        """Object property sort flag value"""
        return self._flag

    @property
    def displayed_flag(self):
        """Object property sort flag displayed name"""
        return self._disp_name

    @classmethod
    def from_flag(cls, flag):
        """
        Parameters
        ----------
        flag: :obj:`string`
            property sort flag value

        Returns
        -------
        t: :class:`~astrophysix.simdm.catalogs.targobj.PropertySortFlag`
            Property sort flag matching the requested flag value.

        Raises
        ------
        ValueError
            if requested flag value does not match any property sort flag.

        Example
        -------
            >>> flag = PropertySortFlag.from_flag("basic_sort")
            >>> flag.displayed_flag
            "Sort in basic form"
            >>> flag2 = PropertySortFlag.from_flag("MY_UNKNOWN_FLAG")
            ValuerError: No PropertySortFlag defined with the flag 'MY_UNKNOWN_FLAG'.
        """
        for sflag in cls:
            if sflag.flag == flag:
                return sflag
        raise ValueError("No PropertySortFlag defined with the flag '{f:s}'".format(f=flag))


class ObjectProperty(Hdf5StudyPersistent, GalacticaValidityCheckMixin, Stringifiable):
    """
    Target object property class (Simulation data model)

    Parameters
    ----------
    property_name: :obj:`string`
        property name (mandatory)
    description: :obj:`string`
        object property description
    unit: :obj:`string` or :class:`~astrophysix.units.unit.Unit`
        object property physical unit
    filter_flag: :class:`~astrophysix.simdm.catalogs.targobj.PropertyFilterFlag`
        target object property filter flag. Default :attr:`PropertyFilterFlag.NO_FILTER <astrophysix.simdm.catalogs.targobj.PropertyFilterFlag.NO_FILTER>`
    sort_flag: :class:`~astrophysix.simdm.catalogs.targobj.PropertySortFlag`
        target object property sort flag. Default :attr:`PropertySortFlag.NO_SORT <astrophysix.simdm.catalogs.targobj.PropertySortFlag.NO_SORT>`
    dtype: :class`simdm.utils.DataType`
        property data type. Default DataType.REAL.
    """
    def __init__(self, **kwargs):
        super(ObjectProperty, self).__init__(**kwargs)
        self._prop_name = ""
        self._description = ""

        # Target object property name
        if "property_name" not in kwargs:
            raise AttributeError("{cname:s} 'property_name' attribute is not defined "
                                 "(mandatory).".format(cname=self.__class__.__name__))
        self.property_name = kwargs["property_name"]

        # Target object property description
        if "description" in kwargs:
            self.description = kwargs["description"]

        # Target object property filter/sort flags
        self._filter_flag = PropertyFilterFlag.NO_FILTER
        if "filter_flag" in kwargs:
            self.filter_flag = kwargs["filter_flag"]
        self._sort_flag = PropertySortFlag.NO_SORT
        if "sort_flag" in kwargs:
            self.sort_flag = kwargs["sort_flag"]

        # Target object property datatype
        self._dtype = DataType.REAL
        if "dtype" in kwargs:
            self.datatype = kwargs["dtype"]

        # Target object property unit
        self._unit = U.none
        if "unit" in kwargs:
            self.unit = kwargs["unit"]

    def __eq__(self, other):
        """
        ObjectProperty comparison method

        other: :class:`~astrophysix.simdm.catalogs.targobj.ObjectProperty`
            target object property instance to compare to
        """
        if not super(ObjectProperty, self).__eq__(other):
            return False

        # Compare property name
        if self._prop_name != other.property_name:
            return False

        # Compare property description
        if self._description != other.description:
            return False

        # Compare datatype
        if self._dtype != other.datatype:
            return False

        # Compare sort/filter flags
        if self._filter_flag != other.filter_flag or self._sort_flag != other.sort_flag:
            return False

        # Compare units
        return self._unit == other.unit and self._unit.name == other.unit.name

    @property
    def property_name(self):
        """Target object property name. Can be edited."""
        return self._prop_name

    @property_name.setter
    def property_name(self, new_prop_name):
        try:
            self._prop_name = Stringifiable.cast_string(new_prop_name, valid_empty=False)
        except TypeError:
            err_msg = "{cname:s} 'property_name' property is not a valid (non-empty) string.".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

    @property
    def display_name(self):
        """Object property display name. Concatenation of the property name and its unit LaTex formula, if defined."""
        if self._unit == U.none:
            return self._prop_name
        d = "{n:s} ({ul:s})".format(n=self._prop_name, ul=self._unit.latex)
        return d

    @property
    def datatype(self):
        """Object property datatype (:class:`~astrophysix.simdm.utils.DataType`)"""
        return self._dtype

    @datatype.setter
    def datatype(self, dtype):
        try:
            tk = Stringifiable.cast_string(dtype)
            self._dtype = DataType.from_key(tk)
        except ValueError as ve:
            err_msg = "Object property 'datatype' error : {verr:s}".format(verr=str(ve))
            log.error(err_msg)
            raise AttributeError(err_msg)
        except TypeError:  # Not a valid string
            if not isinstance(dtype, DataType):
                err_msg = "Object property 'datatype' attribute is not a valid DataType enum value."
                log.error(err_msg)
                raise AttributeError(err_msg)
            self._dtype = dtype

    @property
    def description(self):
        """Object property description. Can be edited."""
        return self._description

    @description.setter
    def description(self, new_descr):
        try:
            self._description = Stringifiable.cast_string(new_descr)
        except TypeError:
            err_msg = "{cname:s} 'description' property is not a valid string.".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

    @property
    def filter_flag(self):
        """
        Object property filter flag. Can be edited.

        Returns
        -------
        f: :class:`~atrophysix.simdm.catalogs.targob.PropertyFilterFlag`
            object property filter flag
        """
        return self._filter_flag

    @filter_flag.setter
    def filter_flag(self, new_fflag):
        try:
            fflag = Stringifiable.cast_string(new_fflag)
            self._filter_flag = PropertyFilterFlag.from_flag(fflag)
        except ValueError as ve:
            err_msg = "Object property 'filter_flag' property error : {verr:s}.".format(verr=str(ve))
            log.error(err_msg)
            raise AttributeError(err_msg)
        except TypeError:  # Not a valid string
            if not isinstance(new_fflag, PropertyFilterFlag):
                err_msg = "Object property 'filter_flag' attribute is not a valid PropertyFilterFlag enum value."
                log.error(err_msg)
                raise AttributeError(err_msg)
            self._filter_flag = new_fflag

    @property
    def sort_flag(self):
        """
        Object property sort flag. Can be edited.

        Returns
        -------
        f: :class:`~atrophysix.simdm.catalogs.targob.PropertySortFlag`
            object property sort flag
        """
        return self._sort_flag

    @sort_flag.setter
    def sort_flag(self, new_sflag):
        try:
            sflag = Stringifiable.cast_string(new_sflag)
            self._sort_flag = PropertySortFlag.from_flag(sflag)
        except ValueError as ve:
            err_msg = "Object property 'sort_flag' property error : {verr:s}.".format(verr=str(ve))
            log.error(err_msg)
            raise AttributeError(err_msg)
        except TypeError:  # Not a valid string
            if not isinstance(new_sflag, PropertySortFlag):
                err_msg = "Object property 'sort_flag' attribute is not a valid PropertySortFlag enum value."
                log.error(err_msg)
                raise AttributeError(err_msg)
            self._sort_flag = new_sflag

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, new_unit):
        if isinstance(new_unit, U.Unit):
            self._unit = new_unit
        else:
            try:
                s = Stringifiable.cast_string(new_unit, valid_empty=False)
                self._unit = U.Unit.from_name(s)
            except TypeError:  # Not a valid string
                err_msg = "Object property 'unit' property is not a valid (non-empty) string."
                log.error(err_msg)
                raise AttributeError(err_msg)
            except AttributeError as aerr:
                err_msg = "Object property 'unit' property error : {uerr:s}.".format(uerr=str(aerr))
                log.error(err_msg)
                raise AttributeError(err_msg)

    @classmethod
    def _hsp_valid_attributes(cls):
        """List of valid kwargs in __init__() method"""
        return ["property_name", "description", "filter_flag", "sort_flag", "dtype", "unit"]

    def _hsp_write(self, h5group, **kwargs):
        """
        Serialize a ObjectProperty object into a HDF5 file.

        Parameters
        ----------
        h5group: ``h5py.Group``
            Main group to write the ObjectProperty into.
        kwargs: ``dict``
            keyword argument dictionary.
        """
        # Call to parent class _hsp_write() : write UUID, etc.
        super(ObjectProperty, self)._hsp_write(h5group, **kwargs)

        # Write object property name
        self._hsp_write_attribute(h5group, ('name', self._prop_name), **kwargs)

        # Write target object property description, if defined
        self._hsp_write_attribute(h5group, ('description', self._description), **kwargs)

        # Write object property filter/sort flags
        self._hsp_write_attribute(h5group, ('filter_flag', self._filter_flag.flag), **kwargs)
        self._hsp_write_attribute(h5group, ('sort_flag', self._sort_flag.flag), **kwargs)

        # Write property type
        self._hsp_write_attribute(h5group, ("datatype", self._dtype.key), **kwargs)

        # Write object property unit
        self._hsp_write_attribute(h5group, ('unit', self._unit), **kwargs)

    @classmethod
    def _hsp_read(cls, h5group, version, dependency_objdict=None):
        """
        Read a ObjectProperty instance from a HDF5 file (*.h5).

        Parameters
        ----------
        h5group: ``h5py.Group``
            Main group to read the object from.
        version: ``int``
            version of the object to read.
        dependency_objdict: ``dict``
            dependency object dictionary. Default None

        Returns
        -------
        prop: ``ObjectProperty``
            Read ObjectProperty instance
        """
        # Handle different versions here

        # Fetch Hdf5StudyPersistent object UUID
        uid = super(ObjectProperty, cls)._hsp_read(h5group, version, dependency_objdict=dependency_objdict)

        # Read catalog name
        name = cls._hsp_read_attribute(h5group, 'name', "generic result name")

        # Read property filter/sort flags
        fflag = cls._hsp_read_attribute(h5group, "filter_flag", "object property filter flag")
        sflag = cls._hsp_read_attribute(h5group, "sort_flag", "object property sort flag")

        dtype = cls._hsp_read_attribute(h5group, "datatype", "object property type", raise_error_if_not_found=False)
        if dtype is None:
            dtype = DataType.REAL

        # Read parameter setting unit
        u = cls._hsp_read_unit(h5group, "unit")

        # Create target object property
        prop = cls(uid=uid, property_name=name, unit=u, filter_flag=fflag, sort_flag=sflag, dtype=dtype)

        # Read target object property description, if defined
        pdesc = cls._hsp_read_attribute(h5group, 'description', "target object property description",
                                        raise_error_if_not_found=False)
        if pdesc is not None:
            prop.description = pdesc

        return prop

    def galactica_validity_check(self, **kwargs):
        """
        Perform validity checks on this  instance and eventually log warning messages.

        Parameters
        ----------
        kwargs: :obj:`dict`
            keyword arguments (optional)
        """
        # Check property name length
        if len(self._prop_name) > 64:
            log.warning("{t!s} name is too long for Galactica (max. 64 characters).".format(t=self))

    def __unicode__(self):
        """
        String representation of the instance
        """
        return "'{pname:s}' target object property".format(pname=self._prop_name)


class ObjectPropertyGroup(Hdf5StudyPersistent, GalacticaValidityCheckMixin, Stringifiable):
    """
    Target object property group class (Simulation data model)

    Parameters
    ----------
    group_name: property group name (mandatory)
    description: property group description
    """
    def __init__(self, **kwargs):
        super(ObjectPropertyGroup, self).__init__(**kwargs)
        self._group_name = ""
        self._description = ""
        self._group_properties = ObjectList(ObjectProperty, 'property_name')

        # Target object property group name
        if "group_name" not in kwargs:
            raise AttributeError("{cname:s} 'group_name' attribute is not defined "
                                 "(mandatory).".format(cname=self.__class__.__name__))
        self.group_name = kwargs["group_name"]

        if "description" in kwargs:
            self.description = kwargs["description"]

    def __eq__(self, other):
        """
        ObjectPropertyGroup comparison method

        other: :class:`~astrophysix.simdm.catalogs.targobj.ObjectPropertyGroup`
            target object property group instance to compare to
        """
        if not super(ObjectPropertyGroup, self).__eq__(other):
            return False

        if self._group_name != other.group_name:
            return False

        if self._description != other.description:
            return False

        if self._group_properties != other.group_properties:
            return False

        return True

    @property
    def group_name(self):
        """Object property group name. Can be edited."""
        return self._group_name

    @group_name.setter
    def group_name(self, new_grp_name):
        try:
            self._group_name = Stringifiable.cast_string(new_grp_name, valid_empty=False)
        except TypeError:
            err_msg = "{cname:s} 'group_name' property is not a valid (non-empty) string.".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

    @property
    def group_properties(self):
        """Object property group :class:`~astrophysix.simdm.catalogs.targobj.ObjectProperty` list
        (:class:`~astrophysix.simdm.utils.ObjectList`)"""
        return self._group_properties

    @property
    def description(self):
        """Object property group description. Can be edited."""
        return self._description

    @description.setter
    def description(self, new_descr):
        try:
            self._description = Stringifiable.cast_string(new_descr)
        except TypeError:
            err_msg = "{cname:s} 'description' property is not a valid string.".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

    @classmethod
    def _hsp_valid_attributes(cls):
        """List of valid kwargs in __init__() method"""
        return ["group_name", "description"]

    def _hsp_write(self, h5group, **kwargs):
        """
        Serialize a ObjectPropertyGroup object into a HDF5 file.

        Parameters
        ----------
        h5group: ``h5py.Group``
            Main group to write the ObjectPropertyGroup into.
        kwargs: ``dict``
            keyword argument dictionary.
        """
        # Call to parent class _hsp_write() : write UUID, etc.
        super(ObjectPropertyGroup, self)._hsp_write(h5group, **kwargs)

        # Write object property group name
        self._hsp_write_attribute(h5group, ('name', self._group_name), **kwargs)

        # Write target object property group description, if defined
        self._hsp_write_attribute(h5group, ('description', self._description), **kwargs)

        # Write group properties UUID list
        self._hsp_write_object_list(h5group, "GROUP_PROPERTIES", self._group_properties, "group_prop_",
                                    uid_list_only=True, **kwargs)

    @classmethod
    def _hsp_read(cls, h5group, version, dependency_objdict=None):
        """
        Read a ObjectProperty instance from a HDF5 file (*.h5).

        Parameters
        ----------
        h5group: ``h5py.Group``
            Main group to read the object from.
        version: ``int``
            version of the object to read.
        dependency_objdict: ``dict``
            dependency object dictionary. Default None

        Returns
        -------
        prop: ``ObjectProperty``
            Read ObjectProperty instance
        """
        # Handle different versions here

        # Fetch Hdf5StudyPersistent object UUID
        uid = super(ObjectPropertyGroup, cls)._hsp_read(h5group, version, dependency_objdict=dependency_objdict)

        # Read object property group name
        name = cls._hsp_read_attribute(h5group, 'name', "generic result name")

        # Create target object property group
        pgroup = cls(uid=uid, group_name=name)

        # ---------------------- Read target object property group members (object properties) ----------------------- #
        # Search for already instantiated target object properties in dependency object dictionary
        if dependency_objdict is None:
            err_msg = "Cannot find any target object property already instantiated in the TargetObject instance."
            log.error(err_msg)
            raise IOError(err_msg)

        # Get dictionary of target object properties of the corresponding class :
        if ObjectProperty.__name__ not in dependency_objdict:
            err_msg = "Cannot find any {cname:s} instance.".format(cname=ObjectProperty.__name__)
            log.error(err_msg)
            raise IOError(err_msg)
        obj_prop_dict = dependency_objdict[ObjectProperty.__name__]

        # Find object property
        for spuid in ObjectProperty._hsp_read_object_list(h5group, "GROUP_PROPERTIES", "group_prop_", "group property",
                                                          uid_list_only=True, dependency_objdict=dependency_objdict):
            objprop_uid = uuid.UUID(spuid)

            # Find target object property according to its UUID
            if objprop_uid not in obj_prop_dict:
                err_msg = "Cannot find {cname:s} instance with uid {uid:s}.".format(cname=ObjectProperty.__name__,
                                                                                    uid=spuid)
                log.error(err_msg)
                raise IOError(err_msg)

            p = obj_prop_dict[objprop_uid]
            pgroup.group_properties.add(p)
        # ------------------------------------------------------------------------------------------------------------ #

        # Read target object property group description, if defined
        pdesc = cls._hsp_read_attribute(h5group, 'description', "target object property group description",
                                        raise_error_if_not_found=False)
        if pdesc is not None:
            pgroup.description = pdesc

        return pgroup

    def galactica_validity_check(self, **kwargs):
        """
        Perform validity checks on this instance and eventually log warning messages.

        Parameters
        ----------
        kwargs: :obj:`dict`
            keyword arguments (optional)
        """
        # Check property group name length
        if len(self._group_name) > 32:
            log.warning("{t!s} name is too long for Galactica (max. 32 characters).".format(t=self))

        # Pointless to run the Galactica validity check on the group properties ? If it is already done at the
        # TargetObject level...

    def __unicode__(self):
        """
        String representation of the instance
        """
        return "'{gname:s}' property group".format(gname=self._group_name)


class TargetObject(Hdf5StudyPersistent, GalacticaValidityCheckMixin, Stringifiable):
    """
    Catalog target object class (Simulation data model)

    Parameters
    ----------
    name: :obj:`string`
        object name (mandatory)
    description: :obj:`string`
        result description
    """
    def __init__(self, **kwargs):
        super(TargetObject, self).__init__(**kwargs)
        self._name = ""
        self._description = ""
        self._obj_properties = ObjectList(ObjectProperty, "property_name")
        self._obj_properties.add_deletion_handler(self._can_delete_object_property)
        self._obj_property_groups = ObjectList(ObjectPropertyGroup, "group_name",
                                               object_addition_vcheck=(self._can_add_objet_property_in_a_group,
                                                                       "group_properties"))
        self._obj_property_groups.add_validity_check_method(self._can_add_prop_group)

        # Target object name
        if "name" not in kwargs:
            raise AttributeError("{cname:s} 'name' attribute is not defined "
                                 "(mandatory).".format(cname=self.__class__.__name__))
        self.name = kwargs["name"]

        if "description" in kwargs:
            self.description = kwargs["description"]

    def __eq__(self, other):
        """
        TargetObject comparison method

        other: :class:`~astrophysix.simdm.catalogs.targobj.TargetObject`
            target object instance to compare to
        """
        if not super(TargetObject, self).__eq__(other):
            return False

        if self._name != other.name:
            return False

        if self._description != other.description:
            return False

        # Compare opbject properties and property groups
        if self._obj_properties != other.object_properties:
            return False
        if self._obj_property_groups != other.property_groups:
            return False

        return True

    @property
    def name(self):
        """Target object name. Can be edited."""
        return self._name

    @name.setter
    def name(self, new_cat_name):
        try:
            self._name = Stringifiable.cast_string(new_cat_name, valid_empty=False)
        except TypeError:
            err_msg = "{cname:s} 'name' property is not a valid (non-empty) string.".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

    @property
    def object_properties(self):
        """Target object :class:`~astrophysix.simdm.catalogs.targobj.ObjectProperty` list
        (:class:`~astrophysix.simdm.utils.ObjectList`)"""
        return self._obj_properties

    @property
    def property_groups(self):
        """Target object :class:`~astrophysix.simdm.catalogs.targobj.ObjectPropertyGroup` list
        (:class:`~astrophysix.simdm.utils.ObjectList`)"""
        return self._obj_property_groups

    @property
    def description(self):
        """Target object description. Can be edited."""
        return self._description

    @description.setter
    def description(self, new_descr):
        try:
            self._description = Stringifiable.cast_string(new_descr)
        except TypeError:
            err_msg = "{cname:s} 'description' property is not a valid string.".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

    def _can_add_prop_group(self, prop_group):
        """
        Checks that a given ObjectPropertyGroup instance can be added into this Target object group list.
        Verifies that each one of the ObjectProperty instance of this group already belongs to the TargetObject object
        property list. Raises an AttributeError if not.

        Parameters
        ----------
        prop_group: ``astrophysix.simdm.catalogs.targobj.ObjectPropertyGroup``
            Object property group to add
        """
        for obj_prop in prop_group.group_properties:
            self._can_add_objet_property_in_a_group(obj_prop)

    def _can_add_objet_property_in_a_group(self, obj_prop):
        """
        Checks that a given ObjectProperty instance can be added into any of this TargetObject's ObjectPropertyGroup.
        Verifies that the ObjectProperty instance belongs to the TargetObject object propert list. Raises an
        AttributeError if not.

        Parameters
        ----------
        obj_prop: ``astrophysix.simdm.catalogs.targobj.ObjectProperty``
            Object property to add
        """
        if obj_prop not in self._obj_properties:
            err_msg = "{op!s} does not belong to this {cname:s} object property " \
                      "list.".format(cname=self.__class__.__name__, op=obj_prop)
            log.error(err_msg)
            raise AttributeError(err_msg)

    def _can_delete_object_property(self, obj_prop):
        """
        Checks if an object property is not linked to any object property group and can be safely deleted.
        Returns None if it can be deleted, otherwise returns a string.

        Parameters
        ----------
        obj_prop: ``:class:~astrophysix.simdm.catalogs.targobj.ObjectProperty``
            target object property about to be deleted

        Returns
        -------
        o: str or None
        """
        prop_list = []
        for pgroup in self._obj_property_groups:
            if obj_prop in pgroup.group_properties:
                prop_list.append("{s!s} - {pg!s} - {op!s}".format(s=self, pg=pgroup, op=obj_prop))

        if len(prop_list) > 0:
            return prop_list

        return None

    @classmethod
    def _hsp_valid_attributes(cls):
        """List of valid kwargs in __init__() method"""
        return ["name", "description"]

    def _hsp_write(self, h5group, **kwargs):
        """
        Serialize a TargetObject object into a HDF5 file.

        Parameters
        ----------
        h5group: ``h5py.Group``
            Main group to write the TargetObject into.
        kwargs: ``dict``
            keyword argument dictionary.
        """
        # Call to parent class _hsp_write() : write UUID, etc.
        super(TargetObject, self)._hsp_write(h5group, **kwargs)

        # Write target object name
        self._hsp_write_attribute(h5group, ('name', self._name), **kwargs)

        # Write target object description, if defined
        self._hsp_write_attribute(h5group, ('description', self._description), **kwargs)

        # Write target object properties
        self._hsp_write_object_list(h5group, "OBJ_PROPERTIES", self._obj_properties, "obj_prop_", **kwargs)

        # Write target object property groups
        self._hsp_write_object_list(h5group, "OBJ_PROPERTY_GROUPS", self._obj_property_groups, "obj_prop_group_",
                                    **kwargs)

        self._hsp_write_callback(str(self), **kwargs)

    @classmethod
    def _hsp_read(cls, h5group, version, dependency_objdict=None):
        """
        Read a TargetObject instance from a HDF5 file (*.h5).

        Parameters
        ----------
        h5group: ``h5py.Group``
            Main group to read the object from.
        version: ``int``
            version of the object to read.
        dependency_objdict: ``dict``
            dependency object dictionary. Default None

        Returns
        -------
        targobj: ``TargetObject``
            Read TargetObject instance
        """
        # Handle different versions here

        # Fetch Hdf5StudyPersistent object UUID
        uid = super(TargetObject, cls)._hsp_read(h5group, version, dependency_objdict=dependency_objdict)

        # Read target object name
        name = cls._hsp_read_attribute(h5group, 'name', "generic result name")

        # Create target object
        targobj = cls(uid=uid, name=name)

        # Build object property list and add each property into its target object property list + build target object
        # property dictionary indexed by their UUID
        if ObjectProperty.__name__ not in dependency_objdict:
            dependency_objdict[ObjectProperty.__name__] = {}
        obj_prop_dict = dependency_objdict[ObjectProperty.__name__]
        for p in ObjectProperty._hsp_read_object_list(h5group, "OBJ_PROPERTIES", "obj_prop_", "target object property",
                                                      dependency_objdict=dependency_objdict):
            obj_prop_dict[p.uid] = p
            targobj.object_properties.add(p)

        # Build object property group list and add each property group into the target object
        for pgroup in ObjectPropertyGroup._hsp_read_object_list(h5group, "OBJ_PROPERTY_GROUPS", "obj_prop_group_",
                                                                "target object property groups",
                                                                dependency_objdict=dependency_objdict):
            targobj.property_groups.add(pgroup)

        # Read target object description, if defined
        targobj_desc = cls._hsp_read_attribute(h5group, 'description', "target object description",
                                               raise_error_if_not_found=False)
        if targobj_desc is not None:
            targobj.description = targobj_desc

        return targobj

    def galactica_validity_check(self, **kwargs):
        """
        Perform validity checks on this  instance and eventually log warning messages.

        Parameters
        ----------
        kwargs: :obj:`dict`
            keyword arguments (optional)
        """
        # Check target object name
        if len(self._name) > 32:
            log.warning("{t!s} name is too long for Galactica (max. 32 characters).".format(t=self))

        # Check target object property and object property groups validity
        self._obj_properties.galactica_validity_check(**kwargs)
        self._obj_property_groups.galactica_validity_check(**kwargs)

    def __unicode__(self):
        """
        String representation of the instance
        """
        return "'{targobj_name:s}' target object".format(targobj_name=self._name)


__all__ = ["ObjectProperty", "ObjectPropertyGroup", "TargetObject", "PropertySortFlag", "PropertyFilterFlag"]
