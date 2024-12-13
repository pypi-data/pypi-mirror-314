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
"""

.. autoclass:: astrophysix.simdm.datafiles.file.AssociatedFile

.. autoclass:: astrophysix.simdm.datafiles.file.FitsFile
    :members: filename, last_modified, load_file, save_to_disk, raw_file_data
    :show-inheritance: AssociatedFile

.. autoclass:: astrophysix.simdm.datafiles.file.PickleFile
    :members: filename, last_modified, load_file, save_to_disk, raw_file_data
    :show-inheritance: AssociatedFile

.. autoclass::  astrophysix.simdm.datafiles.file.AsciiFile
    :members: filename, last_modified, load_file, save_to_disk, raw_file_data
    :show-inheritance: AssociatedFile

.. autoclass:: astrophysix.simdm.datafiles.file.HDF5File
    :members: filename, last_modified, load_file, save_to_disk, raw_file_data
    :show-inheritance: AssociatedFile

.. autoclass::  astrophysix.simdm.datafiles.file.JsonFile
    :members: filename, last_modified, load_file, save_to_disk, raw_file_data
    :show-inheritance: AssociatedFile

.. autoclass::  astrophysix.simdm.datafiles.file.CSVFile
    :members: filename, last_modified, load_file, save_to_disk, raw_file_data
    :show-inheritance: AssociatedFile

.. autoclass::  astrophysix.simdm.datafiles.file.YamlFile
    :members: filename, last_modified, load_file, save_to_disk, raw_file_data
    :show-inheritance: AssociatedFile

.. autoclass::  astrophysix.simdm.datafiles.file.TarGzFile
    :members: filename, last_modified, load_file, save_to_disk, raw_file_data
    :show-inheritance: AssociatedFile

"""
from __future__ import print_function, unicode_literals, division, absolute_import  # Python 2 and 3 compatibility
from future.builtins import str, list, int
import logging
import os
import datetime
import numpy as N

from astrophysix.utils import FileType, FileUtil
from astrophysix.utils.dt_utils import DatetimeUtil
from astrophysix.utils.persistency import Hdf5StudyPersistent
from astrophysix.utils.strings import Stringifiable
from ..utils import GalacticaValidityCheckMixin


log = logging.getLogger("astrophysix.simdm")


class AssociatedFile(Hdf5StudyPersistent, GalacticaValidityCheckMixin, Stringifiable):
    FILE_MD5SUM_HDF5_ATTR_NAME = "file_md5sum"
    FILE_RAW_DATA_ATTR_NAME = "file_raw_data"
    FILE_TYPE = FileType.ASCII_FILE

    def __init__(self, **kwargs):
        """
        Datafile associated file base class (Simulation data model)

        Parameters
        ----------
        filename: :obj:`string`
            file name (mandatory)
        file_md5sum: :obj:`string`
            MD5SUM of the file (mandatory)
        """
        super(AssociatedFile, self).__init__(**kwargs)

        self._filename = ""
        self._file_md5sum = ""
        self._last_modif_time = None
        self._raw_file_data = None

        # ------------------------------------------------ File name ------------------------------------------------- #
        if "filename" not in kwargs:
            err_msg = "{cname:s} 'filename' attribute is not defined (mandatory).".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)
        fname = kwargs["filename"]
        if self.FILE_TYPE != FileUtil.get_file_type(fname):  # File type does not match defined file type
            err_msg = "'{fname!s}' is not a valid {fta:s} file name".format(fname=fname, fta=self.FILE_TYPE.alias)
            log.error(err_msg)
            raise AttributeError(err_msg)
        self._filename = fname
        # ------------------------------------------------------------------------------------------------------------ #

        # ------------------------------------------------ File md5sum ----------------------------------------------- #
        if "file_md5sum" not in kwargs:
            err_msg = "{cname:s} 'file_md5sum' attribute is not defined " \
                      "(mandatory).".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)
        try:
            self._file_md5sum = Stringifiable.cast_string(kwargs["file_md5sum"])
        except TypeError:
            err_msg = "{cname:s} 'file_md5sum' attribute is not a valid string".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)
        # ------------------------------------------------------------------------------------------------------------ #

        # -------------------------------------- File last modification datetime ------------------------------------- #
        if "modif_dt" not in kwargs:
            err_msg = "{cname:s} 'modif_dt' attribute is not defined (mandatory).".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)
        dt = kwargs["modif_dt"]
        if not isinstance(dt, datetime.datetime):
            err_msg = "{cname:s} 'modif_dt' attribute is not a valid datetime instance."
            log.error(err_msg)
            raise AttributeError(err_msg)
        self._last_modif_time = dt
        # ------------------------------------------------------------------------------------------------------------ #

        # ------------------------------------------ Raw file data bytes --------------------------------------------- #
        if "raw_file_data" in kwargs:
            rfd = kwargs["raw_file_data"]
            if not isinstance(rfd, N.void):
                err_msg = "{cname:s} 'raw_file_data' attribute is not a valid numpy void object."
                log.error(err_msg)
                raise AttributeError(err_msg)
            self._raw_file_data = rfd
        # ------------------------------------------------------------------------------------------------------------ #

    @property
    def filename(self):
        """Gets associated file name. Cannot be edited."""
        return self._filename

    @property
    def file_md5sum(self):
        """Datafile associated file MD5sum getter."""
        return self._file_md5sum

    @property
    def last_modified(self):
        """Returns file last modification time. Cannot be edited."""
        return self._last_modif_time

    @property
    def raw_file_data(self):
        """
        File binary raw data. Cannot be edited.

        Returns
        -------
        raw_data: :obj:`bytes`
        """
        # Force file data loading if not already read from HDF5 file
        self._hsp_lazy_read()

        return self._raw_file_data.tobytes()

    def __eq__(self, other):
        """
        Rich comparison method for associated files

        Parameters
        ----------
        other: ``AssociatedFile``
            associated file to compare to:
        """
        # Avoid Hdf5StudyPersistent comparison test => it compares the UUID !
        # if not super(AssociatedFile, self).__eq__(other):
        #     return False
        # Compares only the equality of the object classes
        if self.__class__ != other.__class__:
            return False

        if self._filename != other.filename:
            return False

        if self._file_md5sum != other.file_md5sum:
            return False

        if self._last_modif_time != other.last_modified:
            return False

        return True

    @classmethod
    def _all_subclasses(cls):
        """
        Returns a list of all sub(sub*)classes of a given class (recursive class method)

        Returns
        -------
        subclass_list: ``list``
            list of all subclasses of a given class
        """
        subclass_list = cls.__subclasses__()
        other_subclasses = [c for subclass in subclass_list for c in subclass._all_subclasses()]
        return other_subclasses + subclass_list

    @classmethod
    def load_file(cls, filepath):
        """
        Loads an :class:`~astrophysix.simdm.datafiles.file.AssociatedFile` object from a filepath

        Parameters
        ----------
        filepath: :obj:`string`
            path of the file to load.

        Returns
        -------
        f: :class:`~astrophysix.simdm.datafiles.file.AssociatedFile` instance
            Loaded associatedfile
        """
        file_path = Stringifiable.cast_string(filepath, valid_empty=False)
        fpath = FileUtil.locate_file(file_path)
        filename = os.path.basename(fpath)
        ftype = FileUtil.get_file_type(fpath)
        if ftype != cls.FILE_TYPE:
            err_msg = "Invalid filename for a {ft:s} file ({fp!s}).".format(ft=cls.FILE_TYPE.alias, fp=file_path)
            log.error(err_msg)
            raise AttributeError(err_msg)
        file_md5sum = FileUtil.md5sum(fpath)
        last_modified = DatetimeUtil.utc_from_timestamp(FileUtil.last_modification_timestamp(fpath))
        with open(file_path, 'rb') as fp:
            raw_file_data = N.void(fp.read())

        f = cls(filename=filename, file_md5sum=file_md5sum, modif_dt=last_modified, raw_file_data=raw_file_data)

        return f

    def _export_file(self, filepath):
        with open(filepath, 'wb') as fp:
            fp.write(self.raw_file_data)

    def save_to_disk(self, filepath=None):
        """
        Save associated file to an external file on the local filesystem

        Parameters
        ----------
        filepath: :obj:`string`
            external file path
        """
        if filepath is not None:
            file_path = Stringifiable.cast_string(filepath, valid_empty=False)
            fpath = FileUtil.new_filepath(file_path, self.FILE_TYPE, create_dir=True)
            ftype = FileUtil.get_file_type(filepath)
            if ftype != self.FILE_TYPE:
                err_msg = "Invalid filename for a {ft:s} file ({fp!s}).".format(ft=self.FILE_TYPE.alias, fp=filepath)
                log.error(err_msg)
                raise AttributeError(err_msg)
        else:
            fpath = os.path.abspath(self._filename)

        # Force file data loading if not already read from HDF5 file
        self._hsp_lazy_read()

        # Do the actual file saving operation...
        self._export_file(fpath)
        log.info("File '{fp:s}' saved.".format(fp=fpath))

        # Update file 'Last modified' time and 'Last access' time
        lm_ts = DatetimeUtil.utc_to_timestamp(self._last_modif_time)
        os.utime(fpath, (-1, lm_ts))  # Set last access time to 'now' and last modified time to original modif. time.

        # Validity check (Md5 sum comparison)
        if self._file_md5sum != FileUtil.md5sum(fpath):
            err_msg = "MD5 sum validity check failed upon {ft:s} file export into " \
                      "'{fp!s}'.".format(ft=self.FILE_TYPE.alias, fp=fpath)
            log.error(err_msg)
            raise IOError(err_msg)

        return fpath

    @classmethod
    def _hsp_valid_attributes(cls):
        """List of valid kwargs in __init__() method"""
        return ["filename", "file_md5sum", "modif_dt", "raw_file_data"]

    def _hsp_write(self, h5group, **kwargs):
        """
        Serialize a AssociatedFile object into a HDF5 file.

        Parameters
        ----------
        h5group: ``h5py.Group``
            Main group to write the AssociatedFile into.
        kwargs: ``dict``
            keyword argument dictionary.
        """
        # Call to parent class _hsp_write() : write UUID, etc.
        super(AssociatedFile, self)._hsp_write(h5group, **kwargs)

        # Write AssociatedFile attributes
        self._hsp_write_attribute(h5group, ("filename", self._filename), **kwargs)
        modif_tms = DatetimeUtil.utc_to_timestamp(self._last_modif_time)
        self._hsp_write_attribute(h5group, ("last_modif_date", modif_tms), **kwargs)

        # Write file raw data
        raw_data_attribute_name = "_raw_file_data"  # => self._raw_file_data
        write_dataset = self._hsp_write_dataset(h5group, (self.FILE_RAW_DATA_ATTR_NAME, raw_data_attribute_name),
                                                md5sum_params=(self.FILE_MD5SUM_HDF5_ATTR_NAME, self._file_md5sum),
                                                **kwargs)
        if write_dataset:
            self._hsp_write_callback(str(self), **kwargs)

    @classmethod
    def _hsp_read(cls, h5group, version, dependency_objdict=None):
        """
        Read a AssociatedFile object from a HDF5 file (*.h5).

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
        af: ``AssociatedFile``
            Read AssociatedFile instance
        """
        # Handle different versions here

        # Fetch Hdf5StudyPersistent object UUID
        uid = super(AssociatedFile, cls)._hsp_read(h5group, version, dependency_objdict=dependency_objdict)

        # Read AssociatedFile info from HDF5
        # ftype = FileType.from_alias(cls._hsp_read_attribute(h5group, "file_type", "associated file type"))
        fname = cls._hsp_read_attribute(h5group, "filename", "associated file name")
        file_md5sum = cls._hsp_read_attribute(h5group, cls.FILE_MD5SUM_HDF5_ATTR_NAME, "associated file MD5SUM")
        mod_dt = cls._hsp_read_attribute(h5group, "last_modif_date", "associated file last modification datetime")
        mod_dt_utc = DatetimeUtil.utc_from_timestamp(mod_dt)
        # af = cls(uid=uid, file_type=ftype, filename=fname, file_md5sum=file_md5sum, modif_dt=mod_dt)
        af = cls(uid=uid, filename=fname, file_md5sum=file_md5sum, modif_dt=mod_dt_utc)

        # Set HDF5 group/file info for lazy I/O
        af._hsp_set_lazy_source(h5group)

        return af

    def _hsp_lazy_read_data(self, h5group):
        """
        Lazy read method to load RawBinaryFile from HDF5 file (*.h5)

        Parameters
        ----------
        h5group: `h5py.Group`
        """
        log.info("Reading {ft:s} data from {gname:s} ({f!s} file).".format(ft=self.FILE_TYPE.alias, gname=h5group.name,
                                                                           f=h5group.file.filename))

        # Read raw data file, if any + md5sum
        self._raw_file_data = self._hsp_read_dataset(h5group, self.FILE_RAW_DATA_ATTR_NAME,
                                                     "{ft:s} file raw data".format(ft=self.FILE_TYPE.alias),
                                                     raise_error_if_not_found=True)

    def galactica_validity_check(self, **kwargs):
        """
        Perform validity checks on this  instance and eventually log warning messages.

        Parameters
        ----------
        kwargs: `dict`
            keyword arguments (optional)
        """
        # Galactica validity check for associated file
        pass

    def __unicode__(self):
        """
        String representation of the instance
        """
        s = "[{fname:s}] datafile associated {ft:s} file".format(fname=self._filename, ft=self.FILE_TYPE.alias)
        return s


class FitsFile(AssociatedFile):
    """
    Datafile associated :attr:`~astrophysix.utils.file.FileType.FITS_FILE` file class.
    """
    FILE_TYPE = FileType.FITS_FILE


class PickleFile(AssociatedFile):
    """
    Datafile associated :attr:`~astrophysix.utils.file.FileType.PICKLE_FILE` file class.
    """
    FILE_TYPE = FileType.PICKLE_FILE


class TarGzFile(AssociatedFile):
    """
    Datafile associated :attr:`~astrophysix.utils.file.FileType.TARGZ_FILE` file class.
    """
    FILE_TYPE = FileType.TARGZ_FILE


class JsonFile(AssociatedFile):
    """
    Datafile associated :attr:`~astrophysix.utils.file.FileType.JSON_FILE` file class.
    """
    FILE_TYPE = FileType.JSON_FILE


class CSVFile(AssociatedFile):
    """
    Datafile associated :attr:`~astrophysix.utils.file.FileType.CSV_FILE` file class.
    """
    FILE_TYPE = FileType.CSV_FILE


class AsciiFile(AssociatedFile):
    """
    Datafile associated :attr:`~astrophysix.utils.file.FileType.ASCII_FILE` file class.
    """
    FILE_TYPE = FileType.ASCII_FILE


class YamlFile(AssociatedFile):
    """
    Datafile associated :attr:`~astrophysix.utils.file.FileType.YAML_FILE` file class.
    """
    FILE_TYPE = FileType.YAML_FILE


class HDF5File(AssociatedFile):
    """
    Datafile associated :attr:`~astrophysix.utils.file.FileType.HDF5_FILE` file class.
    """
    FILE_TYPE = FileType.HDF5_FILE


__all__ = ["AssociatedFile", "PickleFile", "TarGzFile", "JsonFile", "CSVFile", "AsciiFile", "HDF5File", "YamlFile"]
