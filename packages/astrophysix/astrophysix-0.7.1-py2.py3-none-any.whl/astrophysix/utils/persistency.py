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
import numpy as N
from enum import Enum
import uuid
import sys
import logging

from .file import FileType, FileUtil
from .strings import Stringifiable
from astrophysix import units as U

try:
    import h5py
    _h5py_available = True
except ImportError as imperr:
    _h5py_available = False

try:
    from PIL import Image
    _Pillow_available = True
except ImportError:
    _Pillow_available = False


log = logging.getLogger("astrophysix")


class Hdf5StudyFileMode(Enum):
    NEW_WRITE = 1
    READ_ONLY = 2
    APPEND = 3


class Hdf5StudyPersistent(object):
    _hsp_version = 1
    __fact_subclasses_dict = {}

    def __init__(self, uid=None, lazy_persistant=False, **kwargs):
        super(Hdf5StudyPersistent, self).__init__()
        self._lazy_h5group_name = None
        self._lazy_h5file_path = None
        self._is_lazy_read = not lazy_persistant

        # Persistent object UUID
        if uid is None:
            self.__uid = uuid.uuid4()
        else:
            if not isinstance(uid, uuid.UUID):
                err_msg = "'uid' attribute is not a valid UUID."
                log.error(err_msg)
                raise AttributeError(err_msg)
            self.__uid = uid

        # Check valid kwargs attributes
        valid_attrs = self._hsp_valid_attributes()
        for key in kwargs:
            if key not in valid_attrs:
                log.warning("'{k:s}' attribute is unknown for a '{kln:s}' object. It "
                            "is therefore ignored.".format(k=key, kln=self.__class__.__name__))

    @classmethod
    def _hsp_valid_attributes(cls):
        """List of valid kwargs in __init__() method"""
        raise NotImplementedError()

    def __eq__(self, other):
        """Basic instance comparison : test class equality + identical UUID"""
        if self.__class__ != other.__class__:
            return False

        return self.__uid == other.uid

    def __ne__(self, other):
        """
        Not an implied relationship between "rich comparison" equality methods in Python 2.X but only in Python 3.X
        see https://docs.python.org/2.7/reference/datamodel.html#object.__ne__

        other: other instance to compare to
        """
        # --------------------------------------------- Python 2 ----------------------------------------------------- #
        #  There are no implied relationships among the comparison operators. The truth of x==y does not imply that
        #  x!=y is false. Accordingly, when defining __eq__(), one should also define __ne__() so that the operators
        #  will behave as expected.
        # --------------------------------------------- Python 3 ----------------------------------------------------- #
        # By default, __ne__() delegates to __eq__() and inverts the result unless it is NotImplemented. There are no
        # other implied relationships among the comparison operators, for example, the truth of (x<y or x==y) does not
        # imply x<=y.
        # ------------------------------------------------------------------------------------------------------------ #
        return not self.__eq__(other)

    @property
    def uid(self):
        return self.__uid

    def _hsp_lazy_read_data(self, h5group):
        pass

    def _hsp_set_lazy_read(self):
        self._is_lazy_read = True

    def _hsp_lazy_read(self):
        if not self._is_lazy_read:
            h5f, h5group, close_when_done = self.open_h5file(self._lazy_h5file_path, where=self._lazy_h5group_name)
            try:
                self._hsp_lazy_read_data(h5group)
                self._hsp_set_lazy_read()
            except:
                pass
            finally:
                h5f.close()

    def _hsp_set_lazy_source(self, h5group):
        self._lazy_h5group_name = h5group.name
        self._lazy_h5file_path = h5group.file.filename
        self._is_lazy_read = False

    @staticmethod
    def open_h5file(hsf, where="/", mode=Hdf5StudyFileMode.READ_ONLY):
        """
        Returns a HDF5 h5py.File object and a h5py.Group object

        Parameters
        ----------
        hsf: ``str`` or ``h5py.File``
            HDF5 (h5py) File object or filename
        where: ``string``
            location of the object in the HDF5 tree. Default "/"
        mode: ``Hdf5StudyFileMode``
            File mode. Default Hdf5StudyFileMode.READ_ONLY

        Returns
        -------
        f: ``h5py.File``
            HDF5 file object.
        g: ``h5py.Group``
            HDF5 group object.

        Raises
        ------
        imperr: ``ImportError``
            raises an ImportError if the 'h5py'  module is not found.
        atterr: ``AttributeError``
            raises an AttributeError if any attribute is not valid.
        """
        if not _h5py_available:
            err_msg = "h5py (>= 2.9)  module is required to read/write HDF5 files !"
            log.error(err_msg)
            raise ImportError(err_msg)

        # Check the 'where' kwarg is a valid string.
        if not Stringifiable.is_type_string(where):
            err_msg = "'where' attribute must be a string. Got '{wtype!s}'".format(wtype=type(where))
            log.error(err_msg)
            raise AttributeError(err_msg)

        if Stringifiable.is_type_string(hsf):
            if mode == Hdf5StudyFileMode.NEW_WRITE:  # Create new file
                f = h5py.File(FileUtil.new_filepath(hsf, FileType.HDF5_FILE), 'w')
            else:  # Read (and maybe edit) existing file
                hsf_path = FileUtil.locate_file(hsf)
                if mode == Hdf5StudyFileMode.APPEND:
                    f = h5py.File(FileUtil.valid_filepath(hsf_path, FileType.HDF5_FILE), 'r+')
                else:  # mode == Hdf5StudyFileMode.READ_ONLY =>  Read an existing HDF5 study persistent file
                    f = h5py.File(FileUtil.valid_filepath(hsf_path, FileType.HDF5_FILE), 'r')

            close_when_done = True
        elif isinstance(hsf, h5py.File):
            f = hsf
            close_when_done = False
        else:
            err_msg = "'hsf' must be a HDF5 file path or a valid h5py.File object. Got " \
                      "'{wtype!s}'".format(wtype=type(hsf))
            log.error(err_msg)
            raise AttributeError(err_msg)

        # Get base Group
        group = f[where]

        return f, group, close_when_done

    @classmethod
    def _hsp_version_write(cls, h5group):
        h5group.attrs["_hsp_version_"] = cls._hsp_version

    @classmethod
    def _hsp_version_read(cls, h5group):
        if "_hsp_version_" not in h5group.attrs:
            err_msg = "Cannot find object version in '{gname:s}'.".format(gname=h5group.name)
            log.error(err_msg)
            raise IOError(err_msg)
        vers = h5group.attrs['_hsp_version_']
        return vers

    @classmethod
    def _hsp_classname_write(cls, h5group):
        h5group.attrs["_hsp_class_name_"] = "{kl_name!s}".format(kl_name=cls.__name__)

    @classmethod
    def _hsp_classname_read(cls, h5group):
        if "_hsp_class_name_" not in h5group.attrs:
            err_msg = "Missing class name in '{gname:s}'.".format(gname=h5group.name)
            log.error(err_msg)
            raise IOError(err_msg)
        class_name = h5group.attrs["_hsp_class_name_"]
        return class_name

    def _hsp_subgroup_id(self):
        """
        Get subgroup identifier (suffix)
        """
        return "{uid!s}".format(uid=self.__uid)

    @staticmethod
    def _hsp_write_callback(callback_string, **kwargs):
        # If necessary, call callback function with object name
        cb_func = kwargs.get("callback_func", None)
        if cb_func is not None:
            cb_func(callback_string)

    def _hsp_write(self, h5group, **kwargs):
        """
        Serialize a Hdf5StudyPersistent object into a HDF5 file.

        Parameters
        ----------
        h5group: ``h5py.Group``
            Main group to write the object into.
        kwargs: ``dict``
            keyword argument dictionary.
        """
        # Write uid
        self._hsp_write_attribute(h5group, ("_hsp_uuid_", self.__uid), **kwargs)

    def _hsp_write_attribute(self, h5group, attr_params, clear_if_none=True, **kwargs):
        """
        Write an attribute into a HDF5 study persistent file

        Parameters
        ----------
        h5group: h5py.Group
        attr_params: (attribute name, attribute value) tuple
        clear_if_none: ``bool`` delete entry if attribute is None ? Default True.
        kwargs: keyword argument dict.
        """
        attr_name, attr_value = attr_params
        if not kwargs.get("dry_run", False):
            if attr_value is None:
                if attr_name in h5group.attrs and clear_if_none:
                    del h5group.attrs[attr_name]
                if attr_name in h5group and clear_if_none:  # Delete Unit group if any
                    del h5group[attr_name]
            else:
                if Stringifiable.is_type_string(attr_value):
                    if sys.version_info.major > 2:  # Python 3.+
                        h5group.attrs[attr_name] = str(attr_value)
                    else:  # Python 2.x
                        h5group.attrs[attr_name] = unicode(attr_value)
                elif isinstance(attr_value, uuid.UUID):
                    # Convert string or UUID into unicode
                    h5group.attrs[attr_name] = "{uid!s}".format(uid=attr_value)
                elif isinstance(attr_value, bool):
                    # Convert bool value to int
                    h5group.attrs[attr_name] = int(attr_value)
                elif isinstance(attr_value, U.Unit):
                    # Write Unit instance into HDF5 Group only if unit is not U.none
                    if attr_value != U.none:
                        ugroup = self._hsp_get_or_create_h5group(h5group, attr_name, **kwargs)
                        self._hsp_write_dataset(ugroup, ("dimensions", attr_value.dimensions), **kwargs)
                        self._hsp_write_attribute(ugroup, ("coefficient", attr_value.coeff), **kwargs)
                        self._hsp_write_attribute(ugroup, ("name", attr_value.name), **kwargs)
                        self._hsp_write_attribute(ugroup, ("description", attr_value.description), **kwargs)
                        if attr_value.latex != attr_value.name:  # === attr_value._latex is not None
                            self._hsp_write_attribute(ugroup, ("latex", attr_value.latex), **kwargs)
                        elif not kwargs.get("new_file", True):  # Old HDF5 file being modified
                            # attr_value._latex is None
                            if "latex" in ugroup:
                                del ugroup["latex"]  # Delete old unit LaTex formula
                    elif not kwargs.get("new_file", True):  # Old HDF5 file being modified
                        # attr_value == U.none
                        if attr_name in h5group:
                            del h5group[attr_name]  # Delete old unit group
                else:  # Numerical value
                    h5group.attrs[attr_name] = attr_value

    def _hsp_write_dataset(self, h5group, dset_params, md5sum_params=None, **kwargs):
        """
        Write a dataset (Numpy ndarray/Pillow Image) into a HDF5 study persistent file

        Parameters
        ----------
        h5group: h5py.Group
        dset_params: (dataset name, dataset array) tuple
        md5sum_params: (md5sum attribute name, md5sum attribute value) tuple. Default None.
        kwargs: keyword argument dict.
        """
        dset_name, dset_attr_name = dset_params
        dset = None

        if md5sum_params is None:  # No lazy I/O of the dataset, write new dataset only if not None
            if isinstance(dset_attr_name, N.ndarray):
                dset = dset_attr_name
                write_dataset = True
            else:
                dset = getattr(self, dset_attr_name, None)
                write_dataset = dset is not None
        else:  # Lazy I/O case
            md5sum_attr_name, md5sum_value = md5sum_params
            if kwargs.get("new_file", True):  # New file => dataset needs to be written in this new file
                write_dataset = True
            else:  # Pre-existing file
                if dset_name not in h5group:  # New dataset in a pre-existing study file
                    write_dataset = True
                else:
                    # Check if new dataset is different from already saved dataset in HDF5 file
                    write_dataset = md5sum_attr_name not in h5group.attrs or md5sum_value is None or \
                                    h5group.attrs[md5sum_attr_name] != str(md5sum_value)
                    # MD5sum differ => must overwrite dataset!

        if not kwargs.get("dry_run", False):
            # Dataset already exist, perhaps with a different data shape/size => first you need to delete it
            if dset_name in h5group:
                if md5sum_params is None:  # No lazy I/O of the dataset
                    del h5group[dset_name]  # Delete dataset from HDF5 group
                else:  # Lazy I/O case
                    if write_dataset:
                        del h5group[dset_name]  # Delete dataset from HDF5 group

            if md5sum_params is not None:  # Lazy I/O case : define dataset
                if write_dataset:  # Dataset must be written : read it first
                    # Make sure data is actually read from HDF5 file (Lazy read) => No use (in theory)
                    self._hsp_lazy_read()
                    # Then get the dataset (eventually previously read just before if not earlier) from HDF5 file
                    dset = getattr(self, dset_attr_name, None)

            if write_dataset and dset is not None:
                if isinstance(dset, Image.Image):
                    if not _Pillow_available:
                        err_msg = "Pillow module is required to write images !"
                        log.error(err_msg)
                        raise ImportError(err_msg)

                    # Write a PIL Image object into a HDF5 file following the HDF5 Image standard v1.2 (see
                    # https://support.hdfgroup.org/HDF5/doc/ADGuide/ImageSpec.html).
                    width, height = dset.size
                    d = N.array(dset.getdata(), dtype='uint8').reshape(height, width, -1)
                    ds = h5group.create_dataset(dset_name, data=d, compression='gzip',  # dtype=h5py.h5t.STD_U8BE,
                                                compression_opts=9)  # Best compression
                    ds.attrs['CLASS'] = N.string_("IMAGE")  # Fixed length string
                    ds.attrs['IMAGE_VERSION'] = N.string_("1.2")  # Fixed length string
                    ds.attrs['IMAGE_SUBCLASS'] = N.string_("IMAGE_TRUECOLOR")  # Fixed length string
                    ds.attrs['IMAGE_MINMAXRANGE'] = N.array([0, 255], dtype='uint8')  # Must be same type as dataset
                    ds.attrs['INTERLACE_MODE'] = N.string_("INTERLACE_PIXEL")  # Fixed length string
                else:  # Regular numpy ndarray object
                    # Write dataset array
                    if dset.shape == ():
                        h5group.create_dataset(dset_name, data=dset)
                    else:
                        h5group.create_dataset(dset_name, data=dset, compression='gzip', compression_opts=9)  # Best compression)

        if md5sum_params is not None:
            # Set values array MD5 sum
            md5sum_attr_name, md5sum_value = md5sum_params
            self._hsp_write_attribute(h5group, (md5sum_attr_name, md5sum_value), **kwargs)

        return write_dataset

    @staticmethod
    def _hsp_write_object(h5group, subgroup_name, obj, **kwargs):
        """
        Write an object into a HDF5 study persistent file

        Parameters
        ----------
        h5group: h5py.Group
        subgroup_name: name of the subgroup (get/create) where to save the object
        obj: instance to save
        kwargs: keyword argument dict.
        """
        # Write object
        if obj is not None:
            subgroup = Hdf5StudyPersistent._hsp_get_or_create_h5group(h5group, subgroup_name, **kwargs)
            return obj.hsp_save_to_h5(subgroup, **kwargs)
        elif not kwargs.get("dry_run", False) and subgroup_name is not None and subgroup_name in h5group:
            # Save a None object => clear subgroup from HDF5 file
            del h5group[subgroup_name]

    @staticmethod
    def _hsp_get_or_create_h5group(h5group, subgroup_name, **kwargs):
        """
        Get or create a HDF5 subgroup in an existing h5py.Group object

        Parameters
        ----------
        h5group: h5py.Group
        subgroup_name: name of the subgroup to get/create
        kwargs: keyword argument dict.
        """
        is_dry_run = kwargs.get("dry_run", False)

        if subgroup_name is None:
            subgroup = h5group
        elif subgroup_name in h5group:
            subgroup = h5group[subgroup_name]
        else:
            if not is_dry_run:
                # subgroup directory creation, if necessary
                subgroup = h5group.create_group(subgroup_name)
            else:  # Do not create anything in 'dry' runs
                subgroup = h5group
        return subgroup

    @staticmethod
    def _hsp_write_object_list(h5group, subgroup_name, obj_iterator, obj_group_prefix, uid_list_only=False, **kwargs):
        """
        Write a list of objects into a HDF5 study persistent file

        Parameters
        ----------
        h5group: h5py.Group
        subgroup_name: name of the subgroup (get/create) where to save all the objects
        obj_iterator: object iterator
        obj_group_prefix: object subgroup prefix
        kwargs: keyword argument dict.
        """
        objlist_group = Hdf5StudyPersistent._hsp_get_or_create_h5group(h5group, subgroup_name, **kwargs)

        if not kwargs.get("dry_run", False):
            list_updated = False
            list_size_changed = False
            current_ids = []
            is_new_file = kwargs.get("new_file", True)  # Create new HDF5 study persistent *.h5 file
            is_new_entry = is_new_file or "_object_id_list_" not in objlist_group
            if is_new_entry:
                list_updated = True
                list_size_changed = True

                # Create all object subgroups
                for obj in obj_iterator():
                    obj_group_suffix = obj._hsp_subgroup_id()
                    obj_group_name = "{obj_group_prefix!s}{obj_id:s}".format(obj_group_prefix=obj_group_prefix,
                                                                             obj_id=obj_group_suffix)
                    Hdf5StudyPersistent._hsp_get_or_create_h5group(objlist_group, obj_group_name, **kwargs)
                    current_ids.append(obj_group_suffix)
            else:  # Update existing object subgroups
                saved_object_id_list = list(objlist_group["_object_id_list_"][...])
                if len(saved_object_id_list) > 0 and sys.version_info.major >= 3 and type(saved_object_id_list[0]) is not str:  # h5py v >= 3.0, strings are stored as bytes
                    saved_object_id_list = list(h5py.Dataset.asstr(objlist_group["_object_id_list_"]))

                    # Create missing/clean unused object subgroups, if necessary

                # -> Create missing object groups (new objects)
                for obj in obj_iterator():
                    obj_group_suffix = obj._hsp_subgroup_id()
                    obj_group_name = "{obj_group_prefix!s}{obj_id:s}".format(obj_group_prefix=obj_group_prefix,
                                                                             obj_id=obj_group_suffix)
                    current_ids.append(obj_group_suffix)
                    if obj_group_name not in objlist_group:
                        Hdf5StudyPersistent._hsp_get_or_create_h5group(objlist_group, obj_group_name, **kwargs)
                        list_updated = True

                # -> Delete old object groups (deleted objects)
                for old_id in saved_object_id_list:
                    if old_id not in current_ids:
                        obj_group_name = "{obj_group_prefix!s}{obj_id:s}".format(obj_group_prefix=obj_group_prefix,
                                                                                 obj_id=old_id)
                        del objlist_group[obj_group_name]
                        list_updated = True

                list_size_changed = len(saved_object_id_list) != len(current_ids)

            # Save all objects
            if not uid_list_only:  # Do record objects or only their UUID ?
                for obj in obj_iterator():
                    obj_group_suffix = obj._hsp_subgroup_id()
                    obj_group_name = "{obj_group_prefix!s}{obj_id:s}".format(obj_group_prefix=obj_group_prefix,
                                                                             obj_id=obj_group_suffix)
                    obj_group = Hdf5StudyPersistent._hsp_get_or_create_h5group(objlist_group, obj_group_name, **kwargs)
                    obj.hsp_save_to_h5(obj_group, **kwargs)

            # Write list of object identifiers
            if list_updated:
                if "_object_id_list_" in objlist_group and list_size_changed:  # Clear existing dataset, if size changed
                    del objlist_group["_object_id_list_"]
                if len(current_ids) > 0:  # Non empty object unique id list => create or update (unchanged size) list
                    if list_size_changed:
                        ds = objlist_group.create_dataset("_object_id_list_", shape=(len(current_ids),),
                                                          dtype=h5py.string_dtype(encoding='utf-8'))  # h5py > 2.10
                    else:  # List size did not change => update existing dataset
                        ds = objlist_group["_object_id_list_"]
                    ds[:] = current_ids[:]
        else:  # Dry run
            if uid_list_only:  # Do not record objects
                return
            # Write all objects
            for obj in obj_iterator():
                obj_group_suffix = obj._hsp_subgroup_id()
                obj_group_name = "{obj_group_prefix!s}{obj_id:s}".format(obj_group_prefix=obj_group_prefix,
                                                                         obj_id=obj_group_suffix)
                # Won't create anything here (dry run). Might return 'objlist_group'
                obj_group = Hdf5StudyPersistent._hsp_get_or_create_h5group(objlist_group, obj_group_name, **kwargs)

                # 1. Object subgroup does not exist, try to write directly in object list group
                # or 2. Object subgroup already exist, try to write in it, see if anything changed
                obj.hsp_save_to_h5(obj_group, **kwargs)

    @classmethod
    def _hsp_read_object(cls, h5group, subgroup_name, obj_descr, dependency_objdict=None):
        """
        Read an object from a HDF5 study persistent file

        Parameters
        ----------
        h5group: h5py.Group
        subgroup_name: name of the subgroup to read the object from
        obj_descr: object description, for error message display purpose only
        dependency_objdict: dependency object dictionary. Default None
        """
        if subgroup_name not in h5group:
            err_msg = "Cannot find {cl_name!s} in '{path!s}'.".format(cl_name=obj_descr, path=h5group.name)
            log.error(err_msg)
            raise IOError(err_msg)
        obj_group = h5group[subgroup_name]
        return cls.hsp_load_from_h5(obj_group, dependency_objdict=dependency_objdict)

    @classmethod
    def _hsp_read_attribute(cls, h5group, attr_name, attr_descr, raise_error_if_not_found=True):
        """
        Read an attribute from a HDF5 study persistent file

        Parameters
        ----------
        h5group: h5py.Group
        attr_name: attribute name
        attr_descr: attribute description, for error message display purpose only
        raise_error_if_not_found: should an IOError be raised if the attribute is not found

        Returns
        -------
        v: attribute value, or None if 'raise_error_if_not_found' is False and attribute is not found.
        """
        if attr_name not in h5group.attrs:
            if raise_error_if_not_found:
                err_msg = "Cannot find object {descr!s} attribute in '{path!s}'.".format(descr=attr_descr,
                                                                                         path=h5group.name)
                log.error(err_msg)
                raise IOError(err_msg)
            else:
                return None
        return h5group.attrs[attr_name]

    @classmethod
    def _hsp_read_unit(cls, h5group, unit_name):
        """
        Read a Unit instance from a HDF5 study persistent file

        Parameters
        ----------
        h5group: h5py.Group
        unit_name: Unit group prefix

        Returns
        -------
        u: ``Unit``
            Unit instance.
        """
        if unit_name not in h5group:
            return U.none
        ugroup = h5group[unit_name]
        uname = cls._hsp_read_attribute(ugroup, "name", "unit name", raise_error_if_not_found=True)
        dims = cls._hsp_read_dataset(ugroup, "dimensions", "unit dimensions", raise_error_if_not_found=True)
        coeff = cls._hsp_read_attribute(ugroup, "coefficient", "unit coefficient", raise_error_if_not_found=True)
        desc = cls._hsp_read_attribute(ugroup, "description", "unit description", raise_error_if_not_found=True)
        ltx = cls._hsp_read_attribute(ugroup, "latex", "unit latex formula", raise_error_if_not_found=False)
        try:
            u = U.Unit.create_unit(uname, coeff=coeff, dims=dims, descr=desc, latex=ltx)
        except ValueError:
            # Unit already exist in registry
            u = U.Unit.from_name(uname)
            if not (u.dimensions == dims).all() or coeff != u.coeff or desc != u.description or \
                    (ltx is not None and ltx != u.latex):
                log.warning("'{un:s}' Unit definition read from HDF5 file differ from Unit registry.".format(un=uname))

        return u

    @classmethod
    def _hsp_read_object_list(cls, h5group, subgroup_name, obj_group_prefix, obj_descr, uid_list_only=False,
                              dependency_objdict=None):
        """
        Read an object (or its UUID) from a HDF5 study persistent file

        Parameters
        ----------
        h5group: h5py.Group
        subgroup_name: name of the subgroup to read the objects from
        obj_group_prefix: object subgroup prefix
        obj_descr: object description, for error message display purpose only
        uid_list_only: bool. Returns the object UUID only, and not the object themselves. Default False
        dependency_objdict: dependency object dictionary. Default None
        """
        # Read objects
        if subgroup_name is None:
            objlist_group = h5group
        elif subgroup_name in h5group:
            objlist_group = h5group[subgroup_name]
        else:
            err_msg = "Cannot find {obj_descr!s} directory in '{path!s}'.".format(obj_descr=obj_descr,
                                                                                  path=h5group.name)
            log.error(err_msg)
            raise IOError(err_msg)
        # "/PROJECT/SIMULATIONS/simu_39dba0dd-43e5-430f-893c-09137a276317/SNAPSHOTS"
        # Read object id list
        if "_object_id_list_" not in objlist_group:
            return
        obj_id_list = list(objlist_group["_object_id_list_"][...])
        if len(obj_id_list) > 0 and sys.version_info.major >= 3 and type(obj_id_list[0]) is not str:  # h5py v >= 3.0, strings are stored as bytes
                obj_id_list = list(h5py.Dataset.asstr(objlist_group["_object_id_list_"]))  # https://docs.h5py.org/en/3.0.0/strings.html#strings-in-hdf5

        if uid_list_only:  # Yield object UUIDs
            for suid in obj_id_list:
                yield suid
        else:  # Yield objects
            for iobj in range(len(obj_id_list)):
                obj_group_name = "{pref!s}{obj_id:s}".format(pref=obj_group_prefix, obj_id=obj_id_list[iobj])
                if obj_group_name not in objlist_group:
                    err_msg = "Cannot find object {descr!s} #{obj_index:d} in '{path!s}'.".format(descr=obj_descr,
                                                                                                  obj_index=iobj+1,
                                                                                                  path=objlist_group.name)
                    log.error(err_msg)
                    raise IOError(err_msg)
                object_subgroup = objlist_group[obj_group_name]
                yield cls.hsp_load_from_h5(object_subgroup, dependency_objdict=dependency_objdict)

    @classmethod
    def _hsp_read_dataset(cls, h5group, dataset_name, dataset_descr, raise_error_if_not_found=True):
        """
        Read a dataset from a HDF5 study persistent file

        Parameters
        ----------
        h5group: h5py.Group
        dataset_name: dataset name
        dataset_descr: dataset description, for error message display purpose only
        raise_error_if_not_found: should an IOError be raised if the dataset is not found

        Returns
        -------
        a: dataset array, or None if 'raise_error_if_not_found' is False and dataset is not found.
        """
        if dataset_name not in h5group:
            if raise_error_if_not_found:
                err_msg = "Cannot find {descr!s} dataset in '{path!s}'.".format(descr=dataset_descr, path=h5group.name)
                log.error(err_msg)
                raise IOError(err_msg)
            else:
                return None
        return h5group[dataset_name][...]

    @classmethod
    def _hsp_read_pil_image(cls, h5group, img_group_name, raise_error_if_not_found=True):
        """
        Read a PIL Image object from a HDF5 file following the HDF5 Image standard v1.2 (see
        https://support.hdfgroup.org/HDF5/doc/ADGuide/ImageSpec.html).

        Parameters
         ---------
        h5group: ``h5py.H5Group``
        img_group_name: ``string``
        raise_error_if_not_found: should an IOError be raised if the PIL image dataset is not found. Default True.

        Returns
        -------
        pil_image: ``PIL.Image``
            Loaded PIL Image from HDF5 file
        """
        if not _Pillow_available:
            err_msg = "Pillow module is required to read images !"
            log.error(err_msg)
            raise ImportError(err_msg)

        ds = cls._hsp_read_dataset(h5group, img_group_name, "PIL image",
                                   raise_error_if_not_found=raise_error_if_not_found)

        if ds is None:
            return ds

        return Image.fromarray(N.asarray(ds, dtype="uint8"))

    @classmethod
    def _hsp_read(cls, h5group, version, dependency_objdict=None):
        """
        Read a Hdsf5StudyPersistent object from a HDF5 file (\\*.h5).

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
        uid: ``uuid.UUID``
            object unique identifier
        """
        # Read node unique id
        uid = uuid.UUID(cls._hsp_read_attribute(h5group, "_hsp_uuid_", "object unique id"))

        return uid

    @classmethod
    def _fact_all_subclasses(cls, store_cache=True):
        """
        Returns a list of all sub(sub*)classes of a given class. Handles a subclass list cache dictionary.

        Parameters
        ----------
        store_cache; ``bool``
            Whether the list of subclasses of the class must be stored in a cache dictionary or not. Default True.

        Returns
        -------
        subclass_list: ``list``
            list of all subclasses of a given class
        """
        if cls in Hdf5StudyPersistent.__fact_subclasses_dict:
            return Hdf5StudyPersistent.__fact_subclasses_dict[cls]

        subclass_list = cls.__subclasses__() + [c for subclass in cls.__subclasses__()
                                                for c in subclass._fact_all_subclasses(store_cache=False)]

        if store_cache:
            Hdf5StudyPersistent.__fact_subclasses_dict[cls] = subclass_list
        return subclass_list

    @classmethod
    def hsp_load_from_h5(cls, h5fg, dependency_objdict=None):
        """
        Returns an object from a HDF5 study persistent file (\\*.h5).

        Parameters
        ----------
        h5fg: ``h5py.Group``
            HDF5 (h5py) group.
        dependency_objdict: ``dict``
            dependency object dictionary. Default None

        Raises
        ------
        imperr: ``ImportError``
            raises an ImportError if the 'h5py' module is not found.
        atterr: ``AttributeError``
            raises an AttributeError if any attribute is not valid.
        ioerr: ``IOError``
            raises an IOError if an error occurred while reading the HDF5 study persistent file.
        """
        if not isinstance(h5fg, h5py.Group) or h5fg.__class__ != h5py.Group:
            # f, group, close_when_done = cls.open_h5file(h5fg, where, mode=Hdf5StudyFileMode.READ_ONLY)
            err_msg = "h5fg is not a valid h5py.Group instance. Cannot load {cname:s} object from HDF5 " \
                      "file.".format(cname=cls.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

        class_name = cls._hsp_classname_read(h5fg)
        # Instance class is a subclass of the current class => find the right class
        if class_name != cls.__name__:
            subclasses = cls._fact_all_subclasses()
            o = None
            for kl in subclasses:
                if kl.__name__ == class_name:
                    o = kl.hsp_load_from_h5(h5fg, dependency_objdict=dependency_objdict)
                    break
            if o is None:
                err_msg = "Cannot instantiate object of class '%s' in '%s'." % (class_name, h5fg.name)
                log.error(err_msg)
                raise IOError(err_msg)
        else:
            # Read version number
            v = cls._hsp_version_read(h5fg)

            # Read object
            o = cls._hsp_read(h5fg, v, dependency_objdict=dependency_objdict)

        return o

    def hsp_save_to_h5(self, h5fg, **kwargs):
        """
        Saves an object into a HDF5 study persistent file (\\*.h5).

        Parameters
        ----------
        h5fg: ``h5py.Group``
            HDF5 (h5py) group.

        Raises
        ------
        imperr: ``ImportError``
            raises an ImportError if the 'h5py' module is not found.
        atterr: ``AttributeError``
            raises an AttributeError if any attribute is not valid.
        ioerr: ``IOError``
            raises an IOError if an error occured while writing into the HDF5 study persistent file.
        """
        if not isinstance(h5fg, h5py.Group) or h5fg.__class__ != h5py.Group:
            err_msg = "h5fg is not a valid h5py.Group instance. Cannot save {cname:s} object into HDF5 " \
                      "file.".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

        if not kwargs.get("dry_run", False):
            # Write version number
            self._hsp_version_write(h5fg)

            # Write class name
            self._hsp_classname_write(h5fg)

        # Serialize object
        self._hsp_write(h5fg, **kwargs)


__all__ = ["Hdf5StudyPersistent", "Hdf5StudyFileMode"]
