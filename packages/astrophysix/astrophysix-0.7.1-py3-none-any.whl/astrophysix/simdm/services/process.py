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
from __future__ import absolute_import, unicode_literals
import uuid
from future.builtins import str, list, dict
import logging

from astrophysix.simdm.catalogs import CatalogField
from astrophysix.simdm.utils import GalacticaValidityCheckMixin, ObjectList, DataType
from astrophysix.utils.persistency import Hdf5StudyPersistent
from astrophysix.utils.strings import Stringifiable

log = logging.getLogger("astrophysix.simdm")


class DataProcessingService(Hdf5StudyPersistent, GalacticaValidityCheckMixin, Stringifiable):
    """
    Data processing service description defining a service name and a data host server name. Use it to bind
    a Snapshot to a specific data-processing service on Galactica.

    Parameters
    ----------
    service_name: :obj:`string`
        data processing service name (mandatory)
    data_host: :obj:`string`
        data host server name name (mandatory)

    Example
    -------

        >>> # To bind a given simulation snapshot to a data-processing service :
        >>> sn = Snapshot(name="Third pericenter", time=(254.7, U.Myr),
        ...               data_reference="output_00034")
        >>> serv = DataProcessingService(service_name="ray_tracer_amr",
        ...                              data_host="my_institute_cluster")
        >>> sn.processing_services.add(serv)

    """
    def __init__(self, **kwargs):
        super(DataProcessingService, self).__init__(**kwargs)

        self._service_name = ""
        self._data_host = ""

        if "service_name" not in kwargs:
            raise AttributeError("Data processing service 'service_name' attribute is not defined (mandatory).")
        self.service_name = kwargs["service_name"]

        if "data_host" not in kwargs:
            raise AttributeError("Data processing service 'data_host' attribute is not defined (mandatory).")
        self.data_host = kwargs["data_host"]

    def __eq__(self, other):
        """
        DataProcessingService comparison method

        other: :class:`~astrophysix.simdm.services.DataProcessingService`
            Data processing service to compare to
        """
        if not super(DataProcessingService, self).__eq__(other):
            return False

        if self._service_name != other.service_name:
            return False

        if self._data_host != other.data_host:
            return False

        return True

    @property
    def service_name(self):
        """Data processing service name"""
        return self._service_name

    @service_name.setter
    def service_name(self, new_service_name):
        try:
            self._service_name = Stringifiable.cast_string(new_service_name, valid_empty=False)
        except TypeError:
            raise AttributeError("Data processing service 'service_name' property is not a valid (non empty) string.")

    @property
    def data_host(self):
        """Data processing service host server name"""
        return self._data_host

    @data_host.setter
    def data_host(self, new_host):
        try:
            self._data_host = Stringifiable.cast_string(new_host, valid_empty=False)
        except TypeError:
            raise AttributeError("Data processing service 'data_host' property is not a valid (non empty) string.")

    @property
    def hosted_service(self):
        """Data processing service full description *service_name @ data_host*"""
        return "{sn:s} @ {hn:s}".format(sn=self._service_name, hn=self._data_host)

    @classmethod
    def _hsp_valid_attributes(cls):
        """List of valid kwargs in __init__() method"""
        return ["service_name", "data_host"]

    def _hsp_write(self, h5group, **kwargs):
        """
        Serialize an DataProcessingService object into a HDF5 file.

        Parameters
        ----------
        h5group: ``h5py.Group``
            Main group to write the DataProcessingService into.
        kwargs: ``dict``
            keyword argument dictionary.
        """
        # Call to parent class _hsp_write() : write UUID, etc.
        super(DataProcessingService, self)._hsp_write(h5group, **kwargs)

        # Write data processing service name
        self._hsp_write_attribute(h5group, ('service_name', self._service_name), **kwargs)

        # Write data processing host server name
        self._hsp_write_attribute(h5group, ('data_host', self._data_host), **kwargs)

    @classmethod
    def _hsp_read(cls, h5group, version, dependency_objdict=None):
        """
        Read an DataProcessingService object from a HDF5 file (*.h5).

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
        serv: ``DataProcessingService``
            Read DataProcessingService instance
        """
        # Handle different versions here

        # Fetch Hdf5StudyPersistent object UUID
        uid = super(DataProcessingService, cls)._hsp_read(h5group, version, dependency_objdict=dependency_objdict)

        # Read data processing service name
        serv_name = cls._hsp_read_attribute(h5group, 'service_name', "data processing service name")

        # Read data processing host server name
        host_name = cls._hsp_read_attribute(h5group, 'data_host', "data processing host server name")

        # Create data processing service object
        serv = cls(service_name=serv_name, data_host=host_name, uid=uid)

        return serv

    def galactica_validity_check(self, **kwargs):
        """
        Perform validity checks on this instance and eventually log warning messages.

        Parameters
        ----------
        kwargs: :obj:`dict`
            keyword arguments (optional)
        """
        # Check data host + service name lengths
        if len(self._data_host) > 16:
            log.warning("Data processing service host name '{h:s}' is too long for Galactica (max. 16 "
                        "characters).".format(h=self._data_host))
        if len(self._service_name) > 32:
            log.warning("Data processing service name '{s:s}' is too long for Galactica (max. 32 "
                        "characters).".format(s=self._service_name))

    def __unicode__(self):
        """
        String representation of the instance
        """
        return "'{sn:s}' data processing service (host: {hn:s})".format(sn=self._service_name, hn=self._data_host)


class CatalogFieldBinding(Hdf5StudyPersistent, GalacticaValidityCheckMixin, Stringifiable):
    """
    Service input parameter - catalog field value binding for (catalog-bound) data processing services. The applied
    scaling formula is : :math:`\\textrm{param_value} = \\textrm{scale} \\times \\textrm{field_value} + \\textrm{offset}`.

    Parameters
    ----------
    catalog_field: :class:`~astrophysix.simdm.catalogs.field.CatalogField`
        bound catalog field (mandatory)
    param_key: :obj:`string`
        data processing service input parameter key (mandatory)
    scale: :obj:`float`
        field value to service parameter scaling factor. Default 1.0
    offset: : obj:`float`
        field value to service parameter offset value. Default 0.0

    Example
    -------

        >>> # Define a catalog
        >>> cat = Catalog(target_object=gal_cluster, name="Galaxy cluster catalog")
        >>> # Add the catalog fields into the catalog (100 clusters)
        >>> fx = cat.catalog_fields.add(CatalogField(x, values=N.random.uniform(size=100)))
        >>> fy = cat.catalog_fields.add(CatalogField(y, values=N.random.uniform(size=100)))
        >>> fz = cat.catalog_fields.add(CatalogField(z, values=N.random.uniform(size=100)))
        >>> fm = cat.catalog_fields.add(CatalogField(m, values=N.random.uniform(size=100)))
        >>> # To bind a given object catalog to a data-processing service :
        >>> cat_dps = CatalogDataProcessingService(service_name="slice_map",
        ...                                     data_host="Lab_Cluster")
        >>> cat.processing_services.add(cat_dps)
        >>>
        >>> # Define catalog field bindings to automatically fill the data processing service
        >>> # parameter value 'pv' with a catalog field value 'fv' of one of your catalog's object
        >>> # according to the formula : pv = scale * fv + offset.
        >>> fbx = CatalogFieldBinding(catalog_field=fx, param_key="x", scale=1.0e2, offset=-50.0))
        >>> fby = CatalogFieldBinding(catalog_field=fy, param_key="y", scale=1.0e2, offset=-50.0))
        >>> fbz = CatalogFieldBinding(catalog_field=fz, param_key="z", scale=1.0e2, offset=-50.0))
        >>> cat_dps.catalog_field_bindings.add(fbx)
        >>> cat_dps.catalog_field_bindings.add(fby)
        >>> cat_dps.catalog_field_bindings.add(fbz)

    """
    def __init__(self, *args, **kwargs):
        super(CatalogFieldBinding, self).__init__(**kwargs)

        self._param_key = ""

        # Bound catalog field
        self._bound_field = None
        if len(args) > 0:
            cat_field = args[0]
        elif "catalog_field" in kwargs:
            cat_field = kwargs["catalog_field"]
        else:
            raise AttributeError("Undefined 'catalog_field' attribute in "
                                 "{cname:s}.".format(cname=self.__class__.__name__))

        if not isinstance(cat_field, CatalogField):
            err_msg = "{cname:s} 'catalog_field' attribute is not a valid CatalogField " \
                      "instance.".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)
        self._bound_field = cat_field

        # Service parameter key
        if "param_key" not in kwargs:
            raise AttributeError("{cname:s} 'param_key' attribute is not defined "
                                 "(mandatory).".format(cname=self.__class__.__name__))
        self.param_key = kwargs["param_key"]

        # Init scale/factor
        self._scale_factor = 1.0
        if "scale" in kwargs:
            self.scale = kwargs["scale"]
        self._offset = 0.0
        if "offset" in kwargs:
            self.offset = kwargs["offset"]

    def __eq__(self, other):
        """
        CatalogDataProcessingService comparison method

        other: :class:`~astrophysix.simdm.services.process.CatalogFieldBinding`
            catalog field binding to compare to
        """
        if not super(CatalogFieldBinding, self).__eq__(other):
            return False

        # Compare service parameter keys
        if self._param_key != other.param_key:
            return False

        # Compare catalog fields
        if self._bound_field != other.catalog_field:
            return False

        # Compare scale/offset
        if self._scale_factor != other.scale or self._offset != other.offset:
            return False

        return True

    @property
    def field_property_name(self):
        """Associated catalog field's target object property name. Cannot be edited"""
        return self._bound_field.property_name

    @property
    def catalog_field(self):
        """Associated catalog field (:class:`~astrophysix.simdm.catalogs.field.CatalogField`). Cannot be edited."""
        return self._bound_field

    @property
    def param_key(self):
        """Data processing service parameter key. Can be edited."""
        return self._param_key

    @param_key.setter
    def param_key(self, new_param_key):
        try:
            self._param_key = Stringifiable.cast_string(new_param_key, valid_empty=False)
        except TypeError:
            err_msg = "{cname:s} 'param_key' property is not a valid (non-empty) " \
                      "string.".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

    @property
    def scale(self):
        """
        Returns the scaling factor to apply between the catalog field value and input value provided to the
        data-processing service parameter value. Can be edited.
        """
        return self._scale_factor

    @scale.setter
    def scale(self, new_scale):
        try:
            self._scale_factor = float(new_scale)
        except (ValueError, TypeError):  # Not a numeric/string value that can be casted into a real number
            raise AttributeError("{cn:s} 'scale' attribute is not a valid numeric "
                                 "value.".format(cn=self.__class__.__name__))

    @property
    def offset(self):
        """
        Returns the offset to apply between the catalog field value and input value provided to the data-processing
        service parameter value. Can be edited.
        """
        return self._offset

    @offset.setter
    def offset(self, new_offset):
        try:
            self._offset = float(new_offset)
        except (ValueError, TypeError):  # Not a numeric/string value that can be casted into a real number
            raise AttributeError("{cn:s} 'offset' attribute is not a valid numeric "
                                 "value.".format(cn=self.__class__.__name__))

    @classmethod
    def _hsp_valid_attributes(cls):
        """List of valid kwargs in __init__() method"""
        return ["catalog_field", "param_key", "scale", "offset"]

    def _hsp_write(self, h5group, **kwargs):
        """
        Serialize an CatalogFieldBinding object into a HDF5 file.

        Parameters
        ----------
        h5group: ``h5py.Group``
            Main group to write the CatalogFieldBinding into.
        kwargs: ``dict``
            keyword argument dictionary.
        """
        # Call to parent class _hsp_write() : write UUID, etc.
        super(CatalogFieldBinding, self)._hsp_write(h5group, **kwargs)

        # Write catalog field UUID
        self._hsp_write_attribute(h5group, ('cat_field_uid', self._bound_field.uid), **kwargs)

        # Write data processing service parameter key
        self._hsp_write_attribute(h5group, ('serv_param_key', self._param_key), **kwargs)

        # Write scale/offset parameters
        self._hsp_write_attribute(h5group, ('scale_fact', self._scale_factor), **kwargs)
        self._hsp_write_attribute(h5group, ('offset', self._offset), **kwargs)

    @classmethod
    def _hsp_read(cls, h5group, version, dependency_objdict=None):
        """
        Read an CatalogFieldBinding object from a HDF5 file (*.h5).

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
        serv: ``CatalogFieldBinding``
            Read CatalogFieldBinding instance
        """
        # Handle different versions here

        # Read catalog field binding
        uid = super(CatalogFieldBinding, cls)._hsp_read(h5group, version, dependency_objdict=dependency_objdict)

        # Read data processing service parameter key
        param_key = cls._hsp_read_attribute(h5group, 'serv_param_key', "service parameter key")

        # Try to read/find protocol
        try:
            cat_field_uid = uuid.UUID(cls._hsp_read_attribute(h5group, "cat_field_uid", "catalog field UUID",
                                                              raise_error_if_not_found=True))

            # Search for already instantiated catalog field in dependency object dictionary
            if dependency_objdict is None:
                err_msg = "Cannot find any catalog field object already instantiated in the project."
                log.error(err_msg)
                raise IOError(err_msg)

            # Get dictionary of catalog field instances of the corresponding class :
            if CatalogField.__name__ not in dependency_objdict:
                err_msg = "Cannot find any {cname:s} instance.".format(cname=CatalogField.__name__)
                log.error(err_msg)
                raise IOError(err_msg)

            # Find catalog field according to its UUID
            catfield_dict = dependency_objdict[CatalogField.__name__]
            if cat_field_uid not in catfield_dict:
                err_msg = "Cannot find {cname:s} instance with uid {uid:s}.".format(cname=CatalogField.__name__,
                                                                                    uid=str(uid))
                log.error(err_msg)
                raise IOError(err_msg)

            cfield = catfield_dict[cat_field_uid]
        except IOError:  # Catalog field UUID not found in CatalogFieldBinding
            raise

        binding = cls(uid=uid, param_key=param_key, catalog_field=cfield)

        # Read scale/offset attributes
        binding.scale = cls._hsp_read_attribute(h5group, 'scale_fact', "binding scaling factor")
        binding.offset = cls._hsp_read_attribute(h5group, 'offset', "binding offset")

        return binding

    def galactica_validity_check(self, **kwargs):
        """
        Perform validity checks on this instance and eventually log warning messages.

        Parameters
        ----------
        kwargs: :obj:`dict`
            keyword arguments (optional)
        """
        # Check data-processing service parameter name length
        if len(self._param_key) > 16:
            log.warning("Data processing service parameter key '{p:s}' is too long for Galactica (max. 16 "
                        "characters).".format(p=self._param_key))

        # Check target object property type is numerical
        if self._bound_field.object_property.datatype not in [DataType.REAL, DataType.INTEGER]:
            log.warning("{cfb!s} is not a numerical type, it cannot be bound to a data processing service "
                        "parameter.".format(cfb=self))

    def __unicode__(self):
        """
        String representation of the instance
        """
        return "'{fn:s}' catalog field binding".format(fn=self.field_property_name)


class CatalogDataProcessingService(DataProcessingService):
    """
    Catalog item-bound data-processing service defining a service name and a data host server name. Use it to bind
    a Catalog to a specific data-processing service on Galactica.

    Parameters
    ----------
    service_name: :obj:`string`
        data processing service name (mandatory)
    data_host: :obj:`string`
        data host server name (mandatory)

    Example
    -------

        >>> # Define a catalog
        >>> cat = Catalog(target_object=gal_cluster, name="Galaxy cluster catalog")
        >>>
        >>> # To bind a given object catalog to a data-processing service :
        >>> cat_dps = CatalogDataProcessingService(service_name="slice_map",
        ...                                        data_host="Lab_Cluster")
        >>> cat.processing_services.add(cat_dps)
    """
    def __init__(self, **kwargs):
        super(CatalogDataProcessingService, self).__init__(**kwargs)
        self._cat_field_bindings = ObjectList(CatalogFieldBinding, "param_key")

    def __eq__(self, other):
        """
        CatalogDataProcessingService comparison method

        other: :class:`~astrophysix.simdm.services.CatalogDataProcessingService`
            Data processing service to compare to
        """
        if not super(CatalogDataProcessingService, self).__eq__(other):
            return False

        if self._cat_field_bindings != other.catalog_field_bindings:
            return False

        return True

    @property
    def catalog_field_bindings(self):
        """Catalog data processing service list of catalog field bindings"""
        return self._cat_field_bindings

    def _hsp_write(self, h5group, **kwargs):
        """
        Serialize an CatalogDataProcessingService object into a HDF5 file.

        Parameters
        ----------
        h5group: ``h5py.Group``
            Main group to write the CatalogDataProcessingService into.
        kwargs: ``dict``
            keyword argument dictionary.
        """
        # Call to parent class _hsp_write() : write UUID, data host, service name, etc.
        super(CatalogDataProcessingService, self)._hsp_write(h5group, **kwargs)

        # Write catalog field bindings, if any defined
        self._hsp_write_object_list(h5group, "CAT_FIELD_BINDINGS", self._cat_field_bindings, "catfbind_", **kwargs)

    @classmethod
    def _hsp_read(cls, h5group, version, dependency_objdict=None):
        """
        Read an CatalogDataProcessingService object from a HDF5 file (*.h5).

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
        serv: ``CatalogDataProcessingService``
            Read CatalogDataProcessingService instance
        """
        # Handle different versions here

        # Read data processing service
        service = super(CatalogDataProcessingService, cls)._hsp_read(h5group, version,
                                                                     dependency_objdict=dependency_objdict)

        # Build catalog field binding list and add each catalog field binding into service, if any defined
        if "CAT_FIELD_BINDINGS" in h5group:
            for cfb in CatalogFieldBinding._hsp_read_object_list(h5group, "CAT_FIELD_BINDINGS", "catfbind_",
                                                                 "catalog field binding",
                                                                 dependency_objdict=dependency_objdict):
                service.catalog_field_bindings.add(cfb)

        return service

    def galactica_validity_check(self, **kwargs):
        """
        Perform validity checks on this  instance and eventually log warning messages.

        Parameters
        ----------
        kwargs: :obj:`dict`
            keyword arguments (optional)
        """
        super(CatalogDataProcessingService, self).galactica_validity_check(**kwargs)

        # Check catalog field bind list validity
        self._cat_field_bindings.galactica_validity_check(**kwargs)

    def __unicode__(self):
        """
        String representation of the instance
        """
        return "'{sn:s}' catalog-bound data processing service (host: {hn:s})".format(sn=self.service_name,
                                                                                      hn=self.data_host)


__all__ = ["DataProcessingService", "CatalogDataProcessingService", "CatalogFieldBinding"]
