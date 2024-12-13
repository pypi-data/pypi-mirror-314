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
from future.builtins import str, list, int
import logging

from .generic import GenericResult
from astrophysix.utils.strings import Stringifiable
from astrophysix import units as U
from ..services import DataProcessingService
from ..utils import ObjectList

log = logging.getLogger("astrophysix.simdm")


class Snapshot(GenericResult):
    """
    Experiment snapshot class (Simulation data model)

    Parameters
    ----------
    name: :obj:`string`
        snapshot name (mandatory)
    description: :obj:`string`
        snapshot description
    directory_path: :obj:`string`
        snapshot directory path
    time: (:obj:`float`, :class:`~astrophysix.units.unit.Unit`) :obj:`tuple`
        snapshot time info (value, unit) tuple
    physical_size: (:obj:`float`, :class:`~astrophysix.units.unit.Unit`) :obj:`tuple`
        snapshot physical size info (value, unit) tuple
    data_reference: :obj:`string`
        snapshot data reference (e.g. data directory name, snapshot number) string
    """
    _hsp_version = 2  # With data processing services
    def __init__(self, **kwargs):
        super(Snapshot, self).__init__(**kwargs)
        self._time = 0.0
        self._time_unit = U.none
        self._phys_size = 0.0
        self._phys_size_unit = U.none
        self._data_reference = ""
        self._proc_services = ObjectList(DataProcessingService, "hosted_service")

        if "time" in kwargs:
            self.time = kwargs["time"]

        if "physical_size" in kwargs:
            self.physical_size = kwargs["physical_size"]

        if "data_reference" in kwargs:
            self.data_reference = kwargs["data_reference"]

    def __eq__(self, other):
        """
        Snapshot comparison method

        other: :class:`~astrophysix.simdm.results.snapshot.Snapshot`
            snapshot to compare to
        """
        if not super(Snapshot, self).__eq__(other):
            return False

        otime, otime_unit = other.time
        if self._time != otime or self._time_unit != otime_unit or self._time_unit.name != otime_unit.name:
            return False

        opsize, opsize_unit = other.physical_size
        if self._phys_size != opsize or self._phys_size_unit != opsize_unit or \
                self._phys_size_unit.name != opsize_unit.name:
            return False

        if self._data_reference != other.data_reference:
            return False

        if self._proc_services != other.processing_services:
            return False

        return True

    @property
    def time(self):
        """Snapshot time info (value, unit) tuple . Can be set to a :obj:`float` value (unitless) or a
        (:obj:`float`, :class:`~astrophysix.units.unit.Unit`) tuple.

        Example
        -------
            >>> sn = Snapshot(name="My super snapshot")
            >>> sn.time = "0.256"
            >>> sn.time[1] == U.none
            True
            >>> sn.time = ("0.24", U.year)
            >>> sn.time = ("0.45", "Myr")
            >>> sn.time[1] == U.Myr
            True
            >>> sn.time = (7.89e2, "Gyr")
            >>> sn.time = (78.54, U.min)
        """
        return self._time, self._time_unit

    @time.setter
    def time(self, new_time):
        if isinstance(new_time, tuple) or isinstance(new_time, list):
            if len(new_time) != 2:
                err_msg = "Snapshot 'time' property cannot be of length != 2"
                log.error(err_msg)
                raise AttributeError(err_msg)
            t_val, t_unit = new_time

            if not isinstance(t_unit, U.Unit):
                try:
                    s = Stringifiable.cast_string(t_unit, valid_empty=False)
                    t_unit = U.Unit.from_name(s)
                except TypeError:  # Not a valid string
                    err_msg = "Snapshot 'time' property must be defined with a valid (non-empty) time unit string."
                    log.error(err_msg)
                    raise AttributeError(err_msg)
                except AttributeError as aerr:
                    err_msg = "Snapshot 'time' property error : {uerr:s}.".format(uerr=str(aerr))
                    log.error(err_msg)
                    raise AttributeError(err_msg)

            if t_unit.physical_type not in ["time", "dimensionless"]:
                err_msg = "Error while setting {cn:s} 'time' property : unit is not a valid time unit (physical " \
                          "type: '{pt:s}')".format(pt=t_unit.physical_type, cn=self.__class__.__name__)
                log.error(err_msg)
                raise AttributeError(err_msg)

            self._time_unit = t_unit
        else:
            self._time_unit = U.none
            t_val = new_time

        try:
            self._time = float(t_val)
        except ValueError:
            err_msg = "Snapshot 'time' property must be set as a (time_float_value, time_unit) tuple."
            log.error(err_msg)
            raise AttributeError(err_msg)
        except TypeError:
            err_msg = "Snapshot 'time' property must be set as a (time_float_value, time_unit) tuple."
            log.error(err_msg)
            raise AttributeError(err_msg)

    @property
    def physical_size(self):
        """
        Snapshot physical size info (value, unit) tuple . Can be set to a :obj:`float` value (unitless) or a
        (:obj:`float`, :class:`~astrophysix.units.unit.Unit`) tuple.

        Example
        -------
            >>> sn = Snapshot(name="My super snapshot")
            >>> sn.physical_size = "0.256"
            >>> sn.physical_size = ("0.24", U.pc)
            >>> sn.physical_size = ("0.45", "kpc")
            >>> sn.physical_size[1] == U.kpc
            True
            >>> sn.physical_size = 4.46
            >>> sn.physical_size = (7.89e2, "Mpc")
            >>> sn.physical_size[1] == U.Mpc
            True
            >>> sn.physical_size = (78.54, U.ly)
        """
        return self._phys_size, self._phys_size_unit

    @physical_size.setter
    def physical_size(self, new_psize):
        if isinstance(new_psize, tuple) or isinstance(new_psize, list):
            if len(new_psize) != 2:
                err_msg = "Snapshot 'physical_size' property cannot be of length != 2"
                log.error(err_msg)
                raise AttributeError(err_msg)
            s_val, s_unit = new_psize

            if not isinstance(s_unit, U.Unit):
                try:
                    s = Stringifiable.cast_string(s_unit, valid_empty=False)
                    s_unit = U.Unit.from_name(s)
                except TypeError:  # Not a valid string
                    err_msg = "Snapshot 'physical_size' property must be defined with a valid (non-empty) length " \
                              "unit string."
                    log.error(err_msg)
                    raise AttributeError(err_msg)
                except AttributeError as aerr:
                    err_msg = "Snapshot 'physical_size' property error : {uerr:s}.".format(uerr=str(aerr))
                    log.error(err_msg)
                    raise AttributeError(err_msg)

            if s_unit.physical_type not in ["length", "dimensionless"]:
                err_msg = "Error while setting Snaphsot 'physical_size' property : unit is not a valid length unit " \
                          "(physical type: '{pt:s}')".format(pt=s_unit.physical_type)
                log.error(err_msg)
                raise AttributeError(err_msg)

            self._phys_size_unit = s_unit
        else:
            self._phys_size_unit = U.none
            s_val = new_psize

        try:
            self._phys_size = float(s_val)
        except ValueError:
            err_msg = "Snapshot 'physical_size' property must be set as a (size_float_value, length_unit) tuple."
            log.error(err_msg)
            raise AttributeError(err_msg)
        except TypeError:
            err_msg = "Snapshot 'physical_size' property must be set as a (size_float_value, length_unit) tuple."
            log.error(err_msg)
            raise AttributeError(err_msg)

    @property
    def data_reference(self):
        """Snapshot data reference (e.g. data directory name, snapshot number). Can be set to any :obj:`string` value."""
        return self._data_reference

    @data_reference.setter
    def data_reference(self, new_data_ref):
        try:
            self._data_reference = Stringifiable.cast_string(new_data_ref, valid_empty=True)
        except TypeError:
            err_msg = "{cname:s} 'data_reference' property is not a valid string.".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

    @property
    def processing_services(self):
        """:class:`~astrophysix.simdm.services.process.DataProcessingService` list
        (:class:`~astrophysix.simdm.utils.ObjectList`)"""
        return self._proc_services

    def _can_add_catalog(self, new_cat):
        """
        Catalog addition validity check method. Overrides GenericResult._can_add_catalog()

        Parameters
        ----------
        new_cat: :class:`~astrophysix.simdm.catalogs.catalog.Catalog`
            new Catalog to add into the Snapshot
        """
        pass

    def _can_add_data_proc_service_in_catalog(self, cat_data_proc_service):
        """
        CatalogDataProcessingService addition validity check method. Verifies that the added catalog data processing
        service is added into a Snapshot's catalog.

        Parameters
        ----------
        cat_data_proc_service: :class:`~astrophysix.simdm.services.process.CatalogDataProcessingService`
            new catalog <=> data processing service to add into this Catalog.
        """
        pass

    @classmethod
    def _hsp_valid_attributes(cls):
        """List of valid kwargs in __init__() method"""
        genres_valid_attrs = super(Snapshot, cls)._hsp_valid_attributes()
        genres_valid_attrs += ["time", "physical_size", "data_reference"]
        return genres_valid_attrs

    def _hsp_write(self, h5group, **kwargs):
        """
        Serialize a Snapshot object into a HDF5 file.

        Parameters
        ----------
        h5group: ``h5py.Group``
            Main group to write the Snapshot into.
        kwargs: ``dict``
            keyword argument dictionary.
        """
        # Call to parent class _hsp_write()
        super(Snapshot, self)._hsp_write(h5group, **kwargs)

        # Write snapshot time
        self._hsp_write_attribute(h5group, ('time', self._time), **kwargs)
        self._hsp_write_attribute(h5group, ('time_unit', self._time_unit), **kwargs)

        # Write snapshot physical size
        self._hsp_write_attribute(h5group, ('phys_size', self._phys_size), **kwargs)
        self._hsp_write_attribute(h5group, ('phys_size_unit', self._phys_size_unit), **kwargs)

        # Write snapshot data reference
        self._hsp_write_attribute(h5group, ("data_reference", self._data_reference), **kwargs)

        # Write processing services, if any defined
        self._hsp_write_object_list(h5group, "SERVICES", self._proc_services, "service_", **kwargs)

    @classmethod
    def _hsp_read(cls, h5group, version, dependency_objdict=None):
        """
        Read a Snapshot object from a HDF5 file (*.h5).

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
        sn: ``Snapshot``
            Read Snapshot instance
        """
        # Handle different versions here

        # Read Hdf5StudyPersistent object
        sn = super(Snapshot, cls)._hsp_read(h5group, version, dependency_objdict=dependency_objdict)

        # Read snapshot time
        t_value = cls._hsp_read_attribute(h5group, 'time', "snapshot time")
        t_unit = cls._hsp_read_unit(h5group, 'time_unit')
        if t_unit is U.none:
            sn.time = t_value
        else:
            sn.time = (t_value, t_unit)

        # Read snapshot physical size
        s_value = cls._hsp_read_attribute(h5group, 'phys_size', "snapshot size")
        s_unit = cls._hsp_read_unit(h5group, 'phys_size_unit')
        if s_unit is U.none:
            sn.physical_size = s_value
        else:
            sn.physical_size = (s_value, s_unit)

        # Read snapshot data reference
        sn.data_reference = cls._hsp_read_attribute(h5group, "data_reference", "data reference")

        # Build data processing service list and add each data processing service into the snapshot, if any defined
        if version >= 2 and "SERVICES" in h5group:
            for service in DataProcessingService._hsp_read_object_list(h5group, "SERVICES", "service_",
                                                                       "snapshot data processing service",
                                                                       dependency_objdict=dependency_objdict):
                sn.processing_services.add(service)

        return sn

    def galactica_validity_check(self, **kwargs):
        """
        Perform validity checks on this instance and eventually log warning messages.

        Parameters
        ----------
        kwargs: :obj:`dict`
            keyword arguments (optional)
        """
        super(Snapshot, self).galactica_validity_check(**kwargs)

        # Check time value
        if self._time < -10000.0 or self._time > 10000.0:
            log.warning("{sn!s} time value must be defined in the range [-10000.0, 10000.0].".format(sn=self))

        # Check physical size value
        if self._phys_size < 0.0 or self._phys_size > 10000.0:
            log.warning("{sn!s} physical size value must be defined in the range [0.0, 10000.0].".format(sn=self))

        # Check data reference is not too long
        if len(self._data_reference) > 64:
            log.warning("{sn!s} data reference is too long (max. 64 characters).".format(sn=self))

        # Check data reference is filled if linked to a processing service
        if len(self._proc_services) > 0 and len (self._data_reference) == 0:
            log.warning("{sn!s} data reference is not defined while data processing services are bound "
                        "to it.".format(sn=self))

        # Perform validity checks on processing service list
        self._proc_services.galactica_validity_check(**kwargs)

    def __unicode__(self):
        """
        String representation of the instance
        """
        s = "'{sn_name:s}' snapshot".format(sn_name=self._name)
        return s


__all__ = ["Snapshot"]
