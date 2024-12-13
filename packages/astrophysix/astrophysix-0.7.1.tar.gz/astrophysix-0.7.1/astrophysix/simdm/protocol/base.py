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
@startwbs

+ Simulation study
 + Project
  + Simulation codes
   +_ 'RAMSES 3.1 (MHD)' simulation code
    + Input parameters
    + Algorithms
    + Physical processes
   +_ 'AREPO' simulation code
    + Input parameters
    + Algorithms
    + Physical processes
  + Post-processing codes
   +_ 'RADMC-3D v2.0' post-processing code
    + Input parameters
    + Algorithms

@endwbs

"""
from __future__ import print_function, unicode_literals, division, absolute_import  # Python 2 and 3 compatibility
from future.builtins import str, list, dict
import logging
from ..utils import ObjectList, GalacticaValidityCheckMixin
from astrophysix.utils.strings import Stringifiable
from astrophysix.utils.persistency import Hdf5StudyPersistent
from .input_parameters import InputParameter
from .algorithm import Algorithm
from .physics import PhysicalProcess


__doc__ = """

:obj:`Protocol` is the generic term for a software tool used to conduct a numerical :obj:`Experiment`. There are two
different types of protocols :

* :class:`~astrophysix.simdm.protocol.SimulationCode`,
* :class:`~astrophysix.simdm.protocol.PostProcessingCode`.

.. autoclass:: astrophysix.simdm.protocol.SimulationCode
   :members:
   :undoc-members:
   :inherited-members:
   :exclude-members: open_h5file, is_type_string, hsp_save_to_h5, cast_string, hsp_load_from_h5, 
                      INVALID_ALIAS_ERROR_MESSAGE, VALID_ALIAS_REGEX

.. autoclass:: astrophysix.simdm.protocol.PostProcessingCode
   :members:
   :undoc-members:
   :inherited-members:
   :exclude-members: open_h5file, is_type_string, hsp_save_to_h5, cast_string, hsp_load_from_h5, 
                      INVALID_ALIAS_ERROR_MESSAGE, VALID_ALIAS_REGEX

"""

log = logging.getLogger("astrophysix.simdm")


class Protocol(Hdf5StudyPersistent, GalacticaValidityCheckMixin, Stringifiable):
    """
    Abstract Protocol class

    Parameters
    ----------
    name: ``string``
        protocol name (mandatory)
    code_name: ``string``
        code name (mandatory)
    alias: ``string``
        protocol alias
    url: ``string``
        reference URL
    code_version: ``string``
        code version
    description: ``string``
        protocol description
    """
    def __init__(self, **kwargs):
        super(Protocol, self).__init__(**kwargs)

        self._name = ""
        self._alias = ""
        self._url = ""
        self._code_name = ""
        self._code_version = ""
        self._description = ""

        self._inpparam_list = ObjectList(InputParameter, "name")
        self._algo_list = ObjectList(Algorithm, "name")

        if "name" not in kwargs:
            raise AttributeError("{cname:s} 'name' attribute is not defined (mandatory).".format(cname=self.__class__.__name__))
        self.name = kwargs["name"]

        if "code_name" not in kwargs:
            raise AttributeError("{cname:s} 'code_name' attribute is not defined (mandatory).".format(cname=self.__class__.__name__))
        self.code_name = kwargs["code_name"]

        if "alias" in kwargs:
            self.alias = kwargs["alias"]

        if "url" in kwargs:
            self.url = kwargs["url"]

        if "code_version" in kwargs:
            self.code_version = kwargs["code_version"]

        if "description" in kwargs:
            self.description = kwargs["description"]

    def __eq__(self, other):
        """
        Protocol comparison method

        other: :obj:`Protocol`
            Protocol to compare to
        """
        if not super(Protocol, self).__eq__(other):
            return False

        if self._name != other.name:
            return False

        if self._code_name != other.code_name:
            return False

        if self._alias != other.alias:
            return False

        if self._url != other.url:
            return False

        if self._code_version != other.code_version:
            return False

        if self._description != other.description:
            return False

        if self._inpparam_list != other.input_parameters:
            return False

        if self._algo_list != other.algorithms:
            return False

        return True

    @property
    def alias(self):
        """Protocol alias"""
        return self._alias

    @alias.setter
    def alias(self, new_alias):
        try:
            self._alias = Stringifiable.cast_string(new_alias)
        except TypeError:
            raise AttributeError("{cname:s} 'alias' property is not a valid "
                                 "string".format(cname=self.__class__.__name__))

    @property
    def name(self):
        """Protocol name"""
        return self._name

    @name.setter
    def name(self, new_protocol_name):
        try:
            self._name = Stringifiable.cast_string(new_protocol_name, valid_empty=False)
        except TypeError:
            raise AttributeError("{cname:s} 'name' property is not a valid (non empty) "
                                 "string.".format(cname=self.__class__.__name__))

    @property
    def code_name(self):
        """Protocol code name"""
        return self._code_name

    @code_name.setter
    def code_name(self, new_code_name):
        try:
            self._code_name = Stringifiable.cast_string(new_code_name, valid_empty=False)
        except TypeError:
            raise AttributeError("{cname:s} 'code_name' property is not a valid (non empty) "
                                 "string.".format(cname=self.__class__.__name__))

    @property
    def code_version(self):
        """Protocol code version"""
        return self._code_version

    @code_version.setter
    def code_version(self, new_code_version):
        try:
            self._code_version = Stringifiable.cast_string(new_code_version)
        except TypeError:
            raise AttributeError("{cname:s} 'code_version' property is not a valid "
                                 "string.".format(cname=self.__class__.__name__))

    @property
    def url(self):
        """Protocol code url"""
        return self._url

    @url.setter
    def url(self, new_url):
        try:
            self._url = Stringifiable.cast_string(new_url)
        except TypeError:
            raise AttributeError("{cname:s} 'url' property is not a valid "
                                 "string.".format(cname=self.__class__.__name__))

    @property
    def description(self):
        """Protocol description"""
        return self._description

    @description.setter
    def description(self, new_descr):
        try:
            self._description = Stringifiable.cast_string(new_descr)
        except TypeError:
            raise AttributeError("{cname:s} 'description' property is not a valid string.".format(cname=self.__class__.__name__))

    @property
    def input_parameters(self):
        """Protocol :class:`~astrophysix.simdm.protocol.InputParameter` list
        (:class:`~astrophysix.simdm.utils.ObjectList`)"""
        return self._inpparam_list

    @property
    def algorithms(self):
        """Protocol :class:`~astrophysix.simdm.protocol.Algorithm` list
        (:class:`~astrophysix.simdm.utils.ObjectList`)"""
        return self._algo_list

    @classmethod
    def _hsp_valid_attributes(cls):
        """List of valid kwargs in __init__() method"""
        return ["name", "code_name", "alias", "url", "code_version", "description"]

    def _hsp_write(self, h5group, **kwargs):
        """
        Serialize a Protocol object into a HDF5 file.

        Parameters
        ----------
        h5group: ``h5py.Group``
            Main group to write the Protocol into.
        kwargs: ``dict``
            keyword argument dictionary.
        """
        # Call to parent class _hsp_write() : write UUID, etc.
        super(Protocol, self)._hsp_write(h5group, **kwargs)

        # Write protocol name
        self._hsp_write_attribute(h5group, ('name', self._name), **kwargs)

        # Write protocol code name
        self._hsp_write_attribute(h5group, ('code_name', self._code_name), **kwargs)

        # Write protocol code version, if defined
        self._hsp_write_attribute(h5group, ('code_version', self._code_version), **kwargs)

        # Write protocol Galactica alias, if defined
        self._hsp_write_attribute(h5group, ('galactica_alias', self._alias), **kwargs)

        # Write protocol URL, if defined
        self._hsp_write_attribute(h5group, ('url', self._url), **kwargs)

        # Write protocol description, if defined
        self._hsp_write_attribute(h5group, ('description', self._description), **kwargs)

        # Write input parameters, if any defined
        self._hsp_write_object_list(h5group, "INPUT_PARAMS", self._inpparam_list, "inpparam_", **kwargs)

        # Write algorithms, if any defined
        self._hsp_write_object_list(h5group, "ALGORITHMS", self._algo_list, "algo_", **kwargs)

    @classmethod
    def _hsp_read(cls, h5group, version, dependency_objdict=None):
        """
        Read a Protocol object from a HDF5 file (*.h5).

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
        exp: ``Protocol``
            Read Protocol instance
        """
        # Handle different versions here

        # Fetch Hdf5StudyPersistent object UUID
        uid = super(Protocol, cls)._hsp_read(h5group, version, dependency_objdict=dependency_objdict)

        # Read protocol name
        name = cls._hsp_read_attribute(h5group, 'name', "protocol name")

        # Read protocol code name
        code_name = cls._hsp_read_attribute(h5group, 'code_name', "protocol code name")

        # Create protocol object
        prot = cls(uid=uid, name=name, code_name=code_name)

        # Read code version, if defined
        prot_codvers = cls._hsp_read_attribute(h5group, "code_version", "protocol code version",
                                               raise_error_if_not_found=False)
        if prot_codvers is not None:
            prot.code_version = prot_codvers

        # Read protocol Galactica alias, if defined
        palias = cls._hsp_read_attribute(h5group, 'galactica_alias', "protocol Galactica alias",
                                         raise_error_if_not_found=False)
        if palias is not None:
            prot.alias = palias

        # Read protocol URL, if defined
        prot_url = cls._hsp_read_attribute(h5group, 'url', "protocol URL", raise_error_if_not_found=False)
        if prot_url is not None:
            prot.url = prot_url

        # Read protocol description, if defined
        prot_descr = cls._hsp_read_attribute(h5group, 'description', "protocol description",
                                             raise_error_if_not_found=False)
        if prot_descr is not None:
            prot.description = prot_descr

        # Build input parameter list and add each input parameter into protocol, if any define
        if "INPUT_PARAMS" in h5group:
            for inpparam in InputParameter._hsp_read_object_list(h5group, "INPUT_PARAMS", "inpparam_",
                                                                 "protocol input parameter",
                                                                 dependency_objdict=dependency_objdict):
                prot.input_parameters.add(inpparam)

        # Build algorithm list and add each algorithm into protocol, if any defined
        if "ALGORITHMS" in h5group:
            for algo in Algorithm._hsp_read_object_list(h5group, "ALGORITHMS", "algo_", "protocol algorithm",
                                                        dependency_objdict=dependency_objdict):
                prot.algorithms.add(algo)

        return prot

    def galactica_validity_check(self, **kwargs):
        """
        Perform validity checks on this  instance and eventually log warning messages.

        Parameters
        ----------
        kwargs: :obj:`dict`
            keyword arguments (optional)
        """
        # Check protocol alias
        if len(self._alias) == 0:
            log.warning("{p!s} Galactica protocol alias is missing.".format(p=self))
        elif len(self._alias) > 16:
            log.warning("{p!s} Galactica protocol alias is too long (max. 16 characters).".format(p=self))
        else:
            err_msg = self.galactica_valid_alias(self._alias)
            if err_msg is not None:
                log.warning("{p!s} Galactica protocol alias is not valid ({m:s})".format(p=self, m=err_msg))

        # Check protocol name
        if len(self._name) == 0:
            log.warning("{p!s} Galactica protocol name is missing.".format(p=self))
        elif len(self._name) > 128:
            log.warning("{p!s} Galactica protocol name is too long (max. 128 characters).".format(p=self))

        # Check protocol code name
        if len(self._code_name) == 0:
            log.warning("{p!s} Galactica protocol code name is missing.".format(p=self))
        elif len(self._code_name) > 32:
            log.warning("{p!s} Galactica protocol code name is too long (max. 32 characters).".format(p=self))

        # Check protocol name
        if len(self._code_version) == 0:
            log.warning("{p!s} Galactica protocol code version is missing.".format(p=self))
        elif len(self._code_version) > 8:
            log.warning("{p!s} Galactica protocol code version is too long (max. 8 characters).".format(p=self))

        # Perform Galactica validity checks on input parameter/algorithm list
        self._inpparam_list.galactica_validity_check(**kwargs)
        self._algo_list.galactica_validity_check(**kwargs)

    def __unicode__(self):
        """
        String representation of the instance
        """
        if len(self._name) > 0:
            s = "[{name:s}]".format(name=self._name)
        elif len(self._alias) > 0:
            s = "[{alias:s}]".format(alias=self._alias)
        else:
            s = ""
        return s


class PostProcessingCode(Protocol):
    """
    Post-processing code

    Parameters
    ----------
    name: :obj:`string`
        name (mandatory)
    code_name: `:obj:`string`
        base code name (mandatory)
    alias: :obj:`string`
        code alias
    url: :obj:`string`
        reference URL
    code_version: :obj:`string`
        code version
    description: :obj:`string`
        code description
    """
    def __init__(self, **kwargs):
        super(PostProcessingCode, self).__init__(**kwargs)

    def __unicode__(self):
        """
        String representation of the instance
        """
        s = super(PostProcessingCode, self).__unicode__()
        if len(s) == 0:
            return "Post-processing code"
        else:
            s += " post-processing code"
            return s


class SimulationCode(Protocol):
    """
    Simulation code

    Parameters
    ----------
    name: :obj:`string`
        name (mandatory)
    code_name: :obj:`string`
        base code name (mandatory)
    alias: :obj:`string`
        code alias
    url: :obj:`string`
        reference URL
    code_version: :obj:`string`
        code version
    description: :obj:`string`
        code description
    """
    def __init__(self, **kwargs):
        super(SimulationCode, self).__init__(**kwargs)
        self._phys_procs_list = ObjectList(PhysicalProcess, "name")

    def __eq__(self, other):
        """
        SimulationCode comparison method

        other: :class:`~astrophysix.simdm.protocool.SimulationCode`
            simulation code to compare to
        """
        if not super(SimulationCode, self).__eq__(other):
            return False

        if self._phys_procs_list != other.physical_processes:
            return False

        return True

    @property
    def physical_processes(self):
        """Simulation code :class:`~astrophysix.simdm.protocol.PhysicalProcess` list
        (:class:`~astrophysix.simdm.utils.ObjectList`)"""
        return self._phys_procs_list

    def _hsp_write(self, h5group, **kwargs):
        """
        Serialize a SimulationCode object into a HDF5 file.

        Parameters
        ----------
        h5group: ``h5py.Group``
            Main group to write the SimulationCode into.
        kwargs: ``dict``
            keyword argument dictionary.
        """
        # Call to parent class _hsp_write()
        super(SimulationCode, self)._hsp_write(h5group, **kwargs)

        # Write physical processes, if any defined
        self._hsp_write_object_list(h5group, "PHYS_PROCS", self._phys_procs_list, "phys_proc_", **kwargs)

    @classmethod
    def _hsp_read(cls, h5group, version, dependency_objdict=None):
        """
        Read an SimulationCode object from a HDF5 file (*.h5).

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
        exp: ``SimulationCode``
            Read SimulationCode instance
        """
        # Handle different versions here

        # Read base Protocol object
        prot = super(SimulationCode, cls)._hsp_read(h5group, version, dependency_objdict=dependency_objdict)

        # Build applied physical process list and add each physical process into simulation code, if any defined
        if "PHYS_PROCS" in h5group:
            for phys_proc in PhysicalProcess._hsp_read_object_list(h5group, "PHYS_PROCS", "phys_proc_",
                                                                   "simulation code physical process",
                                                                   dependency_objdict=dependency_objdict):
                prot.physical_processes.add(phys_proc)

        return prot

    def galactica_validity_check(self, **kwargs):
        """
        Perform validity checks on this  instance and eventually log warning messages.

        Parameters
        ----------
        kwargs: :obj:`dict`
            keyword arguments (optional)
        """
        super(SimulationCode, self).galactica_validity_check(**kwargs)

        # Perform Galactica validity checks on physical process list
        self._phys_procs_list.galactica_validity_check(**kwargs)

    def __unicode__(self):
        """
        String representation of the instance
        """
        s = super(SimulationCode, self).__unicode__()
        if len(s) == 0:
            return "Simulation code"
        else:
            s += " simulation code"
            return s


__all__ = ["SimulationCode", "PostProcessingCode", "Protocol"]
