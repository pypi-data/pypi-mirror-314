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
import logging

from future.builtins import str, int
import pytest
import numpy as N

from astrophysix.simdm import Project, ProjectCategory, SimulationStudy
from astrophysix.simdm.experiment import Simulation
from astrophysix.simdm.protocol import SimulationCode
from astrophysix.simdm.results import GenericResult, Snapshot
from astrophysix.simdm.catalogs import Catalog, TargetObject, ObjectProperty, CatalogField, ObjectPropertyGroup
from astrophysix.simdm.datafiles import Datafile
from astrophysix.simdm.services import CatalogDataProcessingService, CatalogFieldBinding
from astrophysix import units as U
from astrophysix.simdm.utils import DataType

from astrophysix.utils import Hdf5StudyPersistent, Hdf5StudyFileMode


class TestCatalogField(object):
    def test_catalog_field_init(self):
        """
        Tests object catalog field instance initialisation
        """
        # Catalog field initialisation
        tobj = TargetObject(name="Elliptic galaxy")
        x = tobj.object_properties.add(ObjectProperty(property_name="pos_x"))
        y = tobj.object_properties.add(ObjectProperty(property_name="pos_y"))
        cat = Catalog(target_object=tobj, name="Elliptic galaxy catalog")
        fx = cat.catalog_fields.add(CatalogField(x, values=N.random.uniform(size=10)))
        fy = cat.catalog_fields.add(CatalogField(y, values=N.random.uniform(size=10)))

        assert fx.property_name == x.property_name
        assert fy.object_property is y
        assert fx.nobjects == cat.nobjects == 10

        # Test str() conversion
        assert str(fx) == "'pos_x' catalog field"

    def test_catalog_field_values_exc(self):
        """
        Tests that a catalog field set with empty value array or array with dimensions != 1 raises an error
        """
        y = ObjectProperty(property_name="pos_y")

        # Undefined value array => error
        with pytest.raises(AttributeError, match="Undefined 'values' property in CatalogField."):
            f = CatalogField(y)

        # Empty array => error
        with pytest.raises(AttributeError, match="CatalogField 'values' array need at least 1 value."):
            f = CatalogField(y, values=N.array([]))

        # 2D array => error
        with pytest.raises(AttributeError, match="'values' CatalogField attribute must be a 1-dimensional array."):
            f = CatalogField(y, values=N.random.uniform(size=(10, 5)))

        # Ok => 10 items in fields
        fy = CatalogField(y, values=N.random.uniform(size=10))

        # Tries to change the size of a CatalogField => error
        with pytest.raises(AttributeError, match="The number of items in this CatalogField is 10 and cannot be changed."):
            fy.field_values = N.random.uniform(size=12)

    def test_catalog_field_object_property_setting_exc(self):
        """
        Tests setting an ObjectProperty into a CatalogField object
        """
        tobj = TargetObject(name="My object")
        y = tobj.object_properties.add(ObjectProperty(property_name="pos_y"))

        # Tests CatalogField defined without target object property
        with pytest.raises(AttributeError, match="Undefined 'obj_prop' object property attribute in CatalogField."):
            CatalogField()  # No target object property defined

        # Tests invalid target object property initialisation exception
        invalid_objprop_err = "CatalogField 'obj_prop' attribute is not a valid ObjectProperty instance."
        with pytest.raises(AttributeError, match=invalid_objprop_err):
            CatalogField(obj_prop=-5)  # Invalid target object property
        with pytest.raises(AttributeError, match=invalid_objprop_err):
            CatalogField("Test")  # Invalid target object property

        # Catalog field initialisation : valid => should not raise any exception
        f1 = CatalogField(obj_prop=y, values=N.random.uniform(size=5))
        f2 = CatalogField(y, values=N.random.uniform(size=5))

    def test_catalog_field_equality(self):
        """
        Tests catalog field rich comparison method CatalogField.__eq__()
        """
        x = ObjectProperty(property_name="pos_x")
        y = ObjectProperty(property_name="pos_y")
        z = ObjectProperty(property_name="pos_z")
        cfx = CatalogField(x, values=N.random.uniform(size=20))

        # Different UUID => not equals
        assert cfx != CatalogField(cfx.object_property, values=cfx.field_values)

        # Different object property => not equals
        assert cfx != CatalogField(y, values=cfx.field_values, uid=cfx.uid)

        # Different values => not equals
        assert cfx != CatalogField(cfx.object_property, values=N.random.uniform(size=20), uid=cfx.uid)

        # Identical catalog fields
        f = CatalogField(cfx.object_property, values=cfx.field_values, uid=cfx.uid)
        assert cfx == f

    def test_catalog_field_to_pandas(self):
        """Tests CatalogField conversion into a pandas.Series"""
        x = ObjectProperty(property_name="pos_x", unit=U.kpc)
        cf = CatalogField(obj_prop=x, values=N.random.uniform(size=200))
        s = cf.to_pandas()
        assert s.size == 200
        assert s.name == "pos_x (\\textrm{kpc})"

    def test_catalog_field_hdf5_io(self, tmp_path):
        """
        Tests saving/loading CatalogField from HDF5 file

        Parameters
        ----------
        tmp_path: temporary path  PyTest fixture
        """
        # Add tabulated values in catalog + properties in target object
        tobj = TargetObject(name="Spiral galaxy")
        x = tobj.object_properties.add(ObjectProperty(property_name="pos_x"))
        y = tobj.object_properties.add(ObjectProperty(property_name="pos_y"))
        z = tobj.object_properties.add(ObjectProperty(property_name="pos_z"))
        cat = Catalog(target_object=tobj, name="Spiral galaxy catalog", description="My descr.")
        vals_x = N.random.uniform(size=200)
        cfx = cat.catalog_fields.add(CatalogField(obj_prop=x, values=vals_x))

        res = GenericResult(name="Key result")
        res.catalogs.add(cat)

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

        # Compare catalog fields
        res_loaded = simu_loaded.generic_results[res.name]
        cat_loaded = res_loaded.catalogs[cat.name]
        field_loaded = cat_loaded.catalog_fields[cfx.property_name]
        assert cfx == field_loaded and field_loaded.nobjects == 200

        cfx_min, cfx_max, cfx_mean, cfx_std = field_loaded.field_value_stats
        assert cfx_min == vals_x.min() and cfx_max == vals_x.max()
        assert cfx_mean == vals_x.mean() and cfx_std == vals_x.std()


class TestCatalog(object):
    def test_catalog_init(self):
        """
        Tests object catalog instance initialisation
        """
        # Object catalog initialisation
        tobj = TargetObject(name="Elliptic galaxy")
        cat = Catalog(target_object=tobj, name="Elliptic galaxy catalog",
                      description="This is the catalog of all elliptic galaxies identified in the simulation")

        assert cat.name == "Elliptic galaxy catalog"
        assert cat.target_object is tobj
        assert cat.description == "This is the catalog of all elliptic galaxies identified in the simulation"

        # Test str() conversion
        assert str(cat) == "'Elliptic galaxy catalog' catalog"

    def test_catalog_targetobject_setting_exc(self):
        """
        Tests setting a TargetObject into a Catalog object
        """
        # Tests Catalog defined without target object
        with pytest.raises(AttributeError, match="Undefined target object for 'My super catalog' catalog."):
            cat_exc = Catalog(name="My super catalog")  # No target object defined

        # Tests invalid target_object initialisation exception
        invalid_targobj_err = "Catalog 'target_object' attribute is not a valid TargetObject instance."
        with pytest.raises(AttributeError, match=invalid_targobj_err):
            cat_exc = Catalog(name="My catalog", target_object=-5)  # Invalid target object
        with pytest.raises(AttributeError, match=invalid_targobj_err):
            cat_exc = Catalog(-5, name="My catalog")  # Invalid target object

        # Catalog initialisation : valid => should not raise any exception
        core = TargetObject(name="Pre-stellar core")
        cat1 = Catalog(core, name="My pre-stellar core catalog")
        cat2 = Catalog(name="My pre-stellar core catalog", target_object=core)

    def test_setting_catalog_name_exc(self):
        """
        Tests that a catalog defined without name raises an exception
        """
        # Tests catalog defined without name
        with pytest.raises(AttributeError) as e:
            cat_exc = Catalog()  # No catalog name defined
        assert str(e.value) == "Catalog 'name' attribute is not defined (mandatory)."

        cat = Catalog(target_object=TargetObject(name="Pre-stellar core"), name="My catalog")

        # ------------------- Tests invalid catalog name setting exception ----------------------- #
        empty_name_err = "Catalog 'name' property is not a valid (non-empty) string."
        with pytest.raises(AttributeError) as e:
            cat.name = -1
        assert str(e.value) == empty_name_err

        with pytest.raises(AttributeError) as e:
            cat.name = ""
        assert str(e.value) == empty_name_err
        # ---------------------------------------------------------------------------------------- #

        # Valid => should not raise any exception
        cat.name = "My best catalog"

    def test_setting_catalog_description(self):
        """
        Tests setting catalog description property
        """
        cat = Catalog(target_object=TargetObject(name="Pre-stellar core"), name="My super catalog")

        # ------------------------------ Tests invalid catalog description setting exception ------------------------- #
        with pytest.raises(AttributeError) as e:
            cat.description = 0
        assert str(e.value) == "Catalog 'description' property is not a valid string."

        # Valid => should not raise any exception
        cat.description = "My catalog description"
        # ------------------------------------------------------------------------------------------------------------ #

    def test_catalog_field_binding_insertion(self):
        """
        Tests exceptions raised upon object catalog field binding insertion into Catalog instances
        """
        # Create TargetObject + properties
        tobj = TargetObject(name="Spiral galaxy", description="This is a disk-like galaxy")
        alpha = tobj.object_properties.add(ObjectProperty(property_name='alpha'))
        beta = tobj.object_properties.add(ObjectProperty(property_name='beta'))
        gamma = tobj.object_properties.add(ObjectProperty(property_name='gamma'))

        # Create catalog + fields
        cat = Catalog(target_object=tobj, name="Elliptic galaxy catalog")
        alpha_f = CatalogField(alpha, values=N.random.uniform(size=100))
        beta_f = cat.catalog_fields.add(CatalogField(beta, values=N.random.uniform(size=100)))
        gamma_f = cat.catalog_fields.add(CatalogField(gamma, values=N.random.uniform(size=100)))

        # Create data processing service
        serv = cat.processing_services.add(CatalogDataProcessingService(service_name="my_service", data_host="IClust"))
        fb_alpha = CatalogFieldBinding(catalog_field=alpha_f, param_key="alpha")

        # Tries to add catalog field binding to the service before the field has been added to the catalog field
        # list => raises an error
        with pytest.raises(AttributeError, match="Cannot add catalog field binding in this data processing service, "
                                                 "{f!s} is not a field of the {cat!s}.".format(f=alpha_f, cat=cat)):
            serv.catalog_field_bindings.add(fb_alpha)

        # Tries to add a data processing service into a catalog while one of its field binding refers to a catalog field
        # that does not belong to the catalog field list (yet) => raises an error
        serv2 = CatalogDataProcessingService(service_name="my_service2", data_host="IClust")
        serv2.catalog_field_bindings.add(fb_alpha)
        fb_beta = serv2.catalog_field_bindings.add(CatalogFieldBinding(catalog_field=beta_f, param_key="beta"))
        fb_gamma = serv2.catalog_field_bindings.add(CatalogFieldBinding(catalog_field=gamma_f, param_key="gamma"))
        with pytest.raises(AttributeError, match="Cannot add catalog processing service. {f!s} is not a field of "
                                                 "the {cat!s}.".format(f=alpha_f, cat=cat)):
            cat.processing_services.add(serv2)

        # # Valid => no error
        cat.catalog_fields.add(alpha_f)
        cat.processing_services.add(serv2)  # Ok
        serv.catalog_field_bindings.add(fb_alpha)  # Ok

    def test_deleting_catfield_from_catalog_while_referenced_in_binding(self):
        """
        Tests object property deletion from TargetObject's property list while object property is included in one of the
        TargetObject's ObjectPropertyGroup.
        """
        # Create TargetObject + properties
        tobj = TargetObject(name="Spiral galaxy", description="This is a disk-like galaxy")
        alpha = tobj.object_properties.add(ObjectProperty(property_name='alpha'))

        # Create catalog + fields
        cat = Catalog(target_object=tobj, name="Elliptic galaxy catalog")
        alpha_f = cat.catalog_fields.add(CatalogField(alpha, values=N.random.uniform(size=100)))

        # Create data processing service
        serv = cat.processing_services.add(CatalogDataProcessingService(service_name="Best service", data_host="IClust"))
        fb_alpha = serv.catalog_field_bindings.add(CatalogFieldBinding(catalog_field=alpha_f, param_key="alpha"))

        # Tries to delete 'alpha' catalog field, while it is referenced in a binding of the 'Best service' service
        with pytest.raises(AttributeError, match="'{f!s}' cannot be deleted, the following items depend on it \\(try to"
                                                 " delete them first\\) : \\[{fb!s}\\].".format(f=alpha_f,
                                                                                                fb=fb_alpha)):
            del cat.catalog_fields[alpha_f.property_name]

        # Delete 'alpha' field binding from 'Best service' data processing service first
        del serv.catalog_field_bindings[fb_alpha.field_property_name]

        # THEN delete the 'alpha' field from the catalog => Ok
        del cat.catalog_fields[alpha_f.property_name]

    def test_catalog_equality(self):
        """
        Tests catalog rich comparison method Catalog.__eq__()
        """
        tobj = TargetObject(name="Elliptic galaxy")
        x = tobj.object_properties.add(ObjectProperty(property_name="pos_x"))
        y = tobj.object_properties.add(ObjectProperty(property_name="pos_y"))
        z = tobj.object_properties.add(ObjectProperty(property_name="pos_z"))
        cat = Catalog(tobj, name="Elliptic galaxy catalog", description="This is my elliptic galaxy catalog")

        # Different UUID => not equals
        assert cat != Catalog(tobj, name=cat.name, description=cat.description)

        # Different target object => not equals
        assert cat != Catalog(TargetObject(name="Spiral galaxy"), name=cat.name, description=cat.description,
                              uid=cat.uid)

        # Different name => not equals
        assert cat != Catalog(tobj, name="Name", description=cat.description, uid=cat.uid)

        # Different description => not equals
        assert cat != Catalog(tobj, name=cat.name, description="Alt. description", uid=cat.uid)

        # Identical catalogs
        c = Catalog(tobj, name=cat.name, description=cat.description, uid=cat.uid)
        assert cat == c

        # Add datafiles
        df1 = cat.datafiles.add(Datafile(name="My important datafile"))
        df2 = cat.datafiles.add(Datafile(name="My important datafile (2)"))
        # Datafile list differ => not equals
        c.datafiles.add(df1)
        assert c != cat
        # Identical catalogs
        c.datafiles.add(df2)
        assert c == cat

        # Compare catalog tabulated values + fields
        cfx = cat.catalog_fields.add(CatalogField(x, values=N.random.uniform(size=10)))
        cfy = cat.catalog_fields.add(CatalogField(y, values=N.random.uniform(size=10)))
        # Catalog field list differ => not equals
        c.catalog_fields.add(cfx)
        assert cat != c
        # Identical catalogs
        c.catalog_fields.add(cfy)
        assert cat == c

        # Compare catalog data processing services
        cdps = cat.processing_services.add(CatalogDataProcessingService(service_name="surface_density_map",
                                                                        data_host="IClust"))
        # Catalog data processing service list differ => not equals
        assert cat != c
        # Identical catalogs
        c.processing_services.add(cdps)
        assert cat == c

    def test_catalog_with_incompatible_fields(self):
        """
        Tests that adding two fields with different number of items in a catalog raises an Exception
        """
        tobj = TargetObject(name="Pre-stellar core")
        x = tobj.object_properties.add(ObjectProperty(property_name="pos_x"))
        y = tobj.object_properties.add(ObjectProperty(property_name="pos_y"))
        cat = Catalog(target_object=tobj, name="Elliptic galaxy catalog")
        cat.catalog_fields.add(CatalogField(x, values=N.random.uniform(size=10)))
        with pytest.raises(AttributeError, match="Cannot add a catalog field with 12 item values in a catalog "
                                                 "containing 10 items."):
            cat.catalog_fields.add(CatalogField(y, values=N.random.uniform(size=12)))

    def test_catalog_adding_field_with_unknown_targobj_property(self):
        """
        Tests that adding a field linked to a property that does not belong to the catalog's target object property list
        raises an Exception
        """
        tobj = TargetObject(name="Pre-stellar core")
        x = tobj.object_properties.add(ObjectProperty(property_name="pos_x"))
        y = tobj.object_properties.add(ObjectProperty(property_name="pos_y"))
        z = ObjectProperty(property_name="pos_z")  # z not added in target object
        cat = Catalog(target_object=tobj, name="Elliptic galaxy catalog")

        # Tries to add a catalog field with z property => error
        with pytest.raises(AttributeError, match="Cannot add catalog field. 'pos_z' target object property is not a "
                                                 "property of 'Pre-stellar core' target object."):
            cat.catalog_fields.add(CatalogField(z, values=N.random.uniform(size=5)))

    def test_deleting_object_prop_from_catalog_targobj_while_linked_to_field(self):
        """
        Tests object property deletion from catalog's target object while object property is linked to a catalog field.
        """
        tobj = TargetObject(name="Pre-stellar core")
        x = tobj.object_properties.add(ObjectProperty(property_name="pos_x"))
        cat = Catalog(target_object=tobj, name="Elliptic galaxy catalog")
        fx = cat.catalog_fields.add(CatalogField(x, values=N.random.uniform(size=10)))

        # Tries to delete x, while it is linked to fx catalog field
        with pytest.raises(AttributeError, match="''pos_x' target object property' cannot be deleted, the following "
                                                 "items depend on it \\(try to delete them first\\) : \\['Elliptic "
                                                 "galaxy catalog' catalog 'pos_x' catalog field\\]."):
            del tobj.object_properties[x.property_name]

        # Delete CatalogField from Catalog first
        del cat.catalog_fields[x.property_name]

        # THEN delete Property from TargetObject => Ok
        del tobj.object_properties[x.property_name]

    def test_catalog_galactica_validity_checks(self, caplog):
        """
        Tests catalog Galactica validity checks

        Parameters
        ----------
        caplog: captured log PyTest fixture
        """
        # Add tabulated values in catalog + properties in target object
        tobj = TargetObject(name="Spiral galaxy")
        x = tobj.object_properties.add(ObjectProperty(property_name="pos_x"))
        y = tobj.object_properties.add(ObjectProperty(property_name="pos_y"))
        z = tobj.object_properties.add(ObjectProperty(property_name="pos_z"))
        cat = Catalog(target_object=tobj, name="Spiral galaxy catalog at $Z \\simeq 1.0$", description="My descr.")

        # Empty catalog nofield, no object within
        cat.galactica_validity_check()
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "'Spiral galaxy catalog at $Z \\simeq 1.0$' catalog does not contain any "
                                            "object.")
        cat.catalog_fields.add(CatalogField(obj_prop=x, values=N.random.uniform(size=100)))

        # Catalog name too long
        cat.name = "This is a way too long catalog name for a 'Spiral galaxy catalog at $Z \\simeq 1.0$'"
        cat.galactica_validity_check()
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "'This is a way too long catalog name for a 'Spiral galaxy catalog at $Z "
                                            "\\simeq 1.0$'' catalog name is too long for Galactica (max. 64 "
                                            "characters).")

    def test_catalog_hdf5_io(self, tmp_path):
        """
        Tests saving/loading Catalog from HDF5 file

        Parameters
        ----------
        tmp_path: temporary path  PyTest fixture
        """
        # Add tabulated values in catalog + properties in target object
        tobj = TargetObject(name="Spiral galaxy")
        x = tobj.object_properties.add(ObjectProperty(property_name="pos_x"))
        y = tobj.object_properties.add(ObjectProperty(property_name="pos_y"))
        z = tobj.object_properties.add(ObjectProperty(property_name="pos_z"))
        cat = Catalog(target_object=tobj, name="Spiral galaxy catalog at $Z \\simeq 1.0$", description="My descr.")
        vals_x = N.random.uniform(size=20)
        cat.catalog_fields.add(CatalogField(obj_prop=x, values=vals_x))

        cat.datafiles.add(Datafile(name="My datafile"))
        cat.datafiles.add(Datafile(name="My datafile (2)"))
        res = GenericResult(name="Key result 1 !", description="My description", directory_path="/my/path/to/result")
        res.catalogs.add(cat)

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

        # Compare catalogs
        res_loaded = simu_loaded.generic_results[res.name]
        cat_loaded = res_loaded.catalogs[cat.name]
        assert cat == cat_loaded and cat.nobjects == cat_loaded.nobjects and cat_loaded.nobjects == 20

    def test_catalog_targobj_hdf5_io_compatibility_v1(self):
        """Backward compatibility test : tests loading a Simulation study saved with version v<0.5 where Catalog and
        TargetObject instances did not exist."""
        # Try to load a Project with no catalog/target object (v1), saved by an older version of astrophysix (v<0.5)
        study_0_4_2_path = os.path.join(os.path.dirname(__file__), "io", "backward_compat", "study_v0.4.2.h5")
        study = SimulationStudy.load_HDF5(study_0_4_2_path)
        # No catalog
        assert len(study.project.simulations[0].snapshots[0].catalogs) == 0

    def test_catalog_to_pandas(self):
        """Tests Catalog conversion into a pandas.Dataframe"""
        x = ObjectProperty(property_name="pos_x", unit=U.kpc)
        y = ObjectProperty(property_name="pos_y", unit=U.kpc)
        z = ObjectProperty(property_name="pos_z", unit=U.kpc)
        tobj = TargetObject(name="galaxy")
        tobj.object_properties.add(x)
        tobj.object_properties.add(y)
        tobj.object_properties.add(z)
        cat = Catalog(target_object=tobj, name="catalog #1")
        fx = cat.catalog_fields.add(CatalogField(obj_prop=x, values=N.random.uniform(size=200)*10.0+100.0))
        fy = cat.catalog_fields.add(CatalogField(obj_prop=y, values=N.random.uniform(size=200)*3.0+50.0))
        fz = cat.catalog_fields.add(CatalogField(obj_prop=z, values=N.random.uniform(size=200)*4.0+250.0))
        df = cat.to_pandas()
        assert df.shape == (200, 3)
        assert (fx.field_values == df[fx.object_property.display_name].values).all()
        assert (fy.field_values == df[fy.object_property.display_name].values).all()
        assert (fz.field_values == df[fz.object_property.display_name].values).all()

    def test_catalog_hdf5_standalone_export(self, tmp_path):
        """
        Tests exporting Catalog into a standalone HDF5 file

        Parameters
        ----------
        tmp_path: temporary path  PyTest fixture
        """
        # Add tabulated values in catalog + properties/property group in target object
        tobj = TargetObject(name="Spiral galaxy")
        x = tobj.object_properties.add(ObjectProperty(property_name="pos_x"))
        y = tobj.object_properties.add(ObjectProperty(property_name="pos_y"))
        z = tobj.object_properties.add(ObjectProperty(property_name="pos_z"))
        m = tobj.object_properties.add(ObjectProperty(property_name="mass"))
        pos_group = ObjectPropertyGroup(group_name="position")
        pos_group.group_properties.add(x)
        pos_group.group_properties.add(y)
        pos_group.group_properties.add(z)
        tobj.property_groups.add(pos_group)

        cat = Catalog(target_object=tobj, name="Spiral galaxy catalog at $Z \\simeq 1.2$",
                      description="My description of the catalog")
        vals_x = N.random.uniform(size=20) * 3.0 + 10.0
        vals_y = N.random.uniform(size=20) * 2.0 + 50.0
        vals_z = N.random.uniform(size=20) * 5.0 + 100.0
        vals_m = N.random.uniform(size=20) * 40.0 + 1000.0
        cat.catalog_fields.add(CatalogField(obj_prop=x, values=vals_x))
        cat.catalog_fields.add(CatalogField(obj_prop=y, values=vals_y))
        cat.catalog_fields.add(CatalogField(obj_prop=z, values=vals_z))
        cat.catalog_fields.add(CatalogField(obj_prop=m, values=vals_m))

        # Save catalog into a standalone HDF5 file
        h5_fpath = str(tmp_path / "catalog.h5")
        cat.save_HDF5(h5_fpath, galactica_checks=True)

        lcat = Catalog.load_HDF5(h5_fpath)
        assert lcat == cat


class TestCatalogDataProcessingService(object):
    def test_process_service_comparison(self):
        """
        Tests rich comparison method CatalogDataProcessingService.__eq__()
        """
        dps = CatalogDataProcessingService(service_name="my_service", data_host="my_workstation")

        # Identical data processing service
        dps2 = CatalogDataProcessingService(service_name=dps.service_name, uid=dps.uid, data_host=dps.data_host)
        assert dps == dps2

        # Compare with different catalog field bindings
        tobj = TargetObject(name="Spiral galaxy")
        x = tobj.object_properties.add(ObjectProperty(property_name="pos_x"))
        y = tobj.object_properties.add(ObjectProperty(property_name="pos_y"))
        z = tobj.object_properties.add(ObjectProperty(property_name="pos_z"))
        vals_x = N.random.uniform(size=20) * 3.0 + 10.0
        vals_y = N.random.uniform(size=20) * 2.0 + 50.0
        vals_z = N.random.uniform(size=20) * 5.0 + 100.0
        cf_x = CatalogField(obj_prop=x, values=vals_x)
        cf_y = CatalogField(obj_prop=y, values=vals_y)
        cf_z = CatalogField(obj_prop=z, values=vals_z)
        bx = dps.catalog_field_bindings.add(CatalogFieldBinding(catalog_field=cf_x, param_key="xcenter"))
        by = dps.catalog_field_bindings.add(CatalogFieldBinding(catalog_field=cf_y, param_key="ycenter"))
        bz = dps.catalog_field_bindings.add(CatalogFieldBinding(catalog_field=cf_z, param_key="zcenter"))
        # Catalog field binding list differ => not equals
        assert dps != dps2
        dps2.catalog_field_bindings.add(bx)
        dps2.catalog_field_bindings.add(by)
        dps2.catalog_field_bindings.add(bz)
        # Identical CatalogDataProcessingService objects
        assert dps == dps2

    def test_cannot_add_data_proc_service_in_genresult_catalogs(self):
        """
        Tests that trying to add a CatalogDataProcessingService into a GerericResult's catalog raises an error.
        """
        dps1 = CatalogDataProcessingService(service_name="slice_map", data_host="my_cluster")
        dps2 = CatalogDataProcessingService(service_name="ppv_cube", data_host="my_GPU_cluster")

        tobj = TargetObject(name="Spiral galaxy")
        sn = Snapshot(name="My snapshot")
        gres = GenericResult(name="My result")
        gres_cat = Catalog(target_object=tobj, name="Spiral galaxy catalog")
        gres_cat2 = Catalog(target_object=tobj, name="Spiral galaxy catalog 2")
        gres.catalogs.add(gres_cat2)
        gres_cat.processing_services.add(dps1)

        # Tries to add a a catalog linked to data-processing services into a GenericResult => error
        with pytest.raises(AttributeError, match="Cannot add a 'Spiral galaxy catalog' catalog with any data-processing"
                                                 " service linked to it into a GenericResult."):
            gres.catalogs.add(gres_cat)

        # Tries to add a data-processing service into a GenericResult's catalog => error
        with pytest.raises(AttributeError, match="Cannot add a data-processing service into a GenericResult's "
                                                 "catalog."):
            gres_cat2.processing_services.add(dps2)

        # With snapshots, should work. (# 1 first add catalog into snapshot, then add dps to catalog)
        cat_sn = sn.catalogs.add(Catalog(target_object=tobj, name="Spiral galaxy catalog"))
        cat_sn.processing_services.add(dps2)

        # (#2 first add dps to catalog, then add catalog into snapshot)
        cat_sn2 = Catalog(target_object=tobj, name="Spiral galaxy catalog 2")
        cat_sn2.processing_services.add(dps2)
        sn.catalogs.add(cat_sn2)

    def test_data_proc_service_hdf5_io(self, tmp_path):
        """
        Tests saving/loading CatalogDataProcessingService from HDF5 file

        Parameters
        ----------
        tmp_path: temporary path  PyTest fixture
        """
        dps1 = CatalogDataProcessingService(service_name="slice_map", data_host="my_cluster")
        dps2 = CatalogDataProcessingService(service_name="ppv_cube", data_host="my_GPU_cluster")

        tobj = TargetObject(name="Spiral galaxy")
        cat = Catalog(target_object=tobj, name="Spiral galaxy catalog")
        # Add data processing services
        dps1 = cat.processing_services.add(dps1)
        dps2 = cat.processing_services.add(dps2)

        sn = Snapshot(name="My snapshot")
        sn.catalogs.add(cat)

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
        cat_loaded = sn_loaded.catalogs[cat.name]

        # Compare services
        dps1_loaded = cat_loaded.processing_services[dps1.hosted_service]
        dps2_loaded = cat_loaded.processing_services[dps2.hosted_service]
        assert dps1 == dps1_loaded
        assert dps2 == dps2_loaded

    def test_data_proc_service_galactica_validity_checks(self, caplog):
        """
        Tests data processing service Galactica validity checks

        Parameters
        ----------
        caplog: captured log PyTest fixture
        """
        pass


class TestCatalogFieldBinding(object):
    def test_catalog_field_binding_init(self):
        """
        Tests object catalog field binding instance initialisation
        """
        tobj = TargetObject(name="Spiral galaxy")
        x = tobj.object_properties.add(ObjectProperty(property_name="pos_x"))
        vals_x = N.random.uniform(size=20) * 3.0 + 10.0
        cf_x = CatalogField(obj_prop=x, values=vals_x)

        # Object catalog initialisation
        fbx = CatalogFieldBinding(catalog_field=cf_x, param_key="alpha", scale=2.0, offset=0.5)

        assert fbx.field_property_name == "pos_x"
        assert fbx.catalog_field is cf_x
        assert fbx.param_key == "alpha"
        assert  fbx.scale == 2.0
        assert fbx.offset == 0.5

        # Test str() conversion
        assert str(fbx) == "'pos_x' catalog field binding"

    def test_catalog_field_binding_catfield_setting_exc(self):
        """
        Tests setting a CatalogField into a CatalogFieldBinding object
        """
        # Tests CatalogFieldBinding defined without CatalogField
        with pytest.raises(AttributeError, match="Undefined 'catalog_field' attribute in CatalogFieldBinding."):
            catf_exc = CatalogFieldBinding(param_key="alpha")  # No catalog field defined

        # Tests invalid catalog_field initialisation exception
        invalid_catfield_err = "CatalogFieldBinding 'catalog_field' attribute is not a valid CatalogField instance."
        with pytest.raises(AttributeError, match=invalid_catfield_err):
            catf_exc = CatalogFieldBinding(catalog_field={2: "abcd"}, param_key="My catalog")  # Invalid catalog field
        with pytest.raises(AttributeError, match=invalid_catfield_err):
            catf_exc = CatalogFieldBinding(-5, param_key="My catalog")  # Invalid catalog field

        # Catalog field initialisation : valid => should not raise any exception
        tobj = TargetObject(name="Spiral galaxy")
        x = tobj.object_properties.add(ObjectProperty(property_name="pos_x"))
        vals_x = N.random.uniform(size=20) * 3.0 + 10.0
        cf_x = CatalogField(obj_prop=x, values=vals_x)

        fb1 = CatalogFieldBinding(catalog_field=cf_x, param_key="alpha")
        fb2 = CatalogFieldBinding(cf_x, param_key="alpha")

    def test_setting_catalog_field_binding_param_key_exc(self):
        """
        Tests that a catalog field binding defined without a param_key  raises an exception
        """
        tobj = TargetObject(name="Spiral galaxy")
        x = tobj.object_properties.add(ObjectProperty(property_name="pos_x"))
        vals_x = N.random.uniform(size=20) * 3.0 + 10.0
        cf_x = CatalogField(obj_prop=x, values=vals_x)

        # Tests catalog field binding defined without parameter key
        with pytest.raises(AttributeError, match="CatalogFieldBinding 'param_key' attribute is not defined \(mandatory\)."):
            fb1 = CatalogFieldBinding(catalog_field=cf_x)

        fb1 = CatalogFieldBinding(catalog_field=cf_x, param_key="alpha")
        # ------------------- Tests invalid catalog field binding param_key setting exception ----------------------- #
        empty_param_key_err = "CatalogFieldBinding 'param_key' property is not a valid \(non-empty\) string."
        with pytest.raises(AttributeError, match=empty_param_key_err):
            fb1.param_key = -1

        with pytest.raises(AttributeError, match=empty_param_key_err):
            fb1.param_key = ""

        # ----------------------------------------------------------------------------------------------------------- #

        # Valid => should not raise any exception
        fb1.name = "beta"

    def test_setting_catalog_field_binding_scale_offset_exc(self):
        """
        Tests that a catalog field binding defined with an invalid scale/offset value raises an exception
        """
        tobj = TargetObject(name="Spiral galaxy")
        x = tobj.object_properties.add(ObjectProperty(property_name="pos_x"))
        vals_x = N.random.uniform(size=20) * 3.0 + 10.0
        cf_x = CatalogField(obj_prop=x, values=vals_x)
        pkey = "alhpa"

        # ---------------- Tests catalog field binding defined with an invalid scale/offset value -------------------- #
        invalid_scale_num_value_err = "CatalogFieldBinding 'scale' attribute is not a valid numeric value."
        with pytest.raises(AttributeError, match=invalid_scale_num_value_err):
            fb1 = CatalogFieldBinding(catalog_field=cf_x, param_key=pkey, scale=(-4, "Planet", True))
        with pytest.raises(AttributeError, match=invalid_scale_num_value_err):
            fb1 = CatalogFieldBinding(catalog_field=cf_x, param_key=pkey, scale="Black hole")
        invalid_offset_num_value_err = "CatalogFieldBinding 'offset' attribute is not a valid numeric value."
        with pytest.raises(AttributeError, match=invalid_offset_num_value_err):
            fb1 = CatalogFieldBinding(catalog_field=cf_x, param_key=pkey, offset=("A", 1.256))
        with pytest.raises(AttributeError, match=invalid_offset_num_value_err):
            fb1 = CatalogFieldBinding(catalog_field=cf_x, param_key=pkey, offset="Galaxy")
        # ------------------------------------------------------------------------------------------------------------ #

        # Valid => should not raise any exception
        fb = CatalogFieldBinding(catalog_field=cf_x, param_key=pkey, scale=1.0e6, offset=-100.0)
        for valid_num_val in [0.52, -256.2, "1.0e3", "-45.2"]:
            fb.scale = valid_num_val
            fb.offset = valid_num_val

    def test_cat_field_binding_comparison(self):
        """
        Tests rich comparison method CatalogFieldBinding.__eq__()
        """
        tobj = TargetObject(name="Spiral galaxy")
        x = tobj.object_properties.add(ObjectProperty(property_name="pos_x"))
        vals_x = N.random.uniform(size=20) * 3.0 + 10.0
        cf_x = CatalogField(obj_prop=x, values=vals_x)
        cfb = CatalogFieldBinding(catalog_field=cf_x, param_key="xcenter", scale=4.0, offset=-1.0)

        # Different UUID => not equals
        assert cfb != CatalogFieldBinding(cf_x, param_key=cfb.param_key, scale=cfb.scale, offset=cfb.offset)

        # Different catalog field => not equals
        assert cfb != CatalogFieldBinding(CatalogField(obj_prop=x, values=vals_x*3.0), param_key=cfb.param_key,
                                          uid=cfb.uid, scale=cfb.scale, offset=cfb.offset)

        # Different service parameter key => not equals
        assert cfb != CatalogFieldBinding(cf_x, param_key="alpha", uid=cfb.uid, scale=cfb.scale, offset=cfb.offset)

        # Different scaling/offset num. values
        assert cfb != CatalogFieldBinding(cf_x, param_key=cfb.param_key, uid=cfb.uid, scale=cfb.scale, offset=1.5)
        assert cfb != CatalogFieldBinding(cf_x, param_key=cfb.param_key, uid=cfb.uid, scale=1.2, offset=cfb.offset)

        # Identical catalog field bindings
        cfb2 = CatalogFieldBinding(cf_x, param_key=cfb.param_key, uid=cfb.uid, scale=cfb.scale, offset=cfb.offset)
        assert cfb == cfb2

    def test_cat_field_binding_hdf5_io(self, tmp_path):
        """
        Tests saving/loading CatalogFieldBinding from HDF5 file

        Parameters
        ----------
        tmp_path: temporary path  PyTest fixture
        """
        dps1 = CatalogDataProcessingService(service_name="slice_map", data_host="my_cluster")

        tobj = TargetObject(name="Spiral galaxy")
        x = tobj.object_properties.add(ObjectProperty(property_name="pos_x"))
        vals_x = N.random.uniform(size=20) * 3.0 + 10.0
        cat = Catalog(target_object=tobj, name="Spiral galaxy catalog")
        cf_x = cat.catalog_fields.add(CatalogField(obj_prop=x, values=vals_x))

        # Add data processing service
        fbx = dps1.catalog_field_bindings.add(CatalogFieldBinding(catalog_field=cf_x, param_key="xcenter", scale=1.0e6,
                                                                  offset=-100.0))
        dps1 = cat.processing_services.add(dps1)

        sn = Snapshot(name="My snapshot")
        sn.catalogs.add(cat)

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
        cat_loaded = sn_loaded.catalogs[cat.name]
        dps1_loaded = cat_loaded.processing_services[dps1.hosted_service]

        # Compare catalog field bindings
        assert fbx == dps1_loaded.catalog_field_bindings[fbx.param_key]

    def test_cat_field_binding_galactica_validity_checks(self, caplog):
        """
        Tests catalog data processing service field binding Galactica validity checks

        Parameters
        ----------
        caplog: captured log PyTest fixture
        """
        dps1 = CatalogDataProcessingService(service_name="slice_map", data_host="my_cluster")

        tobj = TargetObject(name="Spiral galaxy")
        x = tobj.object_properties.add(ObjectProperty(property_name="pos_x", dtype=DataType.REAL))
        cl = tobj.object_properties.add(ObjectProperty(property_name="class", dtype=DataType.STRING))

        vals_x = N.random.uniform(size=20) * 3.0 + 10.0
        vals_cl = N.array(["A"]*20)
        cat = Catalog(target_object=tobj, name="Spiral galaxy catalog")
        cf_x = cat.catalog_fields.add(CatalogField(obj_prop=x, values=vals_x))

        # Set a catalog field binding on 'cf_x' catalog field associated with a 'long_serv_param_name' data processing
        # service parameter (name of the parameter is too long)
        fbx = dps1.catalog_field_bindings.add(CatalogFieldBinding(catalog_field=cf_x,
                                                                  param_key="long_serv_param_name"))
        # Add data processing service
        dps1 = cat.processing_services.add(dps1)

        # Check data-processing service parameter name length
        cat.galactica_validity_check()
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "Data processing service parameter key 'long_serv_param_name' is too long "
                                            "for Galactica (max. 16 characters).")

        # Check catalog field associated object property type (is it numerical ?)
        cf_cl = cat.catalog_fields.add(CatalogField(obj_prop=cl, values=vals_cl))
        # Set a catalog field binding on 'cf_cl' catalog field associated to a STRING datatyped object property
        # (not a numerical property)
        fb_cl = dps1.catalog_field_bindings.add(CatalogFieldBinding(catalog_field=cf_cl, param_key="alpha"))
        cat.galactica_validity_check()

        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "'class' catalog field binding is not a numerical type, it cannot be bound "
                                            "to a data processing service parameter.")


__all__ = ["TestCatalog", "TestCatalogDataProcessingService", ]
