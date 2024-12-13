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

import logging

from future.builtins import str, int
import pytest

from astrophysix import units as U
from astrophysix.simdm import Project, ProjectCategory, SimulationStudy
from astrophysix.simdm.experiment import Simulation
from astrophysix.simdm.protocol import SimulationCode
from astrophysix.simdm.results import GenericResult
from astrophysix.simdm.catalogs import TargetObject, ObjectProperty, ObjectPropertyGroup, Catalog, PropertySortFlag, \
    PropertyFilterFlag
from astrophysix.simdm.utils import DataType


class TestObjectProperty(object):
    def test_target_object_property_init(self):
        """
        Tests target object property instance initialisation
        """
        # Object property initialisation
        x = ObjectProperty(property_name="pos_x", description="My property descr.", unit=U.Mpc, dtype=DataType.INTEGER,
                           filter_flag=PropertyFilterFlag.BASIC_FILTER, sort_flag=PropertySortFlag.ADVANCED_SORT)

        assert x.property_name == "pos_x"
        assert x.description == "My property descr."
        assert x.unit == U.Mpc
        assert x.filter_flag == PropertyFilterFlag.BASIC_FILTER
        assert x.sort_flag == PropertySortFlag.ADVANCED_SORT
        assert x.datatype == DataType.INTEGER

        # Test str() conversion
        assert str(x) == "'pos_x' target object property"

    def test_setting_object_property_name_exc(self):
        """
        Tests that a target object  property defined without name raises an exception
        """
        # Tests target object property defined without name
        with pytest.raises(AttributeError, match="ObjectProperty 'property_name' attribute is not defined \\(mandatory\\)."):
            objprop_exc = ObjectProperty()  # No object property name defined

        x = ObjectProperty(property_name="pos_x")

        # -------------- Tests invalid object property name setting exception -------------------- #
        empty_name_err = "ObjectProperty 'property_name' property is not a valid \\(non-empty\\) string."
        with pytest.raises(AttributeError, match=empty_name_err):
            x.property_name = -1

        with pytest.raises(AttributeError, match=empty_name_err):
            x.property_name = ""
        # ---------------------------------------------------------------------------------------- #

        # Valid => should not raise any exception
        x.property_name = "Disk-like galaxy"

    def test_setting_object_property_description(self):
        """
        Tests setting object property description property
        """
        vx = ObjectProperty(property_name="v_x")

        # ---------------------- Tests invalid object property description setting exception ------------------------- #
        with pytest.raises(AttributeError, match="ObjectProperty 'description' property is not a valid string."):
            vx.description = {'a': [0, 1, 3]}

        # Valid => should not raise any exception
        vx.description = "My target object velocity property"
        # ------------------------------------------------------------------------------------------------------------ #

    def test_setting_object_property_sort_filter_flags(self):
        """
        Tests setting object property filter/sort flag property
        """
        vx = ObjectProperty(property_name="v_x")

        # ----------------------- Tests invalid object property filter flag setting exception ------------------------ #
        with pytest.raises(AttributeError, match="Object property 'filter_flag' property error : No PropertyFilterFlag "
                                                 "defined with the flag 'UNKNOWN_FLAG'."):
            vx.filter_flag = "UNKNOWN_FLAG"

        with pytest.raises(AttributeError, match="Object property 'filter_flag' attribute is not a valid "
                                                 "PropertyFilterFlag enum value."):
            vx.filter_flag = {"a": 0.45}
        # ------------------------------------------------------------------------------------------------------------ #

        # ------------------------- Tests invalid object property sort flag setting exception ------------------------ #
        with pytest.raises(AttributeError, match="Object property 'sort_flag' property error : No PropertySortFlag "
                                                 "defined with the flag 'UNKNOWN_SORT'."):
            vx.sort_flag = "UNKNOWN_SORT"

        with pytest.raises(AttributeError, match="Object property 'sort_flag' attribute is not a valid PropertySortFlag"
                                                 " enum value."):
            vx.sort_flag = {"a": 0.45}
        # ------------------------------------------------------------------------------------------------------------ #

        # Valid => should not raise any exception
        vx.filter_flag = PropertyFilterFlag.BASIC_FILTER
        vx.sort_flag = PropertySortFlag.ADVANCED_SORT
        assert vx.filter_flag == PropertyFilterFlag.BASIC_FILTER
        assert vx.sort_flag == PropertySortFlag.ADVANCED_SORT

    def test_setting_object_property_datatype(self):
        """
        Tests setting object property datatype property
        """
        vx = ObjectProperty(property_name="v_x", dtype=DataType.INTEGER)
        assert vx.datatype == DataType.INTEGER

        # ----------------------- Tests invalid object property datatype setting exception ------------------------ #
        with pytest.raises(AttributeError, match="Object property 'datatype' error : No DataType "
                                                 "defined with the key 'unkn_dtype'."):
            vx.datatype = "unkn_dtype"

        with pytest.raises(AttributeError, match="Object property 'datatype' attribute is not a valid "
                                                 "DataType enum value."):
            vx.datatype = {"bcde": 1.5, 23: [1.2, 3.4, 5.6]}
        # ------------------------------------------------------------------------------------------------------------ #

        # Valid => should not raise any exception
        vx.datatype = DataType.BOOLEAN
        assert vx.datatype == DataType.BOOLEAN

    def test_setting_object_property_unit(self):
        """
        Tests setting object property unit property
        """
        alpha = ObjectProperty(property_name="alpha")

        # --------------------------- Tests invalid object property unit setting exception --------------------------- #
        with pytest.raises(AttributeError, match="Object property 'unit' property error : Unknown unit name 'fairies'."):
            alpha.unit = "fairies"

        invalid_objprop_unit_err = "Object property 'unit' property is not a valid \\(non-empty\\) string."
        with pytest.raises(AttributeError, match=invalid_objprop_unit_err):
            alpha.unit = ""

        with pytest.raises(AttributeError, match=invalid_objprop_unit_err):
            alpha.unit = ["kg", "V", "cm", "Gauss"]
        # ------------------------------------------------------------------------------------------------------------ #

        # Valid => should not raise any exception
        alpha.unit = U.mGauss
        assert alpha.unit == U.mGauss

    def test_object_property_display_name(self):
        """Tests object property display name name + (unit)"""
        vx = ObjectProperty(property_name="V_x", unit=U.km_s)
        assert vx.display_name == "V_x (\\textrm{km}\\cdot\\textrm{s}^{-1})"

    def test_object_property_equality(self):
        """
        Tests object property rich comparison method ObjectProperty.__eq__()
        """
        vx = ObjectProperty(property_name="v_x", sort_flag=PropertySortFlag.BASIC_SORT, unit=U.km_s,
                            filter_flag=PropertyFilterFlag.BASIC_FILTER, dtype=DataType.RATIONAL,
                            description="Galaxy global velocity coordinate along x-axis")

        # Different UUID => not equals
        assert vx != ObjectProperty(property_name=vx.property_name, description=vx.description, sort_flag=vx.sort_flag,
                                    filter_flag=vx.filter_flag, unit=vx.unit)

        # Different name => not equals
        vx2 = ObjectProperty(property_name="different name", description=vx.description, sort_flag=vx.sort_flag,
                             filter_flag=vx.filter_flag, unit=vx.unit, uid=vx.uid)
        assert vx != vx2
        vx2.property_name = vx.property_name

        # Different description => not equals
        vx2.description = "Different description"
        assert vx != vx2
        vx2.description = vx.description

        # Different filter/sort flags => not equals
        vx2.filter_flag = PropertyFilterFlag.NO_FILTER
        assert vx != vx2
        vx2.filter_flag = vx.filter_flag
        vx2.sort_flag = PropertySortFlag.NO_SORT
        assert vx != vx2
        vx2.sort_flag = vx.sort_flag

        # Different datatpy => not equals
        vx2.datatype = DataType.INTEGER
        assert vx != vx2
        vx2.datatype = vx.datatype

        # Different unit => not equals
        vx2.unit = U.pc
        assert vx != vx2
        vx2.unit = vx.unit

        # Identical object properties
        assert vx == vx2

    def test_target_object_property_galactica_validity_checks(self, caplog):
        """
        Tests target object property Galactica validity checks

        Parameters
        ----------
        caplog: captured log PyTest fixture
        """
        # Create target object
        tobj = TargetObject(name="Spiral galaxy")
        tobj.object_properties.add(ObjectProperty(property_name="This is a way too long property name for a 'Spiral "
                                                                "galaxy' target object"))

        # Object property name too long
        tobj.galactica_validity_check()
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "'This is a way too long property name for a 'Spiral galaxy' target object'"
                                            " target object property name is too long for Galactica (max. 64 "
                                            "characters).")

    def test_object_property_hdf5_io(self, tmp_path):
        """
        Tests saving/loading ObjectProperty from HDF5 file

        Parameters
        ----------
        tmp_path: temporary path  PyTest fixture
        """
        res = GenericResult(name="Key result 1 !")
        tobj = TargetObject(name="Spiral galaxy")

        # Add properties + property groups
        vx = tobj.object_properties.add(ObjectProperty(property_name="v_x", sort_flag=PropertySortFlag.BASIC_SORT,
                                                       unit=U.km_s, filter_flag=PropertyFilterFlag.BASIC_FILTER,
                                                       dtype=DataType.RATIONAL,
                                                       description="Galaxy global velocity coordinate along x-axis"))
        cat = res.catalogs.add(Catalog(target_object=tobj, name="Spiral galaxy catalog"))
        ramses = SimulationCode(name="Ramses 3 (MHD)", code_name="Ramses")
        simu = Simulation(simu_code=ramses, name="My simu énorme")
        simu.generic_results.add(res)

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

        # Compare object properties
        res_loaded = simu_loaded.generic_results[res.name]
        cat_loaded = res_loaded.catalogs[cat.name]
        loaded_vx = cat_loaded.target_object.object_properties[vx.property_name]
        assert vx == loaded_vx


class TestObjectPropertyGroup(object):
    def test_target_object_property_group_init(self):
        """
        Tests target object property group instance initialisation
        """
        # Object property group initialisation
        g = ObjectPropertyGroup(group_name="velocity", description="My group descr.")

        assert g.group_name == "velocity"
        assert g.description == "My group descr."

        # Test str() conversion
        assert str(g) == "'velocity' property group"

    def test_setting_object_property_group_name_exc(self):
        """
        Tests that a target object property group defined without name raises an exception
        """
        # Tests target object property group defined without name
        with pytest.raises(AttributeError, match="ObjectPropertyGroup 'group_name' attribute is not defined \\(mandatory\\)."):
            pgroup_exc = ObjectPropertyGroup()  # No object property group name defined

        g = ObjectPropertyGroup(group_name="velocity")

        # ------------ Tests invalid object property group name setting exception ---------------- #
        empty_name_err = "ObjectPropertyGroup 'group_name' property is not a valid \\(non-empty\\) string."
        with pytest.raises(AttributeError, match=empty_name_err):
            g.group_name = -1

        with pytest.raises(AttributeError, match=empty_name_err):
            g.group_name = ""
        # ---------------------------------------------------------------------------------------- #

        # Valid => should not raise any exception
        g.group_name = "Velocity"

    def test_setting_object_property_group_description(self):
        """
        Tests setting object property description property
        """
        g = ObjectPropertyGroup(group_name="velocities")

        # ------------------- Tests invalid object property group description setting exception ---------------------- #
        with pytest.raises(AttributeError, match="ObjectPropertyGroup 'description' property is not a valid string."):
            g.description = {'a': [0, 1, 3]}

        # Valid => should not raise any exception
        g.description = "My target object velocity property group"
        # ------------------------------------------------------------------------------------------------------------ #

    def test_object_property_group_equality(self):
        """
        Tests object property rich comparison method ObjectProperty.__eq__()
        """
        vel = ObjectPropertyGroup(group_name="velocity", description="My descr.")

        # Different UUID => not equals
        assert vel != ObjectPropertyGroup(group_name=vel.group_name, description=vel.description)

        # Different name => not equals
        vel2 = ObjectPropertyGroup(group_name="other name", description=vel.description, uid=vel.uid)
        assert vel != vel2
        vel2.group_name = vel.group_name
        assert vel == vel2

        # Different description => not equals
        vel2.description = "Different description"
        assert vel != vel2
        vel2.description = vel.description

        # Group property list differ => not equals
        vx = vel.group_properties.add(ObjectProperty(property_name="vel_x"))
        vy = vel.group_properties.add(ObjectProperty(property_name="vel_y"))
        vel2.group_properties.add(vx)
        assert vel2 != vel
        vel2.group_properties.add(vy)

        # Identical object property groups
        assert vel == vel2

    def test_target_object_property_group_galactica_validity_checks(self, caplog):
        """
        Tests target object property group Galactica validity checks

        Parameters
        ----------
        caplog: captured log PyTest fixture
        """
        # Create target object with object property group
        tobj = TargetObject(name="Spiral galaxy")
        tobj.property_groups.add(ObjectPropertyGroup(group_name="This is a way too long object property group name"))

        # Object property name too long
        tobj.galactica_validity_check()
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "'This is a way too long object property group name' property group name "
                                            "is too long for Galactica (max. 32 characters).")

    def test_object_property_group_hdf5_io(self, tmp_path):
        """
        Tests saving/loading ObjectPropertyGroup from HDF5 file

        Parameters
        ----------
        tmp_path: temporary path  PyTest fixture
        """
        res = GenericResult(name="Key result 1 !")
        tobj = TargetObject(name="Spiral galaxy")

        # Add properties + property groups
        vx = tobj.object_properties.add(ObjectProperty(property_name="v_x"))
        vy = tobj.object_properties.add(ObjectProperty(property_name="v_y"))
        vz = tobj.object_properties.add(ObjectProperty(property_name="v_z"))
        vel = tobj.property_groups.add(ObjectPropertyGroup(group_name="velocity", description="Galaxy global velocity"))
        vel.group_properties.add(vx)
        vel.group_properties.add(vy)
        vel.group_properties.add(vz)
        cat = res.catalogs.add(Catalog(target_object=tobj, name="Spiral galaxy catalog"))
        ramses = SimulationCode(name="Ramses 3 (MHD)", code_name="Ramses")
        simu = Simulation(simu_code=ramses, name="My simu énorme")
        simu.generic_results.add(res)

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

        # Compare object propertiy groups
        res_loaded = simu_loaded.generic_results[res.name]
        cat_loaded = res_loaded.catalogs[cat.name]
        tobj_loaded = cat_loaded.target_object
        velocities_loaded = tobj_loaded.property_groups[vel.group_name]
        assert vel == velocities_loaded


class TestTargetObject(object):
    def test_target_object_init(self):
        """
        Tests target object instance initialisation
        """
        # Target object initialisation
        tobj = TargetObject(name="Spiral galaxy", description="This is a disk-like galaxy")
        tobj.object_properties.add(ObjectProperty(property_name="pos_x"))
        tobj.object_properties.add(ObjectProperty(property_name="pos_y"))
        tobj.object_properties.add(ObjectProperty(property_name="mass"))

        assert tobj.name == "Spiral galaxy"
        assert tobj.description == "This is a disk-like galaxy"
        assert len(tobj.object_properties) == 3

        # Test str() conversion
        assert str(tobj) == "'Spiral galaxy' target object"

    def test_target_object_property_insertion(self):
        """
        Tests exceptions raised upon object property(-group) insertion into TargetObject instances
        """
        tobj = TargetObject(name="Spiral galaxy", description="This is a disk-like galaxy")
        alpha = ObjectProperty(property_name='alpha')
        delta = ObjectProperty(property_name='delta')
        beta = ObjectProperty(property_name='beta')
        gamma = ObjectProperty(property_name='gamma')

        # Tries to add property to a group and then add group before the property has been added to the TargetObject
        # property list => raises an error
        g = ObjectPropertyGroup(group_name="G1")
        g.group_properties.add(alpha)
        g.group_properties.add(delta)
        with pytest.raises(AttributeError, match="{p!s} does not belong to this TargetObject object property "
                                                 "list.".format(p=alpha)):
            tobj.property_groups.add(g)

        # Tries to add a property to an already registered group in the TargetObject property group list while the
        # property has not added yet to the TargetObject property list => raises an error
        tobj.object_properties.add(alpha)
        tobj.object_properties.add(delta)
        tobj.property_groups.add(g)  # => Ok
        with pytest.raises(AttributeError, match="{p!s} does not belong to this TargetObject object property "
                                                 "list.".format(p=beta)):
            g.group_properties.add(beta)

        # Valid => no error
        tobj.object_properties.add(gamma)
        g.group_properties.add(gamma)  # Ok

    def test_deleting_object_prop_from_targobj_while_inserted_in_group(self):
        """
        Tests object property deletion from TargetObject's property list while object property is included in one of the
        TargetObject's ObjectPropertyGroup.
        """
        tobj = TargetObject(name="Pre-stellar core")
        x = tobj.object_properties.add(ObjectProperty(property_name="pos_x"))
        y = tobj.object_properties.add(ObjectProperty(property_name="pos_y"))
        z = tobj.object_properties.add(ObjectProperty(property_name="pos_z"))
        pos = tobj.property_groups.add(ObjectPropertyGroup(group_name="position"))
        pos.group_properties.add(x)
        pos.group_properties.add(y)
        pos.group_properties.add(z)

        # Tries to delete x, while it is in 'position' group
        with pytest.raises(AttributeError, match="''pos_x' target object property' cannot be deleted, the following "
                                                 "items depend on it \\(try to delete them first\\) : \\['Pre-stellar "
                                                 "core' target object - 'position' property group - 'pos_x' target "
                                                 "object property\\]."):
            del tobj.object_properties[x.property_name]

        # Delete property from 'position' group first
        del pos.group_properties[x.property_name]

        # THEN delete Property from TargetObject => Ok
        del tobj.object_properties[x.property_name]

    def test_setting_target_object_name_exc(self):
        """
        Tests that a target object defined without name raises an exception
        """
        # Tests target object defined without name
        with pytest.raises(AttributeError, match="TargetObject 'name' attribute is not defined \\(mandatory\\).") as e:
            tobj_exc = TargetObject()  # No target object name defined

        tobj = TargetObject(name="Spiral galaxy")

        # --------------- Tests invalid target object name setting exception --------------------- #
        empty_name_err = "TargetObject 'name' property is not a valid \\(non-empty\\) string."
        with pytest.raises(AttributeError, match=empty_name_err):
            tobj.name = -1

        with pytest.raises(AttributeError, match=empty_name_err):
            tobj.name = ""
        # ---------------------------------------------------------------------------------------- #

        # Valid => should not raise any exception
        tobj.name = "Disk-like galaxy"

    def test_setting_target_object_description(self):
        """
        Tests setting target object description property
        """
        tobj = TargetObject(name="Pre-stellar core")

        # ------------------------ Tests invalid target object description setting exception ------------------------- #
        with pytest.raises(AttributeError, match="TargetObject 'description' property is not a valid string."):
            tobj.description = 0

        # Valid => should not raise any exception
        tobj.description = "My target object"
        # ------------------------------------------------------------------------------------------------------------ #

    def test_targetobject_equality(self):
        """
        Tests target object rich comparison method Catalog.__eq__()
        """
        tobj = TargetObject(name="Elliptic galaxy", description="Reddish roundish old galaxy")

        # Different UUID => not equals
        assert tobj != TargetObject(name=tobj.name, description=tobj.description)

        # Different name => not equals
        assert tobj != TargetObject(name="Name", description=tobj.description, uid=tobj.uid)

        # Different description => not equals
        assert tobj != TargetObject(name=tobj.name, description="Alt. description", uid=tobj.uid)

        # Identical target objects
        t = TargetObject(name=tobj.name, description=tobj.description, uid=tobj.uid)
        assert tobj == t

        # Add object properties
        a1 = tobj.object_properties.add(ObjectProperty(property_name="property #1"))
        a2 = tobj.object_properties.add(ObjectProperty(property_name="property #2"))
        # Object property list differ => not equals
        t.object_properties.add(a1)
        assert t != tobj
        # Identical object properties
        t.object_properties.add(a2)
        assert t == tobj

        # Add Object property groups
        g = tobj.property_groups.add(ObjectPropertyGroup(group_name="Group #1"))
        g.group_properties.add(a1)
        g.group_properties.add(a2)
        # Object property group list differ => not equals
        assert t != tobj
        # Identical object properties
        t.property_groups.add(g)
        assert t == tobj

    def test_target_object_galactica_validity_checks(self, caplog):
        """
        Tests target object Galactica validity checks

        Parameters
        ----------
        caplog: captured log PyTest fixture
        """
        # Create target object
        tobj = TargetObject(name="Spiral galaxy")

        # Target object name too long
        tobj.name = "Spiral galaxy with boxy shapes but not strictly speaking disky"
        tobj.galactica_validity_check()
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "'Spiral galaxy with boxy shapes but not strictly speaking disky' target "
                                            "object name is too long for Galactica (max. 32 characters).")

    def test_target_object_hdf5_io(self, tmp_path):
        """
        Tests saving/loading TargetObject from HDF5 file

        Parameters
        ----------
        tmp_path: temporary path  PyTest fixture
        """
        res = GenericResult(name="Key result 1 !")
        tobj = TargetObject(name="Spiral galaxy", description="My object full description")

        # Add properties + property groups
        alpha = tobj.object_properties.add(ObjectProperty(property_name='alpha'))
        beta = tobj.object_properties.add(ObjectProperty(property_name='beta'))
        g = tobj.property_groups.add(ObjectPropertyGroup(group_name="G"))
        g.group_properties.add(alpha)
        g.group_properties.add(beta)

        cat = res.catalogs.add(Catalog(target_object=tobj, name="Spiral galaxy catalog"))
        ramses = SimulationCode(name="Ramses 3 (MHD)", code_name="Ramses")
        simu = Simulation(simu_code=ramses, name="My simu énorme")
        simu.generic_results.add(res)

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

        # Compare target objects
        res_loaded = simu_loaded.generic_results[res.name]
        cat_loaded = res_loaded.catalogs[cat.name]
        assert tobj == cat_loaded.target_object


__all__ = ["TestTargetObject"]
