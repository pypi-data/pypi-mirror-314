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

import os

from future.builtins import str
import pytest
import logging
import numpy as N

from astrophysix.simdm import Project, ProjectCategory, protocol, experiment, SimulationStudy
from astrophysix.simdm.catalogs import Catalog, TargetObject, ObjectProperty, CatalogField
from astrophysix.simdm.datafiles import PngImageFile
from astrophysix.simdm.protocol import InputParameter
from astrophysix.simdm.results import Snapshot


class TestProjectCategory(object):
    def test_from_alias_exceptions(self):
        """
        Tests exceptions raised by ProjectCategory.from_alias(method)
        """
        # Check unknown category
        with pytest.raises(ValueError) as e:
            cat = ProjectCategory.from_alias("TRICOT")
        assert str(e.value) == "No ProjectCategory defined with the alias 'TRICOT'."

    def test_init(self):
        """
        Tests valid ProjectCategory initialisation from aliases
        """
        assert ProjectCategory.from_alias("SOLAR_PHYSICS") == ProjectCategory.SolarPhysics
        assert ProjectCategory.from_alias("PLANET_ATMO") == ProjectCategory.PlanetaryAtmospheres
        assert ProjectCategory.from_alias("STAR_PLANET_INT") == ProjectCategory.StarPlanetInteractions
        assert ProjectCategory.from_alias("STAR_FORM") == ProjectCategory.StarFormation
        assert ProjectCategory.from_alias("ISM") == ProjectCategory.InterstellarMedium
        assert ProjectCategory.from_alias("MHD") == ProjectCategory.Magnetohydrodynamics
        assert ProjectCategory.from_alias("SUPERNOVAE") == ProjectCategory.Supernovae
        assert ProjectCategory.from_alias("STELLAR_ENVS") == ProjectCategory.StellarEnvironments
        assert ProjectCategory.from_alias("GALAXIES") == ProjectCategory.GalacticDynamics
        assert ProjectCategory.from_alias("COSMOLOGY") == ProjectCategory.Cosmology


class TestProject(object):
    def test_project_init(self):
        """
        Tests Project instance initialisation
        """
        # Project initialisation
        proj = Project(category=u"COSMOLOGY", project_title="My awesome project", alias="NEW_PROJ",
                       short_description="Short description of my project",
                       general_description="""This is a pretty long description for my project""",
                       data_description="The data available in this project...", acknowledgement="To cite me, ...",
                       thumbnail_image=os.path.join(os.path.dirname(__file__), "io", "datafiles", "CEA.png"),
                       directory_path="/path/to/my_data/",)
        assert isinstance(proj.project_title, str)
        assert isinstance(proj.alias, str)
        assert proj.category == ProjectCategory.Cosmology
        assert proj.project_title == "My awesome project"
        assert proj.alias == "NEW_PROJ"
        assert isinstance(proj.alias, str)
        assert proj.short_description == "Short description of my project"
        assert proj.general_description == "This is a pretty long description for my project"
        assert proj.data_description == "The data available in this project..."
        assert proj.directory_path == "/path/to/my_data/"
        assert proj.thumbnail_image == PngImageFile.load_file(os.path.join(os.path.dirname(__file__), "io",
                                                                           "datafiles", "CEA.png"))

        # Test str() conversion
        assert str(proj) == "[Cosmology] 'My awesome project' project"

    def test_setting_project_title_exc(self):
        """
        Tests that a project defined without title raises an exception
        """
        # Tests project defined without title
        with pytest.raises(AttributeError) as e:
            proj_exc = Project(category=ProjectCategory.StarFormation)  # No project title defined
        assert str(e.value) == "Project 'project_title' attribute is not defined (mandatory)."

        proj = Project(category="COSMOLOGY", project_title="My awesome project")

        # ------------- Tests invalid project title setting exception ---------------------- #
        empty_proj_title_err = "Project 'project_title' property is not a valid (non empty) string."
        with pytest.raises(AttributeError) as e:
            proj.project_title = (3, "Bananas")
        assert str(e.value) == empty_proj_title_err

        with pytest.raises(AttributeError) as e:
            proj.project_title = ""
        assert str(e.value) == empty_proj_title_err
        # ---------------------------------------------------------------------------------- #

        # Valid => should not raise any exception
        proj.project_title = "The best project of the world"

    def test_project_category_setting_exc(self):
        """
        Tests setting a project category
        """
        # Tests project defined without category
        with pytest.raises(AttributeError) as e:
            proj_exc = Project(project_title="My awesome project")  # No project category defined
        assert str(e.value) == "Project 'category' attribute is not defined (mandatory)."

        # Tests invalid category property initialisation exception
        with pytest.raises(AttributeError) as e:
            proj_exc = Project(category="TRICOT", project_title="My awesome project")  # Invalid project category
        assert str(e.value) == "No ProjectCategory defined with the alias 'TRICOT'."

        # Project initialisation
        proj = Project(category=ProjectCategory.PlanetaryAtmospheres, project_title="My awesome project")
        proj2 = Project(category="STAR_FORM", project_title="My second awesome project")

        # Tests invalid category property setting exception
        with pytest.raises(AttributeError) as e:
            proj.category = "BRODERIE"
        assert str(e.value) == "No ProjectCategory defined with the alias 'BRODERIE'."

        with pytest.raises(AttributeError) as e:
            proj.category = (3, "Strawberries")
        assert str(e.value) == "Project 'category' attribute is not a valid ProjectCategory enum value."

        # Valid => should not raise any exception
        proj.category = ProjectCategory.StarFormation

    def test_setting_project_alias_exc(self, caplog):
        """
        Tests setting a project alias

        caplog: captured log PyTest fixture
        """
        proj = Project(category="COSMOLOGY", project_title="My awesome project")

        # Tests invalid project alias setting exception
        with pytest.raises(AttributeError) as e:
            proj.alias = 25.5
        assert str(e.value) == "Project 'alias' property is not a valid string"

        # Valid => should not raise any exception
        proj.alias = "TOP_PROJ"

    def test_setting_project_long_text_fields(self):
        """
        Tests setting project short/general/data description + acknowledgement properties
        """
        proj = Project(category="COSMOLOGY", project_title="My awesome project")

        # ------------------------ Tests invalid project description setting exception ------------------------------- #
        with pytest.raises(AttributeError) as e:
            proj.short_description = 0
        assert str(e.value) == "Project 'short_description' property is not a valid string"

        # Valid => should not raise any exception
        proj.short_description = "Short description of the best project of the world"

        with pytest.raises(AttributeError) as e:
            proj.general_description = 0.1
        assert str(e.value) == "Project 'general_description' property is not a valid string"

        # Valid => should not raise any exception
        proj.general_description = "General description of the best project of the world"

        with pytest.raises(AttributeError) as e:
            proj.data_description = (23, "Monkeys")
        assert str(e.value) == "Project 'data_description' property is not a valid string"

        # Valid => should not raise any exception
        proj.data_description = "Data description of the best project of the world"

        with pytest.raises(AttributeError) as e:
            proj.acknowledgement = {"Il": "etait une fois"}
        assert str(e.value) == "Project 'acknowledgement' property is not a valid string"

        # Valid => should not raise any exception
        proj.acknowledgement = "To cite this project, please make me a coffee first..."
        # ------------------------------------------------------------------------------------------------------------ #

    def test_setting_project_directory_path(self):
        """
        Tests setting a project directory path
        """
        proj = Project(category="COSMOLOGY", project_title="My awesome project")

        with pytest.raises(AttributeError) as e:
            proj.directory_path = {'a': 45.2}
        assert str(e.value) == "Project 'directory_path' property is not a valid string"

        # Valid => should not raise any exception
        proj.directory_path = "/data/ramses/simulations/run_1/outputs/"

    def test_setting_thumbnail_image(self, tmp_path):
        """
        Tests setting a thumbnail image

        Parameters
        ----------
        tmp_path: temporary path  PyTest fixture
        """
        proj = Project(category="COSMOLOGY", project_title="My awesome project")

        # Test setting a thumbnail image with a tuple
        with pytest.raises(ValueError, match="Only image \(JPEG/PNG\) image file paths or ImageFile objects can be set "
                                             "in Project as thumbnail images."):
            proj.thumbnail_image = (4, True)

        # Try setting a . ini file as thumbnail image
        with pytest.raises(ValueError, match="Only image \(PNG/JPEG\) image file paths can be set in Project as "
                                             "thumbnail images."):
            proj.thumbnail_image = os.path.join(os.path.dirname(__file__), "io", "datafiles", "test_implode_2D.ini")

        # All good
        proj.thumbnail_image = None
        png_fpath = os.path.join(os.path.dirname(__file__), "io", "datafiles", "CEA.png")
        proj.thumbnail_image = png_fpath

        # Save study
        s = SimulationStudy(project=proj)
        study_fname = str(tmp_path / "project_thumbnail.h5")
        # Save study with a thumbnail image file
        s.save_HDF5(study_fname)

        # Reload it and save it again in same study HDF5 file with no thumbnail image defined
        ls = SimulationStudy.load_HDF5(study_fname)
        assert ls.project.thumbnail_image == PngImageFile.load_file(png_fpath)
        ls.project.thumbnail_image = None
        ls.save_HDF5(study_fname)  # new_file = False here
        ls2 = SimulationStudy.load_HDF5(study_fname)
        assert ls2.project.thumbnail_image is None

        # Relaod it and save it again in new HDF5 study file with no thumbnail image defined
        study_fname_none = str(tmp_path / "project_thumbnail_none.h5")
        ls2.save_HDF5(study_fname_none)  # new file = True here
        lsnone = SimulationStudy.load_HDF5(study_fname_none)
        assert lsnone.project.thumbnail_image is None

    def test_project_comparison(self):
        """
        Tests Project instance equality method
        """
        proj1 = Project(category=ProjectCategory.Cosmology, project_title="My awesome project", alias="NEW_PROJ",
                        short_description="Short description of my project",
                        general_description="""This is a pretty long description for my project""",
                        data_description="The data available in this project...", acknowledgement="Cite me !",
                        thumbnail_image=os.path.join(os.path.dirname(__file__), "io", "datafiles", "CEA.png"),
                        directory_path="/path/to/my_data/")

        # Different UUID => not equals
        assert proj1 != Project(category=ProjectCategory.Cosmology, project_title=proj1.project_title,
                                alias=proj1.alias, short_description=proj1.short_description,
                                general_description=proj1.general_description, data_description=proj1.data_description,
                                acknowledgement=proj1.acknowledgement, directory_path=proj1.directory_path,
                                thumbnail_image=os.path.join(os.path.dirname(__file__), "io", "datafiles", "CEA.png"))

        # Different category => not equals
        assert proj1 != Project(category=ProjectCategory.StarFormation, project_title=proj1.project_title, uid=proj1.uid,
                                alias=proj1.alias, short_description=proj1.short_description,
                                general_description=proj1.general_description, data_description=proj1.data_description,
                                acknowledgement=proj1.acknowledgement, directory_path=proj1.directory_path,
                                thumbnail_image=os.path.join(os.path.dirname(__file__), "io", "datafiles", "CEA.png"))

        # Different title => not equals
        assert proj1 != Project(category=ProjectCategory.Cosmology, project_title="My best project", uid=proj1.uid,
                                alias=proj1.alias, short_description=proj1.short_description,
                                general_description=proj1.general_description, data_description=proj1.data_description,
                                acknowledgement=proj1.acknowledgement, directory_path=proj1.directory_path,
                                thumbnail_image=os.path.join(os.path.dirname(__file__), "io", "datafiles", "CEA.png"))

        # Different alias => not equals
        assert proj1 != Project(category=ProjectCategory.Cosmology, project_title=proj1.project_title, uid=proj1.uid,
                                alias="PROJ_A", short_description=proj1.short_description,
                                general_description=proj1.general_description, data_description=proj1.data_description,
                                acknowledgement=proj1.acknowledgement, directory_path=proj1.directory_path,
                                thumbnail_image=os.path.join(os.path.dirname(__file__), "io", "datafiles", "CEA.png"))

        # Different short description => not equals
        assert proj1 != Project(category=ProjectCategory.Cosmology, project_title=proj1.project_title, uid=proj1.uid,
                                alias=proj1.alias, short_description="short project description",
                                general_description=proj1.general_description, data_description=proj1.data_description,
                                acknowledgement=proj1.acknowledgement, directory_path=proj1.directory_path,
                                thumbnail_image=os.path.join(os.path.dirname(__file__), "io", "datafiles", "CEA.png"))

        # Different general description => not equals
        assert proj1 != Project(category=ProjectCategory.Cosmology, project_title=proj1.project_title, uid=proj1.uid,
                                alias=proj1.alias, short_description=proj1.short_description,
                                general_description="gen. desc.", data_description=proj1.data_description,
                                acknowledgement=proj1.acknowledgement, directory_path=proj1.directory_path,
                                thumbnail_image=os.path.join(os.path.dirname(__file__), "io", "datafiles", "CEA.png"))

        # Different data description => not equals
        assert proj1 != Project(category=ProjectCategory.Cosmology, project_title=proj1.project_title, uid=proj1.uid,
                                alias=proj1.alias, short_description=proj1.short_description,
                                general_description=proj1.general_description, data_description="data desc",
                                acknowledgement=proj1.acknowledgement, directory_path=proj1.directory_path,
                                thumbnail_image=os.path.join(os.path.dirname(__file__), "io", "datafiles", "CEA.png"))

        # Different data directory path => not equals
        assert proj1 != Project(category=ProjectCategory.Cosmology, project_title=proj1.project_title, uid=proj1.uid,
                                alias=proj1.alias, short_description=proj1.short_description,
                                general_description=proj1.general_description, data_description=proj1.data_description,
                                acknowledgement=proj1.acknowledgement, directory_path="/other/path/",
                                thumbnail_image=os.path.join(os.path.dirname(__file__), "io", "datafiles", "CEA.png"))

        # Different project acknowledgement text => not equals
        assert proj1 != Project(category=ProjectCategory.Cosmology, project_title=proj1.project_title, uid=proj1.uid,
                                alias=proj1.alias, short_description=proj1.short_description,
                                general_description=proj1.general_description, data_description=proj1.data_description,
                                acknowledgement="Hey ! This is a good citation...", directory_path=proj1.directory_path,
                                thumbnail_image=os.path.join(os.path.dirname(__file__), "io", "datafiles", "CEA.png"))

        # Different project thumbnail images
        assert proj1 != Project(category=ProjectCategory.Cosmology, project_title=proj1.project_title, uid=proj1.uid,
                                alias=proj1.alias, short_description=proj1.short_description,
                                general_description=proj1.general_description, data_description=proj1.data_description,
                                acknowledgement=proj1.acknowledgement, directory_path=proj1.directory_path,
                                thumbnail_image=os.path.join(os.path.dirname(__file__), "io",
                                                             "datafiles", "irfu_simple.jpg"))

        # Identical projects
        p = Project(category=ProjectCategory.Cosmology, project_title=proj1.project_title, uid=proj1.uid,
                    alias=proj1.alias, short_description=proj1.short_description, directory_path=proj1.directory_path,
                    general_description=proj1.general_description, data_description=proj1.data_description,
                    thumbnail_image=os.path.join(os.path.dirname(__file__), "io", "datafiles", "CEA.png"),
                    acknowledgement=proj1.acknowledgement)
        assert proj1 == p

        # Simulation list differ => not equals
        ramses = protocol.SimulationCode(name="Ramses 3 (MHD)", code_name="Ramses")
        proj1.simulations.add(experiment.Simulation(name="My simu épatante", alias="SIMU_1", simu_code=ramses))
        assert proj1 != p

    def test_project_invalid_attribute(self, caplog):
        """
        Tests project invalid attribute warning log message

        Parameters
        ----------
        caplog: captured log PyTest fixture
        """
        proj = Project(category="COSMOLOGY", project_title="Proj title",
                       attribute_A=34.619)
        assert caplog.record_tuples[-1] == ('astrophysix', logging.WARNING,
                                            "'attribute_A' attribute is unknown for a 'Project' object. It is therefore"
                                            " ignored.")

    def test_project_simu_datatable_insertion_deletion(self):
        """

        :return:
        """
        """
        Tests project Galactica validity checks

        Parameters
        ----------
        caplog: captured log PyTest fixture
        """
        proj = Project(category="COSMOLOGY", project_title="Proj title", alias="TEST_PROJ")
        ramses = protocol.SimulationCode(name="Ramses 3.0 (Hydro)", code_name="RAMSES", alias="RAMSES_CODE")
        # Add input parameters
        lmin = ramses.input_parameters.add(InputParameter(key="levelmin", name="l_min", description="min. level of AMR refinement"))
        lmax = ramses.input_parameters.add(InputParameter(key="levelmax", name="l_max", description="max. level of AMR refinement"))
        boxlen = InputParameter(key="boxlen", name="L_box", description="size of simulation domain")

        proj.simulations.add(experiment.Simulation(ramses, name="My simu (hydro)", alias="SIMU_1",
                                                   execution_time="2020-11-01 10:30:00"))

        with pytest.raises(AttributeError, match="Project '\[boxlen\] 'L_box' input parameter' does not refer to any "
                                                 "input parameter of the project's simulation codes."):
            proj.simu_datatable_params.add(boxlen)  # Boxlen is not an input parameter of RAMSES

        proj.simu_datatable_params.add(lmin)
        proj.simu_datatable_params.add(lmax)
        with pytest.raises(AttributeError, match="'\[levelmin\] 'l_min' input parameter' cannot be deleted, the "
                                                 "following items depend on it \(try to delete them first\) : "
                                                 "\[Simulation datatable \[levelmin\] 'l_min' input parameter\]."):
            del ramses.input_parameters[lmin]  # lmin belongs to the list of simulation datatable parameters, you cannot delete it

        # Delete it first from the simu datatable parameter list, then delete it from RAMSES input parameter list
        del proj.simu_datatable_params[lmin]
        del ramses.input_parameters[lmin]  # Ok

    def test_project_galactica_validity_checks(self, caplog):
        """
        Tests project Galactica validity checks

        Parameters
        ----------
        caplog: captured log PyTest fixture
        """
        proj = Project(category="COSMOLOGY", project_title="Proj title",
                       short_description="This is short description of my project")

        # No alias defined
        proj.galactica_validity_check()
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "[Cosmology] 'Proj title' project Galactica alias is missing.")

        # Alias too long
        proj.alias = "MY_ALIAS_123456789_10"
        proj.galactica_validity_check()
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "[Cosmology] 'Proj title' project Galactica alias is too long (max. 16 "
                                            "characters).")
        proj.alias = "MY_ALIAS"  # => Ok

        # Invalid Galactica aliases
        for inv_alias in ["8PROJ", "PROJ+SCIENCE", "_PROJ_A", "PROJ_", "PROJ_hydro", "hydro_RUN_4", "MY_hydro_8", "B_"]:
            proj.alias = inv_alias
            proj.galactica_validity_check()
            assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                                "[Cosmology] 'Proj title' project Galactica alias is not valid (The "
                                                "alias can contain capital letters, digits and '_' only. It must start "
                                                "with a capital letter and cannot end with a '_'.)")
            proj.alias = "MY_ALIAS_123456789_10"  # Alias too long => just to interleave another warning message
            proj.galactica_validity_check()
        proj.alias = "MY_ALIAS"  # => Ok

        # No project title defined => Should never happen
        # [...]

        # Project title too long
        proj.project_title = "This  is a pretty long title for a project that has absolutely no sense. It means that " \
                             "this project title can be as long as 400 hundred chars and still be valid ? Come on..."
        proj.galactica_validity_check()
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "[Cosmology] 'This  is a pretty long title for a project that has "
                                            "absolutely no sense. It means that this project title can be as long as "
                                            "400 hundred chars and still be valid ? Come on...' project Galactica "
                                            "project title is too long (max. 128 characters).")
        proj.project_title = "Proj title"  # => Ok

        # No short description defined
        proj.short_description = ""
        proj.galactica_validity_check()
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "[Cosmology] 'Proj title' project Galactica short description is missing.")

        # Short description too long
        proj.short_description = "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz" \
                                 "yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy" \
                                 "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
                                 "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww"
        proj.galactica_validity_check()
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "[Cosmology] 'Proj title' project Galactica short description is too long "
                                            "(max. 256 characters).")
        proj.short_description = "This is a pretty short description"  # => Ok

        # Simulation code duplicates (same aliases)
        ramses1 = protocol.SimulationCode(name="Ramses 3.0 (Hydro)", code_name="RAMSES", alias="RAMSES_CODE")
        ramses2 = protocol.SimulationCode(name="Ramses 3.1 (MHD)", code_name="RAMSES", alias="RAMSES_CODE")
        simu1 = proj.simulations.add(experiment.Simulation(ramses1, name="My simu (hydro)", alias="SIMU_1",
                                                           execution_time="2020-11-01 10:30:00"))
        simu2 = proj.simulations.add(experiment.Simulation(ramses2, name="My simu (MHD)", alias="SIMU_2",
                                                           execution_time="2020-11-01 10:30:00"))
        proj.galactica_validity_check()
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "[Ramses 3.0 (Hydro)] simulation code and [Ramses 3.1 (MHD)] simulation "
                                            "code protocols share the same alias. They must be unique.")
        ramses2.alias = "RAMSES_OTHER"  # protocol.alias differ => Ok

        # Simulation duplicates (same aliases)
        simu2.alias = simu1.alias
        proj.galactica_validity_check()
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "'My simu (hydro)' simulation and 'My simu (MHD)' simulation experiments "
                                            "share the same alias. They must be unique.")
        simu1.alias = "MY_ALIAS_SIMU"

        # Tests target object duplicates (same name)
        sn1 = simu1.snapshots.add(Snapshot(name="My snapshot"))
        sn2 = simu2.snapshots.add(Snapshot(name="My snapshot (2)"))
        tobj = TargetObject(name="Galaxy")
        m = tobj.object_properties.add(ObjectProperty(property_name="mass"))
        cat1 = sn1.catalogs.add(Catalog(name="My catalog", target_object=tobj))
        cat1.catalog_fields.add(CatalogField(obj_prop=m, values=N.random.uniform(size=10)))
        tobj2 = TargetObject(name="Galaxy")
        m2 = tobj2.object_properties.add(ObjectProperty(property_name="mass"))
        cat2 = sn2.catalogs.add(Catalog(name="My catalog", target_object=tobj2))
        cat2.catalog_fields.add(CatalogField(obj_prop=m2, values=N.random.uniform(size=10)))
        proj.galactica_validity_check()
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "'Galaxy' target object and 'Galaxy' target object share the same name. "
                                            "They must be unique.")

    def test_project_targobj_hdf5_io_compatibility_v1(self):
        """Backward compatibility test : tests loading a Simulation study saved with version v<0.5.0 where Catalog and
        TargetObject instances did not exist."""
        # Try to load a Project with no catalog/target object (v1), saved by an older version of astrophysix (v<0.5)
        study_0_4_2_path = os.path.join(os.path.dirname(__file__), "io", "backward_compat", "study_v0.4.2.h5")
        study = SimulationStudy.load_HDF5(study_0_4_2_path)
        assert study.project.project_title == "My awesome project"
        assert study.project.acknowledgement == ""  # No 'acknowledgement' property defined in v0.4.2
        assert study.project.thumbnail_image is None  # No 'thumbnail_image' property defined in v0.6
        # No target object
        assert len([tobj for tobj in study.project._target_objects()]) == 0

    def test_project_hdf5_io(self, tmp_path):
        """
        Tests saving/loading Project from HDF5 file

        Parameters
        ----------
        tmp_path: temporary path  PyTest fixture
        """
        proj = Project(category="COSMOLOGY", project_title="My awesome project€", alias="NEW_PROJ",
                       short_description="Short description of my project",
                       general_description="""This is a pretty long description for my project""",
                       data_description="The data available in this project...", acknowledgement="Cite me !",
                       thumbnail_image=os.path.join(os.path.dirname(__file__), "io", "datafiles", "irfu_simple.jpg"),
                       directory_path="/path/to/my_data/")
        ramses = protocol.SimulationCode(name="Ramses 3 (MHD)", code_name="Ramses", code_version="3.0.0")
        proj.simulations.add(experiment.Simulation(name="My simu épatante", alias="SIMU_1",
                                                   description="simu description", simu_code=ramses))

        fname = str(tmp_path / "proj.h5")
        study = SimulationStudy(project=proj)
        study.save_HDF5(fname)
        study_loaded = SimulationStudy.load_HDF5(fname)
        proj_loaded = study_loaded.project
        assert proj_loaded == proj


__all__ = ["TestProjectCategory", "TestProject"]

