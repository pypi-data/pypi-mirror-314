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

Numerical :obj:`Experiments` can be of two different types:

* :class:`~astrophysix.simdm.experiment.Simulation`,
* :class:`~astrophysix.simdm.experiment.PostProcessingRun`.

.. autoclass:: astrophysix.simdm.experiment.Simulation
   :members:
   :undoc-members:
   :inherited-members:
   :exclude-members: open_h5file, is_type_string, hsp_save_to_h5, cast_string, hsp_load_from_h5,
                      INVALID_ALIAS_ERROR_MESSAGE, VALID_ALIAS_REGEX

.. autoclass:: astrophysix.simdm.experiment.PostProcessingRun
   :members:
   :undoc-members:
   :inherited-members:
   :exclude-members: open_h5file, is_type_string, hsp_save_to_h5, cast_string, hsp_load_from_h5,
                      INVALID_ALIAS_ERROR_MESSAGE, VALID_ALIAS_REGEX

"""
from __future__ import print_function, unicode_literals, division, absolute_import  # Python 2 and 3 compatibility
from future.builtins import str, list, dict
import logging
import uuid
from datetime import datetime

from ..datafiles import JsonFile, AsciiFile, YamlFile
from ..datafiles.file import AssociatedFile
from ...utils.strings import Stringifiable
from ...utils.persistency import Hdf5StudyPersistent
from ...utils import DatetimeUtil

from ..protocol import SimulationCode, PostProcessingCode
from ..protocol.base import Protocol
from ..utils import ObjectList, GalacticaValidityCheckMixin
from .param_setting import ParameterSetting
from .app_algo import AppliedAlgorithm
from .resolved_physics import ResolvedPhysicalProcess
from ..results import Snapshot, GenericResult


log = logging.getLogger("astrophysix.simdm")


class Experiment(Hdf5StudyPersistent, GalacticaValidityCheckMixin):
    """
    Abstract Experiment class

    Parameters
    ----------
    name: :obj:`string`
        Experiment name (mandatory)
    alias: :obj:`string`
        Experiment alias (if defined, 16 max characters is recommended)
    description: :obj:`string`
        Long experiment description
    directory_path: :obj:`string`
        Experiment directory path
    config_file: :class:`~astrophysix.simdm.datafiles.file.JsonFile` or :class:`~astrophysix.simdm.datafiles.file.YamlFile` or :class:`~astrophysix.simdm.datafiles.file.AsciiFile`
        Experiment configuration file or None
    """
    def __init__(self, **kwargs):
        super(Experiment, self).__init__(**kwargs)

        self._alias = ""
        self._name = ""
        self._description = ""
        self._protocol = None
        self._directory_path = ""
        self._results = ObjectList(GenericResult, "name")
        self._snapshots = ObjectList(Snapshot, "name")
        self._psettings = ObjectList(ParameterSetting, "parameter_key")
        self._psettings.add_validity_check_method(self._check_valid_input_parameter)
        self._app_algos = ObjectList(AppliedAlgorithm, "algo_name")
        self._app_algos.add_validity_check_method(self._check_valid_algorithm)
        self._config_file = None

        # Simulation name
        if "name" not in kwargs:
            raise AttributeError("{cname:s} 'name' attribute is not defined (mandatory).".format(cname=self.__class__.__name__))
        self.name = kwargs["name"]

        if "alias" in kwargs:
            self.alias = kwargs["alias"]

        if "description" in kwargs:
            self.description = kwargs["description"]

        if "directory_path" in kwargs:
            self.directory_path = kwargs["directory_path"]

        if "config_file" in kwargs:
            self.configuration_file = kwargs["config_file"]

    def __eq__(self, other):
        """
        Experiment comparison method

        other: :obj:`Experiment`
            experiment to compare to
        """
        if not super(Experiment, self).__eq__(other):
            return False

        if self._name != other.name:
            return False

        if self._alias != other.alias:
            return False

        if self._description != other.description:
            return False

        if self._directory_path != other.directory_path:
            return False

        if self._psettings != other.parameter_settings:
            return False

        if self._app_algos != other.applied_algorithms:
            return False

        if self._snapshots != other.snapshots:
            return False

        if self._results != other.generic_results:
            return False

        if self._config_file != other.configuration_file:
            return False

        return True

    def _check_valid_input_parameter(self, param_setting):
        """
        Checks that a given parameter setting can be added into this experiment parameter setting list. Verifies that
        the parameter setting's input parameter belongs to the experiment protocol's input parameter list. Raises an
        AttributeError if not.

        Parameters
        ----------
        param_setting: ``astrophysix.simdm.experiment.param_setting.ParameterSetting``
            parameter setting to add
        """
        if param_setting.input_parameter not in self._protocol.input_parameters:
            err_msg = "{cname:s} '{ps!s}' does not refer to one of the input parameters of " \
                      "'{prot!s}'.".format(cname=self.__class__.__name__, ps=param_setting, prot=self._protocol)
            log.error(err_msg)
            raise AttributeError(err_msg)

    def _can_delete_input_param(self, inp_param):
        """
        Checks if an input parameter is not linked to any experiment's parameter setting and can be safely deleted.
        Returns None if it can be deleted, otherwise returns a string.

        Parameters
        ----------
        inp_param: ``astrophysix.simdm.protocol.input_parameters.InputParameter``
            input parameter about to be deleted

        Returns
        -------
        o: str or None
        """
        for psetting in self._psettings:
            if psetting.input_parameter is inp_param:  # Reference identity, not equality ??? Should work
                return "{s!s} {ps!s}".format(s=self, ps=psetting)
        return None

    def _check_valid_algorithm(self, applied_algo):
        """
        Checks that a given applied algorithm can be added into this experiment applied algorithm list. Verifies that
        the applied algorithm's algorithm belongs to the experiment protocol's algorithm list. Raises an
        AttributeError if not.

        Parameters
        ----------
        applied_algo: ``astrophysix.simdm.experiment.app_algo.AppliedAlgorithm``
            applied algorithm to add
        """
        if applied_algo.algorithm not in self._protocol.algorithms:
            err_msg = "{cname:s} '{aa!s}' does not refer to one of the algorithms of " \
                      "'{prot!s}'.".format(cname=self.__class__.__name__, aa=applied_algo, prot=self._protocol)
            log.error(err_msg)
            raise AttributeError(err_msg)

    def _can_delete_algo(self, algo):
        """
        Checks if an algorithm is not linked to any experiment's applied algorithm and can be safely deleted.
        Returns None if it can be deleted, otherwise returns a string.

        Parameters
        ----------
        algo: ``astrophysix.simdm.protocol.algorithm.Algorithm``
            algorithm about to be deleted

        Returns
        -------
        o: str or None
        """
        for app_algo in self._app_algos:
            if app_algo.algorithm is algo: # Reference identity, not equality ??? Should work
                return "{s!s} {aa!s}".format(s=self, aa=app_algo)
        return None

    @property
    def alias(self):
        """Experiment alias. Can be edited."""
        return self._alias

    @alias.setter
    def alias(self, new_alias):
        try:
            self._alias = Stringifiable.cast_string(new_alias)
            if len(new_alias) > 16:
                log.warning("{cname:s} 'alias' attribute is too long (max 16 characters).".format(
                    cname=self.__class__.__name__))

        except TypeError:
            err_msg = "{cname:s} 'alias' property is not a valid string".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

    @property
    def name(self):
        """Experiment name. Can be edited."""
        return self._name

    @name.setter
    def name(self, new_simu_name):
        try:
            self._name = Stringifiable.cast_string(new_simu_name, valid_empty=False)
        except TypeError:
            err_msg = "{cname:s} 'name' property is not a valid (non-empty) string".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

    @property
    def description(self):
        """Experiment description. Can be edited."""
        return self._description

    @description.setter
    def description(self, new_descr):
        try:
            self._description = Stringifiable.cast_string(new_descr)
        except TypeError:
            err_msg = "{cname:s} 'description' property is not a valid string".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

    @property
    def directory_path(self):
        """Experiment data directory path. Can be edited."""
        return self._directory_path

    @directory_path.setter
    def directory_path(self, new_path):
        try:
            self._directory_path = Stringifiable.cast_string(new_path)
        except TypeError:
            err_msg = "{cname:s} 'directory_path' property is not a valid string".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

    @property
    def applied_algorithms(self):
        """Experiment applied algorithm list (:class:`~astrophysix.simdm.utils.ObjectList`)"""
        return self._app_algos

    @property
    def parameter_settings(self):
        """Experiment parameter setting list (:class:`~astrophysix.simdm.utils.ObjectList`)"""
        return self._psettings

    @property
    def snapshots(self):
        """Experiment snapshot list (:class:`~astrophysix.simdm.utils.ObjectList`)"""
        return self._snapshots

    @property
    def generic_results(self):
        """Experiment generic result list (:class:`~astrophysix.simdm.utils.ObjectList`)"""
        return self._results

    @property
    def configuration_file(self):
        """
        Experiment configuration file (:class:`~astrophysix.simdm.datafiles.file.JsonFile`,
        :class:`~astrophysix.simdm.datafiles.file.YamlFile` or :class:`~astrophysix.simdm.datafiles.file.AsciiFile`).
        Set to None to leave undefined. Can be edited."""
        return self._config_file

    @configuration_file.setter
    def configuration_file(self, new_cfg_file):
        if new_cfg_file is not None and not isinstance(new_cfg_file, JsonFile) and not \
                isinstance(new_cfg_file, AsciiFile) and not isinstance(new_cfg_file, YamlFile):
            err_msg = "{cname:s} 'configuration_file' property is neither None nor a valid JsonFile, YamlFile or " \
                      "AsciiFile instance.".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)
        self._config_file = new_cfg_file

    @classmethod
    def _protocol_class_name(cls):
        raise NotImplementedError()

    @classmethod
    def _hsp_valid_attributes(cls):
        """List of valid kwargs in __init__() method"""
        return ["name", "alias", "description", "directory_path", "config_file"]

    def _hsp_write(self, h5group, **kwargs):
        """
        Serialize an Experiment object into a HDF5 file.

        Parameters
        ----------
        h5group: ``h5py.Group``
            Main group to write the Experiment into.
        kwargs: ``dict``
            keyword argument dictionary.
        """
        # Call to parent class _hsp_write() : write UUID, etc.
        super(Experiment, self)._hsp_write(h5group, **kwargs)

        # Check that protocol is defined
        if self._protocol is None:
            err_msg = "Undefined protocol for {exp!s}".format(exp=self)
            log.error(err_msg)
            raise ValueError(err_msg)

        # Write experiment name
        self._hsp_write_attribute(h5group, ('name', self._name), **kwargs)

        # Write experiment Galactica alias, if defined
        self._hsp_write_attribute(h5group, ('galactica_alias', self._alias), **kwargs)

        # Write experiment description, if defined
        self._hsp_write_attribute(h5group, ('description', self._description), **kwargs)

        # Write experiment directory path, if defined
        self._hsp_write_attribute(h5group, ('experiment_directory', self._directory_path), **kwargs)

        # Write protocol
        if kwargs.get("from_project", False):  # Write protocol UUID
            self._hsp_write_attribute(h5group, ('protocol_uid', self._protocol.uid), **kwargs)
        else:  # Write complete protocol description (full serialization)
            self._hsp_write_object(h5group, "PROTOCOL", self._protocol, **kwargs)

        # Write configuration file into HDF5 file
        self._hsp_write_object(h5group, "config_file", self._config_file, **kwargs)

        # Write parameter settings, if any defined
        # # -- Security check : checks that parameter settings refers to a actual input parameters of the protocol - #
        # for psetting in self._psettings:
        #     if psetting.input_parameter not in self._protocol.input_parameters:
        #         err_msg = "{cname:s} '{ps!s}' does not refer to one of the input parameters of '{prot!s}'" \
        #                   ".".format(cname=self.__class__.__name__, ps=psetting, prot=self._protocol)
        #         log.error(err_msg)
        #         raise ValueError(err_msg)
        # # -------------------------------------------------------------------------------------------------------- #
        self._hsp_write_object_list(h5group, "PARAM_SETTINGS", self._psettings, "psetting_", **kwargs)

        # Write applied algorithms, if any defined
        # # ---- Security check : checks that applied algorithms refers to a actual algorithms of the protocol ----- #
        # for app_algo in self._app_algos:
        #     if app_algo.algorithm not in self._protocol.algorithms:
        #         err_msg = "{cname:s} '{aa!s}' does not refer to one of the algorithms of '{prot!s}'" \
        #                   ".".format(cname=self.__class__.__name__, aa=app_algo, prot=self._protocol)
        #         log.error(err_msg)
        #         raise ValueError(err_msg)
        # # -------------------------------------------------------------------------------------------------------- #
        self._hsp_write_object_list(h5group, "APPLIED_ALGOS", self._app_algos, "app_algo_", **kwargs)

        # Write all snapshots, if any defined
        self._hsp_write_object_list(h5group, "SNAPSHOTS", self._snapshots, "sn_", **kwargs)

        # Write generic results, if any defined
        self._hsp_write_object_list(h5group, "RESULTS", self._results, "res_", **kwargs)

    @classmethod
    def _hsp_read(cls, h5group, version, dependency_objdict=None):
        """
        Read an Experiment object from a HDF5 file (*.h5).

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
        exp: ``Experiment``
            Read Experiment instance
        """
        # Handle different versions here

        # Fetch Hdf5StudyPersistent object UUID
        uid = super(Experiment, cls)._hsp_read(h5group, version, dependency_objdict=dependency_objdict)

        # Try to read/find protocol
        try:
            prot_uid = uuid.UUID(cls._hsp_read_attribute(h5group, "protocol_uid", "protocol UUID",
                                                         raise_error_if_not_found=True))

            # Search for already instantiated protocol in dependency object dictionary
            if dependency_objdict is None:
                err_msg = "Cannot find any protocol already instantiated in the project."
                log.error(err_msg)
                raise IOError(err_msg)

            # Get dictionary of protocol objects of the corresponding class : simulation / post-processing codes
            pcn = cls._protocol_class_name()
            if pcn not in dependency_objdict:
                err_msg = "Cannot find any protocol of type '{n:s}'".format(n=pcn)
                log.error(err_msg)
                raise IOError(err_msg)

            # Find protocol according to its UUID
            proto_dict = dependency_objdict[pcn]
            if prot_uid not in proto_dict:
                err_msg = "Cannot find protocol of type '{n:s}' with uid {uid:s}.".format(n=pcn, uid=str(prot_uid))
                log.error(err_msg)
                raise IOError(err_msg)

            prot = proto_dict[prot_uid]
        except IOError:  # Protocol UUID not found in Experiment
            # Read protocol info from "PROTOCOL" subgroup
            prot = Protocol._hsp_read_object(h5group, "PROTOCOL", "experiment protocol",
                                             dependency_objdict=dependency_objdict)

        # Read experiment name
        exp_name = cls._hsp_read_attribute(h5group, "name", "experiment name")

        # Instantiate experiment object
        exp = cls(prot, uid=uid, name=exp_name)

        # Read experiment Galactica alias, if defined
        exp_alias = cls._hsp_read_attribute(h5group, 'galactica_alias', "experiment Galactica alias",
                                            raise_error_if_not_found=False)
        if exp_alias is not None:
            exp.alias = exp_alias

        # Read experiment description, if defined
        exp_descr = cls._hsp_read_attribute(h5group, 'description', "experiment description",
                                            raise_error_if_not_found=False)
        if exp_descr is not None:
            exp.description = exp_descr

        # Read experiment directory path, if defined
        exp_dpath = cls._hsp_read_attribute(h5group, 'experiment_directory', "experiment directory path",
                                            raise_error_if_not_found=False)
        if exp_dpath is not None:
            exp.directory_path = exp_dpath

        # Read configuration file, if defined
        if "config_file" in h5group:
            exp.configuration_file = AssociatedFile._hsp_read_object(h5group, "config_file", "configuration file")

        dod = {prot.__class__.__name__: prot}
        # Build parameter setting list and add each parameter setting into experiment
        if "PARAM_SETTINGS" in h5group:
            for psetting in ParameterSetting._hsp_read_object_list(h5group, "PARAM_SETTINGS", "psetting_",
                                                                   "experiment parameter setting",
                                                                   dependency_objdict=dod):
                exp.parameter_settings.add(psetting)

        # Build applied algorithm list and add each applied algorithm into experiment
        if "APPLIED_ALGOS" in h5group:
            for app_algo in AppliedAlgorithm._hsp_read_object_list(h5group, "APPLIED_ALGOS", "app_algo_",
                                                                   "experiment applied algorithm",
                                                                   dependency_objdict=dod):
                exp.applied_algorithms.add(app_algo)

        # Build snapshot list and add each snapshot into experiment
        if "SNAPSHOTS" in h5group:
            for sn in Snapshot._hsp_read_object_list(h5group, "SNAPSHOTS", "sn_", "experiment snapshot",
                                                     dependency_objdict=dependency_objdict):
                exp.snapshots.add(sn)

        # Build generic result list and add each generic result into experiment
        if "RESULTS" in h5group:
            for res in GenericResult._hsp_read_object_list(h5group, "RESULTS", "res_", "experiment generic result",
                                                           dependency_objdict=dependency_objdict):
                exp.generic_results.add(res)

        return exp

    def galactica_validity_check(self, **kwargs):
        """
        Perform validity checks on this  instance and eventually log warning messages.

        Parameters
        ----------
        kwargs: `dict`
            keyword arguments (optional)
        """
        # Check experiment alias
        if len(self.alias) == 0:
            log.warning("{p!s} Galactica alias is missing.".format(p=self))
        elif len(self._alias) > 64:
            log.warning("{p!s} Galactica alias is too long (max. 64 characters).".format(p=self))
        else:
            err_msg = self.galactica_valid_alias(self._alias)
            if err_msg is not None:
                log.warning("{p!s} Galactica alias is not valid ({m:s})".format(p=self, m=err_msg))

        # Check configuration file
        if self._config_file is not None:
            self._config_file.galactica_validity_check(**kwargs)

        # Perform Galactica validity checks on parameter setting/applied algorithm list
        self._psettings.galactica_validity_check(**kwargs)
        self._app_algos.galactica_validity_check(**kwargs)

        # Check generic result/snapshot validity + ensure generic result/snapshot name unicity in this experiment
        result_names = {}
        for gres in self._results():
            gres.galactica_validity_check()
            if len(gres.name) > 0:
                if gres.name in result_names:
                    log.warning("{r1!s} and {r2!s} results share the same name. They must be "
                                "unique.".format(r1=result_names[gres.name], r2=gres))
                else:
                    result_names[gres.name] = gres
        for sn in self._snapshots():
            sn.galactica_validity_check()
            if len(sn.name) > 0:
                if sn.name in result_names:
                    log.warning("{r1!s} and {r2!s} results share the same name. They must be "
                                "unique.".format(r1=result_names[sn.name], r2=sn))
                else:
                    result_names[sn.name] = sn


class Simulation(Experiment, Stringifiable):
    """
    Simulation (Simulation data model)

    Parameters
    ----------
    name: :obj:`string`
        Simulation name (mandatory)
    simu_code: :class:`~astrophysix.simdm.protocol.SimulationCode`
        Simulation code used for this simulation (mandatory)
    alias: :obj:`string`
        Simulation alias (if defined, 16 max characters is recommended)
    description: :obj:`string`
        Long simulation description
    directory_path: :obj:`string`
        Simulation data directory path
    execution_time: :obj:`string`
        Simulation execution time in the format '%Y-%m-%d %H:%M:%S'
    config_file: :class:`~astrophysix.simdm.datafiles.file.JsonFile` or :class:`~astrophysix.simdm.datafiles.file.YamlFile` or :class:`~astrophysix.simdm.datafiles.file.AsciiFile`
        Simulation configuration file or :obj:`None`
    """
    EXETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self, *args, **kwargs):
        super(Simulation, self).__init__(**kwargs)

        # Protocol (simulation code)
        if len(args) > 0:
            simulation_code = args[0]
        elif "simu_code" in kwargs:
            simulation_code = kwargs["simu_code"]
        else:
            raise AttributeError("Undefined simulation code for '{sname:s}' Simulation.".format(sname=self._name))

        if not isinstance(simulation_code, SimulationCode):
            err_msg = "Simulation 'simulation_code' attribute is not a valid SimulationCode instance."
            log.error(err_msg)
            raise AttributeError(err_msg)
        self._protocol = simulation_code

        # Simulation execution time
        self._execution_time = None
        if "execution_time" in kwargs:
            self.execution_time = kwargs["execution_time"]

        # Post-processing runs
        self._ppruns = ObjectList(PostProcessingRun, "name")
        # Resolved physical processes
        self._resolved_physics = ObjectList(ResolvedPhysicalProcess, "process_name")
        self._resolved_physics.add_validity_check_method(self._check_valid_physics)

        # Add deletion handler to the simulation code input parameter list and algorithm list
        simulation_code.input_parameters.add_deletion_handler(self._can_delete_input_param)
        simulation_code.algorithms.add_deletion_handler(self._can_delete_algo)
        simulation_code.physical_processes.add_deletion_handler(self._can_delete_phys_proc)

    def __eq__(self, other):
        """
        Simulation comparison method

        other: :class:`~astrophysix.simdm.experiment.Simulation`
            simulation to compare to
        """
        if not super(Simulation, self).__eq__(other):
            return False

        if self._protocol != other.simulation_code:
            return False

        if self._execution_time != other.execution_time:
            return False

        if self._resolved_physics != other.resolved_physics:
            return False

        if self._ppruns != other.post_processing_runs:
            return False

        return True

    def _check_valid_physics(self, res_phys):
        """
        Checks that a given resolved physical process can be added into this simulation resolved physical process list.
        Verifies that the resolved physical process's physical process belongs to the simulation protocol's physical
        process list. Raises an AttributeError if not.

        Parameters
        ----------
        res_phys: ``astrophysix.simdm.experiment.resolved_physics.ResolvedPhysicalProcess``
            resolved physical process to add
        """
        if res_phys.physical_process not in self._protocol.physical_processes:
            err_msg = "{cname:s} '{aa!s}' does not refer to one of the physical processes of " \
                      "'{prot!s}'.".format(cname=self.__class__.__name__, aa=res_phys, prot=self._protocol)
            log.error(err_msg)
            raise AttributeError(err_msg)

    def _can_delete_phys_proc(self, phys_proc):
        """
        Checks if a physical process is not linked to any simulation's resolved physical process and can be safely
        deleted. Returns None if it can be deleted, otherwise returns a string.

        Parameters
        ----------
        phys_proc: ``astrophysix.simdm.protocol.physics.PhysicalProcess``
            physical process about to be deleted

        Returns
        -------
        o: str or None
        """
        for res_pproc in self._resolved_physics:
            if res_pproc.physical_process is phys_proc:  # Reference identity, not equality ??? Should work
                return "{s!s} {rpp!s}".format(s=self, rpp=res_pproc)
        return None

    @property
    def simulation_code(self):
        """
        :class:`~astrophysix.simdm.protocol.SimulationCode` used to run this simulation. Cannot be changed after
        simulation initialisation.
        """
        return self._protocol

    @property
    def post_processing_runs(self):
        """Simulation associated post-processing run list (:class:`~astrophysix.simdm.utils.ObjectList`)"""
        return self._ppruns

    @classmethod
    def _protocol_class_name(cls):
        return SimulationCode.__name__

    @property
    def execution_time(self):
        """Simulation execution date/time. Can be edited.

        Example
        -------
        >>> simu = Simulation(simu_code=gadget4, name="Maxi Cosmic", execution_time="2020-09-10 14:25:48")
        >>> simu.execution_time = '2020-09-28 18:45:24'
        """
        return self._execution_time

    @execution_time.setter
    def execution_time(self, new_time_value):
        try:
            t_str = Stringifiable.cast_string(new_time_value, valid_empty=False)
            t = datetime.strptime(t_str, self.EXETIME_FORMAT)
            self._execution_time = t_str
        except (TypeError, ValueError):
            err_msg = "{cn:s} 'execution_time' property is not a valid datetime " \
                      "string.".format(cn=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

    @property
    def execution_time_as_utc_datetime(self):
        """UTC execution time of the simulation (timezone aware)"""
        return DatetimeUtil.utc_from_string(self._execution_time, self.EXETIME_FORMAT)

    @property
    def resolved_physics(self):
        """Simulation resolved physical process list (:class:`~astrophysix.simdm.utils.ObjectList`)."""
        return self._resolved_physics

    @classmethod
    def _hsp_valid_attributes(cls):
        """List of valid kwargs in __init__() method"""
        experiment_valid_attrs = super(Simulation, cls)._hsp_valid_attributes()
        experiment_valid_attrs += ["simu_code", "execution_time"]
        return experiment_valid_attrs

    def _hsp_write(self, h5group, **kwargs):
        """
        Serialize a Simulation object into a HDF5 file.

        Parameters
        ----------
        h5group: ``h5py.Group``
            Main group to write the Simulation into.
        kwargs: ``dict``
            keyword argument dictionary.
        """
        # If necessary, call callback function with experiment name
        self._hsp_write_callback(str(self), **kwargs)

        # Call to parent class _hsp_write()
        super(Simulation, self)._hsp_write(h5group, **kwargs)

        # Simulation execution time
        self._hsp_write_attribute(h5group, ('execution_time', self._execution_time), **kwargs)

        # Write simulation resolved physics, if any defined
        # # -- Security check : checks that resolved physics refers to an actual physical process of the protocol -- #
        # for res_phys in self._resolved_physics:
        #     if res_phys.physical_process not in self._protocol.physical_processes:
        #         err_msg = "{cname:s} '{rp!s}' does not refer to one of the physical processes of '{prot!s}'" \
        #                   ".".format(cname=self.__class__.__name__, rp=res_phys, prot=self._protocol)
        #         log.error(err_msg)
        #         raise ValueError(err_msg)
        # # -------------------------------------------------------------------------------------------------------- #
        self._hsp_write_object_list(h5group, "RESOLVED_PHYSICS", self._resolved_physics, "res_phys_", **kwargs)

        # Write simulation post-processing runs, if any defined
        self._hsp_write_object_list(h5group, "POST-PRO_RUNS", self._ppruns, "pprun_", **kwargs)

    @classmethod
    def _hsp_read(cls, h5group, version, dependency_objdict=None):
        """
        Read a Simulation object from a HDF5 file (*.h5).

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
        simu: ``Simulation``
            Read Simulation instance
        """
        # Handle different versions here

        # Read base experiment parameters
        simu = super(Simulation, cls)._hsp_read(h5group, version, dependency_objdict=dependency_objdict)

        # Read simulation execution time, if defined
        exec_time = cls._hsp_read_attribute(h5group, 'execution_time', "simulation execution time",
                                            raise_error_if_not_found=False)
        if exec_time is not None:
            simu.execution_time = exec_time

        # Build resolved physics list and add each resolved physics into simulation, if any defined
        if "RESOLVED_PHYSICS" in h5group:
            dod = {simu.simulation_code.__class__.__name__: simu.simulation_code}
            for res_phys in ResolvedPhysicalProcess._hsp_read_object_list(h5group, "RESOLVED_PHYSICS", "res_phys_",
                                                                          "simulation resolved physical process",
                                                                          dependency_objdict=dod):
                simu.resolved_physics.add(res_phys)

        # Build post-processing run list and add each post-processing run into simulation, if any defined
        if "POST-PRO_RUNS" in h5group:
            for pprun in PostProcessingRun._hsp_read_object_list(h5group, "POST-PRO_RUNS", "pprun_",
                                                                 "simulation post-processing run",
                                                                 dependency_objdict=dependency_objdict):
                simu.post_processing_runs.add(pprun)

        return simu

    def galactica_validity_check(self, **kwargs):
        """
        Perform validity checks on this  instance and eventually log warning messages.

        Parameters
        ----------
        kwargs: `dict`
            keyword arguments (optional)
        """
        super(Simulation, self).galactica_validity_check(**kwargs)

        # Check that simulation execution time is defined
        if self.execution_time is None:
            log.warning("{p!s} Galactica execution time is not defined.".format(p=self))

        # Perform Galactica validity checks on resolved physical process + post-processing runs list
        self._resolved_physics.galactica_validity_check(**kwargs)
        self._ppruns.galactica_validity_check(**kwargs)

    def __unicode__(self):
        """
        String representation of the instance
        """
        return "'{simname:s}' simulation".format(simname=self._name)


class PostProcessingRun(Experiment, Stringifiable):
    """
    Post-processing run (Simulation data model)

    Parameters
    ----------
    name: :obj:`string`
        post-processing run name (mandatory)
    ppcode: :class:`~astrophysix.simdm.protocol.PostProcessingCode`
        post-processing code used for this post-processing run (mandatory)
    alias: :obj:`string`
        Post-processing run alias (if defined, 16 max characters is recommended)
    description: :obj:`string`
        Long post-processing run description
    config_file: :class:`~astrophysix.simdm.datafiles.file.JsonFile` or :class:`~astrophysix.simdm.datafiles.file.YamlFile` or :class:`~astrophysix.simdm.datafiles.file.AsciiFile`
        Post-processing run configuration file or None

    """
    def __init__(self, *args, **kwargs):
        super(PostProcessingRun, self).__init__(**kwargs)

        # Protocol (simulation code)
        if len(args) > 0:
            postpro_code = args[0]
        elif "ppcode" in kwargs:
            postpro_code = kwargs["ppcode"]
        else:
            raise AttributeError("Undefined post-processing code for '{ppname:s}' Post-processing run.".format(ppname=self._name))

        if not isinstance(postpro_code, PostProcessingCode):
            err_msg = "PostProcessingRun 'postpro_code' attribute is not a valid PostProcessingCode instance."
            log.error(err_msg)
            raise AttributeError(err_msg)

        self._protocol = postpro_code

        # Add deletion handler to the post-processing code input parameter list and algorithm list
        postpro_code.input_parameters.add_deletion_handler(self._can_delete_input_param)
        postpro_code.algorithms.add_deletion_handler(self._can_delete_algo)

    def __eq__(self, other):
        """
        PostProcessingRun comparison method

        other: :class:`~astrophysix.simdm.protocol.PostProcessingRun`
            post-processing run to compare to
        """
        if not super(PostProcessingRun, self).__eq__(other):
            return False

        if self._protocol != other.postpro_code:
            return False

        return True

    @property
    def postpro_code(self):
        """:class:`~astrophysix.simdm.protocol.PostProcessingCode` used to run this post-processing run. Cannot be
        changed after post-processing run initialisation."""
        return self._protocol

    @classmethod
    def _protocol_class_name(cls):
        return PostProcessingCode.__name__

    @classmethod
    def _hsp_valid_attributes(cls):
        """List of valid kwargs in __init__() method"""
        experiment_valid_attrs = super(PostProcessingRun, cls)._hsp_valid_attributes()
        experiment_valid_attrs.append("ppcode")
        return experiment_valid_attrs

    def _hsp_write(self, h5group, **kwargs):
        """
        Serialize a PostProcessingRun object into a HDF5 file.

        Parameters
        ----------
        h5group: ``h5py.Group``
            Main group to write the PostProcessingRun into.
        kwargs: ``dict``
            keyword argument dictionary.
        """
        # If necessary, call callback function with post-processing run name
        self._hsp_write_callback(str(self), **kwargs)

        # Call to parent class _hsp_write()
        super(PostProcessingRun, self)._hsp_write(h5group, **kwargs)

    @classmethod
    def _hsp_read(cls, h5group, version, dependency_objdict=None):
        """
        Read a PostProcessingRun object from a HDF5 file (*.h5).

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
        pprun: :class:`~astrophysix.simdm.experiment.PostProcessingRun`
            Read PostProcessingRun instance
        """
        # Handle different versions here

        # Read base experiment parameters
        pprun = super(PostProcessingRun, cls)._hsp_read(h5group, version, dependency_objdict=dependency_objdict)

        return pprun

    def __unicode__(self):
        """
        String representation of the instance
        """
        return "'{pprun_name:s}' post-processing run".format(pprun_name=self._name)


__all__ = ["Simulation", "PostProcessingRun", "Experiment"]
