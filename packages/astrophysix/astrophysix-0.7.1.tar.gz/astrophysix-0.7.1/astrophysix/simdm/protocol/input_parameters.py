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

.. autoclass:: astrophysix.simdm.protocol.InputParameter
    :members:
    :undoc-members:
    :inherited-members:
    :exclude-members: open_h5file, is_type_string, hsp_save_to_h5, cast_string, hsp_load_from_h5,
                      INVALID_ALIAS_ERROR_MESSAGE, VALID_ALIAS_REGEX

"""
from __future__ import absolute_import, unicode_literals
from future.builtins import str, list, dict
import logging

from astrophysix.simdm.utils import GalacticaValidityCheckMixin
from astrophysix.utils.persistency import Hdf5StudyPersistent
from astrophysix.utils.strings import Stringifiable

log = logging.getLogger("astrophysix.simdm")


class InputParameter(Hdf5StudyPersistent, GalacticaValidityCheckMixin, Stringifiable):
    """
    Protocol input parameter

    Parameters
    ----------
    name: :obj:`string`
        input parameter name (mandatory)
    key: :obj:`string`
        input parameter configuration key
    description: :obj:`string`
        input parameter description
    """
    def __init__(self, **kwargs):
        super(InputParameter, self).__init__(**kwargs)

        self._key = ""
        self._name = ""
        self._description = ""

        if "name" not in kwargs:
            raise AttributeError("Input parameter 'name' attribute is not defined (mandatory).")
        self.name = kwargs["name"]

        if "key" in kwargs:
            self.key = kwargs["key"]

        if "description" in kwargs:
            self.description = kwargs["description"]

    def __eq__(self, other):
        """
        InputParameter comparison method

        other: :class:`~astrophysix.simdm.protocol.InputParameter`
            input parameter to compare to
        """
        if not super(InputParameter, self).__eq__(other):
            return False

        if self._name != other.name:
            return False

        if self._key != other.key:
            return False

        if self._description != other.description:
            return False

        return True

    @property
    def key(self):
        """Input parameter configuration key"""
        return self._key

    @key.setter
    def key(self, new_key):
        try:
            self._key = Stringifiable.cast_string(new_key)
        except TypeError:
            raise AttributeError("Input parameter 'key' property is not a valid string.")

    @property
    def name(self):
        """Input parameter name"""
        return self._name

    @name.setter
    def name(self, new_name):
        try:
            self._name = Stringifiable.cast_string(new_name, valid_empty=False)
        except TypeError:
            raise AttributeError("Input parameter 'name' property is not a valid (non empty) string.")

    @property
    def description(self):
        """Input parameter description"""
        return self._description

    @description.setter
    def description(self, new_descr):
        try:
            self._description = Stringifiable.cast_string(new_descr)
        except TypeError:
            raise AttributeError("Input parameter 'description' property is not a valid string.")

    @classmethod
    def _hsp_valid_attributes(cls):
        """List of valid kwargs in __init__() method"""
        return ["name", "key", "description"]

    def _hsp_write(self, h5group, **kwargs):
        """
        Serialize an InputParameter object into a HDF5 file.

        Parameters
        ----------
        h5group: ``h5py.Group``
            Main group to write the InputParameter into.
        kwargs: ``dict``
            keyword argument dictionary.
        """
        # Call to parent class _hsp_write() : write UUID, etc.
        super(InputParameter, self)._hsp_write(h5group, **kwargs)

        # Write input parameter key
        self._hsp_write_attribute(h5group, ('key', self._key), **kwargs)

        # Write input parameter name, if defined
        self._hsp_write_attribute(h5group, ('name', self._name), **kwargs)

        # Write input parameter description, if defined
        self._hsp_write_attribute(h5group, ('description', self._description), **kwargs)

    @classmethod
    def _hsp_read(cls, h5group, version, dependency_objdict=None):
        """
        Read an InputParameter object from a HDF5 file (*.h5).

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
        exp: ``InputParameter``
            Read InputParameter instance
        """
        # Handle different versions here

        # Fetch Hdf5StudyPersistent object UUID
        uid = super(InputParameter, cls)._hsp_read(h5group, version, dependency_objdict=dependency_objdict)

        # Read input parameter key
        ip_name = cls._hsp_read_attribute(h5group, 'name', "input parameter name")

        # Create input parameter object
        ip = cls(uid=uid, name=ip_name)

        # Read input parameter key, if defined
        ip_key = cls._hsp_read_attribute(h5group, 'key', "input parameter key", raise_error_if_not_found=False)
        if ip_key is not None:
            ip.key = ip_key

        # Read input parameter description, if defined
        ip_descr = cls._hsp_read_attribute(h5group, 'description', "input parameter description",
                                           raise_error_if_not_found=False)
        if ip_descr is not None:
            ip.description = ip_descr

        return ip

    def galactica_validity_check(self, **kwargs):
        """
        Perform validity checks on this instance and eventually log warning messages.

        Parameters
        ----------
        kwargs: :obj:`dict`
            keyword arguments (optional)
        """
        # Check input parameter name
        if len(self._name) == 0:
            log.warning("{p!s} Galactica input parameter name is missing.".format(p=self))
        elif len(self._name) > 64:
            log.warning("{p!s} Galactica input parameter name is too long (max. 64 characters).".format(p=self))

        # Check input parameter key
        if len(self._key) > 16:
            log.warning("{p!s} Galactica input parameter key is too long (max. 16 characters).".format(p=self))

    def __unicode__(self):
        """
        String representation of the instance
        """
        s = "[{ipk:s}]".format(ipk=self._key)
        if len(self._name) > 0:
            s += " '{ipname:s}'".format(ipname=self._name)
        s += " input parameter"
        return s


__all__ = ["InputParameter"]
