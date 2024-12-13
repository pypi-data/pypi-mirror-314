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

import uuid
import os
import shutil
import pandas as pd

from future.builtins import str
import logging

from astrophysix.utils.persistency import Hdf5StudyPersistent, Hdf5StudyFileMode
from astrophysix.utils.strings import Stringifiable
from .field import CatalogField
from .targobj import TargetObject
from ..datafiles import Datafile
from ..services import CatalogDataProcessingService
from ..utils import ObjectList, GalacticaValidityCheckMixin
from ...utils import FileUtil, FileType, DatetimeUtil, HDF5IOFile

log = logging.getLogger("astrophysix.simdm")


class Catalog(Hdf5StudyPersistent, HDF5IOFile, GalacticaValidityCheckMixin, Stringifiable):
    """
    Result object catalog class (Simulation data model)

    Parameters
    ----------
    target_object: :class:`~astrophysix.simdm.catalogs.targobj.TargetObject`
        catalog object type (mandatory)
    name: :obj:`string`
        catalog name (mandatory)
    description: :obj:`string`
        catalog description
    """
    _hsp_version = 2  # With data processing services
    def __init__(self, *args, **kwargs):
        super(Catalog, self).__init__(**kwargs)
        self._name = ""
        self._description = ""
        self._fields = ObjectList(CatalogField, "property_name")
        self._fields.add_validity_check_method(self._does_field_have_same_number_of_items)
        self._fields.add_validity_check_method(self._does_field_property_is_target_obj_prop)
        self._fields.add_deletion_handler(self._can_delete_catalog_field)
        self._datafiles = ObjectList(Datafile, "name")
        self._targobj = None
        self._proc_services = ObjectList(CatalogDataProcessingService, "hosted_service",
                                         object_addition_vcheck=(self._can_add_field_binding_in_proc_service,
                                                                 "catalog_field_bindings"))
        self._proc_services.add_validity_check_method(self._can_add_proc_service)

        # Object catalog name
        if "name" not in kwargs:
            raise AttributeError("{cname:s} 'name' attribute is not defined "
                                 "(mandatory).".format(cname=self.__class__.__name__))
        self.name = kwargs["name"]

        # ------------------------------------- Target object ------------------------------------- #
        if len(args) > 0:
            targobj = args[0]
        elif "target_object" in kwargs:
            targobj = kwargs["target_object"]
        else:
            raise AttributeError("Undefined target object for {cat!s}.".format(cat=self))

        if not isinstance(targobj, TargetObject):
            err_msg = "Catalog 'target_object' attribute is not a valid TargetObject instance."
            log.error(err_msg)
            raise AttributeError(err_msg)
        self._targobj = targobj

        # Add deletion handler to the target object's property list
        targobj.object_properties.add_deletion_handler(self._can_delete_object_property)
        # ----------------------------------------------------------------------------------------- #

        if "description" in kwargs:
            self.description = kwargs["description"]

    def __eq__(self, other):
        """
        Catalog comparison method

        other: :class:`~astrophysix.simdm.catalogs.catalog.Catalog`
            Other catalog instance to compare to
        """
        if not super(Catalog, self).__eq__(other):
            return False

        if self._name != other.name:
            return False

        # Compare target object
        if self._targobj != other.target_object:
            return False

        #  Compare datafiles
        if self._datafiles != other.datafiles:
            return False

        if self._description != other.description:
            return False

        # Compare catalog fields
        if self._fields != other.catalog_fields:
            return False

        # Compare data processing service list
        if self._proc_services != other.processing_services:
            return False

        return True

    @property
    def name(self):
        """Catalog name. can be edited"""
        return self._name

    @name.setter
    def name(self, new_cat_name):
        try:
            self._name = Stringifiable.cast_string(new_cat_name, valid_empty=False)
        except TypeError:
            err_msg = "{cname:s} 'name' property is not a valid (non-empty) string.".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

    @property
    def datafiles(self):
        """Catalog :class:`~astrophysix.simdm.datafiles.Datafile` list
        (:class:`~astrophysix.simdm.utils.ObjectList`)"""
        return self._datafiles

    @property
    def catalog_fields(self):
        """Catalog :class:`~astrophysix.simdm.catalogs.field.CatalogField` list
        (:class:`~astrophysix.simdm.utils.ObjectList`)"""
        return self._fields

    @property
    def nobjects(self):
        """Returns the total number of objects in this catalog"""
        if len(self._fields) == 0:
            return 0
        return self._fields[0].nobjects

    @property
    def target_object(self):
        """Catalog associated :class:`~astrophysix.simdm.catalogs.targobj.TargetObject`."""
        return self._targobj

    @property
    def description(self):
        """Catalog description"""
        return self._description

    @description.setter
    def description(self, new_descr):
        try:
            self._description = Stringifiable.cast_string(new_descr)
        except TypeError:
            err_msg = "{cname:s} 'description' property is not a valid string.".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

    @property
    def processing_services(self):
        """Catalog :class:`~astrophysix.simdm.catalogs.catalog.CatalogDataProcessingService` list
        (:class:`~astrophysix.simdm.utils.ObjectList`)"""
        return self._proc_services

    def _can_delete_object_property(self, obj_prop):
        """
        Checks if a target object property is not linked to any catalog field and can be safely deleted.
        Returns None if it can be deleted, otherwise returns a string.

        Parameters
        ----------
        obj_prop: ``:class:~astrophysix.simdm.catalogs.targobj.ObjectProperty``
            target object property about to be deleted

        Returns
        -------
        o: str or None
        """
        # Checks that a given ObjectProperty instance is not associated to any field of this catalog
        for f in self._fields:
            if f.object_property is obj_prop:  # Reference identity, not equality ??? Should work
                return "{s!s} {field!s}".format(s=self, field=f)
        return None

    def _can_delete_catalog_field(self, cat_field):
        """
        Checks if a catalog field is not bound to any catalog data processing service and can be safely deleted.
        Returns None if it can be deleted, otherwise returns a string.

        Parameters
        ----------
        cat_field: ``:class:~astrophysix.simdm.catalogs.field.CatalogField``
            catalog field about to be deleted

        Returns
        -------
        o: str or None
        """
        # Checks that a given CatalogField is not associated to any CatalogDataProcessingService in this catalog
        bound_fields = []
        for serv in self._proc_services:
            for field_binding in serv.catalog_field_bindings:
                if field_binding.catalog_field is cat_field:  # Reference identity, not equality ??? Should work
                    bound_fields.append("{bind!s}".format(bind=field_binding))

        if len(bound_fields) > 0:
            return bound_fields

        return None

    def _can_add_proc_service(self, process_service):
        """
        CatalogDataProcessingService addition validity check method. Verifies that the added data processing service
        contains only CatalogFieldBinding objects associated to a CatalogField currently listed in this catalog.
        Otherwise raises an AttributeError.

        Parameters
        ----------
        process_service: :class:`~astrophysix.simdm.services.process.CatalogDataProcessingService`
            new data processing service to bind to the Catalog
        """
        for field_binding in process_service.catalog_field_bindings:
            if field_binding.catalog_field not in self._fields:
                err_msg = "Cannot add catalog processing service. {f!s} is not a field of the " \
                          "{cat!s}.".format(f=field_binding.catalog_field, cat=self)
                log.error((err_msg))
                raise AttributeError(err_msg)

    def _can_add_field_binding_in_proc_service(self, field_binding):
        """
        CatalogFieldBinding addition validity check method. Verifies that the added catalog field binding is associated
        to a CatalogField that already belongs to this Catalog. Otherwise raises an AttributeError.

        Parameters
        ----------
        field_binding: :class:`~astrophysix.simdm.services.process.CatalogFieldBinding`
            new catalog field <=> data processing service binding to add to a data processing service within this
            Catalog.
        """
        if field_binding.catalog_field not in self._fields:
            err_msg = "Cannot add catalog field binding in this data processing service, {f!s} is not a " \
                      "field of the {cat!s}.".format(f=field_binding.catalog_field, cat=self)
            log.error((err_msg))
            raise AttributeError(err_msg)

    def _does_field_have_same_number_of_items(self, cat_field):
        """
        CatalogField addition validity check nethod. Verifies that the added field has the same number of items in it
        then other catalog fields, if there is any. Raises an AttributeError in case number of items differ.

        Parameters
        ----------
        cat_field: ``CatalogField``
            new catalog field to add to the Catalog
        """
        if self.nobjects == 0:  # No field yet in catalog
            return

        if cat_field.nobjects != self.nobjects:  # Number of catalog items differ => error
            err_msg = "Cannot add a catalog field with {n:d} item values in a catalog containing {cn:d} " \
                      "items.".format(n=cat_field.nobjects, cn=self.nobjects)
            log.error((err_msg))
            raise AttributeError(err_msg)

    def _does_field_property_is_target_obj_prop(self, cat_field):
        """
        CatalogField addition validity check method. Verifies that the added field property is one of the catalog's
        target object property. Otherwise raises an AttributeError.

        Parameters
        ----------
        cat_field: ``CatalogField``
            new catalog field to add to the Catalog
        """
        if cat_field.object_property not in self._targobj.object_properties:
            err_msg = "Cannot add catalog field. {p!s} is not a property of " \
                      "{tobj!s}.".format(tobj=self._targobj, p=cat_field.object_property)
            log.error((err_msg))
            raise AttributeError(err_msg)

    def to_pandas(self):
        """
        Convert a Catalog into a Pandas Dataframe object

        Returns
        -------
        df: pandas.DataFrame
            pandas DataFrame containing the catalog data
        """
        series_dict = {}
        for cat_field in self._fields:
            s = cat_field.to_pandas()
            series_dict[s.name] = s
        return pd.DataFrame(data=series_dict)

    def save_HDF5(self, catalog_fname=None, galactica_checks=False):
        """
        Save the Catalog into a HDF5 (\\*.h5) file

        *New in version 0.7.0*.

        Parameters
        ----------
        catalog_fname: :obj:`string`
            Catalog HDF5 filename.
        galactica_checks: :obj:`bool`
            Perform Galactica database validity checks and display warning in case of invalid content for upload on
            Galactica. Default False (quiet mode).
        """
        if catalog_fname is None:
            # No file path provided : should never happen
            err_msg = "No filename provided. Please provide a HDF5 filename to save the catalog."
            log.error(err_msg)
            raise AttributeError(err_msg)
        else:
            dest_catalog_h5fname = FileUtil.valid_filepath(catalog_fname, FileType.HDF5_FILE)

        # Move temporary file to the requested study HDF5 file path
        overwrite_catalog_file = False
        if os.path.exists(dest_catalog_h5fname):  # Delete first the already existing file
            while True:
                answer = input("File '{ch5f:s}' already exists. Overwrite? [Y/n] ".format(ch5f=dest_catalog_h5fname))
                if answer == "Y" or answer == "y":
                    overwrite_catalog_file = True
                    break
                else:
                    return

        # If Galactica database validity checks is enabled, perform a full check of the project before saving it.
        if galactica_checks:
            self.galactica_validity_check()

        # Save catalog into the temp. file
        temp_catalog_h5fname = FileUtil.new_temp_filepath("catalog")
        h5f, h5group, close_when_done = Hdf5StudyPersistent.open_h5file(temp_catalog_h5fname , mode=Hdf5StudyFileMode.NEW_WRITE)
        try:
            Hdf5StudyPersistent._hsp_write_object(h5group, "CATALOG", self, new_file=True, dry_run=False,
                                                  from_project=False)
            h5group.attrs["ObjectClass"] = "astrophysix.simdm.catalogs.Catalog"
            h5group.attrs["creation_time"] = DatetimeUtil.utc_to_timestamp(DatetimeUtil.utc_now())
        except Exception:
            raise
        finally:
            if close_when_done and h5f is not None:
                h5f.close()

        # Move temporary file to the requested study HDF5 file path
        if os.path.exists(dest_catalog_h5fname) and overwrite_catalog_file:  # Delete first the already existing file
            os.remove(dest_catalog_h5fname)
        shutil.copy(temp_catalog_h5fname, dest_catalog_h5fname)

    @classmethod
    def _hsp_valid_attributes(cls):
        """List of valid kwargs in __init__() method"""
        return ["name", "target_object",  "description"]

    def _hsp_write(self, h5group, **kwargs):
        """
        Serialize a Catalog object into a HDF5 file.

        Parameters
        ----------
        h5group: ``h5py.Group``
            Main group to write the Catalog into.
        kwargs: ``dict``
            keyword argument dictionary.
        """
        # Call to parent class _hsp_write() : write UUID, etc.
        super(Catalog, self)._hsp_write(h5group, **kwargs)

        # Write catalog name
        self._hsp_write_attribute(h5group, ('name', self._name), **kwargs)

        # Write catalog description, if defined
        self._hsp_write_attribute(h5group, ('description', self._description), **kwargs)

        # Write datafiles, if any defined
        self._hsp_write_object_list(h5group, "DATAFILES", self._datafiles, "datafile_", **kwargs)

        # Write target object
        if kwargs.get("from_project", False):  # Write target object UUID
            self._hsp_write_attribute(h5group, ('targob_uid', self._targobj.uid), **kwargs)
        else:  # Write complete target object description (full serialization)
            self._hsp_write_object(h5group, "TARGET_OBJECT", self._targobj, **kwargs)

        # Write catalog fields, if any defined
        self._hsp_write_object_list(h5group, "CATALOG_FIELDS", self._fields, "cat_field_", **kwargs)

        # Once catalog fields have been written, then write data processing services (and eventually their bindings to
        # catalog fields) bound to this catalog, if any defined.
        self._hsp_write_object_list(h5group, "PROC_SERVICES", self._proc_services, "proc_serv_", **kwargs)

        self._hsp_write_callback(str(self), **kwargs)

    @classmethod
    def load_HDF5(cls, catalog_file_path):
        """
        Loads Catalog from a HDF5 (\\*.h5) file

        *New in version 0.7.0*.

        Parameters
        ----------
        catalog_file_path: :obj:`string`
            Catalog HDF5 (existing) file path

        Returns
        -------
        study: :class:`~astrophysix.simdm.catalogs.catalog.Catalog`
            Catalog loaded from HDF5 file.
        """
        if not os.path.isfile(catalog_file_path):
            raise AttributeError("Cannot find file '{fname:s}'".format(fname=catalog_file_path))

        temp_loaded_file = FileUtil.new_temp_filepath("catalog")
        shutil.copy(catalog_file_path, temp_loaded_file)
        h5f, h5group, close_when_done = Hdf5StudyPersistent.open_h5file(temp_loaded_file,
                                                                        mode=Hdf5StudyFileMode.READ_ONLY)
        try:
            # Check that we are actually reading a Catalog object from a HDF5 file
            if "ObjectClass" not in h5group.attrs or h5group.attrs["ObjectClass"] != "astrophysix.simdm.catalogs.Catalog":
                err_msg = "HDF5 file does not contain a catalog !"
                log.error(err_msg)
                raise IOError(err_msg)

            # Read catalog creation/last modification times
            if "creation_time" not in h5group.attrs:
                err_msg = "Cannot find study creation time attributes in " \
                          "'{path!s}'.".format(path=h5group.name)
                log.error(err_msg)
                raise IOError(err_msg)

            if "CATALOG" not in h5group:
                err_msg = "Missing '/CATALOG' group in HDF5 catalog file."
                log.error(err_msg)
                raise IOError(err_msg)
            catalog_group = h5group["CATALOG"]
            cat = cls.hsp_load_from_h5(catalog_group, dependency_objdict={})
            cat._created = DatetimeUtil.utc_from_timestamp(h5group.attrs["creation_time"])
        except Exception:
            raise
        finally:
            if close_when_done and h5f is not None:
                h5f.close()

        return cat

    @classmethod
    def _hsp_read(cls, h5group, version, dependency_objdict=None):
        """
        Read a Catalog object from a HDF5 file (*.h5).

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
        catalog: ``Catalog``
            Read Catalog instance
        """
        # Handle different versions here

        # Fetch Hdf5StudyPersistent object UUID
        uid = super(Catalog, cls)._hsp_read(h5group, version, dependency_objdict=dependency_objdict)

        # Try to read/find protocol
        try:
            targobj_uid = uuid.UUID(cls._hsp_read_attribute(h5group, "targob_uid", "target object UUID",
                                                            raise_error_if_not_found=True))

            # Search for already instantiated target object in dependency object dictionary
            if dependency_objdict is None:
                err_msg = "Cannot find any target object already instantiated in the project."
                log.error(err_msg)
                raise IOError(err_msg)

            # Get dictionary of target object instances of the corresponding class :
            if TargetObject.__name__ not in dependency_objdict:
                err_msg = "Cannot find any {cname:s} instance.".format(cname=TargetObject.__name__)
                log.error(err_msg)
                raise IOError(err_msg)

            # Find target object according to its UUID
            tobj_dict = dependency_objdict[TargetObject.__name__]
            if targobj_uid not in tobj_dict:
                err_msg = "Cannot find {cname:s} instance with uid {uid:s}.".format(cname=TargetObject.__name__,
                                                                                    uid=str(uid))
                log.error(err_msg)
                raise IOError(err_msg)

            tobj = tobj_dict[targobj_uid]
        except IOError:  # Target Object UUID not found in Catalog
            # Read target object info from "TARGET_OBJECT" subgroup
            tobj = TargetObject._hsp_read_object(h5group, "TARGET_OBJECT", "catalog target object",
                                                 dependency_objdict=dependency_objdict)

        # Read catalog name
        name = cls._hsp_read_attribute(h5group, 'name', "generic result name")

        # Create catalog object
        catalog = cls(uid=uid, target_object=tobj, name=name)

        # Build datafile list and add each datafile into catalog
        for df in Datafile._hsp_read_object_list(h5group, "DATAFILES", "datafile_", "catalog datafile",
                                                 dependency_objdict=dependency_objdict):
            catalog.datafiles.add(df)

        # Build catalog field list and add each field into catalog + build catalog field dictionary indexed by their
        # UUID
        if CatalogField.__name__ not in dependency_objdict:
            dependency_objdict[CatalogField.__name__] = {}
        cat_field_dict = dependency_objdict[CatalogField.__name__]
        for field in CatalogField._hsp_read_object_list(h5group, "CATALOG_FIELDS", "cat_field_", "catalog field",
                                                        dependency_objdict=dependency_objdict):
            catalog.catalog_fields.add(field)
            cat_field_dict[field.uid] = field

        # Read catalog description, if defined
        cat_descr = cls._hsp_read_attribute(h5group, 'description', "catalog description",
                                            raise_error_if_not_found=False)
        if cat_descr is not None:
            catalog.description = cat_descr

        # Read data processing services, if any defined
        if version >= 2 and "PROC_SERVICES" in h5group:
            for dps in CatalogDataProcessingService._hsp_read_object_list(h5group, "PROC_SERVICES", "proc_serv_",
                                                                          "catalog data processing service",
                                                                          dependency_objdict=dependency_objdict):
                catalog.processing_services.add(dps)

        return catalog

    def galactica_validity_check(self, **kwargs):
        """
        Perform validity checks on this  instance and eventually log warning messages.

        Parameters
        ----------
        kwargs: :obj:`dict`
            keyword arguments (optional)
        """
        # Check target object name
        if len(self._name) > 64:
            log.warning("{c!s} name is too long for Galactica (max. 64 characters).".format(c=self))

        # Check that the catalog contain some object
        if self.nobjects == 0:
            log.warning("{c!s} does not contain any object.".format(c=self))

        # Check catalog field and datafile list validity
        self._fields.galactica_validity_check(**kwargs)
        self._datafiles.galactica_validity_check(**kwargs)

        # Check data processing service list validity
        self._proc_services.galactica_validity_check(**kwargs)

    def __unicode__(self):
        """
        String representation of the instance
        """
        return "'{cat_name:s}' catalog".format(cat_name=self._name)


__all__ = ["Catalog"]
