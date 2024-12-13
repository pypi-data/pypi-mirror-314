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
import os
import sys
import shutil
import uuid
import logging

if sys.version_info.major == 2:
    import pytz

log = logging.getLogger("astrophysix.simdm")

from .project import Project
from . import ProjectCategory
from ..utils.persistency import Hdf5StudyPersistent, Hdf5StudyFileMode
from ..utils.dt_utils import DatetimeUtil
from ..utils.file import FileUtil, HDF5IOFile


class SimulationStudy(HDF5IOFile):
    """
    HDF5 simulation study file for Project tree structure persistency

    Parameters
    ----------
    project: :class:`~astrophysix.simdm.Project`
        study main project
    """
    def __init__(self, project=None):
        super(SimulationStudy, self).__init__()

        # Datetimes
        self._created = DatetimeUtil.utc_now()
        self._last_modified = DatetimeUtil.utc_now()

        # Study UUID
        self._uid = uuid.uuid4()

        # Study file paths
        self._study_filepath = None
        self._temp_study_filepath = FileUtil.new_temp_filepath("study")

        # Study project
        if project is None:
            # Create empty dummy project
            self._project = Project(category=ProjectCategory.Cosmology, project_title="My new project")
        else:
            # Check that project is a valid Project instance
            if not isinstance(project, Project):
                err_msg = "{cname:s} 'project' attribute is not a valid Project " \
                          "object.".format(cname=self.__class__.__name__)
                log.error(err_msg)
                raise AttributeError(err_msg)
            self._project = project


    @property
    def study_filepath(self):
        """Simulation study HDF5 file path"""
        return self._study_filepath

    @property
    def project(self):
        """Study main project"""
        return self._project

    @property
    def uid(self):
        """Study UUID"""
        return self._uid

    @property
    def creation_time(self):
        """Study creation date/time (:class:`datetime.datetime`)."""
        return self._created

    @property
    def last_modification_time(self):
        """Study last modification date/time (:class:`datetime.datetime`)."""
        return self._last_modified

    def save_HDF5(self, study_fname=None, dry_run=False, callback=None, galactica_checks=False):
        """
        Save the SimulationStudy into a HDF5 (\\*.h5) file

        Parameters
        ----------
        study_fname: :obj:`string`
            Simulation study HDF5 filename.
        dry_run: :obj:`bool`
            perform a dry run ? Default False.
        callback: :obj:`callable`
            method to execute upon saving each item of the study.
        galactica_checks: :obj:`bool`
            Perform Galactica database validity checks and display warning in case of invalid content for upload on
            Galactica. Default False (quiet mode).
        """
        if study_fname is None and self._study_filepath is None:
            # No file path provided : should never happen
            err_msg = "No filename provided. Please provide a HDF5 filename to save the study."
            log.error(err_msg)
            raise AttributeError(err_msg)

        # If Galactica database validity checks is enabled, perform a full check of the project before saving it.
        if galactica_checks:
            self._project.galactica_validity_check()

        # Save project into the temp. file
        if self._study_filepath is None:  # New file, study was never saved
            h5f, h5group, close_when_done = Hdf5StudyPersistent.open_h5file(self._temp_study_filepath,
                                                                            mode=Hdf5StudyFileMode.NEW_WRITE)
            try:
                Hdf5StudyPersistent._hsp_write_object(h5group, "PROJECT", self._project, new_file=True, dry_run=dry_run,
                                                      callback_func=callback, from_project=True)

                ctms = DatetimeUtil.utc_to_timestamp(self._created)
                h5group.attrs["ObjectClass"] = "Hdf5_Persistent_Simulation_Study"
                h5group.attrs["creation_time"] = ctms
                self._last_modified = DatetimeUtil.utc_now()
                mtms = DatetimeUtil.utc_to_timestamp(self._last_modified)
                h5group.attrs["last_modif_time"] = mtms
                h5group.attrs["study_version"] = 1
                h5group.attrs["study_uid"] = "{uid!s}".format(uid=self._uid)
            except Exception:
                raise
            finally:
                if close_when_done and h5f is not None:
                    h5f.close()

        else:  # Old study (already saved)
            alt_temp_file = FileUtil.new_temp_filepath("study")
            shutil.copy(self._temp_study_filepath, alt_temp_file)
            h5f, h5group, close_when_done = Hdf5StudyPersistent.open_h5file(alt_temp_file,
                                                                            mode=Hdf5StudyFileMode.APPEND)
            try:
                Hdf5StudyPersistent._hsp_write_object(h5group, "PROJECT", self._project, new_file=False,
                                                      dry_run=dry_run, callback_func=callback, from_project=True)

                mtms = DatetimeUtil.utc_to_timestamp(self._last_modified)
                h5group.attrs["last_modif_time"] = mtms
            except Exception:
                raise
            finally:
                if close_when_done and h5f is not None:
                    h5f.close()

            if not dry_run:
                # If no exception was raised, switch temp file
                if os.path.exists(self._temp_study_filepath):
                    os.remove(self._temp_study_filepath)
                self._temp_study_filepath = alt_temp_file
            else:
                # Delete temporary file (used for dry run)
                os.remove(alt_temp_file)

        if not dry_run:
            if study_fname is None:
                dest_path = self._study_filepath  # Keep old study file name
            else:
                dest_path = study_fname  # Change destination study filename

            # Move temporary file to the requested study HDF5 file path
            if os.path.exists(dest_path):  # Delete first the already existing file
                os.remove(dest_path)
            shutil.copy(self._temp_study_filepath, dest_path)

            # Set current study file path
            self._study_filepath = dest_path

    @classmethod
    def load_HDF5(cls, study_file_path):
        """
        Loads a new or existing SimulationStudy from a HDF5 (\\*.h5) file

        Parameters
        ----------
        study_file_path: :obj:`string`
            SimulationStudy HDF5 (existing) file path

        Returns
        -------
        study: :class:`~astrophysix.simdm.SimulationStudy`
            Study loaded from HDF5 file.
        """
        if not os.path.isfile(study_file_path):
            raise AttributeError("Cannot find file '{fname:s}'".format(fname=study_file_path))

        temp_loaded_file = FileUtil.new_temp_filepath("study")
        shutil.copy(study_file_path, temp_loaded_file)
        h5f, h5group, close_when_done = Hdf5StudyPersistent.open_h5file(temp_loaded_file,
                                                                        mode=Hdf5StudyFileMode.READ_ONLY)
        try:
            # Check that we are actually reading a Simulation study object from a HDF5 file
            if "ObjectClass" not in h5group.attrs or h5group.attrs["ObjectClass"] != "Hdf5_Persistent_Simulation_Study":
                err_msg = "HDF5 file does not contain a simulation study !"
                log.error(err_msg)
                raise IOError(err_msg)

            # Read study UUID
            if "study_uid" not in h5group.attrs:
                err_msg = "Cannot find study UUID attribute in '{path!s}'.".format(path=h5group.name)
                log.error(err_msg)
                raise IOError(err_msg)

            # Read study creation/last modification times
            if "creation_time" not in h5group.attrs or "last_modif_time" not in h5group.attrs:
                err_msg = "Cannot find study creation/modification time attributes in " \
                          "'{path!s}'.".format(path=h5group.name)
                log.error(err_msg)
                raise IOError(err_msg)

            if "PROJECT" not in h5group:
                err_msg = "Missing '/PROJECT' group in HDF5 simulation study file."
                log.error(err_msg)
                raise IOError(err_msg)
            proj_group = h5group["PROJECT"]
            p = Project.hsp_load_from_h5(proj_group)
            study = cls(project=p)
            study._temp_study_filepath = temp_loaded_file
            study._study_filepath = study_file_path
            study._uid = uuid.UUID(h5group.attrs["study_uid"])
            study._created = DatetimeUtil.utc_from_timestamp(h5group.attrs["creation_time"])
            study._last_modified = DatetimeUtil.utc_from_timestamp(h5group.attrs["last_modif_time"])
        except Exception:
            raise
        finally:
            if close_when_done and h5f is not None:
                h5f.close()

        return study

    def close(self):
        self._delete()

    def _delete(self):
        """
        Clean the study temporary HDF5 file (in /tmp).
        """
        if os.path.exists(self._temp_study_filepath):
            os.remove(self._temp_study_filepath)


__all__ = ["SimulationStudy"]
