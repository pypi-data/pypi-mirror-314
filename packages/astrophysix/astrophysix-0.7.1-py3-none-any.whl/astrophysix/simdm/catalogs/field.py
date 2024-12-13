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
import numpy as N
import pandas as pd
from future.builtins import str, list, int
import logging

from .targobj import ObjectProperty, PropertyFilterFlag
from ..utils import GalacticaValidityCheckMixin, DataType
from astrophysix.utils import Hdf5StudyPersistent, Stringifiable, NumpyUtil


log = logging.getLogger("astrophysix.simdm")


class CatalogField(Hdf5StudyPersistent, GalacticaValidityCheckMixin, Stringifiable):
    def __init__(self, *args, **kwargs):
        """
        Object catalog field class

        Parameters
        ----------
        obj_prop: :class:`~astrophysix.simdm.catalogs.targobj.ObjectProperty`
            target object property (mandatory)
        values: 1D :class:`numpy.ndarray`
            catalog field value series/1D array (mandatory)
        """
        super(CatalogField, self).__init__(**kwargs)

        # Target object property
        self._obj_property = None
        if len(args) > 0:
            obj_prop = args[0]
        elif "obj_prop" in kwargs:
            obj_prop = kwargs["obj_prop"]
        else:
            raise AttributeError("Undefined 'obj_prop' object property attribute in "
                                 "{cname:s}.".format(cname=self.__class__.__name__))

        if not isinstance(obj_prop, ObjectProperty):
            err_msg = "{cname:s} 'obj_prop' attribute is not a valid ObjectProperty " \
                      "instance.".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)
        self._obj_property = obj_prop

        # Field values for all catalog items
        self._val_series = None
        self._values_md5sum = None
        self._values_min = None
        self._values_max = None
        self._values_mean = None
        self._values_std = None
        self._nobj = 0

        if not kwargs.get("hdf5_init", False):
            if "values" not in kwargs:
                raise AttributeError("Undefined 'values' property in {cname:s}.".format(cname=self.__class__.__name__))
            self.field_values = kwargs["values"]

    def __eq__(self, other):
        """
        CatalogField comparison method

        other: :class:`~astrophysix.simdm.catalogs.field.CatalogField`
            catalog field object to compare to
        """
        if not super(CatalogField, self).__eq__(other):
            return False

        # Compare target object property
        if self._obj_property != other.object_property:
            return False

        # Compare catalog field value MD5 sums
        if self._values_md5sum != other._values_md5sum:
            return False

        return True

    @property
    def property_name(self):
        """Associated target object property name"""
        return self._obj_property.property_name

    @property
    def object_property(self):
        """Associated target object property (:class:`~astrophysix.simdm.catalogs.targobj.ObjectProperty`)"""
        return self._obj_property

    @property
    def field_values(self):
        """
        Catalog field values. Can be edited.

        Returns
        -------
        vals: :obj:`1D numpy.ndarray`
        """
        self._hsp_lazy_read()
        return self._val_series

    @field_values.setter
    def field_values(self, new_vals):
        """
        Set catalog field values arrays. The new array must be of size strictly positive and leave the its size
        unchanged.

        Parameters
        ----------
        new_vals: :obj:`1D numpy.ndarray`
            catalog field value 1D array

        Raises
        ------
        Aerr: :class:`AttributeError`
            an error is raised if the new array does not contain any value or if its size is different from the previous
            value array.

        Example
        -------

            >>> pass
        """
        # Record new catalog field value array
        try:
            NumpyUtil.check_is_array(new_vals, ndim=1)
        except AttributeError:
            err_msg = "'values' {cname:s} attribute must be a 1-dimensional " \
                      "array.".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

        # Check data type
        kind = NumpyUtil.check_dtype(new_vals)
        if kind is None:
            err_msg = "'values' {cname:s} attribute must contain boolean/float/integer/string " \
                      "data.".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

        if self._nobj == 0:  # CatalogField initialisation
            # Array size => number of items in catalog
            if new_vals.size == 0:  # No value in catalog field !
                err_msg = "{cname:s} 'values' array need at least 1 value.".format(cname=self.__class__.__name__)
                log.error(err_msg)
                raise AttributeError(err_msg)
            self._nobj = new_vals.size
        else:  # Field values were previously set. This is an update.
            # Check that array size (number of catalog items) is unchanged
            if self._nobj != new_vals.size:
                err_msg = "The number of items in this {cname:s} is {no:d} and cannot be " \
                          "changed.".format(no=self._nobj, cname=self.__class__.__name__)
                log.error(err_msg)
                raise AttributeError(err_msg)
        self._val_series = N.ascontiguousarray(new_vals.copy())  # Make a copy so that external modification won't impact the catalog field
        if kind == "s":  # String data array
            # Force string dataset encoding as bytes (h5py compatibility, numpy string "U<8" is not supported)
            self._val_series = self._val_series.astype("S")

            self._values_min = 0.0
            self._values_max = 0.0
            self._values_std = 0.0
            self._values_mean = 0.0
        else:
            self._values_max = self._val_series.max()
            self._values_min = self._val_series.min()
            self._values_mean = self._val_series.mean()
            self._values_std = self._val_series.std()

        self._values_md5sum = NumpyUtil.md5sum(new_vals)

        # Flag the CatalogField instance as 'loaded in memory' to avoid reading data from HDF5 study file in the future
        self._hsp_set_lazy_read()

    @property
    def field_values_md5sum(self):
        return self._values_md5sum

    @property
    def field_value_stats(self):
        """Returns (min., max., mean, std) tuple for this field value array"""
        return self._values_min, self._values_max, self._values_mean, self._values_std

    @property
    def nobjects(self):
        """Returns the number of objects in this catalog field => size of the field value 1D array"""
        return self._nobj

    def to_pandas(self):
        """
        Convert a CatalogField into a :class:`pandas.Series` object
        """
        return pd.Series(data=self.field_values, name=self.object_property.display_name, index=range(1, self._nobj+1))

    @classmethod
    def _hsp_valid_attributes(cls):
        """List of valid kwargs in __init__() method"""
        return ["obj_prop", "hdf5_init", "values"]

    def _hsp_write(self, h5group, **kwargs):
        """
        Serialize a CatalogField object into a HDF5 file.

        Parameters
        ----------
        h5group: ``h5py.Group``
            Main group to write the CatalogField into.
        kwargs: ``dict``
            keyword argument dictionary.
        """
        # Call to parent class _hsp_write() : write UUID, etc.
        super(CatalogField, self)._hsp_write(h5group, **kwargs)

        # Write object property UUID
        self._hsp_write_attribute(h5group, ('object_property_uid', self._obj_property.uid), **kwargs)

        # Write catalog field values + stats attributes
        values_attribute_name = "_val_series"  # => self._val_series
        write_values = self._hsp_write_dataset(h5group, ("field_values", values_attribute_name),
                                               md5sum_params=("field_values_md5sum", self._values_md5sum), **kwargs)

        self._hsp_write_attribute(h5group, ('nobjects', self._nobj), **kwargs)
        self._hsp_write_attribute(h5group, ('field_value_min', self._values_min), **kwargs)
        self._hsp_write_attribute(h5group, ('field_value_max', self._values_max), **kwargs)
        self._hsp_write_attribute(h5group, ('field_value_mean', self._values_mean), **kwargs)
        self._hsp_write_attribute(h5group, ('field_value_std', self._values_std), **kwargs)

        if write_values:
            self._hsp_write_callback(str(self), **kwargs)

    @classmethod
    def _hsp_read(cls, h5group, version, dependency_objdict=None):
        """
        Read a CatalogField object from a HDF5 file (*.h5).

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
        catalog: ``CatalogField``
            Read CatalogField instance
        """
        # Handle different versions here

        # Fetch Hdf5StudyPersistent object UUID
        uid = super(CatalogField, cls)._hsp_read(h5group, version, dependency_objdict=dependency_objdict)

        # Try to read/find protocol
        try:
            objprop_uid = uuid.UUID(cls._hsp_read_attribute(h5group, "object_property_uid", "object property UUID",
                                                            raise_error_if_not_found=True))

            # Search for already instantiated object property in dependency object dictionary
            if dependency_objdict is None or ObjectProperty.__name__ not in dependency_objdict:
                err_msg = "Cannot find any object property already instantiated in the project."
                log.error(err_msg)
                raise IOError(err_msg)

            # Find protocol according to its UUID
            objprop_dict = dependency_objdict[ObjectProperty.__name__]
            if objprop_uid not in objprop_dict:
                err_msg = "Cannot find object property with uid {uid:s}.".format(uid=str(objprop_uid))
                log.error(err_msg)
                raise IOError(err_msg)

            obj_prop = objprop_dict[objprop_uid]
        except IOError:  # Protocol UUID not found in Catalog field
            raise

        # Create catalog field object
        cf = cls(uid=uid, obj_prop=obj_prop, hdf5_init=True)

        # Read field value array MD5 sum + stats attributes
        cf._values_md5sum = cls._hsp_read_attribute(h5group, "field_values_md5sum", "catalog field value array md5sum",
                                                    raise_error_if_not_found=True)
        cf._nobj = cls._hsp_read_attribute(h5group, "nobjects", "number of objects",
                                           raise_error_if_not_found=True)
        cf._values_min = cls._hsp_read_attribute(h5group, "field_value_min", "field min. value",
                                                 raise_error_if_not_found=True)
        cf._values_max = cls._hsp_read_attribute(h5group, "field_value_max", "field max. value",
                                                 raise_error_if_not_found=True)
        cf._values_mean = cls._hsp_read_attribute(h5group, "field_value_mean", "field mean. value",
                                                  raise_error_if_not_found=True)
        cf._values_std = cls._hsp_read_attribute(h5group, "field_value_std", "field std. value",
                                                 raise_error_if_not_found=True)

        # Set HDF5 group/file info for lazy I/O
        cf._hsp_set_lazy_source(h5group)

        return cf

    def _hsp_lazy_read_data(self, h5group):
        """
        Lazy read method to load field values from HDF5 file (*.h5)

        Parameters
        ----------
        h5group: `h5py.Group`
        """
        # Read field value array
        self._val_series = self._hsp_read_dataset(h5group, "field_values", "catalog field value array",
                                                  raise_error_if_not_found=True)

    def galactica_validity_check(self, **kwargs):
        """
        Perform validity checks on this instance and eventually log warning messages.

        Parameters
        ----------
        kwargs: :obj:`dict`
            keyword arguments (optional)
        """
        if self._obj_property.filter_flag in [PropertyFilterFlag.BASIC_FILTER, PropertyFilterFlag.ADVANCED_FILTER] and\
                self._obj_property.datatype not in [DataType.REAL, DataType.INTEGER]:
            log.warning("Can only filter numerical fields.")

    def __unicode__(self):
        """
        String representation of the instance
        """
        return "'{pname:s}' catalog field".format(pname=self.property_name)


__all__ = ["CatalogField"]
