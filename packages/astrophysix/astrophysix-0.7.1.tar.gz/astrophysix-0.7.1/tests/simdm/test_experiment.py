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

from future.builtins import str, int
import pytest
import logging
from astrophysix.simdm import SimulationStudy, Project, ProjectCategory
from astrophysix.simdm.protocol import AlgoType, Algorithm, InputParameter, PhysicalProcess, Physics
from astrophysix.simdm.experiment import Simulation, AppliedAlgorithm, ParameterSetting, ParameterVisibility,\
    ResolvedPhysicalProcess, PostProcessingRun
from astrophysix.simdm.protocol import SimulationCode, PostProcessingCode
from astrophysix.simdm.experiment.base import Experiment
from astrophysix.simdm.results import GenericResult, Snapshot
from astrophysix.simdm.datafiles import YamlFile, AsciiFile
from astrophysix.simdm.utils import DataType
from astrophysix import units as U


class TestAppliedAlgorithm(object):
    def test_applied_algo_init(self):
        """
        Tests AppliedAlgorithm instance initialisation
        """
        # Applied algorithm initialisation
        amr_algo = Algorithm(algo_type=AlgoType.AdaptiveMeshRefinement)
        amr = AppliedAlgorithm(algorithm=amr_algo, details="Implementation #3")

        assert amr.implementation_details == "Implementation #3"

        # Test str() conversion
        assert str(amr) == "[Adaptive mesh refinement] applied algorithm"

    def test_setting_algorithm_type_exc(self):
        """
        Tests that an AppliedAlgorithm instantiated without an Algorithm or with an invalid Algorithm instance raises
        an exception
        """
        # Tests applied algorithm defined without algorithm
        with pytest.raises(AttributeError, match="AppliedAlgorithm 'algorithm' attribute is not defined \\(mandatory\\)."):
            app_algo_exc = AppliedAlgorithm()  # No algorithm defined

        with pytest.raises(AttributeError, match="AppliedAlgorithm 'algorithm' attribute is not a valid Algorithm "
                                                 "object."):
            app_algo_exc = AppliedAlgorithm(algorithm=[9, 4.5, 2, 0.2])  # Invalid algorithm

    def test_setting_applied_algorithm_impl_details(self):
        """
        Tests setting applied algorithm implementation details property
        """
        algo = Algorithm(algo_type=AlgoType.Godunov)
        app_algo = AppliedAlgorithm(algorithm=algo)

        # ---------------- Tests invalid applied algorithm implementation details setting exception ------------------ #
        with pytest.raises(AttributeError, match="AppliedAlgorithm 'implementation_details' property is not a valid string."):
            app_algo.implementation_details = 0
        # ------------------------------------------------------------------------------------------------------------ #

        # Valid => should not raise any exception
        app_algo.implementation_details = "Description of the best implementation of the Godunov scheme on Earth"
        assert app_algo.implementation_details == "Description of the best implementation of the Godunov scheme on Earth"

    def test_appalgo_equality(self):
        """
        Tests rich comparison method AppliedAlgorithm.__eq__()
        """
        amr_algo = Algorithm(algo_type=AlgoType.AdaptiveMeshRefinement)
        amr = AppliedAlgorithm(algorithm=amr_algo, details="Implementation #3")

        # Different UUID => not equals
        assert amr != AppliedAlgorithm(algorithm=amr_algo, details=amr.implementation_details)

        # Different algorithm => not equals
        algo2 = Algorithm(algo_type=AlgoType.ParticleMesh)
        assert amr != AppliedAlgorithm(algorithm=algo2, details=amr.implementation_details, uid=amr.uid)

        # Different implementation details => not equals
        assert amr != AppliedAlgorithm(algorithm=amr_algo, uid=amr.uid, details="Alt. details")

        # Identical applied algorithm
        assert amr == AppliedAlgorithm(algorithm=amr_algo, uid=amr.uid, details=amr.implementation_details)


class TestParameterSetting(object):
    def test_psetting_init(self):
        """
        Tests ParameterSetting instance initialisation
        """
        # ParameterSetting code initialisation
        lmin = InputParameter(key="levelmin", name="lmin")
        psetting = ParameterSetting(input_param=lmin, value=7, visibility="not_displayed")

        assert psetting.input_parameter == lmin
        assert psetting.visibility == ParameterVisibility.NOT_DISPLAYED
        assert psetting.unit == U.none

        # Test str() conversion
        assert str(psetting) == "[lmin = 7] parameter setting"

    def test_setting_psetting_inpparam_exc(self):
        """
        Tests that a ParameterSetting instantiated without an InputParameter or an invalid InputParameter object raises
        an exception
        """
        # Tests parameter setting defined without input parameter
        with pytest.raises(AttributeError, match="ParameterSetting 'input_param' attribute is not defined "
                                                 "\\(mandatory\\)."):
            ps_exc = ParameterSetting()  # No input parameter defined

        # Tests parameter setting 'input_param' attribute initialisation exception
        with pytest.raises(AttributeError, match="Parameter setting 'input_param' attribute is not a valid "
                                                 "InputParameter object."):
            ps_exc = ParameterSetting(input_param=("Apple", 3, True))  # Invalid input parameter

    def test_psetting_value_exc(self):
        """
        Tests setting parameter setting 'value' property
        """
        ip = InputParameter(name="rho_saddle")
        # ---------------------- Tests parameter setting instantiation without value exception ----------------------- #
        with pytest.raises(AttributeError, match="ParameterSetting 'value' attribute is not defined \\(mandatory\\)."):
            psetting_exc = ParameterSetting(input_param=ip)
        # ------------------------------------------------------------------------------------------------------------ #

        # --------------------------- Tests invalid parameter setting value setting exception ------------------------ #
        invalid_psetting_value_err = "ParameterSetting 'value' attribute is not a valid string / integer / float " \
                                     "/ boolean value"
        with pytest.raises(AttributeError, match=invalid_psetting_value_err) as e:
            psetting_exc = ParameterSetting(input_param=ip, value=("Star", "Planet", "Galaxy"))

        with pytest.raises(AttributeError, match=invalid_psetting_value_err):
            psetting = ParameterSetting(input_param=ip, value=0.5)
            psetting_exc = psetting.value = [-1, "Black hole", False]
        # ------------------------------------------------------------------------------------------------------------ #

        # Valid => should not raise any exception
        psetting = ParameterSetting(input_param=ip, value=0.5)
        assert type(psetting.value) is float and psetting.value == 0.5 and psetting.value_type == DataType.REAL
        for true_val in [True, "true", "True", "TRUE", ".true."]:
            psetting.value = true_val
            assert type(psetting.value) is bool and psetting.value is True and psetting.value_type == DataType.BOOLEAN
        for false_val in [False, "false", "False", "FALSE", ".false."]:
            psetting.value = false_val
            assert type(psetting.value) is bool and psetting.value is False and psetting.value_type == DataType.BOOLEAN

        psetting.value = "banana"
        assert type(psetting.value) is str and psetting.value == "banana" and psetting.value_type == DataType.STRING
        psetting.value = 4.256
        assert type(psetting.value) is float and psetting.value == 4.256 and psetting.value_type == DataType.REAL
        psetting.value = 58.0
        assert type(psetting.value) is int and psetting.value == 58 and psetting.value_type == DataType.INTEGER
        psetting.value = "12.0"
        assert type(psetting.value) is int and psetting.value == 12 and psetting.value_type == DataType.INTEGER
        psetting.value = "3.584e2"
        assert type(psetting.value) is float and psetting.value == 358.4 and psetting.value_type == DataType.REAL
        psetting.value = "-254"
        assert type(psetting.value) is int and psetting.value == -254 and psetting.value_type == DataType.INTEGER

    def test_setting_psetting_unit(self):
        """
        Tests setting parameter setting unit property
        """
        ip = InputParameter(name="rho_saddle")
        psetting = ParameterSetting(input_param=ip, value=1.0e-6, unit=U.H_cc)

        # --------------------------- Tests invalid parameter setting unit setting exception ------------------------- #
        with pytest.raises(AttributeError, match="Parameter setting 'unit' property error : Unknown unit name "
                                                 "'fairies'."):
            psetting.unit = "fairies"

        invalid_psetting_unit_err = "Parameter setting 'unit' property is not a valid \\(non-empty\\) string."
        with pytest.raises(AttributeError, match=invalid_psetting_unit_err):
            psetting.unit = ""

        with pytest.raises(AttributeError, match=invalid_psetting_unit_err):
            psetting.unit = ["kg", "V", "cm", "Gauss"]
        # ------------------------------------------------------------------------------------------------------------ #

        # Valid => should not raise any exception
        psetting.unit = U.g_cc
        assert psetting.unit == U.g_cc

    def test_setting_psetting_visibility(self):
        """
        Tests setting parameter setting visibility property
        """
        ip = InputParameter(name="rho_saddle")
        psetting = ParameterSetting(input_param=ip, value=1.0e-6, visibility=ParameterVisibility.NOT_DISPLAYED)

        # ----------------------- Tests invalid parameter setting visibility setting exception ----------------------- #
        exc_msg = "Parameter setting 'visibility' property error : No ParameterVisibility defined with the key " \
                  "'custom_display'."
        with pytest.raises(AttributeError, match=exc_msg):
            psetting.visibility = "custom_display"

        with pytest.raises(AttributeError, match="ParameterSetting 'visibility' attribute is not a valid "
                                                 "ParameterVisibility enum value."):
            psetting.visibility = {"a": 0.45}
        # ------------------------------------------------------------------------------------------------------------ #

        # Valid => should not raise any exception
        psetting.visibility = ParameterVisibility.ADVANCED_DISPLAY.key
        assert psetting.visibility == ParameterVisibility.ADVANCED_DISPLAY

    def test_param_setting_equality(self):
        """
        Tests rich comparison method ParameterSetting.__eq__()
        """
        dx_min = InputParameter(key="dx_min", name="min_resolution")
        psetting = ParameterSetting(input_param=dx_min, value=12.5, unit=U.kpc,
                                    visibility=ParameterVisibility.ADVANCED_DISPLAY)

        # Different UUID => not equals
        assert psetting != ParameterSetting(input_param=dx_min, value=psetting.value, unit=psetting.unit,
                                            visibility=psetting.visibility)

        # Different input parameter => not equals
        lmin = InputParameter(key="lmin", name="levelmin")
        assert psetting != ParameterSetting(input_param=lmin, value=psetting.value, unit=psetting.unit,
                                            visibility=psetting.visibility, uid=psetting.uid)

        # Different value => not equals
        assert psetting != ParameterSetting(input_param=dx_min, value=13.3, unit=psetting.unit,
                                            visibility=psetting.visibility, uid=psetting.uid)

        # Different unit => not equals
        assert psetting != ParameterSetting(input_param=dx_min, value=psetting.value, unit=U.km,
                                            visibility=psetting.visibility, uid=psetting.uid)

        # Different visibility => not equals
        assert psetting != ParameterSetting(input_param=dx_min, value=psetting.value, unit=psetting.unit,
                                            visibility=ParameterVisibility.NOT_DISPLAYED, uid=psetting.uid)

        # Identical parameter setting
        assert psetting == ParameterSetting(input_param=dx_min, value=psetting.value, unit=psetting.unit,
                                            visibility=psetting.visibility, uid=psetting.uid)

    def test_param_setting_galactica_validity_checks(self, caplog):
        """
        Tests parameter setting Galactica validity checks

        Parameters
        ----------
        caplog: captured log PyTest fixture
        """
        oredring_inpp = InputParameter(key="decomp", name="Ordering")
        psetting = ParameterSetting(input_param=oredring_inpp, value="hilbert",
                                    visibility=ParameterVisibility.ADVANCED_DISPLAY)

        # Parameter setting string value too long
        psetting.value = "This is a value way too long for a simple 'ordering' RAMSES input parameter"
        psetting.galactica_validity_check()
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "[Ordering = This is a value way too long for a simple 'ordering' RAMSES "
                                            "input parameter] parameter setting Galactica string value is too long "
                                            "(max. 64 characters).")


class TestResolvedPhysicalProcess(object):
    def test_res_physproc_init(self):
        """
        Tests ResolvedPhysicalProcess instance initialisation
        """
        # resolved physical process initialisation
        phys = PhysicalProcess(physics=Physics.AGNFeedback)
        res_agn_fb = ResolvedPhysicalProcess(physics=phys, details="Implemnt. #10")

        assert res_agn_fb.implementation_details == "Implemnt. #10"

        # Test str() conversion
        assert str(res_agn_fb) == "[AGN feedback] resolved physical process"

    def test_setting_physics_exc(self):
        """
        Tests that an ResolvedPhysicalProcess instantiated without a PhysicalProcess or with an invalid PhysicalProcess
        instance raises an exception
        """
        # Tests resolved physical process defined without physical process
        with pytest.raises(AttributeError, match="ResolvedPhysicalProcess 'physics' attribute is not defined "
                                                 "\\(mandatory\\)."):
            res_phys_exc = ResolvedPhysicalProcess()  # No physical process defined

        with pytest.raises(AttributeError, match="ResolvedPhysicalProcess 'physics' attribute is not a valid "
                                                 "PhysicalProcess object."):
            res_phys_exc = ResolvedPhysicalProcess(physics={"B": ["my", "physics"]})  # Invalid physical process

    def test_setting_resolved_physics_impl_details(self):
        """
        Tests setting ResolvedPhysicalProcess implementation details property
        """
        phys = PhysicalProcess(physics=Physics.AGNFeedback)
        res_agn_fb = ResolvedPhysicalProcess(physics=phys)

        # ---------------- Tests invalid applied algorithm implementation details setting exception ------------------ #
        with pytest.raises(AttributeError, match="ResolvedPhysicalProcess 'implementation_details' property is not a "
                                                 "valid string."):
            res_agn_fb.implementation_details = {"are": "you crazy ?"}
        # ------------------------------------------------------------------------------------------------------------ #

        # Valid => should not raise any exception
        res_agn_fb.implementation_details = "Implementation following Dubois & Teyssier 2008"
        assert res_agn_fb.implementation_details == "Implementation following Dubois & Teyssier 2008"

    def test_resolved_physics_equality(self):
        """
        Tests rich comparison method ResolvedPhysicalProcess.__eq__()
        """
        agn = PhysicalProcess(physics=Physics.AGNFeedback)
        res_agn_fb = ResolvedPhysicalProcess(physics=agn, details="Implemnt. #10")

        # Different UUID => not equals
        assert res_agn_fb != ResolvedPhysicalProcess(physics=agn, details=res_agn_fb.implementation_details)

        # Different physical process => not equals
        sf = PhysicalProcess(physics=Physics.StarFormation)
        assert res_agn_fb != ResolvedPhysicalProcess(physics=sf, details=res_agn_fb.implementation_details,
                                                     uid=res_agn_fb.uid)

        # Different implementation details => not equals
        assert res_agn_fb != ResolvedPhysicalProcess(physics=res_agn_fb.physical_process, details="Alt. det",
                                                     uid=res_agn_fb.uid)

        # IDentical resolved physical process
        assert res_agn_fb == ResolvedPhysicalProcess(physics=agn, details=res_agn_fb.implementation_details,
                                                     uid=res_agn_fb.uid)


class TestExperiment(object):
    def test_experiment_init(self):
        """
        Tests Experiment instance initialisation
        """
        # Simulation initialisation
        cfg_filepath = os.path.join(os.path.dirname(__file__), "io", "datafiles", "config.yml")
        exp = Experiment(name="My experiment énorme", alias="EXP_1", directory_path="/path/to/my/experiment",
                         description="""This is a pretty long description for my experiment""",
                         config_file=YamlFile.load_file(cfg_filepath))

        assert isinstance(exp.name, str)
        assert exp.alias == "EXP_1"
        assert isinstance(exp.alias, str)
        assert exp.name == "My experiment énorme"
        assert exp.description == "This is a pretty long description for my experiment"
        assert exp.directory_path == "/path/to/my/experiment"
        assert isinstance(exp.configuration_file, YamlFile) and \
               exp.configuration_file.file_md5sum == "ea17280e7d8cdf602fa7e5a436f00733"

    def test_setting_exp_name_exc(self):
        """
        Tests that an experiment defined without name raises an exception
        """
        # Tests experiment defined without name
        with pytest.raises(AttributeError, match="Experiment 'name' attribute is not defined \\(mandatory\\)."):
            exp_exc = Experiment()  # No experiment name defined

        exp = Experiment(name="My Experiment")

        # ------------- Tests invalid experiment name setting exception ---------------------- #
        empty_name_err = "Experiment 'name' property is not a valid \\(non-empty\\) string"
        with pytest.raises(AttributeError, match=empty_name_err):
            exp.name = -1

        with pytest.raises(AttributeError, match=empty_name_err):
            exp.name = ""
        # ------------------------------------------------------------------------------------ #

        # Valid => should not raise any exception
        exp.name = "The best experiment ever"

    def test_setting_experiment_alias_exc(self, caplog):
        """
        Tests setting an experiment alias

        caplog: captured log PyTest fixture
        """
        exp = Experiment(name="My super experiment")

        # Tests invalid experiment alias setting exception
        with pytest.raises(AttributeError, match="Experiment 'alias' property is not a valid string"):
            simu_exc = Experiment(name="My super experiment", alias=("Dog", 3))

        with pytest.raises(AttributeError, match="Experiment 'alias' property is not a valid string"):
            exp.alias = -2.45

        # Valid => should not raise any exception
        exp.alias = "TOP_EXP_1"

        # Valid but should log a warning
        exp.alias = "ULTRA_AWESOMENESS"
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "Experiment 'alias' attribute is too long (max 16 characters).")

    def test_setting_experiment_description(self):
        """
        Tests setting experiment description property
        """
        exp = Experiment(name="My super experiment")

        # ------------------------ Tests invalid experiment description setting exception ---------------------------- #
        with pytest.raises(AttributeError, match="Experiment 'description' property is not a valid string"):
            exp.description = 0

        # Valid => should not raise any exception
        exp.description = "My experiment description"
        # ------------------------------------------------------------------------------------------------------------ #

    def test_setting_experiment_dirpath(self):
        """
        Tests setting experiment directory path property
        """
        exp = Experiment(name="My super simu")

        # ----------------------- Tests invalid experiment directory path setting exception -------------------------- #
        with pytest.raises(AttributeError, match="Experiment 'directory_path' property is not a valid string"):
            exp.directory_path = (-1, ["Banana", "Apple"])

        # Valid => should not raise any exception
        exp.directory_path = "/better/path/to/my/experiment"
        # ------------------------------------------------------------------------------------------------------------ #

    def test_setting_experiment_config_file(self):
        """
        Tests setting experiment configuration file property
        """
        exp = Experiment(name="My super simu")

        # ---------------------- Tests invalid experiment configuration file setting exception ----------------------- #
        with pytest.raises(AttributeError, match="Experiment 'configuration_file' property is neither None nor a valid "
                                                 "JsonFile, YamlFile or AsciiFile instance."):
            exp.configuration_file = {"A": -23.256}

        # Valid => should not raise any exception
        exp.configuration_file = None
        cfg_filepath = os.path.join(os.path.dirname(__file__), "io", "datafiles", "test_implode_2D.ini")
        exp.configuration_file = AsciiFile.load_file(cfg_filepath)
        # ------------------------------------------------------------------------------------------------------------ #

    def test_experiment_equality(self):
        """
        Tests rich comparison method Experiment.__eq____()
        """
        ramses = SimulationCode(name="Ramses 3 (MHD)", code_name="Ramses")
        cfg_filepath = os.path.join(os.path.dirname(__file__), "io", "datafiles", "config.yml")
        exp = Experiment(name="My experiment énorme", alias="EXP_1", description="experiment description",
                         directory_path="/path/to/my/experiment", config_file=YamlFile.load_file(cfg_filepath))
        exp._protocol = ramses

        # Different UUID => not equals
        assert exp != Experiment(name=exp.name, alias=exp.alias,
                                 description=exp.description, directory_path=exp.directory_path,
                                 config_file=YamlFile.load_file(cfg_filepath))

        # Different alias => not equals
        assert exp != Experiment(name=exp.name, alias="MY_EXP_Q", description=exp.description, uid=exp.uid,
                                 directory_path=exp.directory_path, config_file=YamlFile.load_file(cfg_filepath))

        # Different name => not equals
        assert exp != Experiment(name="other name", alias=exp.alias, description=exp.description, uid=exp.uid,
                                 directory_path=exp.directory_path, config_file=YamlFile.load_file(cfg_filepath))

        # Different description => not equals
        assert exp != Experiment(name=exp.name, alias=exp.alias, description="Alt. description", uid=exp.uid,
                                 directory_path=exp.directory_path, config_file=YamlFile.load_file(cfg_filepath))

        # Different directory path => not equals
        assert exp != Experiment(name=exp.name, alias=exp.alias, description=exp.description, uid=exp.uid,
                                 directory_path="/alt/path/to/experiment", config_file=YamlFile.load_file(cfg_filepath))

        # Identical experiments
        e = Experiment(name=exp.name, alias=exp.alias, description=exp.description, uid=exp.uid,
                       directory_path=exp.directory_path, config_file=YamlFile.load_file(cfg_filepath))
        e._protocol = ramses
        assert exp == e

        # Add applied algorithms
        ramses.algorithms.add(Algorithm(algo_type=AlgoType.AdaptiveMeshRefinement, description="AMR descr"))
        ramses.algorithms.add(Algorithm(algo_type=AlgoType.Godunov, description="Godunov scheme"))
        ramses.algorithms.add(Algorithm(algo_type=AlgoType.HLLCRiemann, description="HLLC Riemann solver"))
        ramses.algorithms.add(Algorithm(algo_type=AlgoType.PoissonMultigrid, description="Multigrid Poisson solver"))
        ramses.algorithms.add(Algorithm(algo_type=AlgoType.ParticleMesh, description="PM solver"))
        aa1 = exp.applied_algorithms.add(AppliedAlgorithm(algorithm=ramses.algorithms["Adaptive mesh refinement"],
                                                          details="My implementation"))
        aa2 = exp.applied_algorithms.add(AppliedAlgorithm(algorithm=ramses.algorithms["Harten-Lax-van Leer-Contact Riemann solver"],
                                                          details="My second implementation"))
        # Applied algorithms list differ => not equals
        e.applied_algorithms.add(aa1)
        assert exp != e
        # Identical experiments
        e.applied_algorithms.add(aa2)
        assert exp == e

        # Add parameter settings
        ramses.input_parameters.add(InputParameter(key="levelmin", name="Lmin",
                                                   description="min. level of AMR refinement"))
        ramses.input_parameters.add(InputParameter(key="levelmax", name="Lmax",
                                                   description="max. level of AMR refinement"))
        ps1 = exp.parameter_settings.add(ParameterSetting(input_param=ramses.input_parameters["Lmin"], value=8,
                                                          visibility=ParameterVisibility.BASIC_DISPLAY))
        ps2 = exp.parameter_settings.add(ParameterSetting(input_param=ramses.input_parameters["Lmax"], value=12,
                                                          visibility=ParameterVisibility.BASIC_DISPLAY))
        # Parameter settings list differ => not equals
        e.parameter_settings.add(ps1)
        assert exp != e
        # Identical experiments
        e.parameter_settings.add(ps2)
        assert exp == e

        # Add snapshots
        sn = exp.snapshots.add(Snapshot(name="First pericenter", description="Snapshot of the first pericenter",
                                        time=(100.25, U.Myr), physical_size=(1.0, U.pc),
                                        directory_path="/path/to/my/snapshot"))
        # Snapshot list differ => not equals
        assert e != exp
        # Identical experiments
        e.snapshots.add(sn)
        assert e == exp

        # Add generic results
        gres = exp.generic_results.add((GenericResult(name="Experiment main result")))
        # Generic result list differ => not equals
        assert exp != e
        # Identical experiments
        e.generic_results.add(gres)
        assert exp == e

    def test_experiment_galactica_validity_checks(self, caplog):
        """
        Tests experiment Galactica validity checks

        Parameters
        ----------
        caplog: captured log PyTest fixture
        """
        ramses = SimulationCode(name="Ramses 3.0 (Hydro)", code_name="RAMSES", alias="RAMSES_CODE")
        exp = Simulation(ramses, name="My simu (hydro)", execution_time="2020-06-01 20:00:00")

        # No alias defined
        exp.galactica_validity_check()
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "'My simu (hydro)' simulation Galactica alias is missing.")

        # Alias too long
        exp.alias = "MY_ALIAS_123456789_10_fgkjhfgoiurt_jnsdfnsdfdgdfgdfgdfgdfgkfgdfgdfgdgf"
        exp.galactica_validity_check()
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "'My simu (hydro)' simulation Galactica alias is too long (max. 64 "
                                            "characters).")

        # Invalid Galactica alias
        exp.alias = "MY_DUMMY_"
        exp.galactica_validity_check()
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "'My simu (hydro)' simulation Galactica alias is not valid (The alias can "
                                            "contain capital letters, digits and '_' only. It must start with a "
                                            "capital letter and cannot end with a '_'.)")

        # Result duplicates (same result names)
        exp.alias = "MY_ALIAS_123456789_10"  # => Ok
        exp.generic_results.add(GenericResult(name="My_result"))
        exp.snapshots.add(Snapshot(name="My_result"))
        exp.galactica_validity_check()
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "'My_result' generic result and 'My_result' snapshot results share the "
                                            "same name. They must be unique.")


class TestSimulation(object):
    def test_simu_init(self):
        """
        Tests Simulation instance initialisation
        """
        # Simulation initialisation
        ramses = SimulationCode(name="Ramses 3 (MHD)", code_name="Ramses")
        simu = Simulation(name="My simulation énorme", alias="SIMU_1", simu_code=ramses,
                          description="""This is a pretty long description for my simulation""",
                          directory_path="/path/to/my/simulation", execution_time="2020-03-01 18:45:30")

        assert isinstance(ramses.name, str)
        assert isinstance(simu.name, str)
        assert simu.alias == "SIMU_1"
        assert isinstance(simu.alias, str)
        assert simu.name == "My simulation énorme"
        assert simu.description == "This is a pretty long description for my simulation"
        assert simu.directory_path == "/path/to/my/simulation"
        assert isinstance(simu.execution_time, str)
        assert simu.execution_time == "2020-03-01 18:45:30"

        # Test str() conversion
        assert str(simu) == "'My simulation énorme' simulation"

    def test_simulation_simu_code_setting_exc(self):
        """
        Tests setting a simulation code into a simulation object
        """
        # Tests simulation defined without code
        with pytest.raises(AttributeError, match="Undefined simulation code for 'My super simulation' Simulation."):
            simu_exc = Simulation(name="My super simulation")  # No simulation code defined

        # Tests invalid simulation_code initialisation exception
        invalid_simu_code_err = "Simulation 'simulation_code' attribute is not a valid SimulationCode instance."
        with pytest.raises(AttributeError, match=invalid_simu_code_err):
            simu_exc = Simulation(name="My simu", simu_code=-5)  # Invalid simulation code
        with pytest.raises(AttributeError, match=invalid_simu_code_err):
            simu_exc = Simulation(-5, name="My simu")  # Invalid simulation code

        # Simulation initialisation : valid => should not raise any exception
        ramses = SimulationCode(name="Ramses", code_name="Ramses")
        simulation = Simulation(name="My simu", simu_code=ramses)
        simulation2 = Simulation(ramses, name="My simu")

    def test_setting_simulation_execution_time(self):
        """
        Tests setting simulation execution time property
        """
        ramses = SimulationCode(name="Ramses 3 (MHD)", code_name="Ramses")
        simu = Simulation(simu_code=ramses, name="My simu")

        # ------------------------ Tests invalid experiment description setting exception ---------------------------- #
        with pytest.raises(AttributeError, match="Simulation 'execution_time' property is not a valid datetime string."):
            simu.execution_time = {"a": 1.435}

        # Valid => should not raise any exception
        simu.execution_time = "2020-04-26 10:52:46"
        # ------------------------------------------------------------------------------------------------------------ #

    def test_simu_equality(self):
        """
        Tests rich comparison method Simulation.__eq____()
        """
        ramses = SimulationCode(name="Ramses 3 (MHD)", code_name="Ramses")
        simu = Simulation(simu_code=ramses, name="My simu énorme", execution_time="2020-03-01 18:45:30")

        # Different simulation code => not equals
        gadget = SimulationCode(name="Gadget 4.2.1", code_name="Gadget")
        assert simu != Simulation(name=simu.name, simu_code=gadget, uid=simu.uid, execution_time=simu.execution_time)

        # Different execution time => not equals
        assert simu != Simulation(name=simu.name, simu_code=simu.simulation_code, uid=simu.uid,
                                  execution_time="2018-09-14 15:48:32")

        # Identical simulations
        s = Simulation(name=simu.name, simu_code=simu.simulation_code, uid=simu.uid, execution_time=simu.execution_time)
        assert simu == s

        # Add resolved physical processes
        ramses.physical_processes.add(PhysicalProcess(physics=Physics.StarFormation, description="descr sf"))
        ramses.physical_processes.add(PhysicalProcess(physics=Physics.Hydrodynamics, description="descr hydro"))
        ramses.physical_processes.add(PhysicalProcess(physics=Physics.SelfGravity, description="descr self G"))
        ramses.physical_processes.add(PhysicalProcess(physics=Physics.SupernovaeFeedback, description="SN feedback"))
        rpp1 = simu.resolved_physics.add(ResolvedPhysicalProcess(physics=ramses.physical_processes["Star formation"],
                                                                 details="Star formation specific implementation"))
        rpp2 = simu.resolved_physics.add(ResolvedPhysicalProcess(physics=ramses.physical_processes["Self-gravity"],
                                                                 details="self-gravity specific implementation"))
        # Resolved physical processes list differ => not equals
        s.resolved_physics.add(rpp1)
        assert simu != s
        # Identical simulations
        s.resolved_physics.add(rpp2)
        assert simu == s

        # Add post-processing runs
        hop = PostProcessingCode(name="Hop", code_name="HOP")
        pprun = simu.post_processing_runs.add(PostProcessingRun(name="My post-processing run", ppcode=hop))
        # Post-processing runs differ => not equals
        assert simu != s
        # Identical simulations
        s.post_processing_runs.add(pprun)
        assert s == simu
        # ------------------------------------------------------------------------------------------------------------ #

    def test_simulation_galactica_validity_checks(self, caplog):
        """
        Tests simulation Galactica validity checks

        Parameters
        ----------
        caplog: captured log PyTest fixture
        """
        ramses = SimulationCode(name="Ramses 3.0 (Hydro)", code_name="RAMSES", alias="RAMSES_CODE")
        simu = Simulation(ramses, name="My simu (hydro)", alias="MY_SIMU")

        # No execution time defined
        simu.galactica_validity_check()
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "'My simu (hydro)' simulation Galactica execution time is not defined.")

    def test_simu_hdf5_io(self, tmp_path):
        """
        Tests saving/loading Simulation from HDF5 file

        Parameters
        ----------
        tmp_path: temporary path  PyTest fixture
        """
        ramses = SimulationCode(name="Ramses 3 (MHD)", code_name="Ramses")
        simu_name = "My most interesting simulation"
        cfg_filepath = os.path.join(os.path.dirname(__file__), "io", "datafiles", "test_implode_2D.ini")
        simu = Simulation(simu_code=ramses, name=simu_name, alias="SIMU_1", description="simu description",
                          execution_time="2020-03-01 18:45:30", config_file=AsciiFile.load_file(cfg_filepath))

        # Add algortihms
        ramses.algorithms.add(Algorithm(algo_type=AlgoType.AdaptiveMeshRefinement, description="AMR descr"))
        ramses.algorithms.add(Algorithm(algo_type=AlgoType.Godunov, description="Godunov scheme"))
        ramses.algorithms.add(Algorithm(algo_type=AlgoType.HLLCRiemann, description="HLLC Riemann solver"))
        ramses.algorithms.add(Algorithm(algo_type=AlgoType.PoissonMultigrid, description="Multigrid Poisson solver"))
        ramses.algorithms.add(Algorithm(algo_type=AlgoType.ParticleMesh, description="PM solver"))
        simu.applied_algorithms.add(AppliedAlgorithm(algorithm=ramses.algorithms["Adaptive mesh refinement"],
                                                     details="My implementation"))
        simu.applied_algorithms.add(AppliedAlgorithm(algorithm=ramses.algorithms["Harten-Lax-van Leer-Contact Riemann solver"],
                                                     details="My second implementation"))

        # Add input parameters
        ramses.input_parameters.add(InputParameter(key="levelmin", name="Lmin",
                                                   description="min. level of AMR refinement"))
        ramses.input_parameters.add(InputParameter(key="levelmax", name="Lmax",
                                                   description="max. level of AMR refinement"))
        boxlen_key = "boxlen"
        ramses.input_parameters.add(InputParameter(key=boxlen_key, name="Lbox",
                                                   description="Simulation domain box size"))
        simu.parameter_settings.add(ParameterSetting(input_param=ramses.input_parameters["Lmin"], value=8,
                                                     visibility=ParameterVisibility.BASIC_DISPLAY))
        simu.parameter_settings.add(ParameterSetting(input_param=ramses.input_parameters["Lmax"], value=12,
                                                     visibility=ParameterVisibility.BASIC_DISPLAY))
        simu.parameter_settings.add(ParameterSetting(input_param=ramses.input_parameters["Lbox"], value=500.0,
                                                     unit=U.kpc, visibility=ParameterVisibility.BASIC_DISPLAY))

        # Add physical processes
        ramses.physical_processes.add(PhysicalProcess(physics=Physics.StarFormation, description="descr sf"))
        ramses.physical_processes.add(PhysicalProcess(physics=Physics.Hydrodynamics, description="descr hydro"))
        ramses.physical_processes.add(PhysicalProcess(physics=Physics.SelfGravity, description="descr self G"))
        ramses.physical_processes.add(PhysicalProcess(physics=Physics.SupernovaeFeedback, description="SN feedback"))
        simu.resolved_physics.add(ResolvedPhysicalProcess(physics=ramses.physical_processes["Star formation"],
                                                          details="Star formation specific implementation"))
        simu.resolved_physics.add(ResolvedPhysicalProcess(physics=ramses.physical_processes["Self-gravity"],
                                                          details="self-gravity specific implementation"))

        # Add snapshot
        sn = Snapshot(name="First pericenter", description="Snapshot of the first pericenter",
                      time=(100.25, U.Myr), physical_size=1.0, directory_path="/path/to/my/snapshot")
        simu.snapshots.add(sn)

        # Add generic result
        simu.generic_results.add(GenericResult(name="Simu key result !"))

        # Add post-processing run
        hop = PostProcessingCode(name="Hop", code_name="HOP")
        simu.post_processing_runs.add(PostProcessingRun(name="My post-processing run", ppcode=hop))

        # Dummy project
        proj = Project(category=ProjectCategory.GalacticDynamics, project_title="My project épatant")
        proj.simulations.add(simu)

        # Save study
        fname = str(tmp_path / "study.h5")
        study = SimulationStudy(project=proj)
        study.save_HDF5(fname)

        # Reload study
        study_loaded = SimulationStudy.load_HDF5(fname)
        proj_loaded = study_loaded.project
        simu_loaded = proj_loaded.simulations[simu_name]
        assert simu_loaded == simu

        # Test modifying unit to U.none, saving and reloading it => check that HDF5 file do not contain unit anymore
        loaded_lbox_psetting = simu_loaded.parameter_settings[boxlen_key]
        loaded_lbox_psetting.unit = U.none  # => Setting the unit to U.none here !
        fname2 = str(tmp_path / "study2.h5")
        study_loaded.save_HDF5(fname2)
        study_reloaded = SimulationStudy.load_HDF5(fname2)
        project_reloaded = study_reloaded.project
        simu_reloaded = project_reloaded.simulations[simu_name]
        reloaded_lbox_psetting = simu_reloaded.parameter_settings[boxlen_key]
        assert reloaded_lbox_psetting.unit == U.none


class TestPostProcessingRun(object):
    def test_simu_init(self):
        """
        Tests PostProcessingRun instance initialisation
        """
        # PostProcessingRun initialisation
        hop = PostProcessingCode(name="Hop", code_name="HOP")
        pprun = PostProcessingRun(name="My post-processing run", alias="PPRUN_1", ppcode=hop,
                                  description="This is a pretty long description for my post-processing run",
                                  directory_path="/path/to/my/simulation")

        assert pprun.alias == "PPRUN_1"
        assert pprun.name == "My post-processing run"
        assert pprun.description == "This is a pretty long description for my post-processing run"
        assert pprun.directory_path == "/path/to/my/simulation"
        assert pprun.configuration_file is None

        # Test str() conversion
        assert str(pprun) == "'My post-processing run' post-processing run"

    def test_post_processing_run_ppcode_setting_exc(self):
        """
        Tests setting a post-processing code into a post-processing run object
        """
        # Tests post-processing run defined without code
        with pytest.raises(AttributeError, match="Undefined post-processing code for 'My super post-processing run' "
                                                 "Post-processing run."):
            pprun_exc = PostProcessingRun(name="My super post-processing run")  # No post-processing code defined

        # Tests invalid post-processing run_code initialisation exception
        invalid_ppcode_err = "PostProcessingRun 'postpro_code' attribute is not a valid PostProcessingCode instance."
        with pytest.raises(AttributeError, match=invalid_ppcode_err):
            pprun_exc = PostProcessingRun(name="My post-processing run", ppcode=-5)  # Invalid post-processing run code
            pprun_exc2 = PostProcessingRun(-5, name="My post-processing run")  # Invalid post-processing run code

        # PostProcessingRun initialisation : valid => should not raise any exception
        RADMC = PostProcessingCode(name="RadMC", code_name="RADMC")
        pprun = PostProcessingRun(name="My run", ppcode=RADMC)
        pprun2 = PostProcessingRun(RADMC, name="My run")

    def test_pprun_equality(self):
        """
        Tests rich comparison method PostProcessingRun.__eq____()
        """
        hop = PostProcessingCode(name="Hop", code_name="HOP")
        pprun = PostProcessingRun(hop, name="My run éblouissant")

        # Different post-processing code => not equals
        adaptaHop = PostProcessingCode(name="AdaptaHOP v2.1", code_name="AdaptaHop")
        assert pprun != PostProcessingRun(name=pprun.name, ppcode=adaptaHop, uid=pprun.uid)

        # Identical post-processing runs
        ppr = PostProcessingRun(name=pprun.name, ppcode=pprun.postpro_code, uid=pprun.uid)
        assert pprun == ppr

    def test_pprun_hdf5_io(self, tmp_path):
        """
        Tests saving/loading PostProcessingRun from HDF5 file

        Parameters
        ----------
        tmp_path: temporary path PyTest fixture
        """
        hop = PostProcessingCode(name="Hop", code_name="HOP")
        cfg_filepath = os.path.join(os.path.dirname(__file__), "io", "datafiles", "test_implode_2D.ini")
        pprun = PostProcessingRun(hop, name="My run éblouissant", alias="PPRUN_1", description="run description",
                                  config_file=AsciiFile.load_file(cfg_filepath))

        # Dummy project
        proj = Project(category=ProjectCategory.GalacticDynamics, project_title="My project")
        ramses = SimulationCode(name="Ramses 3 (MHD)", code_name="Ramses")
        simu = Simulation(simu_code=ramses, name="My simu énorme")
        simu.post_processing_runs.add(pprun)
        proj.simulations.add(simu)

        # Save study
        fname = str(tmp_path / "study.h5")
        study = SimulationStudy(project=proj)
        study.save_HDF5(fname)

        # Reload study
        study_loaded = SimulationStudy.load_HDF5(fname)
        simu_loaded = study_loaded.project.simulations["My simu énorme"]
        pprun_loaded = simu_loaded.post_processing_runs["My run éblouissant"]
        assert pprun_loaded == pprun


__all__ = ["TestSimulation", "TestPostProcessingRun"]

