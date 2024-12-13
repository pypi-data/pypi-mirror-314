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

.. autoclass:: astrophysix.simdm.datafiles.plot.PlotType
    :members:
    :undoc-members:

.. autoclass:: astrophysix.simdm.datafiles.plot.PlotInfo
    :members:

"""
from __future__ import print_function, unicode_literals, division, absolute_import  # Python 2 and 3 compatibility

import json
import os
import tempfile
import webbrowser

from future.builtins import str, list, int
import logging
import enum
import numpy

from astrophysix.utils.persistency import Hdf5StudyPersistent
from astrophysix.utils.numpy import NumpyUtil
from astrophysix.utils.strings import Stringifiable
from astrophysix import units as U
from ..utils import GalacticaValidityCheckMixin
from ...utils import FileType, FileUtil


log = logging.getLogger("astrophysix.simdm")


@enum.unique
class PlotType(enum.Enum):
    """
    Plot type enum

    Example
    -------
    >>> pt = PlotType.HISTOGRAM_2D
    >>> pt.alias
    "2d_hist"
    >>> pt.display_name
    "2D histogram"
    >>> pt.ndimensions
    2
    """
    LINE_PLOT = ("line", "Line plot", 1, 0)
    SCATTER_PLOT = ("scatter", "Scatter plot", 1, 0)
    HISTOGRAM = ("hist", "Histogram", 1, 1)
    HISTOGRAM_2D = ("2d_hist", "2D histogram", 2, 1)
    IMAGE = ("img", "Image", 2, 1)
    MAP_2D = ("2d_map", "2D map", 2, 1)

    def __init__(self, alias, display_name, ndim, aoffset):
        self._alias = alias
        self._display_name = display_name
        self._ndims = ndim
        self._axis_size_offset = aoffset

    @property
    def display_name(self):
        """Plot type verbose name"""
        return self._display_name

    @property
    def ndimensions(self):
        """Plot type number of dimensions"""
        return self._ndims

    @property
    def axis_size_offset(self):
        return self._axis_size_offset

    @property
    def alias(self):
        """Plot type alias"""
        return self._alias

    @classmethod
    def from_alias(cls, alias):
        """
        Find a PlotType according to its alias

        Parameters
        ----------
        alias: :obj:`string`
            required plot type alias

        Returns
        -------
        ft: :class:`~astrophysix.simdm.datafiles.plot.PlotType`
            Plot type matching the requested alias.

        Raises
        ------
        ValueError
            if requested alias does not match any plot type.

        Example
        -------
            >>> pt = PlotType.from_alias("hist")
            >>> pt.display_name
            "Histogram"
            >>> pt2 = PlotType.from_alias("MY_UNKNOWN_PLOT_YPE")
            ValuerError: No PlotType defined with the alias 'MY_UNKNOWN_PLOT_YPE'.
        """
        for t in cls:
            if t.alias == alias:
                return t
        raise ValueError("No PlotType defined with the alias '{a:s}'.".format(a=alias))

    def __str__(self):
        return self._display_name

    def __repr__(self):
        return self.__str__()


class PlotInfo(Hdf5StudyPersistent, GalacticaValidityCheckMixin, Stringifiable):
    """
    Datafile class (Simulation data model)

    Parameters
    ----------
    plot_type: :class:`~astrophysix.simdm.datafiles.plot.PlotType` or :obj:`string`
        Plot type or plot type alias (mandatory)
    xaxis_values: :class:`numpy.ndarray`
        x-axis coordinate values numpy  1D array (mandatory).
    yaxis_values: :class:`numpy.ndarray`
        y-axis coordinate numpy 1D array (mandatory).
    values: :class:`numpy.ndarray`
        plot data values numpy array (mandatory for 2D plots).
    xlabel: :obj:`string`
        x-axis label
    ylabel: :obj:`string`
        y-axis label
    values_label: :obj:`string`
        plot values label
    xaxis_unit:
        TODO
    yaxis_unit:
        TODO
    values_unit:
        TODO
    xaxis_log_scale: :obj:`bool`
        TODO
    yaxis_log_scale: :obj:`bool`
        TODO
    values_log_scale: :obj:`bool`
        TODO
    plot_title: :obj:`string`
        Plot title.
    """

    VALUES_ATTR_NAME = "values"
    VALUES_MD5SUM_ATTR_NAME = "values_md5sum"
    XAXIS_ATTR_NAME = "xaxis_coords"
    XAXIS_MD5SUM_ATTR_NAME = "xaxis_md5sum"
    YAXIS_ATTR_NAME = "yaxis_coords"
    YAXIS_MD5SUM_ATTR_NAME = "yaxis_md5sum"
    PLOT_DATA_JSON_FPATH = "gald3_plot_data.json"

    def __init__(self, **kwargs):
        """

        :param kwargs:
        """
        super(PlotInfo, self).__init__(**kwargs)

        self._type = PlotType.LINE_PLOT
        self._values = None
        self._xaxis = None
        self._yaxis = None
        self._values_md5sum = None
        self._xaxis_md5sum = None
        self._yaxis_md5sum = None

        self._xlabel = ""
        self._ylabel = ""
        self._vlabel = ""
        self._title = ""

        self._xlog = False
        self._ylog = False
        self._vlog = False

        self._xunit = U.none
        self._yunit = U.none
        self._vunit = U.none

        # Set plot type (mandatory)
        if "plot_type" not in kwargs:
            err_msg = "{cname:s} 'plot_type' attribute is not defined (mandatory).".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

        ptype = kwargs["plot_type"]
        try:
            # Cast from string value (PlotType alias)
            sptype = Stringifiable.cast_string(ptype)
            self._type = PlotType.from_alias(sptype)
        except ValueError as ve:  # unknown PlotType alias
            log.error(str(ve))
            raise AttributeError(str(ve))
        except TypeError:  # Not a valid string
            if not isinstance(ptype, PlotType):
                err_msg = "{cname:s} 'plot_type' attribute is not a valid PlotType enum " \
                          "value.".format(cname=self.__class__.__name__)
                log.error(err_msg)
                raise AttributeError(err_msg)
            self._type = ptype

        # Plot title
        if "title" in kwargs:
            self.title = kwargs["title"]

        if not kwargs.get("hdf5_init", False):
            # X-axis coordinates
            if "xaxis_values" not in kwargs:
                err_msg = "{cname:s} 'xaxis_values' attribute is not defined " \
                          "(mandatory).".format(cname=self.__class__.__name__)
                log.error(err_msg)
                raise AttributeError(err_msg)

            # y-axis coordinates
            if "yaxis_values" not in kwargs:
                err_msg = "{cname:s} 'yaxis_values' attribute is not defined " \
                          "(mandatory).".format(cname=self.__class__.__name__)
                log.error(err_msg)
                raise AttributeError(err_msg)

            # Set data
            self.set_data(kwargs["xaxis_values"], kwargs["yaxis_values"], values=kwargs.get("values", None))

        # X-axis label
        if "xlabel" in kwargs:
            self.xlabel = kwargs["xlabel"]

        # X-axis log-scale flag
        if "xaxis_log_scale" in kwargs:
            self.xaxis_log_scale = kwargs["xaxis_log_scale"]

        # Y-axis log-scale flag + label
        if "yaxis_log_scale" in kwargs:
            self.yaxis_log_scale = kwargs["yaxis_log_scale"]
        if "ylabel" in kwargs:
            self.ylabel = kwargs["ylabel"]

        # 2D plot value log-scale flag + label
        if self._type.ndimensions > 1:
            if "values_log_scale" in kwargs:
                self.values_log_scale = kwargs["values_log_scale"]
            if "values_label" in kwargs:
                self.values_label = kwargs["values_label"]

        # Units
        if "xaxis_unit" in kwargs:
            self.xaxis_unit = kwargs["xaxis_unit"]
        if "yaxis_unit" in kwargs:
            self.yaxis_unit = kwargs["yaxis_unit"]
        if self._type.ndimensions > 1 and "values_unit" in kwargs:
            self.values_unit = kwargs["values_unit"]

    def __eq__(self, other_plot_info):
        """
        PlotInfo comparison method

        Parameters
        ----------
        other_plot_info: :class:`~astrophysix.simdm.datafiles.plot.PlotInfo`
            plot info object to compare to:
        """
        if not super(PlotInfo, self).__eq__(other_plot_info):
            return False

        # Plot type comparison
        if self._type != other_plot_info.plot_type:
            return False

        # Label and title comparison
        if self._title != other_plot_info.title:
            return False

        if self._xlabel != other_plot_info.xlabel:
            return False
        if self._ylabel != other_plot_info.ylabel:
            return False
        if self._type.ndimensions > 1 and self._vlabel != other_plot_info.values_label:
            return False

        # Log-scale flag comparison
        if self._xlog != other_plot_info.xaxis_log_scale:
            return False
        if self._ylog != other_plot_info.yaxis_log_scale:
            return False
        if self._type.ndimensions > 1 and self._vlog != other_plot_info.values_log_scale:
            return False

        # Unit comparison
        if not self._xunit.identical(other_plot_info.xaxis_unit):
            return False
        if not self._yunit.identical(other_plot_info.yaxis_unit):
            return False
        if self._type.ndimensions > 1 and not self._vunit.identical(other_plot_info.values_unit):
            return False

        # MD5 sum comparison
        if self._xaxis_md5sum != other_plot_info._xaxis_md5sum or self._yaxis_md5sum != other_plot_info._yaxis_md5sum:
            return False

        if self._type.ndimensions > 1 and self._values_md5sum != other_plot_info._values_md5sum:
            return False

        return True

    @property
    def plot_type(self):
        """Returns the plot type (:class:`~astrophysix.simdm.datafiles.plot.PlotType`). Cannot be edited."""
        return self._type

    @property
    def title(self):
        """Plot title. Can be set to any :obj:`string` value."""
        return self._title

    @title.setter
    def title(self, new_title):
        try:
            self._title = Stringifiable.cast_string(new_title, valid_empty=True)
        except TypeError:
            err_msg = "{cname:s} 'title' property is not a valid string.".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

    def set_data(self, xaxis_values, yaxis_values, values=None):
        """
        Set plot data arrays.

        Parameters
        ----------
        xaxis_values: :class:`numpy.ndarray`
            x-axis coordinate array
        yaxis_values: :class:`numpy.ndarray`
            TODO
        values: :class:`numpy.ndarray`
            TODO
        """
        # X-axis plot coordinates
        try:
            NumpyUtil.check_is_array(xaxis_values, ndim=1)
        except AttributeError:
            err_msg = "'xaxis_values' {cname:s} attribute must be a 1-dimensional " \
                      "array.".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

        # x-axis coordinate array size
        nx = xaxis_values.size

        # Y-axis plot coordinates
        try:
            NumpyUtil.check_is_array(yaxis_values, ndim=1)
        except AttributeError:
            err_msg = "'yaxis_values' {cname:s} attribute must be a 1-dimensional " \
                      "array.".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

        # Check y-axis coordinate array size
        ny = yaxis_values.size
        if self._type.ndimensions == 1:  # 1D plots
            ny_target = nx - self._type.axis_size_offset
            if ny != ny_target:
                raise AttributeError("Array size mismatch : 'yaxis_values' coordinate array size should be {siz:d} "
                                     "(x-axis coordinate array size={nx:d}) for '{pt!s}'.".format(siz=ny_target, nx=nx,
                                                                                                  pt=self._type))

        # Plot values
        if self._type.ndimensions > 1:
            if values is None:
                err_msg = "{cname:s} 'values' attribute is not defined (mandatory for 2D " \
                          "plots).".format(cname=self.__class__.__name__)
                log.error(err_msg)
                raise AttributeError(err_msg)

            try:
                NumpyUtil.check_is_array(values, self._type.ndimensions)
            except AttributeError:
                raise AttributeError("{cname:s} 'values' attribute must be a {nd:d}-dimensional "
                                     "array.".format(cname=self.__class__.__name__, nd=self._type.ndimensions))

            nvx = nx - self._type.axis_size_offset
            nvy = ny - self._type.axis_size_offset
            if values.shape[0] != nvx or values.shape[1] != nvy:
                raise AttributeError("Array size mismatch : 'values' array (shape={sht!s}) should have a shape "
                                     "({nvx:d}, {nvy:d}) (x-axis coordinate array size={nx:d} ; y-axis coordinate "
                                     "array size={ny:d}) for '{pt!s}'.".format(sht=values.shape, nvx=nvx, nvy=nvy,
                                                                               nx=nx, ny=ny, pt=self._type))

        # ------------------------------------------ Set new data ---------------------------------------------------- #
        # Compute the md5 checksum of a the new value array
        self._xaxis = xaxis_values
        self._xaxis_md5sum = NumpyUtil.md5sum(xaxis_values)
        self._yaxis_md5sum = NumpyUtil.md5sum(yaxis_values)
        self._yaxis = yaxis_values
        self._values = values if self._type.ndimensions > 1 else None
        self._values_md5sum = NumpyUtil.md5sum(values) if self._type.ndimensions > 1 else None

        # Flag the PlotInfo object as 'loaded in memory' to avoid reading data from HDF5 study file in the future
        self._hsp_set_lazy_read()
        # ------------------------------------------------------------------------------------------------------------ #

    @property
    def xaxis_values(self):
        """
        Plot x-axis coordinate array (:class:`numpy.ndarray`). Cannot be edited. Implements lazy I/O.

        Note
        ----
            To edit plot values, see :func:`PlotInfo.set_data` method.
        """
        self._hsp_lazy_read()
        return self._xaxis

    @property
    def yaxis_values(self):
        """
        Plot y-axis coordinate array (:class:`numpy.ndarray`). Cannot be edited. Implements lazy I/O.

        Note
        ----
            To edit plot values, see :func:`PlotInfo.set_data` method.
        """
        self._hsp_lazy_read()
        return self._yaxis

    @property
    def values(self):
        """
        Plot values array. Cannot be edited. Implements lazy I/O.

        Note
        ----
            To edit plot values, see :func:`PlotInfo.set_data` method.
        """
        if self._type.ndimensions > 1:
            self._hsp_lazy_read()
            return self._values
        else:
            raise AttributeError("{cname:s} object does not have a 'values' "
                                 "property.".format(cname=self.__class__.__name__))

    @property
    def xlabel(self):
        """x-axis label. Can be set to any :obj:`string` value."""
        return self._xlabel

    @xlabel.setter
    def xlabel(self, new_xaxis_label):
        try:
            self._xlabel = Stringifiable.cast_string(new_xaxis_label, valid_empty=True)
        except TypeError:
            err_msg = "{cname:s} 'xlabel' property is not a valid string.".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

    @property
    def ylabel(self):
        """y-axis label. Can be set to any :obj:`string` value."""
        return self._ylabel

    @ylabel.setter
    def ylabel(self, new_yaxis_label):
        try:
            self._ylabel = Stringifiable.cast_string(new_yaxis_label, valid_empty=True)
        except TypeError:
            err_msg = "{cname:s} 'ylabel' property is not a valid string.".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

    @property
    def values_label(self):
        """plot values label. Can be set to any :obj:`string` value."""
        if self._type.ndimensions < 2:
            raise AttributeError("{cname:s} object does not have a 'values_label' "
                                 "property.".format(cname=self.__class__.__name__))
        return self._vlabel

    @values_label.setter
    def values_label(self, new_vlabel):
        if self._type.ndimensions < 2:
            raise AttributeError("{cname:s} object does not have a 'values_label' "
                                 "property.".format(cname=self.__class__.__name__))

        try:
            self._vlabel = Stringifiable.cast_string(new_vlabel, valid_empty=True)
        except TypeError:
            err_msg = "{cname:s} 'values_label' property is not a valid string.".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

    @property
    def xaxis_unit(self):
        """TODO"""
        return self._xunit

    @xaxis_unit.setter
    def xaxis_unit(self, new_xaxis_unit):
        if isinstance(new_xaxis_unit, U.Unit):
            self._xunit = new_xaxis_unit
        else:
            try:
                s = Stringifiable.cast_string(new_xaxis_unit, valid_empty=False)
                self._xunit = U.Unit.from_name(s)
            except TypeError:  # Not a valid string
                err_msg = "{cname:s} 'xaxis_unit' property is not a valid (non-empty) " \
                          "string.".format(cname=self.__class__.__name__)
                log.error(err_msg)
                raise AttributeError(err_msg)
            except AttributeError as aerr:
                err_msg = "{cname:s} 'xaxis_unit' property error : {uerr:s}.".format(uerr=str(aerr),
                                                                                     cname=self.__class__.__name__)
                log.error(err_msg)
                raise AttributeError(err_msg)

    @property
    def yaxis_unit(self):
        """TODO"""
        return self._yunit

    @yaxis_unit.setter
    def yaxis_unit(self, new_yaxis_unit):
        if isinstance(new_yaxis_unit, U.Unit):
            self._yunit = new_yaxis_unit
        else:
            try:
                s = Stringifiable.cast_string(new_yaxis_unit, valid_empty=False)
                self._yunit = U.Unit.from_name(s)
            except TypeError:  # Not a valid string
                err_msg = "{cname:s} 'yaxis_unit' property is not a valid (non-empty) " \
                          "string.".format(cname=self.__class__.__name__)
                log.error(err_msg)
                raise AttributeError(err_msg)
            except AttributeError as aerr:
                err_msg = "{cname:s} 'yaxis_unit' property error : {uerr:s}.".format(uerr=str(aerr),
                                                                                     cname=self.__class__.__name__)
                log.error(err_msg)
                raise AttributeError(err_msg)

    @property
    def values_unit(self):
        """TODO"""
        if self._type.ndimensions < 2:
            raise AttributeError("{cname:s} object does not have a 'values_unit' "
                                 "property.".format(cname=self.__class__.__name__))

        return self._vunit

    @values_unit.setter
    def values_unit(self, new_vunit):
        if self._type.ndimensions < 2:
            raise AttributeError("{cname:s} object does not have a 'values_unit' "
                                 "property.".format(cname=self.__class__.__name__))

        if isinstance(new_vunit, U.Unit):
            self._vunit = new_vunit
        else:
            try:
                s = Stringifiable.cast_string(new_vunit, valid_empty=False)
                self._vunit = U.Unit.from_name(s)
            except TypeError:  # Not a valid string
                err_msg = "{cname:s} 'values_unit' property is not a valid (non-empty) " \
                          "string.".format(cname=self.__class__.__name__)
                log.error(err_msg)
                raise AttributeError(err_msg)
            except AttributeError as aerr:
                err_msg = "{cname:s} 'values_unit' property error : {uerr:s}.".format(uerr=str(aerr),
                                                                                      cname=self.__class__.__name__)
                log.error(err_msg)
                raise AttributeError(err_msg)

    @property
    def xaxis_log_scale(self):
        """x-axis log scale boolean flag. Can be edited to any :obj:`bool` value."""
        return self._xlog

    @xaxis_log_scale.setter
    def xaxis_log_scale(self, new_log):
        if not isinstance(new_log, bool):
            err_msg = "'xaxis_log_scale' {cname:s} property must be a boolean " \
                      "value.".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)
        self._xlog = new_log

    @property
    def yaxis_log_scale(self):
        """y-axis log scale boolean flag. Can be edited to any :obj:`bool` value."""
        return self._ylog

    @yaxis_log_scale.setter
    def yaxis_log_scale(self, new_log):
        if not isinstance(new_log, bool):
            err_msg = "'yaxis_log_scale' {cname:s} property must be a boolean " \
                      "value.".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)
        self._ylog = new_log

    @property
    def values_log_scale(self):
        """value log scale boolean flag. Can be edited to any :obj:`bool` value."""
        if self._type.ndimensions < 2:
            raise AttributeError("{cname:s} object does not have a 'values_log_scale' "
                                 "property.".format(cname=self.__class__.__name__))
        return self._vlog

    @values_log_scale.setter
    def values_log_scale(self, new_log):
        if self._type.ndimensions < 2:
            raise AttributeError("{cname:s} object does not have a 'values_log_scale' "
                                 "property.".format(cname=self.__class__.__name__))

        if not isinstance(new_log, bool):
            err_msg = "'values_log_scale' {cname:s} property must be a boolean " \
                      "value.".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)
        self._vlog = new_log

    def _export_to_json(self, fpath):
        """
        Export plot information to a dict and dump it into a JSON file
        :param fpath: JSON file path
        """
        json_data = {"type": self._type.alias, "title": self._title, "xaxis_log": self._xlog, "yaxis_log": self._ylog,
                     "xaxis_label": self._xlabel, "yaxis_label": self._ylabel,
                     "xaxis_unit": self._xunit.latex, "yaxis_unit": self._yunit.latex}
        if self._type == PlotType.HISTOGRAM_2D:
            json_data.update({"xaxis_coordinates": list(self._xaxis), "yaxis_coordinates": list(self._yaxis)})
            vals = []
            mnan = numpy.isnan(self._values)
            for i in range(self._xaxis.size - self._type.axis_size_offset):
                for j in range(self._yaxis.size - self._type.axis_size_offset):
                    if not mnan[i, j]:
                        vals.append([i, j, self._values[i, j]])
            json_data["values"] = vals
            json_data["value_log"] = self._vlog
            json_data["value_label"] = self._vlabel
            json_data["value_unit"] = self._vunit.latex
        elif self._type == PlotType.HISTOGRAM:
            json_data.update({"xaxis_coordinates": list(self._xaxis), "values": list(self._yaxis)})
        elif self._type == PlotType.LINE_PLOT:
            json_data.update({"xaxis_coordinates": list(self._xaxis), "values": list(self._yaxis)})
        else:
            raise NotImplementedError()

        with open(fpath, "w") as f:
            json.dump(json_data, f)
        log.info("File '{fp:s}' saved.".format(fp=fpath))

    def save_json_plot_data(self, json_filepath):
        """
        Save plot information into an external JSON file on the local filesystem

        Parameters
        ----------
        json_filepath: :obj:`string`
            valid external JSON file path
        """
        file_path = Stringifiable.cast_string(json_filepath, valid_empty=False)
        fpath = FileUtil.new_filepath(file_path, FileType.JSON_FILE, create_dir=True)
        ftype = FileUtil.get_file_type(json_filepath)
        if ftype != FileType.JSON_FILE:
            err_msg = "Invalid filename for a {ft:s} file ({fp!s}).".format(ft=FileType.JSON_FILE.alias,
                                                                            fp=json_filepath)
            log.error(err_msg)
            raise AttributeError(err_msg)

        # Force file data loading if not already read from HDF5 file
        self._hsp_lazy_read()

        # Do the actual file saving operation...
        self._export_to_json(fpath)

        return fpath

    def gald3_render(self, open_browser=True, local_http_port=8076):
        """
        Exports the PlotInfo object into a temporary JSON file and opens a web browser window to render it using the
        Galactica GalD3.js javascript library.

        Parameters
        ----------
        open_browser: : obj:`bool`
            open a web browser window. Default True. Set to False if already opened
        local_http_port: :obj:`int`
            localhost http port to use in the URL
        """
        f, tfpath = tempfile.mkstemp(prefix="d3_temp_plot_data_", suffix=".json", text=True)
        self.save_json_plot_data(tfpath)
        tmp_http_fpath = os.path.join(tempfile.gettempdir(), PlotInfo.PLOT_DATA_JSON_FPATH)
        if os.path.islink(tmp_http_fpath):
            old_plot_data_file = os.readlink(tmp_http_fpath)
            log.info("Deleting link to temporary JSON data file '{fp:s}'.".format(fp=old_plot_data_file))
            os.remove(tmp_http_fpath)
            os.remove(old_plot_data_file)

        log.info("Creating new symlink to temporary JSON data file '{fp:s}'.".format(fp=tfpath))
        os.symlink(tfpath, tmp_http_fpath)
        log.info("Opening browser to url : http://127.0.0.1:{p:d}/chart".format(p=local_http_port))
        if open_browser:
            webbrowser.open("http://127.0.0.1:{p:d}/chart".format(p=local_http_port))

    @classmethod
    def _hsp_valid_attributes(cls):
        """List of valid kwargs in __init__() method"""
        return ["plot_type", "title", "hdf5_init", "xaxis_values", "yaxis_values", "values", "xlabel", "ylabel",
                "xaxis_log_scale", "yaxis_log_scale", "values_log_scale", "values_label",
                "xaxis_unit", "yaxis_unit", "values_unit"]

    def _hsp_write(self, h5group, **kwargs):
        """
        Serialize a PlotInfo object into a HDF5 file.

        Parameters
        ----------
        h5group: ``h5py.Group``
            Main group to write the PlotInfo into.
        kwargs: ``dict``
            keyword argument dictionary.
        """
        # Call to parent class _hsp_write() : write UUID, etc.
        super(PlotInfo, self)._hsp_write(h5group, **kwargs)

        # -------------------------------- Write datafile plot info info to HDF5 ------------------------------------- #
        # Write plot type
        self._hsp_write_attribute(h5group, ("plot_type", self._type.alias), **kwargs)

        # Write labels (x-axis/y-axis/values/title)
        if self._type.ndimensions > 1:
            self._hsp_write_attribute(h5group, ("vlabel", self._vlabel), **kwargs)
        self._hsp_write_attribute(h5group, ("xlabel", self._xlabel), **kwargs)
        self._hsp_write_attribute(h5group, ("ylabel", self._ylabel), **kwargs)
        self._hsp_write_attribute(h5group, ("title", self._title), **kwargs)

        # Write log-scale flags (x-axis/y-axis/value)
        self._hsp_write_attribute(h5group, ("xlog", self._xlog), **kwargs)
        self._hsp_write_attribute(h5group, ("ylog", self._ylog), **kwargs)
        if self._type.ndimensions > 1:
            self._hsp_write_attribute(h5group, ("vlog", self._vlog), **kwargs)

        # Write units
        self._hsp_write_attribute(h5group, ("xunit", self._xunit), **kwargs)
        self._hsp_write_attribute(h5group, ("yunit", self._yunit), **kwargs)
        if self._type.ndimensions > 1:
            self._hsp_write_attribute(h5group, ("vunit", self._vunit), **kwargs)

        # Write array MD5 sums
        write_values = False
        if self._type.ndimensions > 1:
            values_attribute_name = "_values"  # => self._values
            write_values = self._hsp_write_dataset(h5group, (self.VALUES_ATTR_NAME, values_attribute_name),
                                                   md5sum_params=(self.VALUES_MD5SUM_ATTR_NAME, self._values_md5sum),
                                                   **kwargs)
        xaxis_attribute_name = "_xaxis"  # => self._xaxis
        write_xaxis = self._hsp_write_dataset(h5group, (self.XAXIS_ATTR_NAME, xaxis_attribute_name),
                                              md5sum_params=(self.XAXIS_MD5SUM_ATTR_NAME, self._xaxis_md5sum),
                                              **kwargs)
        yaxis_attribute_name = "_yaxis"  # => self._yaxis
        write_yaxis = self._hsp_write_dataset(h5group, (self.YAXIS_ATTR_NAME, yaxis_attribute_name),
                                              md5sum_params=(self.YAXIS_MD5SUM_ATTR_NAME, self._yaxis_md5sum),
                                              **kwargs)

        if write_values or write_xaxis or write_yaxis:
            self._hsp_write_callback(str(self), **kwargs)
        # ------------------------------------------------------------------------------------------------------------ #

    @classmethod
    def _hsp_read(cls, h5group, version, dependency_objdict=None):
        """
        Read a PlotInfo object from a HDF5 file (*.h5).

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
        pi: ``PlotInfo``
            Read PlotInfo instance
        """
        # Handle different versions here

        # Fetch Hdf5StudyPersistent object UUID
        uid = super(PlotInfo, cls)._hsp_read(h5group, version, dependency_objdict=dependency_objdict)

        # Read plot type and title
        title = cls._hsp_read_attribute(h5group, "title", "plot title")
        ptype = PlotType.from_alias(cls._hsp_read_attribute(h5group, "plot_type", "plot type"))

        # Read labels (x-axis/y-axis/values/title)
        xlabel = cls._hsp_read_attribute(h5group, "xlabel", "x-axis label")
        ylabel = cls._hsp_read_attribute(h5group, "ylabel", "y-axis label")
        kw = {"uid": uid, "plot_type": ptype, "title": title, "xlabel": xlabel, "ylabel": ylabel, "hdf5_init": True}
        if ptype.ndimensions > 1:
            vlabel = cls._hsp_read_attribute(h5group, "vlabel", "plot values label")
            if vlabel is not None:
                kw["values_label"] = vlabel

        # Read log-scale flags
        kw["xaxis_log_scale"] = bool(cls._hsp_read_attribute(h5group, "xlog", "x-axis log-scale flag"))
        kw["yaxis_log_scale"] = bool(cls._hsp_read_attribute(h5group, "ylog", "y-axis log-scale flag"))
        if ptype.ndimensions > 1:
            vlog = cls._hsp_read_attribute(h5group, "vlog", "values log-scale flag")
            if vlog is not None:
                kw["values_log_scale"] = bool(vlog)

        # Read units
        kw["xaxis_unit"] = cls._hsp_read_unit(h5group, "xunit")
        kw["yaxis_unit"] = cls._hsp_read_unit(h5group, "yunit")
        if ptype.ndimensions > 1:
            kw["values_unit"] = cls._hsp_read_unit(h5group, "vunit")

        pinfo = cls(**kw)

        # Read x-axis/y-axis/value array md5sum
        if ptype.ndimensions > 1:
            pinfo._values_md5sum = pinfo._hsp_read_attribute(h5group, cls.VALUES_MD5SUM_ATTR_NAME,
                                                             "plot info value array md5sum",
                                                             raise_error_if_not_found=True)
        pinfo._xaxis_md5sum = pinfo._hsp_read_attribute(h5group, cls.XAXIS_MD5SUM_ATTR_NAME,
                                                        "plot info x-axis coordinate array md5sum",
                                                        raise_error_if_not_found=True,)
        pinfo._yaxis_md5sum = pinfo._hsp_read_attribute(h5group, cls.YAXIS_MD5SUM_ATTR_NAME,
                                                        "plot info y-axis coordinate/value array md5sum",
                                                        raise_error_if_not_found=True)

        # Set HDF5 group/file info for lazy I/O
        pinfo._hsp_set_lazy_source(h5group)

        return pinfo

    def _hsp_lazy_read_data(self, h5group):
        """
        Lazy read method to load plot values + PIL image from HDF5 file (*.h5)

        Parameters
        ----------
        h5group: `h5py.Group`
        """
        # Read coord/value arrays
        if self._type.ndimensions > 1:
            self._values = self._hsp_read_dataset(h5group, self.VALUES_ATTR_NAME, "plot info value array",
                                                  raise_error_if_not_found=True)
        self._xaxis = self._hsp_read_dataset(h5group, self.XAXIS_ATTR_NAME, "plot info x-axis coordinate array",
                                             raise_error_if_not_found=True)
        self._yaxis = self._hsp_read_dataset(h5group, self.YAXIS_ATTR_NAME, "plot info y-axis coordinate/value array",
                                             raise_error_if_not_found=True)

    def galactica_validity_check(self, **kwargs):
        """
        Perform validity checks on this  instance and eventually log warning messages.

        Parameters
        ----------
        kwargs: `dict`
            keyword arguments (optional)
        """
        # TODO Galactica validity check for PlotInfo
        pass

    def __unicode__(self):
        """
        String representation of the instance
        """
        s = "[{tname:s}] plot information".format(tname=self._type.name)
        return s


__all__ = ["PlotType", "PlotInfo"]
