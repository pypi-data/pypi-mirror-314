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
from future.builtins import str, int
import pytest
import logging
from astrophysix import units as U
from astrophysix.simdm import Project, ProjectCategory, SimulationStudy
from astrophysix.simdm.catalogs import Catalog, TargetObject
from astrophysix.simdm.experiment import Simulation
from astrophysix.simdm.protocol import SimulationCode
from astrophysix.simdm.results import GenericResult, Snapshot
from astrophysix.simdm.datafiles import Datafile
from astrophysix.simdm.services import DataProcessingService


class TestGenericResult(object):
    def test_generic_result_init(self):
        """
        Tests generic result instance initialisation
        """
        # Generic result initialisation
        res = GenericResult(name="Light-mass correlation", description="This is the paper major key result",
                            directory_path="/path/to/my/result")

        assert res.description == "This is the paper major key result"
        assert res.name == "Light-mass correlation"
        assert res.directory_path == "/path/to/my/result"

        # Test str() conversion
        assert str(res) == "'Light-mass correlation' generic result"

    def test_setting_generic_result_name_exc(self):
        """
        Tests that a generic result defined without name raises an exception
        """
        # Tests generic result defined without name
        with pytest.raises(AttributeError) as e:
            res_exc = GenericResult()  # No generic result name defined
        assert str(e.value) == "GenericResult 'name' attribute is not defined (mandatory)."

        res = GenericResult(name="My key result")

        # ------------- Tests invalid generic result name setting exception ---------------------- #
        empty_name_err = "GenericResult 'name' property is not a valid (non-empty) string."
        with pytest.raises(AttributeError) as e:
            res.name = -1
        assert str(e.value) == empty_name_err

        with pytest.raises(AttributeError) as e:
            res.name = ""
        assert str(e.value) == empty_name_err
        # ---------------------------------------------------------------------------------------- #

        # Valid => should not raise any exception
        res.name = "My best result"

    def test_setting_generic_result_description(self):
        """
        Tests setting generic result description property
        """
        res = GenericResult(name="My super result")

        # -------------------------- Tests invalid generic result description setting exception ---------------------- #
        with pytest.raises(AttributeError) as e:
            res.description = 0
        assert str(e.value) == "GenericResult 'description' property is not a valid string."

        # Valid => should not raise any exception
        res.description = "My result description"
        # ------------------------------------------------------------------------------------------------------------ #

    def test_setting_generic_result_dirpath(self):
        """
        Tests setting generic result directory path property
        """
        res = GenericResult(name="My awesome key result")

        # --------------------- Tests invalid generic result directory path setting exception ------------------------ #
        with pytest.raises(AttributeError) as e:
            res.directory_path = (-1, ["Banana", "Apple"])
        assert str(e.value) == "GenericResult 'directory_path' property is not a valid string."

        # Valid => should not raise any exception
        res.directory_path = "/better/path/to/my/result"
        # ------------------------------------------------------------------------------------------------------------ #

    def test_generic_result_equality(self):
        """
        Tests generic result rich comparison method GenericResult.__eq__()
        """
        res = GenericResult(name="Light-mass correlation", description="This is the paper major key result",
                            directory_path="/path/to/my/result")

        # Different UUID => not equals
        assert res != GenericResult(name=res.name, description=res.description, directory_path=res.directory_path)

        # Different name => not equals
        assert res != GenericResult(name="Name", description=res.description, directory_path=res.directory_path,
                                    uid=res.uid)

        # Different description => not equals
        assert res != GenericResult(name=res.name, description="Alt. description", directory_path=res.directory_path,
                                    uid=res.uid)

        # Different directory path => not equals
        assert res != GenericResult(name=res.name, description=res.description, directory_path="/alt/path/to/result",
                                    uid=res.uid)

        # Identical generic results
        r = GenericResult(name=res.name, description=res.description, directory_path=res.directory_path, uid=res.uid)
        assert res == r

        # Add datafiles
        df1 = res.datafiles.add(Datafile(name="My important datafile"))
        df2 = res.datafiles.add(Datafile(name="My important datafile (2)"))
        # Datafile list differ => not equals
        r.datafiles.add(df1)
        assert r != res
        # Identical generic results
        r.datafiles.add(df2)
        assert r == res

        # Add products in generic result
        tobj = TargetObject(name="Star")
        cat = res.catalogs.add(Catalog(tobj, name="My catalog"))
        # Catalog list differ => not equals
        assert r != res
        # Identical generic results
        r.catalogs.add(cat)
        assert r == res

    def test_generic_result_galactica_validity_checks(self, caplog):
        """
        Tests generic result Galactica validity checks

        Parameters
        ----------
        caplog: captured log PyTest fixture
        """
        res = GenericResult(name="Light-mass correlation")

        # Result name too long
        res.name = "This is a way too long result name for a 'Light-mass correlation' basic result."
        res.galactica_validity_check()
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "'This is a way too long result name for a 'Light-mass correlation' basic "
                                            "result.' generic result name is too long for Galactica (max. 64 "
                                            "characters).")

    def test_generic_result_hdf5_io(self, tmp_path):
        """
        Tests saving/loading GenericResult from HDF5 file

        Parameters
        ----------
        tmp_path: temporary path  PyTest fixture
        """
        res1 = GenericResult(name="Key result 1 !", description="My description", directory_path="/my/path/to/result")
        res2 = GenericResult(name="Key result 2 !", description="My description", directory_path="/path/to/result")
        tobj = TargetObject(name="My galaxy")
        res1.catalogs.add(Catalog(tobj, name="My catalog"))
        res2.catalogs.add(Catalog(tobj, name="My catalog #2"))
        res1.datafiles.add(Datafile(name="My datafile"))
        res2.datafiles.add(Datafile(name="My datafile (2)"))

        ramses = SimulationCode(name="Ramses 3 (MHD)", code_name="Ramses")
        simu = Simulation(simu_code=ramses, name="My simu énorme")
        simu.generic_results.add(res1)
        simu.generic_results.add(res2)

        # Dummy project
        proj = Project(category=ProjectCategory.GalacticDynamics, project_title="My project")
        proj.simulations.add(simu)

        # Save study
        fname = str(tmp_path / "study.h5")
        study = SimulationStudy(project=proj)
        study.save_HDF5(fname)

        # Reload study
        study_loaded = SimulationStudy.load_HDF5(fname)
        simu_loaded = study_loaded.project.simulations[simu.name]

        # Compare snapshots
        res1_loaded = simu_loaded.generic_results[res1.name]
        res2_loaded = simu_loaded.generic_results[res2.name]
        assert res1_loaded == res1
        assert res2_loaded == res2


class TestSnapshot(object):
    def test_snapshot_init(self):
        """
        Tests Snapshot instance initialisation
        """
        # Snapshot initialisation
        sn = Snapshot(name="First pericenter", time=(105.6, "Myr"), physical_size=(1.0e3, "pc"),
                      description="This is the snapshot of first pericenter", data_reference="OUTPUT_00245")

        assert sn.description == "This is the snapshot of first pericenter"
        assert sn.time[0] == 105.6
        assert sn.time[1] == U.Myr
        assert sn.physical_size[0] == 1000.0
        assert sn.physical_size[1] == U.pc
        assert sn.data_reference == "OUTPUT_00245"

        # Test str() conversion
        assert str(sn) == "'First pericenter' snapshot"

    def test_setting_snapshot_time_value_and_unit(self):
        """
        Tests setting snapshot time property
        """
        sn = Snapshot(name="My super snapshot")

        # ---------------------------- Tests invalid snapshot time setting exception --------------------------------- #
        # Length 3 tuple
        with pytest.raises(AttributeError) as e:
            sn.time = ("Apple", "Elephant", -3.14159)
        assert str(e.value) == "Snapshot 'time' property cannot be of length != 2"

        # Time unit => dict
        with pytest.raises(AttributeError) as e:
            sn.time = (102.6, {"my_unit": -4.3})
        assert str(e.value) == "Snapshot 'time' property must be defined with a valid (non-empty) time unit string."

        # "Empty time unit string
        with pytest.raises(AttributeError) as e:
            sn.time = (1.24, "")
        assert str(e.value) == "Snapshot 'time' property must be defined with a valid (non-empty) time unit string."

        # Unknwon time unit 'carots'
        with pytest.raises(AttributeError) as e:
            sn.time = (52.9, "carots")
        assert str(e.value) == "Snapshot 'time' property error : Unknown unit name 'carots'."

        # Time unit with physical type => mass instead of time
        with pytest.raises(AttributeError) as e:
            sn.time = (568.7, U.Msun)
        assert str(e.value) == "Error while setting Snapshot 'time' property : unit is not a valid time unit " \
                               "(physical type: 'mass')"

        # Invalid time value
        with pytest.raises(AttributeError) as e:
            sn.time = ("3.45.5", "Myr")
        assert str(e.value) == "Snapshot 'time' property must be set as a (time_float_value, time_unit) tuple."
        with pytest.raises(AttributeError) as e:
            sn.time = ([42359, "Goats"], "Myr")
        assert str(e.value) == "Snapshot 'time' property must be set as a (time_float_value, time_unit) tuple."

        # Valid => should not raise any exception
        sn.time = "0.256"
        sn.time = ("0.24", U.year)
        sn.time = ("0.45", "Myr")
        assert sn.time[1] == U.Myr
        sn.time = 4.46
        sn.time = (7.89e2, "Gyr")
        assert sn.time[1] == U.Gyr
        sn.time = (78.54, U.min)
        # ------------------------------------------------------------------------------------------------------------ #

    def test_setting_snapshot_physsize_value_and_unit(self):
        """
        Tests setting snapshot physical size property
        """
        sn = Snapshot(name="My super snapshot")

        # ---------------------------- Tests invalid snapshot time setting exception --------------------------------- #
        # Length 3 tuple
        with pytest.raises(AttributeError) as e:
            sn.physical_size = ("Apple", "Elephant", -3.14159)
        assert str(e.value) == "Snapshot 'physical_size' property cannot be of length != 2"

        # Time unit => dict
        with pytest.raises(AttributeError) as e:
            sn.physical_size = (102.6, {"my_unit": -4.3})
        assert str(e.value) == "Snapshot 'physical_size' property must be defined with a valid (non-empty) length " \
                               "unit string."

        # "Empty time unit string
        with pytest.raises(AttributeError) as e:
            sn.physical_size = (1.24, "")
        assert str(e.value) == "Snapshot 'physical_size' property must be defined with a valid (non-empty) length " \
                               "unit string."

        # Unknwon time unit 'carots'
        with pytest.raises(AttributeError) as e:
            sn.physical_size = (52.9, "carots")
        assert str(e.value) == "Snapshot 'physical_size' property error : Unknown unit name 'carots'."

        # Length unit with physical type => energy instead of length
        with pytest.raises(AttributeError) as e:
            sn.physical_size = (568.7, U.J)
        assert str(e.value) == "Error while setting Snaphsot 'physical_size' property : unit is not a valid length " \
                               "unit (physical type: 'energy')"

        # Invalid physical size value
        with pytest.raises(AttributeError) as e:
            sn.physical_size = ("3.45.5", "kpc")
        assert str(e.value) == "Snapshot 'physical_size' property must be set as a (size_float_value, length_unit) " \
                               "tuple."
        with pytest.raises(AttributeError) as e:
            sn.physical_size = ([42359, "Goats"], "ly")
        assert str(e.value) == "Snapshot 'physical_size' property must be set as a (size_float_value, length_unit) " \
                               "tuple."

        # Valid => should not raise any exception
        sn.physical_size = "0.256"
        sn.physical_size = ("0.24", U.pc)
        sn.physical_size = ("0.45", "kpc")
        assert sn.physical_size[1] == U.kpc
        sn.physical_size = 4.46
        sn.physical_size = (7.89e2, "Mpc")
        assert sn.physical_size[1] == U.Mpc
        sn.physical_size = (78.54, U.ly)
        # ------------------------------------------------------------------------------------------------------------ #

    def test_setting_snapshot_data_reference_exc(self):
        """
        Tests setting snapshot data_reference property
        """
        sn = Snapshot(name="My super snapshot")

        # ----------------------------- Tests invalid snapshot data_reference setting exception ---------------------- #
        with pytest.raises(AttributeError) as e:
            sn.data_reference = {'abcd': (0.1, None)}
        assert str(e.value) == "Snapshot 'data_reference' property is not a valid string."

        # Valid => should not raise any exception
        sn.data_reference = "OUTPUT_00034"

    def test_snapshot_equality(self):
        """
        Tests snapshot rich comparison method Snapshot.__eq__()
        """
        sn = Snapshot(name="My best snapshot ! Délire !", time=(542.1, U.Myr), physical_size=(250.0, U.kpc),
                      data_reference="output_00034")

        # Different UUID => not equals
        assert sn != Snapshot(name=sn.name, time=sn.time, physical_size=sn.physical_size,
                              data_reference=sn.data_reference)

        # Different time => not equals
        assert sn != Snapshot(name=sn.name, time=(542.1, U.kyr), physical_size=sn.physical_size, uid=sn.uid,
                              data_reference=sn.data_reference)

        # Different physical size => not equals
        assert sn != Snapshot(name=sn.name, time=sn.time, physical_size=(0.251, U.Mpc), uid=sn.uid,
                              data_reference=sn.data_reference)

        # Different data reference => not equals
        assert sn != Snapshot(name=sn.name, time=sn.time, physical_size=sn.physical_size, uid=sn.uid,
                              data_reference="other_output")

        # Identical snapshots
        s = Snapshot(name=sn.name, time=sn.time, physical_size=sn.physical_size, uid=sn.uid,
                     data_reference=sn.data_reference)
        assert s == sn

        # Compare bound data processing services
        dps = sn.processing_services.add(DataProcessingService(service_name="my_service", data_host="my_host"))
        assert s != sn
        s.processing_services.add(dps)
        assert s == sn

    def test_snapshot_galactica_validity_checks(self, caplog):
        """
        Tests snapshot Galactica validity checks

        Parameters
        ----------
        caplog: captured log PyTest fixture
        """
        sn = Snapshot(name="Simple snapshot", time=(542.1, U.Myr), physical_size=(250.0, U.kpc),
                      data_reference="output_00038")

        # Check invalid time value
        sn.time = (1.2E6, U.year)
        sn.galactica_validity_check()
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "'Simple snapshot' snapshot time value must be defined in the range "
                                            "[-10000.0, 10000.0].")
        sn.time = (542.1, U.Myr)  # => Ok

        # Check invalid physical size value
        sn.physical_size = (2.5E8, U.au)
        sn.galactica_validity_check()
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "'Simple snapshot' snapshot physical size value must be defined in the "
                                            "range [0.0, 10000.0].")
        sn.physical_size = (250.0, U.kpc)  # => Ok

        # Check data reference
        sn.data_reference = "data_reference whi is way too long for this simple snapshot at t=542.1 Myr"
        sn.galactica_validity_check()
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "'Simple snapshot' snapshot data reference is too long (max. 64 "
                                            "characters).")
        sn.data_reference = "output_00038"  # => Ok

        # Check data reference is not empty if snapshot is bound to a data processing service
        sn.data_reference = ""
        sn.processing_services.add(DataProcessingService(service_name="ray_traced_map", data_host="anais"))
        sn.galactica_validity_check()
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "'Simple snapshot' snapshot data reference is not defined while data "
                                            "processing services are bound to it.")

    def test_snapshot_hdf5_io(self, tmp_path):
        """
        Tests saving/loading Snapshot from HDF5 file

        Parameters
        ----------
        tmp_path: temporary path  PyTest fixture
        """
        sn = Snapshot(name="My best snapshot ! Délire !", description="My description", time=542.1,
                      physical_size=(250.0, U.kpc), directory_path="/path/to/snapshot1", data_reference="OUTPUT_00001")
        sn2 = Snapshot(name="My best snapshot ! Délire ! (2)", description="My description", time=(542.1, U.Myr),
                       physical_size=255.48, directory_path="/path/to/snapshot2", data_reference="OUTPUT_00002")
        sn.datafiles.add(Datafile(name="Datafile 1"))
        sn2.datafiles.add(Datafile(name="Datafile 2"))

        # Add data processing services
        sn.processing_services.add((DataProcessingService(service_name="slice_map", data_host="my_cluster")))
        sn.processing_services.add((DataProcessingService(service_name="ppv_cube", data_host="my_GPU_cluster")))

        ramses = SimulationCode(name="Ramses 3 (MHD)", code_name="Ramses")
        simu = Simulation(simu_code=ramses, name="My simu énorme")
        simu.snapshots.add(sn)
        simu.snapshots.add(sn2)

        # Dummy project
        proj = Project(category=ProjectCategory.GalacticDynamics, project_title="My project")
        proj.simulations.add(simu)

        # Save study
        fname = str(tmp_path / "study.h5")
        study = SimulationStudy(project=proj)
        study.save_HDF5(fname)

        # Reload study
        study_loaded = SimulationStudy.load_HDF5(fname)
        simu_loaded = study_loaded.project.simulations[simu.name]

        # Compare snapshots
        sn_loaded = simu_loaded.snapshots[sn.name]
        sn_loaded2 = simu_loaded.snapshots[sn2.name]
        assert sn_loaded == sn
        assert sn_loaded2 == sn2


class TestDataProcessingService(object):
    def test_proc_service_init(self):
        """
        Tests DataProcessingService instance initialisation
        """
        # Data processing service initialisation
        service = DataProcessingService(service_name="ray_traced_map", data_host="lab_cluster")

        assert service.service_name == "ray_traced_map"
        assert service.data_host == "lab_cluster"
        assert service.hosted_service == "ray_traced_map @ lab_cluster"

        # Test str() conversion
        assert str(service) == "'ray_traced_map' data processing service (host: lab_cluster)"

    def test_setting_process_service_name_exc(self):
        """
        Tests that a data processing service defined without a name raises an exception
        """
        # Data processing service defined without service name
        with pytest.raises(AttributeError) as e:
            dps_exc = DataProcessingService(data_host="lab_GPUCLUST")  # No service name defined
        assert str(e.value) == "Data processing service 'service_name' attribute is not defined (mandatory)."

        # Tests data processing service name property initialisation exception
        invalid_dataprocserv_name_err = "Data processing service 'service_name' property is not a valid " \
                                        "\\(non empty\\) string."
        with pytest.raises(AttributeError, match=invalid_dataprocserv_name_err):
            dps_exc = DataProcessingService(service_name=-2.4, data_host="lab_GPUCLUST")  # Invalid data processing service name

        with pytest.raises(AttributeError, match=invalid_dataprocserv_name_err):
            dps_exc = DataProcessingService(service_name="", data_host="lab_GPUCLUST")  # Invalid data processing service name (empty string)

        dps = DataProcessingService(service_name="my_custom_Service", data_host="lab_GPUCLUST")
        with pytest.raises(AttributeError, match=invalid_dataprocserv_name_err):
            dps.service_name = -1  # Invalid data processing service name

    def test_setting_process_service_data_host(self):
        """
        Tests setting data processing service host server name property
        """
        # Data processing service defined without data host name
        with pytest.raises(AttributeError) as e:
            dps_exc = DataProcessingService(service_name="my_custom_service")  # No data host name defined
        assert str(e.value) == "Data processing service 'data_host' attribute is not defined (mandatory)."

        # Tests data processing service data host server property initialisation exception
        invalid_dataprocserv_ndata_host_err = "Data processing service 'data_host' property is not a valid " \
                                              "\\(non empty\\) string."
        with pytest.raises(AttributeError, match=invalid_dataprocserv_ndata_host_err):
            dps_exc = DataProcessingService(service_name="my_custom_service", data_host=-2.4)  # Invalid data processing service name

        with pytest.raises(AttributeError, match=invalid_dataprocserv_ndata_host_err):
            dps_exc = DataProcessingService(service_name="my_custom_service", data_host="")  # Invalid data processing service data host name (empty string)

        dps = DataProcessingService(service_name="my_custom_service", data_host="lab_gpu_cluster")
        with pytest.raises(AttributeError, match=invalid_dataprocserv_ndata_host_err):
            dps.data_host = {"a": 245.1}  # Invalid data processing service data host name

    def test_process_service_comparison(self):
        """
        Tests rich comparison method DataProcessingService.__eq__()
        """
        dps = DataProcessingService(service_name="my_service", data_host="my_workstation")

        # Different UUID => not equals
        assert dps != DataProcessingService(service_name=dps.service_name, data_host=dps.data_host)

        # Different service name => not equals
        assert dps != DataProcessingService(service_name="other_service", uid=dps.uid, data_host=dps.data_host)

        # Different data host => not equals
        assert dps != DataProcessingService(service_name=dps.service_name, uid=dps.uid, data_host="other_host")

        # Identical data processing service
        assert dps == DataProcessingService(service_name=dps.service_name, uid=dps.uid, data_host=dps.data_host)

    def test_data_proc_service_hdf5_io(self, tmp_path):
        """
        Tests saving/loading DataProcessingService from HDF5 file

        Parameters
        ----------
        tmp_path: temporary path  PyTest fixture
        """
        sn = Snapshot(name="My best snapshot ! Délire !")
        # Add data processing services
        dps1 = sn.processing_services.add((DataProcessingService(service_name="slice_map", data_host="my_cluster")))
        dps2 = sn.processing_services.add((DataProcessingService(service_name="ppv_cube", data_host="my_GPU_cluster")))

        ramses = SimulationCode(name="Ramses 3 (MHD)", code_name="Ramses")
        simu = Simulation(simu_code=ramses, name="My simu énorme")
        simu.snapshots.add(sn)

        # Dummy project
        proj = Project(category=ProjectCategory.GalacticDynamics, project_title="My project")
        proj.simulations.add(simu)

        # Save study
        fname = str(tmp_path / "study.h5")
        study = SimulationStudy(project=proj)
        study.save_HDF5(fname)

        # Reload study
        study_loaded = SimulationStudy.load_HDF5(fname)
        simu_loaded = study_loaded.project.simulations[simu.name]
        sn_loaded = simu_loaded.snapshots[sn.name]

        # Compare services
        dps1_loaded = sn_loaded.processing_services[dps1.hosted_service]
        dps2_loaded = sn_loaded.processing_services[dps2.hosted_service]
        assert dps1 == dps1_loaded
        assert dps2 == dps2_loaded

    def test_data_proc_service_galactica_validity_checks(self, caplog):
        """
        Tests data processing service Galactica validity checks

        Parameters
        ----------
        caplog: captured log PyTest fixture
        """
        sn = Snapshot(name="My best snapshot.")

        # Add data processing services
        dps1 = sn.processing_services.add((DataProcessingService(service_name="My_super_service_that_is_way_too_long",
                                                                 data_host="my_cluster")))
        sn.galactica_validity_check()
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "Data processing service name 'My_super_service_that_is_way_too_long' is "
                                            "too long for Galactica (max. 32 characters).")

        dps1.service_name = "slice_map"
        dps1.data_host = "My_long_host_name"
        sn.galactica_validity_check()
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "Data processing service host name 'My_long_host_name' is too long for "
                                            "Galactica (max. 16 characters).")


__all__ = ["TestSnapshot", "TestGenericResult", "TestDataProcessingService"]
