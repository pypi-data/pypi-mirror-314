# -*- coding: utf-8 -*-
#   This file is part of Horus.
#
#   Horus is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Horus is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Horus.  If not, see <http://www.gnu.org/licenses/>.
"""
.. autoclass:: astrophysix.simdm.experiment.ResolvedPhysicalProcess
    :members:
    :undoc-members:
    :inherited-members:
    :exclude-members: open_h5file, is_type_string, hsp_save_to_h5, cast_string, hsp_load_from_h5,
                      INVALID_ALIAS_ERROR_MESSAGE, VALID_ALIAS_REGEX
"""
from __future__ import absolute_import, unicode_literals
from future.builtins import str
import logging
import uuid

from astrophysix.utils.persistency import Hdf5StudyPersistent
from astrophysix.utils.strings import Stringifiable

from ..protocol import PhysicalProcess
from ..utils import GalacticaValidityCheckMixin

log = logging.getLogger("astrophysix.simdm")


class ResolvedPhysicalProcess(Hdf5StudyPersistent, GalacticaValidityCheckMixin, Stringifiable):
    """
    Simulation resolved physical process class

    Parameters
    ----------
    physics: :class:`~astrophysix.simdm.protocol.PhysicalProcess`
        simulation code's :class:`~astrophysix.simdm.protocol.PhysicalProcess` instance (mandatory)
    details: :obj:`string`
        resolved physical process implementation details
    """
    def __init__(self, **kwargs):
        super(ResolvedPhysicalProcess, self).__init__(**kwargs)

        # Simulation associated physical process
        if "physics" not in kwargs:
            raise AttributeError("ResolvedPhysicalProcess 'physics' attribute is not defined (mandatory).")
        phys = kwargs["physics"]
        if not isinstance(phys, PhysicalProcess):
            raise AttributeError("ResolvedPhysicalProcess 'physics' attribute is not a valid PhysicalProcess object.")
        self._physics = phys

        # Resolved physical process implementation details
        self._details = ""
        if "details" in kwargs:
            self.implementation_details = kwargs["details"]

    def __eq__(self, other):
        """
        ResolvedPhysicalProcess comparison method

        other: :class:`~astrophysix.simdm.experiment.ResolvedPhysicalProcess`
            resolved physical process to compare to
        """
        if not super(ResolvedPhysicalProcess, self).__eq__(other):
            return False

        if self._physics != other.physical_process:
            return False

        if self._details != other.implementation_details:
            return False

        return True

    @property
    def physical_process(self):
        """Simulation code's :class:`~astrophysix.simdm.protocol.PhysicalProcess`. Cannot be edited after instance
        initialisation"""
        return self._physics

    @property
    def process_name(self):
        """Simulation code's :class:`~astrophysix.simdm.protocol.PhysicalProcess` name. Cannot be edited."""
        return self._physics.name

    @property
    def implementation_details(self):
        """Resolved physical process implementation details. Editable."""
        return self._details

    @implementation_details.setter
    def implementation_details(self, new_details):
        try:
            self._details = Stringifiable.cast_string(new_details)
        except TypeError:
            err_msg = "{cname:s} 'implementation_details' property is not a valid string.".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

    @classmethod
    def _hsp_valid_attributes(cls):
        """List of valid kwargs in __init__() method"""
        return ["physics", "details"]

    def _hsp_write(self, h5group, **kwargs):
        """
        Serialize a ResolvedPhysicalProcess object into a HDF5 file.

        Parameters
        ----------
        h5group: ``h5py.Group``
            Main group to write the ResolvedPhysicalProcess into.
        kwargs: ``dict``
            keyword argument dictionary.
        """
        # Call to parent class _hsp_write() : write UUID, etc.
        super(ResolvedPhysicalProcess, self)._hsp_write(h5group, **kwargs)

        # Write algorithm UUID
        self._hsp_write_attribute(h5group, ('physics_uid', self._physics.uid), **kwargs)

        # Write applied algorithm implementation details, if defined
        self._hsp_write_attribute(h5group, ('details', self._details), **kwargs)

    @classmethod
    def _hsp_read(cls, h5group, version, dependency_objdict=None):
        """
        Read a ResolvedPhysicalProcess object from a HDF5 file (*.h5).

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
        res_phys: ``ResolvedPhysicalProcess``
            Read ResolvedPhysicalProcess instance
        """
        # Handle different versions here

        # Fetch Hdf5StudyPersistent object UUID
        uid = super(ResolvedPhysicalProcess, cls)._hsp_read(h5group, version, dependency_objdict=dependency_objdict)

        # Read algorithm UUID
        phys_uid = uuid.UUID(cls._hsp_read_attribute(h5group, 'physics_uid', "physical process UUID"))
        protocol = list(dependency_objdict.values())[0]
        found_pproc = protocol.physical_processes.find_by_uid(phys_uid)
        if found_pproc is None:
            err_msg = "Unknown physical process UUID '{puid!s}' in the {proto!s}.".format(puid=phys_uid, proto=protocol)
            log.error(err_msg)
            raise IOError(err_msg)

        # Create resolved physical process object
        res_phys = cls(uid=uid, physics=found_pproc)

        # Read resolved physical process implementation details, if defined
        phys_details = cls._hsp_read_attribute(h5group, 'details', "physical process implementation details",
                                               raise_error_if_not_found=False)
        if phys_details is not None:
            res_phys.implementation_details = phys_details

        return res_phys

    def __unicode__(self):
        """
        String representation of the instance
        """
        s = "[{resphys_name:s}] resolved physical process".format(resphys_name=self._physics.name)
        return s


__all__ = ["ResolvedPhysicalProcess"]
