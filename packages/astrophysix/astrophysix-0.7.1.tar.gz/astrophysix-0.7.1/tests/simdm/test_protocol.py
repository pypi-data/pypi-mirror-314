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
from future.builtins import str, dict
import pytest
import logging

from astrophysix.simdm import ProjectCategory, Project, SimulationStudy
from astrophysix.simdm.experiment import Simulation
from astrophysix.simdm.protocol import AlgoType, Algorithm, Physics, PhysicalProcess, InputParameter, SimulationCode,\
    PostProcessingCode
from astrophysix.simdm.protocol.base import Protocol


class TestAlgoType(object):
    def test_from_key_exceptions(self):
        """
        Tests exceptions raised by AlgoType.from_alias(method)
        """
        # Check unknown algorithm type
        with pytest.raises(ValueError) as e:
            at = AlgoType.from_key("MENUISERIE")
        assert str(e.value) == "No AlgoType defined with the key 'MENUISERIE'."

    def test_init(self):
        """
        Tests valid AlgoType initialisation from aliases
        """
        assert AlgoType.from_key("PM") == AlgoType.ParticleMesh
        assert AlgoType.from_key("Poisson_MG") == AlgoType.PoissonMultigrid
        assert AlgoType.from_key("Godunov") == AlgoType.Godunov
        assert AlgoType.from_key("HLLC") == AlgoType.HLLCRiemann
        assert AlgoType.from_key("AMR") == AlgoType.AdaptiveMeshRefinement
        assert AlgoType.from_key("Voronoi_MM") == AlgoType.VoronoiMovingMesh
        assert AlgoType.from_key("FOF") == AlgoType.FriendOfFriend
        assert AlgoType.from_key("Poisson_CG") == AlgoType.PoissonConjugateGradient
        assert AlgoType.from_key("SPH") == AlgoType.SmoothParticleHydrodynamics
        assert AlgoType.from_key("ray_tracer") == AlgoType.RayTracer


class TestPhysics(object):
    def test_from_key_exceptions(self):
        """
        Tests exceptions raised by Physics.from_alias(method)
        """
        # Check unknown physical process
        with pytest.raises(ValueError) as e:
            ph = Physics.from_key("Plomberie")
        assert str(e.value) == "No Physics defined with the key 'Plomberie'."

    def test_init(self):
        """
        Tests valid Physics initialisation from aliases
        """
        assert Physics.from_key("sn_feedback") == Physics.SupernovaeFeedback
        assert Physics.from_key("self_gravity") == Physics.SelfGravity
        assert Physics.from_key("hydro") == Physics.Hydrodynamics
        assert Physics.from_key("mhd") == Physics.MHD
        assert Physics.from_key("mol_cooling") == Physics.MolecularCooling
        assert Physics.from_key("star_form") == Physics.StarFormation
        assert Physics.from_key("AGN_feedback") == Physics.AGNFeedback


class TestAlgorithm(object):
    def test_algo_init(self):
        """
        Tests Algorithm instance initialisation
        """
        # Algorithm initialisation
        amr = Algorithm(algo_type=AlgoType.AdaptiveMeshRefinement, description="Adaptive mesh refinement implementation")

        assert amr.name == AlgoType.AdaptiveMeshRefinement.name
        assert amr.description == "Adaptive mesh refinement implementation"

        # Test str() conversion
        assert str(amr) == "'Adaptive mesh refinement' algorithm"

    def test_setting_algorithm_type_exc(self):
        """
        Tests that an algorithm defined without type raises an exception
        """
        # Tests algorithm defined without type
        with pytest.raises(AttributeError) as e:
            algo_exc = Algorithm()  # No algorithm type defined
        assert str(e.value) == "Algorithm 'algo_type' attribute is not defined (mandatory)."

        # Tests invalid algo type property initialisation exception
        with pytest.raises(AttributeError) as e:
            algo_exc = Algorithm(algo_type="CUISINE")  # Invalid algorithm type
        assert str(e.value) == "No AlgoType defined with the key 'CUISINE'."

        with pytest.raises(AttributeError) as e:
            algo_exc = Algorithm(algo_type=(345, "Elephant"))  # Invalid algorithm type
        assert str(e.value) == "Algorithm 'algo_type' attribute is not a valid AlgoType enum value."

    def test_setting_algorithm_description(self):
        """
        Tests setting algorithm description property
        """
        algo = Algorithm(algo_type=AlgoType.Godunov, description="Descr of algo")

        # ------------------------ Tests invalid algorithm description setting exception ----------------------------- #
        with pytest.raises(AttributeError) as e:
            algo.description = 0
        assert str(e.value) == "Algorithm 'description' property is not a valid string."

        # Valid => should not raise any exception
        algo.description = "Description of the best algorithm in the world"
        # ------------------------------------------------------------------------------------------------------------ #

    def test_algorithm_comparison(self):
        """
        Tests rich comparison method Algorithm.__eq__()
        """
        algo = Algorithm(algo_type=AlgoType.ParticleMesh, description="My algo descr.")

        # Different UUID => not equals
        assert algo != Algorithm(algo_type=algo.algo_type, description=algo.description)

        # Different type => not equals
        assert algo != Algorithm(algo_type=AlgoType.AdaptiveMeshRefinement, uid=algo.uid, description=algo.description)

        # Different description => not equals
        assert algo != Algorithm(algo_type=algo.algo_type, uid=algo.uid, description="Other descr.")

        # Identical algorithms
        assert algo == Algorithm(algo_type=algo.algo_type, uid=algo.uid, description=algo.description)


class TestInputParameter(object):
    def test_inpparam_init(self):
        """
        Tests InputParameter instance initialisation
        """
        # Input parameter initialisation
        lmin = InputParameter(key="levelmin", name="lmin", description="Min. level of AMR refinement")

        assert lmin.key == "levelmin"
        assert lmin.name == "lmin"
        assert lmin.description == "Min. level of AMR refinement"

        # Test str() conversion
        assert str(lmin) == "[levelmin] 'lmin' input parameter"

    def test_setting_inpparam_name_exc(self):
        """
        Tests that an input parameter defined without a name raises an exception
        """
        # Tests input parameter defined without name
        with pytest.raises(AttributeError) as e:
            ip_exc = InputParameter(key="ngridmax")  # No input parameter name defined
        assert str(e.value) == "Input parameter 'name' attribute is not defined (mandatory)."

        # Tests input parameter name property initialisation exception
        invalid_inpparam_name_err = "Input parameter 'name' property is not a valid \\(non empty\\) string."
        with pytest.raises(AttributeError, match=invalid_inpparam_name_err):
            ip_exc = InputParameter(name=-4)  # Invalid input parameter name

        with pytest.raises(AttributeError, match=invalid_inpparam_name_err):
            ip_exc = InputParameter(name="")  # Invalid input parameter name (empty string)

        ip = InputParameter(name="a")
        with pytest.raises(AttributeError, match=invalid_inpparam_name_err):
            ip.name = -1  # Invalid input parameter name

    def test_setting_inpparam_description(self):
        """
        Tests setting input parameter description property
        """
        ip = InputParameter(name="x", description="Descr of input parameter")

        # ------------------------ Tests invalid input parameter description setting exception ----------------------- #
        invalid_inpparam_descr_err = "Input parameter 'description' property is not a valid string."
        with pytest.raises(AttributeError) as e:
            ip.description = 0
        assert str(e.value) == invalid_inpparam_descr_err

        with pytest.raises(AttributeError) as e:
            ip_exc = InputParameter(name="x", description=("Blue", "turtle"))
        assert str(e.value) == invalid_inpparam_descr_err
        # ------------------------------------------------------------------------------------------------------------ #

        # Valid => should not raise any exception
        ip.description = "Description of the best algorithm in the world"

    def test_inputparam_comparison(self):
        """
        Tests rich comparison method InputParameter.__eq__()
        """
        lmin = InputParameter(key="levelmin", name="lmin", description="Min. level of AMR refinement")

        # Different UUID => not equals
        assert lmin != InputParameter(key=lmin.key, name=lmin.name, description=lmin.description)

        # Different key => not equals
        assert lmin != InputParameter(key="other_key", uid=lmin.uid, name=lmin.name, description=lmin.description)

        # Different name => not equals
        assert lmin != InputParameter(key=lmin.key, uid=lmin.uid, name="other_name", description=lmin.description)

        # Different description => not equals
        assert lmin != InputParameter(key=lmin.key, uid=lmin.uid, name=lmin.name, description="Alt. description")

        # Identical input parameter
        assert lmin == InputParameter(key=lmin.key, uid=lmin.uid, name=lmin.name, description=lmin.description)

    def test_inpparam_galactica_validity_checks(self, caplog):
        """
        Tests input parameter Galactica validity checks

        Parameters
        ----------
        caplog: captured log PyTest fixture
        """
        lmin = InputParameter(key="levelmin", name="lmin")

        # No input parameter name defined => Should never happen
        # [...]

        # Input parameter name too long
        lmin.name = "This is a much too long name for a basic input parameter of the RAMSES code"
        lmin.galactica_validity_check()
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "[levelmin] 'This is a much too long name for a basic input parameter of "
                                            "the RAMSES code' input parameter Galactica input parameter name is too "
                                            "long (max. 64 characters).")
        lmin.name = "lmin"  # => Ok

        # input parameter key too long
        lmin.key = "my_too_long_input_param_key"
        lmin.galactica_validity_check()
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "[my_too_long_input_param_key] 'lmin' input parameter Galactica input "
                                            "parameter key is too long (max. 16 characters).")
        lmin.key = "levelmin"  # => Ok


class TestPhysicalProcess(object):
    def test_physics_init(self):
        """
        Tests PhysicalProcess instance initialisation
        """
        # Physical process initialisation
        agn_fb = PhysicalProcess(physics=Physics.AGNFeedback, description="feedback from Active Galactic Nuclei")

        assert agn_fb.name == Physics.AGNFeedback.name
        assert agn_fb.description == "feedback from Active Galactic Nuclei"

        # Test str() conversion
        assert str(agn_fb) == "'AGN feedback' physical process"

    def test_setting_physproc_physics_exc(self):
        """
        Tests that a physical process defined without physics raises an exception
        """
        # Tests physical process defined without physics
        with pytest.raises(AttributeError) as e:
            ph_exc = PhysicalProcess(description="simple descr")  # No physics defined
        assert str(e.value) == "PhysicalProcess 'physics' attribute is not defined (mandatory)."

        # Tests invalid physical process 'physics' property initialisation exception
        with pytest.raises(AttributeError) as e:
            ph_exc = PhysicalProcess(physics="Wind")  # Invalid physics
        assert str(e.value) == "No Physics defined with the key 'Wind'."

        with pytest.raises(AttributeError) as e:
            ph_exc = PhysicalProcess(physics=(47, "Zebras"))  # Invalid physics
        assert str(e.value) == "PhysicalProcess 'physics' attribute is not a valid Physics enum value."

    def test_setting_physproc_description(self):
        """
        Tests setting physical process description property
        """
        ph = PhysicalProcess(physics=Physics.Hydrodynamics, description="Descr of process")

        # --------------------- Tests invalid physical process description setting exception ------------------------- #
        with pytest.raises(AttributeError) as e:
            ph.description = -785.2
        assert str(e.value) == "PhysicalProcess 'description' property is not a valid string."

        # Valid => should not raise any exception
        ph.description = "Description of the collisional physics"
        # ------------------------------------------------------------------------------------------------------------ #

    def test_physical_process_comparison(self):
        """
        Tests rich comparison method PhysicalProcess.__eq__()
        """
        agn_fb = PhysicalProcess(physics=Physics.AGNFeedback, description="feedback from Active Galactic Nuclei")

        # Different UUID => not equals
        assert agn_fb != PhysicalProcess(physics=agn_fb.physics, description=agn_fb.description)

        # Different type => not equals
        assert agn_fb != PhysicalProcess(physics=Physics.StarFormation, uid=agn_fb.uid, description=agn_fb.description)

        # Identical physical process
        assert agn_fb == PhysicalProcess(physics=agn_fb.physics, uid=agn_fb.uid, description=agn_fb.description)


class TestProtocol(object):
    def test_protocol_init(self):
        """
        Tests Protocol instance initialisation
        """
        # Protocol initialisation
        prot = Protocol(name="Ramses 3", code_name="RAMSES", code_version="3.10.0", alias="RAMSES_3",
                        url="http://www.my-code.org", description="Code description")
        assert prot.name == "Ramses 3"
        assert prot.code_name == "RAMSES"
        assert prot.code_version == "3.10.0"
        assert prot.alias == "RAMSES_3"
        assert prot.description == "Code description"
        assert prot.url == "http://www.my-code.org"

        # Test str() conversion
        assert str(prot) == "[Ramses 3]"

    def test_setting_protocol_name_exc(self):
        """
        Tests that a protocol defined without name raises an exception
        """
        # Tests protocol defined without name
        with pytest.raises(AttributeError) as e:
            prot_exc = Protocol(code_name="RAMSES")  # No Protocol code name defined
        assert str(e.value) == "Protocol 'name' attribute is not defined (mandatory)."

        code = Protocol(name="Ramses 3", code_name="RAMSES")

        # ------------- Tests invalid protocol name  setting exception ---------------------- #
        empty_protocol_name_err = "Protocol 'name' property is not a valid (non empty) string."
        with pytest.raises(AttributeError) as e:
            code.name = ("Cat", 20)
        assert str(e.value) == empty_protocol_name_err

        with pytest.raises(AttributeError) as e:
            code.name = ""
        assert str(e.value) == empty_protocol_name_err
        # ----------------------------------------------------------------------------------- #

        # Valid => should not raise any exception
        code.name = "The best exascale code on Earth"

    def test_setting_protocol_codename_exc(self):
        """
        Tests that a protocol defined without code name raises an exception
        """
        # Tests protocol defined without code name
        with pytest.raises(AttributeError) as e:
            proto_exc = Protocol(name="Ramses 3")  # No protocol code name defined
        assert str(e.value) == "Protocol 'code_name' attribute is not defined (mandatory)."

        code = Protocol(name="Ramses 3", code_name="RAMSES")

        # ------------- Tests invalid protocol name  setting exception ---------------------- #
        empty_protocol_codename_err = "Protocol 'code_name' property is not a valid (non empty) string."
        with pytest.raises(AttributeError) as e:
            code.code_name = (2, "Dolphin")
        assert str(e.value) == empty_protocol_codename_err

        with pytest.raises(AttributeError) as e:
            code.code_name = ""
        assert str(e.value) == empty_protocol_codename_err
        # ----------------------------------------------------------------------------------- #

        # Valid => should not raise any exception
        code.code_name = "GADGET"

    def test_setting_protocol_codeversion_exc(self):
        """
        Tests setting a protocol code version
        """
        code = Protocol(name="Ramses 3", code_name="RAMSES")

        # ------------- Tests invalid protocol code version setting exception ---------------------- #
        invalid_protocol_codeversion_err = "Protocol 'code_version' property is not a valid string."
        with pytest.raises(AttributeError) as e:
            code.code_version = -4.5
        assert str(e.value) == invalid_protocol_codeversion_err
        # ------------------------------------------------------------------------------------------ #

        # Valid => should not raise any exception
        code.code_version = "GADGET"

    def test_setting_protocol_url_exc(self):
        """
        Tests setting a protocol url
        """
        code = Protocol(name="Ramses 3", code_name="RAMSES")

        # ------------- Tests invalid protocol url setting exception ---------------------- #
        invalid_protocol_url_err = "Protocol 'url' property is not a valid string."
        with pytest.raises(AttributeError) as e:
            code.url = 45
        assert str(e.value) == invalid_protocol_url_err
        # --------------------------------------------------------------------------------- #

        # Valid => should not raise any exception
        code.url = "1.2.3"

    def test_setting_protocol_alias_exc(self, caplog):
        """
        Tests setting a protocol alias

        Parameters
        ----------
        caplog: captured log PyTest fixture
        """
        code = Protocol(name="Ramses 3", code_name="RAMSES", alias="RAMSES_3")

        # Tests invalid protocol alias setting exception
        with pytest.raises(AttributeError) as e:
            code.alias = -1.245
        assert str(e.value) == "Protocol 'alias' property is not a valid string"

        # Valid => should not raise any exception
        code.alias = "TOP_CODE"

    def test_setting_protocol_description(self):
        """
        Tests setting protocol description property
        """
        code = Protocol(name="Ramses 3", code_name="RAMSES")

        # ------------------------ Tests invalid protocol description setting exception ------------------------------ #
        with pytest.raises(AttributeError) as e:
            code.description = 0
        assert str(e.value) == "Protocol 'description' property is not a valid string."

        # Valid => should not raise any exception
        code.description = "Description of the best code in the world"
        # ------------------------------------------------------------------------------------------------------------ #

    def test_protocol_equality(self):
        """
        Tests rich comparison method Protocol.__eq__()
        """
        protocol = Protocol(name="Ramses 3 (MHD)", code_name="Ramses", code_version="3.10.1", alias="RAMSES_3",
                            url="http://www.my-code.net", description="This is a fair description")

        # Different UUID => not equals
        assert protocol != Protocol(name=protocol.name, code_name=protocol.code_name,
                                    code_version=protocol.code_version, alias=protocol.alias, url=protocol.url,
                                    description=protocol.description)

        # Different name => not equals
        assert protocol != Protocol(name="Ramses 3",  uid=protocol.uid, code_name=protocol.code_name,
                                    code_version=protocol.code_version, alias=protocol.alias, url=protocol.url,
                                    description=protocol.description)

        # Different code name => not equals
        assert protocol != Protocol(name=protocol.name,  uid=protocol.uid, code_name="Gadget",
                                    code_version=protocol.code_version, alias=protocol.alias, url=protocol.url,
                                    description=protocol.description)

        # Different code version => not equals
        assert protocol != Protocol(name=protocol.name,  uid=protocol.uid, code_name=protocol.code_name,
                                    code_version="3.10.2", alias=protocol.alias, url=protocol.url,
                                    description=protocol.description)

        # Different alias => not equals
        assert protocol != Protocol(name=protocol.name,  uid=protocol.uid, code_name=protocol.code_name,
                                    code_version=protocol.code_version, alias="RAMSES_3.10.2", url=protocol.url,
                                    description=protocol.description)

        # Different url => not equals
        assert protocol != Protocol(name=protocol.name,  uid=protocol.uid, code_name=protocol.code_name,
                                    code_version=protocol.code_version, alias=protocol.alias, url="http://irfu.cea.fr",
                                    description=protocol.description)

        # Different descritpion => not equals
        assert protocol != Protocol(name=protocol.name,  uid=protocol.uid, code_name=protocol.code_name,
                                    code_version=protocol.code_version, alias=protocol.alias, url=protocol.url,
                                    description="Best description")

        # Identical protocols
        p = Protocol(name=protocol.name, uid=protocol.uid, code_name=protocol.code_name,
                     code_version=protocol.code_version, alias=protocol.alias, url=protocol.url,
                     description=protocol.description)
        assert protocol == p

        # Add algorithms
        a1 = protocol.algorithms.add(Algorithm(algo_type=AlgoType.AdaptiveMeshRefinement, description="AMR descr"))
        a2 = protocol.algorithms.add(Algorithm(algo_type=AlgoType.Godunov, description="Godunov scheme"))
        a3 = protocol.algorithms.add(Algorithm(algo_type=AlgoType.HLLCRiemann, description="HLLC Riemann solver"))
        a4 = protocol.algorithms.add(Algorithm(algo_type=AlgoType.PoissonMultigrid,
                                               description="Multigrid Poisson solver"))
        a5 = protocol.algorithms.add(Algorithm(algo_type=AlgoType.ParticleMesh, description="PM solver"))

        # Protocol algo list differ => not equals
        p.algorithms.add(a1)
        p.algorithms.add(a2)
        p.algorithms.add(a3)
        p.algorithms.add(a4)
        assert p != protocol
        # Same algorithms => identical protocols
        p.algorithms.add(a5)
        assert p == protocol

        # Add input parameters
        ip1 = protocol.input_parameters.add(InputParameter(key="levelmin", name="levelmin",
                                                           description="min. level of AMR refinement"))
        ip2 = protocol.input_parameters.add(InputParameter(key="levelmax", name="levelmax",
                                                           description="max. level of AMR refinement"))

        # Protocol input parameter list differ => not equals
        p.input_parameters.add(ip1)
        assert p != protocol

        # Same input parameters => identical protocols
        p.input_parameters.add(ip2)
        assert p == protocol

    def test_protocol_galactica_validity_checks(self, caplog):
        """
        Tests protocol Galactica validity checks

        Parameters
        ----------
        caplog: captured log PyTest fixture
        """
        protocol = Protocol(name="Ramses 3 (MHD)", code_name="RAMSES", code_version="3.10.1")

        # No alias defined
        protocol.galactica_validity_check()
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "[Ramses 3 (MHD)] Galactica protocol alias is missing.")

        # Alias too long
        protocol.alias = "MY_ALIAS_123456789_10"
        protocol.galactica_validity_check()
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "[Ramses 3 (MHD)] Galactica protocol alias is too long (max. 16 "
                                            "characters).")
        protocol.alias = "MY_ALIAS"  # => Ok

        # Invalid Galactica alias
        protocol.alias = "invalid_ALIAS"  # non capital letters !
        protocol.galactica_validity_check()
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "[Ramses 3 (MHD)] Galactica protocol alias is not valid (The alias can "
                                            "contain capital letters, digits and '_' only. It must start with a capital"
                                            " letter and cannot end with a '_'.)")
        protocol.alias = "MY_ALIAS"  # => Ok

        # No protocol name defined => Should never happen
        # [...]

        # Protocol name too long
        protocol.name = "This  is a pretty long name for a prototol that has absolutely no sense. It means that " \
                        "this protocol can be as long as 400 hundred chars and still be valid ? Come on..."
        protocol.galactica_validity_check()
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "[This  is a pretty long name for a prototol that has absolutely no sense. "
                                            "It means that this protocol can be as long as 400 hundred chars and still "
                                            "be valid ? Come on...] Galactica protocol name is too long (max. 128 "
                                            "characters).")
        protocol.name = "Ramses 3 (MHD)"  # => Ok

        # No protocol code name defined => Should never happen
        # [...]

        # Protocol code name too long
        protocol.code_name = "CODE Ultimate with a much too long name"
        protocol.galactica_validity_check()
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "[Ramses 3 (MHD)] Galactica protocol code name is too long (max. 32 "
                                            "characters).")
        protocol.code_name = "RAMSES"  # => Ok

        # No code version defined
        protocol.code_version = ""
        protocol.galactica_validity_check()
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "[Ramses 3 (MHD)] Galactica protocol code version is missing.")

        # Code version too long
        protocol.code_version = "145.1254.3rc20"
        protocol.galactica_validity_check()
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "[Ramses 3 (MHD)] Galactica protocol code version is too long (max. 8 "
                                            "characters).")
        protocol.code_version = "3.10.1"  # => Ok


class TestPostProcessingCode(object):
    def test_postprocessor_init(self):
        """
        Tests PostProcessingCode instance initialisation
        """
        ramses = PostProcessingCode(name="Ramses 3", code_name="RAMSES")

        # Test str() conversion
        assert str(ramses) == "[Ramses 3] post-processing code"


class TestSimulationCode(object):
    def test_simu_code_init(self):
        """
        Tests SimulationCode instance initialisation
        """
        ramses = SimulationCode(name="Ramses 3", code_name="RAMSES")

        # Test str() conversion
        assert str(ramses) == "[Ramses 3] simulation code"

    def test_simucode_equality(self):
        """
        Tests rich comparison method SimulationCode.__eq__()
        """
        ramses = SimulationCode(name="Ramses 3 (MHD)", code_name="Ramses", code_version="3.10.1", alias="RAMSES_3",
                                url="http://www.my-code.net", description="This is a fair description")

        r2 = SimulationCode(name=ramses.name, code_version=ramses.code_version, uid=ramses.uid,
                            code_name=ramses.code_name, alias=ramses.alias, url=ramses.url,
                            description=ramses.description)

        assert r2 == ramses

        # Add physical processes
        pp1 = ramses.physical_processes.add(PhysicalProcess(physics=Physics.StarFormation, description="descr sf"))
        pp2 = ramses.physical_processes.add(PhysicalProcess(physics=Physics.Hydrodynamics, description="descr hydro"))
        pp3 = ramses.physical_processes.add(PhysicalProcess(physics=Physics.SelfGravity, description="descr self G"))
        pp4 = ramses.physical_processes.add(PhysicalProcess(physics=Physics.SupernovaeFeedback, description="SN feedback"))

        # Protocol physical process list differ => not equals
        r2.physical_processes.add(pp1)
        r2.physical_processes.add(pp2)
        r2.physical_processes.add(pp3)
        assert r2 != ramses

        # Same physical processes => identical simulation codes
        r2.physical_processes.add(pp4)
        assert r2 == ramses

    def test_simucode_hdf5_io(self, tmp_path):
        """
        Tests saving/loading Protocol from HDF5 dict

        Parameters
        ----------
        tmp_path: temporary path  PyTest fixture
        """
        ramses = SimulationCode(name="Ramses 3 (MHD)", code_name="Ramses", code_version="3.10.1", alias="RAMSES_3",
                                url="http://www.my-code.net", description="This is a fair description")

        ramses.algorithms.add(Algorithm(algo_type=AlgoType.AdaptiveMeshRefinement, description="AMR descr"))
        ramses.algorithms.add(Algorithm(algo_type=AlgoType.Godunov, description="Godunov scheme"))
        ramses.algorithms.add(Algorithm(algo_type=AlgoType.HLLCRiemann, description="HLLC Riemann solver"))
        ramses.algorithms.add(Algorithm(algo_type=AlgoType.PoissonMultigrid, description="Multigrid Poisson solver"))
        ramses.algorithms.add(Algorithm(algo_type=AlgoType.ParticleMesh, description="PM solver"))

        # Add input parameters
        ramses.input_parameters.add(InputParameter(key="levelmin", name="levelmin",
                                                   description="min. level of AMR refinement"))
        ramses.input_parameters.add(InputParameter(key="levelmax", name="levelmax",
                                                   description="max. level of AMR refinement"))

        # Add physical processes
        ramses.physical_processes.add(PhysicalProcess(physics=Physics.StarFormation, description="descr sf"))
        ramses.physical_processes.add(PhysicalProcess(physics=Physics.Hydrodynamics, description="descr hydro"))
        ramses.physical_processes.add(PhysicalProcess(physics=Physics.SelfGravity, description="descr self G"))
        ramses.physical_processes.add(PhysicalProcess(physics=Physics.SupernovaeFeedback, description="SN feedback"))

        # Dummy project
        proj = Project(category=ProjectCategory.GalacticDynamics, project_title="My project")
        proj.simulations.add(Simulation(ramses, name="My simu énorme"))

        # Save study
        fname = str(tmp_path / "study.h5")
        study = SimulationStudy(project=proj)
        study.save_HDF5(fname)

        # Reload study
        study_loaded = SimulationStudy.load_HDF5(fname)
        proj_loaded = study_loaded.project
        simu_loaded = proj_loaded.simulations["My simu énorme"]
        ramses_loaded = simu_loaded.simulation_code
        assert ramses_loaded == ramses


__all__ = ["TestAlgoType", "TestPhysics", "TestAlgorithm", "TestInputParameter", "TestSimulationCode"]


