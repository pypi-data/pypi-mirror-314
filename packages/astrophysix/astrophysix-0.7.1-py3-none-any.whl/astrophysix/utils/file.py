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
from __future__ import unicode_literals

from future.builtins import str
from enum import Enum
import hashlib
import re
import os
import tempfile

from .strings import Stringifiable
from .dt_utils import DatetimeUtil


class FileType(Enum):
    """File type enum

    Example
    -------
    >>> ft = FileType.ASCII_FILE
    >>> ft.alias
    "ASCII"
    >>> ft.extension_list
    [".dat", ".DAT", ".txt", ".TXT", ".ini", ".INI"]
    """
    PNG_FILE = ("PNG", [".png", ".PNG"])
    JPEG_FILE = ("JPEG", [".jpg", ".jpeg", ".JPG", ".JPEG"])
    FITS_FILE = ("FITS", [".fits", ".FITS"])
    TARGZ_FILE = ("TARGZ", [".tar.gz", ".TAR.GZ", ".TAR.gz", ".tar.GZ", ".tgz", ".TGZ"])
    PICKLE_FILE = ("PICKLE", [".pkl", ".PKL", ".pickle", ".sav", ".save"])
    HDF5_FILE = ("HDF5", [".h5", ".H5", ".hdf5", ".HDF5"])
    JSON_FILE = ("JSON", [".json", ".JSON"])
    CSV_FILE = ("CSV", [".csv", ".CSV"])
    YAML_FILE = ("YAML", [".yml", ".YML", ".yaml", ".YAML"])
    ASCII_FILE = ("ASCII", [".dat", ".DAT", ".txt", ".TXT", ".ini", ".INI"])
    XML_FILE = ("XML", ['.xml', '.XML'])

    def __init__(self, alias, ext_list):
        self._alias = alias
        self._extension_list = ext_list

    @property
    def alias(self):
        """
        Returns file type alias
        """
        return self._alias

    @property
    def extension_list(self):
        """
        Returns file type valid extension list
        """
        return self._extension_list

    @property
    def default_extension(self):
        """Returns the first item in the file type extension list"""
        return self._extension_list[0]

    @property
    def file_regexp(self):
        """
        Returns filename matching regular expression for the current file type
        """
        ext = "|".join([e[1:] for e in self._extension_list])
        return re.compile("(?P<basename>.+)\\.(?P<extension>({ext:s}))$".format(ext=ext))

    @classmethod
    def from_alias(cls, alias):
        """
        Find a FileType according to its alias

        Parameters
        ----------
        alias: :obj:`string`
            required file type alias

        Returns
        -------
        ft: :class:`~astrophysix.utils.file.FileType`
            File type matching the requested alias.

        Raises
        ------
        ValueError
            if requested alias does not match any file type.

        Example
        -------
            >>> ft = FileType.from_alias("PNG")
            >>> ft.extension_list
            [".png", ".PNG"]
            >>> ft2 = FileType.from_alias("MY_UNKNOWN_FILETYPE")
            ValuerError: No FileType defined with the alias 'MY_UNKNOWN_FILETYPE'.
        """
        for ftype in cls:
            if ftype.alias == alias:
                return ftype
        raise ValueError("No FileType defined with the alias '{a:s}'.".format(a=alias))

    def __unicode__(self):
        """
        String representation of the enum value. Returns alias.
        """
        return self._alias


class FileUtil(object):
    """
    File path utility abstract class
    """
    @classmethod
    def get_file_type(cls, filepath):
        """
        Find the file type or return None is no matching file type has been recognized.
        """
        cls._check_filename_is_string(filepath)
        filename = os.path.basename(filepath)

        for ftype in FileType:
            if ftype.file_regexp.match(filename) is not None:
                return ftype
        return None

    @staticmethod
    def valid_filepath(filepath, append_extension=None):
        """
        Build a valid filepath with a default file extension, if missing.

        Parameters
        ----------
        filepath: file path
        append_extension: optional appended extension FileType. Default None (do not append any extension)

        Returns
        -------
        fname:
        """
        FileUtil._check_filename_is_string(filepath)

        # Get file absolute path
        abs_filepath = os.path.abspath(filepath)

        if append_extension is None:
            return abs_filepath
        else:
            # Check that append_extension is a valid FileType enum value
            FileUtil._check_valid_file_type(append_extension)

            if append_extension.file_regexp.match(abs_filepath) is None:  # Missing extension
                # Append default extension to filename
                ext = append_extension.default_extension
                return "{fpath!s}{default_ext!s}".format(fpath=abs_filepath, default_ext=ext)
            else:  # Extension is not missing => return absolute file path
                return abs_filepath

    @staticmethod
    def find_file(basename, file_type):
        """
        Search a file with a given base name and a given file type: checks the existence of all possible file extensions

        Parameters
        ----------
        basename: file basename
        file_type: FileType enum value

        Returns
        -------
        fname: the file name if it actually exists, otherwise returns None.
        """
        FileUtil._check_filename_is_string(basename)
        FileUtil._check_valid_file_type(file_type)

        if file_type.file_regexp.match(basename) is not None:
            if os.path.isfile(basename):
                return basename
        else:
            for ext in file_type.extension_list:
                fname = "{bname!s}{extension!s}".format(bname=basename, extension=ext)
                if os.path.isfile(fname):
                    return fname
        return None

    @staticmethod
    def md5sum(fname):
        """
        Compute the md5 checksum of a given file

        Parameter
        ---------
        fname: `string`
            path of the file
        """
        if not os.path.isfile(fname):
            raise IOError("Cannot process md5sum of the file '{fname!s}': the file does not exist.".format(fname=fname))

        hash_md5 = hashlib.md5()
        # Read file in chunks to compute byte checksum using MD5 algorithm
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    @staticmethod
    def split_fname_extension(filename, file_type):
        """
        Checks a given filename is a valid file name of type 'file_type' and splits the valid filename into a
        (basename, extension) tuple.

        Parameters
        ----------
        filename: ``string``
            file name
        file_type: ``FileType``
            file type

        Returns
        -------
        t: ``tuple``
            (basename, extension) 2-tuple
        """
        FileUtil._check_filename_is_string(filename)
        FileUtil._check_valid_file_type(file_type)

        fname = os.path.basename(filename)
        m = file_type.file_regexp.match(fname)
        if m is not None:
            # Get basename and extension
            return m.group("basename"), m.group("extension")
        else:
            raise AttributeError("'filename' is not a valid {file_type!s} file name.".format(file_type=str(file_type)))

    @staticmethod
    def new_filepath(filename, append_extension, create_dir=True):
        valid_fname = FileUtil.valid_filepath(filename, append_extension)

        file_dir = os.path.dirname(valid_fname)
        if create_dir and not os.path.isdir(file_dir):  # Create directory if it does not exist
            os.makedirs(file_dir)
        return valid_fname

    @staticmethod
    def new_temp_filepath(prefix):
        # Create a temporary file in /tmp/ directory
        today = DatetimeUtil.today()
        temp_file_prefix = ("Astrophysix_{prefix:s}_{year:04d}.{month:02d}.{day:02d}_"
                            "{hour:02d}-{min:02d}-{sec:02d}").format(year=today.year, month=today.month, day=today.day,
                                                                     hour=today.hour, min=today.minute, sec=today.second,
                                                                     prefix=prefix)
        fd, fpath = tempfile.mkstemp(prefix=temp_file_prefix, suffix=".h5")
        os.close(fd)
        return str(fpath)

    @staticmethod
    def locate_file(path, base_directory=None):
        """
        Try to locate a file given its base path and an optional base directory in which to look for an existing file
        with the same filename in any similar subdirectory tree

        Parameters
        ----------
        path: default filepath
        base_directory: Base directory in which an existing file with identical filename must be searched. If None,
        do not search. Default None.

        Returns
        -------
        out_path: found existing filepath, if found. Otherwise returns None.
        """
        FileUtil._check_filename_is_string(path)

        if base_directory is None:  # Do not search in directory
            if os.path.isfile(path):  # File exists => easy, return file path
                return path

            # File does not exist, raises IOError
            raise IOError("Cannot find file '{fname!s}': the file does not exist.".format(fname=path))

        path, fname = os.path.split(path)  # Split directory and filename  e.g. ("/path/to/my/directory/", "file.png")

        # Simple case : look for existing filename in base directory
        out_path = os.path.join(base_directory, fname)
        if os.path.isfile(out_path):  # Found => return path
            return out_path

        # Full directory tree search
        dirs = [d for d in path.split(os.sep) if len(d) > 0]
        for d in dirs[::-1]:
            # Build a similar subdirectory tree path of the filename
            fname = os.path.join(d, fname)

            # Concatenate with the base_directory
            out_path = os.path.join(base_directory, fname)

            if os.path.isfile(out_path):  # Found existing filename in similar subdirectory tree => return path
                return out_path

        # Nothing found => raises IOError
        raise IOError("Cannot find file '{fname!s}' in '{dpath!s}' directory.".format(dpath=path, fname=fname))

    @staticmethod
    def last_modification_timestamp(file_path):
        """Returns the  POSIX timestamp corresponding to the last modification time of a given file"""
        fpath = FileUtil.locate_file(file_path)
        return int(os.path.getmtime(fpath))

    @staticmethod
    def _check_filename_is_string(filepath):
        if not Stringifiable.is_type_string(filepath):
            raise AttributeError("'filepath' attribute must be a valid string. "
                                 "Got '{fname!s}'.".format(fname=filepath))

    @staticmethod
    def _check_valid_file_type(ftype):
        if not isinstance(ftype, FileType):
            raise AttributeError("'file_type' must be a valid FileType enum value.")


class HDF5IOFile(object):
    def save_HDF5(self, *args, **kwargs):
        raise NotImplementedError()

    @classmethod
    def load_HDF5(cls, hdf5_file_path):
        raise NotImplementedError()

    def close(self):
        pass


__all__ = ["FileType", "FileUtil", "HDF5IOFile"]
