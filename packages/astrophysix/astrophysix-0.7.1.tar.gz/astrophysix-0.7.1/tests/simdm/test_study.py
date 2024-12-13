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
import uuid
import os
import datetime
import sys
from astrophysix.simdm import SimulationStudy, Project, ProjectCategory


class TestStudy(object):
    def test_01_study_init(self):
        """
        Tests Study instance initialisation
        """
        # Tests study defined without a valid Project instance raises an exception
        with pytest.raises(AttributeError, match="SimulationStudy 'project' attribute is not a valid Project object."):
            study_exc = SimulationStudy(project="Hi, My name is Robert !")  # Not a Project instance

        # Study initialisation => Ok should not raise  an error
        proj = Project(category=ProjectCategory.Cosmology, project_title="My awesome project", alias="NEW_PROJ")
        study = SimulationStudy(project=proj)

        assert isinstance(study.uid, uuid.UUID)
        assert isinstance(study.creation_time, datetime.datetime)
        assert isinstance(study.last_modification_time, datetime.datetime)
        assert study.project is proj

    def test_02_study_hdf5_io(self, tmp_path):
        """
        Tests saving/loading SimulationStudy from HDF5 file

        Parameters
        ----------
        tmp_path: temporary path  PyTest fixture
        """
        proj = Project(category=ProjectCategory.Cosmology, project_title="My awesome project", alias="NEW_PROJ")
        study = SimulationStudy(project=proj)

        fname = str(tmp_path / "study.h5")
        study.save_HDF5(study_fname=fname)
        study_loaded = SimulationStudy.load_HDF5(fname)

        print("study UUID : {uid!s}".format(uid=study.uid))
        assert study.uid == study_loaded.uid

        print("Study creation time : {t:s}".format(t=study.creation_time.isoformat()))
        assert study.creation_time == study_loaded.creation_time

        print("Study last modification time : {t:s}".format(t=study.last_modification_time.isoformat()))
        assert study.last_modification_time == study_loaded.last_modification_time

        assert study.project == study_loaded.project

    def test_03_study_hdf5_cross_io(self):
        """
        Tests cross-Python version loading SimulationStudy from HDF5 file (files saved by test_02_study_hdf5_io() method)
        """
        if sys.version_info.major > 2:  # Python 3.+
            # Load from a Python 2-saved HDF5 study
            study_loaded = SimulationStudy.load_HDF5(os.path.join(os.path.dirname(__file__), "io", "python_2", "study.h5"))
            assert study_loaded.creation_time.isoformat() == "2019-11-12T12:35:59.239199+00:00"
            assert study_loaded.last_modification_time.isoformat() == "2019-11-12T12:35:59.247400+00:00"
            assert str(study_loaded.uid) == "690a292b-8c49-4e97-9bd5-71a2159c3924"

            proj = Project(uid=uuid.UUID("df50c695-ad50-4c31-8e9d-1b1327645c22"), category=ProjectCategory.Cosmology,
                           project_title="My awesome project", alias="NEW_PROJ")
        else:  # Python 2.x
            # Load from a Python 3-saved HDF5 study
            study_loaded = SimulationStudy.load_HDF5(os.path.join(os.path.dirname(__file__), "io", "python_3", "study.h5"))
            assert study_loaded.creation_time.isoformat() == "2019-11-12T12:34:35.958546+00:00"
            assert study_loaded.last_modification_time.isoformat() == "2019-11-12T12:34:35.963422+00:00"
            assert str(study_loaded.uid) == "9a3549b2-711a-4f6d-8ece-8cdb203b8dff"

            proj = Project(uid=uuid.UUID("e82c5602-8272-4e6e-b85a-272096980d65"), category=ProjectCategory.Cosmology,
                           project_title="My awesome project", alias="NEW_PROJ")

        study = SimulationStudy(project=proj)
        assert study.project == study_loaded.project


__all__ = ["TestStudy"]

