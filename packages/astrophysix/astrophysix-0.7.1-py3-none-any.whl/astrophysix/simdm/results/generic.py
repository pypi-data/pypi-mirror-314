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
from future.builtins import str, list, int
import logging

from astrophysix.utils.persistency import Hdf5StudyPersistent
from astrophysix.utils.strings import Stringifiable
from ..datafiles import Datafile
from ..utils import ObjectList, GalacticaValidityCheckMixin
from ..catalogs import Catalog

log = logging.getLogger("astrophysix.simdm")


class GenericResult(Hdf5StudyPersistent, GalacticaValidityCheckMixin, Stringifiable):
    """
    Experiment generic result class

    Parameters
    ----------
    name: :obj:`string`
        result name (mandatory)
    description: :obj:`string`
        result description
    directory_path: :obj:`string`
        result data directory path
    """
    _hsp_version = 2  # with Catalogs
    def __init__(self, **kwargs):
        super(GenericResult, self).__init__(**kwargs)
        self._directory_path = ""
        self._name = ""
        self._description = ""
        self._datafiles = ObjectList(Datafile, "name")
        self._catalogs = ObjectList(Catalog, "name", object_addition_vcheck=(self._can_add_data_proc_service_in_catalog,
                                                                             "processing_services"))
        self._catalogs.add_validity_check_method(self._can_add_catalog)

        # Generic result name
        if "name" not in kwargs:
            raise AttributeError("{cname:s} 'name' attribute is not defined "
                                 "(mandatory).".format(cname=self.__class__.__name__))
        self.name = kwargs["name"]

        if "description" in kwargs:
            self.description = kwargs["description"]

        if "directory_path" in kwargs:
            self.directory_path = kwargs["directory_path"]

    def __eq__(self, other):
        """
        GenericResult comparison method

        other: :class:`~astrophysix.simdm.results.generic.GenericResult`
            generic result to compare to
        """
        if not super(GenericResult, self).__eq__(other):
            return False

        if self._name != other.name:
            return False

        if self._description != other.description:
            return False

        if self._directory_path != other.directory_path:
            return False

        #  Compare datafiles
        if self._datafiles != other.datafiles:
            return False

        # Compare object catalogs
        if self._catalogs != other.catalogs:
            return False

        return True

    @property
    def name(self):
        """Result name. Can be set to a non-empty :obj:`string` value."""
        return self._name

    @name.setter
    def name(self, new_res_name):
        try:
            self._name = Stringifiable.cast_string(new_res_name, valid_empty=False)
        except TypeError:
            err_msg = "{cname:s} 'name' property is not a valid (non-empty) string.".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

    @property
    def description(self):
        """Result description. Can be set to any :obj:`string` value."""
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
    def datafiles(self):
        """Result :class:`~astrophysix.simdm.datafiles.Datafile` list (:class:`~astrophysix.simdm.utils.ObjectList`)"""
        return self._datafiles

    @property
    def catalogs(self):
        """Result :class:`~astrophysix.simdm.catalogs.Catalog` list (:class:`~astrophysix.simdm.utils.ObjectList`)

        *New in version 0.5.0*"""
        return self._catalogs

    @property
    def directory_path(self):
        """Result directory.path. Can be set to any :obj:`string` value."""
        return self._directory_path

    @directory_path.setter
    def directory_path(self, new_path):
        try:
            self._directory_path = Stringifiable.cast_string(new_path)
        except TypeError:
            err_msg = "{cname:s} 'directory_path' property is not a valid string.".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

    def _can_add_catalog(self, new_cat):
        """
        Catalog addition validity check method. Verifies that the catalog added into this GenericResult is not lonked to
        any ata processing service. Otherwise raises an AttributeError.

        Parameters
        ----------
        new_cat: :class:`~astrophysix.simdm.catalogs.catalog.Catalog`
            new Catalog to add into the GenericResult
        """
        if len(new_cat.processing_services) > 0:
            err_msg = "Cannot add a {cat!s} with any data-processing service linked to it into a " \
                      "{cn:s}.".format(cat=new_cat, cn=self.__class__.__name__)
            log.error((err_msg))
            raise AttributeError(err_msg)

    def _can_add_data_proc_service_in_catalog(self, cat_data_proc_service):
        """
        CatalogDataProcessingService addition validity check method. Verifies that the added catalog data processing
        service is not added into a GenericResult's catalog. Otherwise raises an AttributeError.

        Parameters
        ----------
        cat_data_proc_service: :class:`~astrophysix.simdm.services.process.CatalogDataProcessingService`
            new catalog <=> data processing service to add into this Catalog.
        """
        err_msg = "Cannot add a data-processing service into a GenericResult's catalog."
        log.error((err_msg))
        raise AttributeError(err_msg)

    @classmethod
    def _hsp_valid_attributes(cls):
        """List of valid kwargs in __init__() method"""
        return ["name", "description", "directory_path"]

    def _hsp_write(self, h5group, **kwargs):
        """
        Serialize a GenericResult object into a HDF5 file.

        Parameters
        ----------
        h5group: ``h5py.Group``
            Main group to write the GenericResult into.
        kwargs: ``dict``
            keyword argument dictionary.
        """
        # Call to parent class _hsp_write() : write UUID, etc.
        super(GenericResult, self)._hsp_write(h5group, **kwargs)

        # Write result name
        self._hsp_write_attribute(h5group, ('name', self._name), **kwargs)

        # Write result directory path, if defined
        self._hsp_write_attribute(h5group, ('directory_path', self._directory_path), **kwargs)

        # Write result description, if defined
        self._hsp_write_attribute(h5group, ('description', self._description), **kwargs)

        # Write datafiles, if any defined
        self._hsp_write_object_list(h5group, "DATAFILES", self._datafiles, "datafile_", **kwargs)

        # Write products, if any defined
        self._hsp_write_object_list(h5group, "CATALOGS", self._catalogs, "catalog_", **kwargs)

        self._hsp_write_callback(str(self), **kwargs)

    @classmethod
    def _hsp_read(cls, h5group, version, dependency_objdict=None):
        """
        Read a GenericResult object from a HDF5 file (*.h5).

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
        res: ``GenericResult``
            Read GenericResult instance
        """
        # Handle different versions here

        # Fetch Hdf5StudyPersistent object UUID
        uid = super(GenericResult, cls)._hsp_read(h5group, version, dependency_objdict=dependency_objdict)

        # Read generic result name
        name = cls._hsp_read_attribute(h5group, 'name', "generic result name")

        # Create generic result object
        res = cls(uid=uid, name=name)

        # Read generic result description, if defined
        res_descr = cls._hsp_read_attribute(h5group, 'description', "generic result description",
                                            raise_error_if_not_found=False)
        if res_descr is not None:
            res.description = res_descr

        # Read generic result directory path, if defined
        res_dpath = cls._hsp_read_attribute(h5group, 'directory_path', "generic result directory path",
                                            raise_error_if_not_found=False)
        if res_dpath is not None:
            res.directory_path = res_dpath

        # Build datafile list and add each datafile into generic result
        if "DATAFILES" in h5group:
            for df in Datafile._hsp_read_object_list(h5group, "DATAFILES", "datafile_", "result datafile",
                                                     dependency_objdict=dependency_objdict):
                res.datafiles.add(df)

        # Read catalogs (version >= 2)
        if version >= 2:
            for cat in Catalog._hsp_read_object_list(h5group, "CATALOGS", "catalog_", "catalog",
                                                     dependency_objdict=dependency_objdict):
                res.catalogs.add(cat)

        return res

    def galactica_validity_check(self, **kwargs):
        """
        Perform validity checks on this instance and eventually log warning messages.

        Parameters
        ----------
        kwargs: :obj:`dict`
            keyword arguments (optional)
        """
        # Check generic result name length
        if len(self._name) > 64:
            log.warning("{r!s} name is too long for Galactica (max. 64 characters).".format(r=self))

        # Perform Galactica validity checks on datafile/catalog list
        self._datafiles.galactica_validity_check(**kwargs)

        # catalog list validity checks
        self._catalogs.galactica_validity_check(**kwargs)

    def __unicode__(self):
        """
        String representation of the instance
        """
        return "'{res_name:s}' generic result".format(res_name=self._name)


__all__ = ["GenericResult"]
