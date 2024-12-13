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

import filecmp

from future.builtins import str, dict
import pytest
import numpy as N
import logging
import os

from astrophysix.simdm import SimulationStudy, ProjectCategory, Project
from astrophysix.simdm.datafiles import Datafile, PlotType, PlotInfo, image, file
from astrophysix.simdm.experiment import Simulation
from astrophysix.simdm.protocol import SimulationCode
from astrophysix.simdm.results import GenericResult
from astrophysix.utils import DatetimeUtil
from astrophysix import units as U
from astrophysix.utils.file import FileType, FileUtil


class TestFileType(object):
    def test_from_key_exceptions(self):
        """
        Tests exceptions raised by FileType.from_alias(method)
        """
        # Check unknown file type
        with pytest.raises(ValueError, match="No FileType defined with the alias 'PLOUC'."):
            ft = FileType.from_alias("PLOUC")

    def test_init(self):
        """
        Tests valid FileType initialisation from aliases
        """
        assert FileType.from_alias("HDF5") == FileType.HDF5_FILE
        assert FileType.from_alias("PNG") == FileType.PNG_FILE
        assert FileType.from_alias("JPEG") == FileType.JPEG_FILE
        assert FileType.from_alias("FITS") == FileType.FITS_FILE
        assert FileType.from_alias("TARGZ") == FileType.TARGZ_FILE
        assert FileType.from_alias("PICKLE") == FileType.PICKLE_FILE
        assert FileType.from_alias("JSON") == FileType.JSON_FILE
        assert FileType.from_alias("CSV") == FileType.CSV_FILE
        assert FileType.from_alias("ASCII") == FileType.ASCII_FILE
        assert FileType.from_alias("YAML") == FileType.YAML_FILE
        assert FileType.from_alias("XML") == FileType.XML_FILE

        # Default HDF5 file extension
        assert FileType.HDF5_FILE.default_extension == ".h5"

        # Pickle file extension regular expression
        assert FileType.PICKLE_FILE.file_regexp.pattern == "(?P<basename>.+)\\.(?P<extension>(pkl|PKL|pickle|sav|save))$"

        # Test valid extension
        assert '.JSON' in FileType.JSON_FILE.extension_list
        assert ".YAML" in FileType.YAML_FILE.extension_list


class TestDatafile(object):
    def test_datafile_init(self):
        """
        Tests Datafile instance initialisation
        """
        # Datafile initialisation
        df = Datafile(name="Gas surface density", description="Gas surface density map of the galactic disk (face on)")
        df[FileType.PNG_FILE] = os.path.join(os.path.dirname(__file__), "io", "datafiles", "CEA.png")

        assert df.name == "Gas surface density"
        assert df.description == "Gas surface density map of the galactic disk (face on)"
        assert df[FileType.PNG_FILE].file_md5sum == "daa130ec42abe0851f78dc73e27900bc"
        assert df[FileType.PNG_FILE].filename == "CEA.png"

        # Test str() conversion
        assert str(df) == "[Gas surface density] datafile"

    def test_setting_datafile_name(self):
        """
        Tests that a datafile defined without name raises an exception
        """
        # Tests datafile defined without name
        with pytest.raises(AttributeError) as e:
            datafile_exc = Datafile()  # No simulation code name defined
        assert str(e.value) == "Datafile 'name' attribute is not defined (mandatory)."

        df = Datafile(name="My plot")

        # ------------- Tests invalid datafile name setting exception ---------------------- #
        empty_protocol_name_err = "Datafile 'name' property is not a valid (non-empty) string."
        with pytest.raises(AttributeError) as e:
            df.name = [-1, 2, 10.5, "Galaxy"]
        assert str(e.value) == empty_protocol_name_err

        with pytest.raises(AttributeError) as e:
            df.name = ""
        assert str(e.value) == empty_protocol_name_err
        # ----------------------------------------------------------------------------------- #

        # Valid => should not raise any exception
        df.name = "The best plot ever published"

    def test_setting_datafile_description(self):
        """
        Tests setting datafile description property
        """
        datafile = Datafile(name="Favorite plot", description="Description of my datafile")
        #
        # ------------------------ Tests invalid datafile description setting exception ------------------------------ #
        with pytest.raises(AttributeError) as e:
            datafile.description = 0
        assert str(e.value) == "Datafile 'description' property is not a valid string."
        # ------------------------------------------------------------------------------------------------------------ #

        # Valid => should not raise any exception
        datafile.description = "Description of the best datafile in the world"

    def test_setting_datafile_plot_info(self):
        """
        Tests setting datafile plot_info property
        """
        df = Datafile(name="Favorite plot")

        # ------------------------ Tests invalid datafile description setting exception ------------------------------ #
        with pytest.raises(AttributeError, match="Datafile 'plot_info' property is not a valid PlotInfo object."):
            df.plot_info = {"Garbage": 102.5}
        # ------------------------------------------------------------------------------------------------------------ #

        # Valid => should not raise any exception
        df.plot_info = PlotInfo(plot_type=PlotType.LINE_PLOT, xaxis_values=N.array([10.0, 20.0, 30.0]),
                                yaxis_values=N.array([1.2, 35.2, 14.9]))

    def test_setting_associated_file(self):
        """
        Add associated files into datafile and tries to get/delete them
        """
        df = Datafile(name="My best datafile")

        # Tests associated file getter and setter
        with pytest.raises(KeyError, match="Datafile 'Salut' key is not a valid FileType index."):
            df["Salut"] = 3.1459

        # Not a valid AssociatedFile object or file path
        with pytest.raises(ValueError,
                           match="Only file paths or PngImageFile objects can be set in Datafile as PNG files."):
            df[FileType.PNG_FILE] = 3.14159

        # Set JPEG file path as PNG file => type mismatch
        jpeg_filepath = os.path.join(os.path.dirname(__file__), "io", "datafiles", "irfu_simple.jpg")
        with pytest.raises(ValueError, match="Datafile associated file type mismatch : expected PngImageFile object "
                                             "but JpegImageFile was provided."):
            df[FileType.PNG_FILE] = image.JpegImageFile.load_file(jpeg_filepath)
        with pytest.raises(AttributeError, match="Invalid filename for a PNG file "
                                                 "\\({fp:s}\\).".format(fp=jpeg_filepath)):
            df[FileType.PNG_FILE] = jpeg_filepath

        # Actually works now it has been implemented...
        # with pytest.raises(NotImplementedError, match="Cannot attach PICKLE file to datafile !"):
        #     df[FileType.PICKLE_FILE] = "/path/to/pickle/file"

        # Valid calls to setter
        df[FileType.PNG_FILE] = os.path.join(os.path.dirname(__file__), "io", "datafiles", "CEA.png")
        df[FileType.JPEG_FILE] = jpeg_filepath
        df[FileType.FITS_FILE] = os.path.join(os.path.dirname(__file__), "io", "datafiles",
                                              "cassiopea_A_0.5-1.5keV.fits")
        df[FileType.TARGZ_FILE] = os.path.join(os.path.dirname(__file__), "io", "datafiles", "archive.tar.gz")
        df[FileType.JSON_FILE] = file.JsonFile.load_file(os.path.join(os.path.dirname(__file__), "io", "datafiles",
                                                                      "test_header_249.json"))
        df[FileType.ASCII_FILE] = os.path.join(os.path.dirname(__file__), "io", "datafiles", "abstract.txt")
        df[FileType.HDF5_FILE] = os.path.join(os.path.dirname(__file__), "io", "python_3", "study.h5")
        df[FileType.YAML_FILE] = os.path.join(os.path.dirname(__file__), "io", "datafiles", "config.yml")
        df[FileType.PICKLE_FILE] = os.path.join(os.path.dirname(__file__), "io", "datafiles", "dict_saved.pkl")

        # Invalid FileType in delitem
        with pytest.raises(KeyError, match="Datafile 'key_1' key is not a valid FileType index."):
            del df["key_1"]

        # Remove PNG image file => should be ok
        del df[FileType.PNG_FILE]
        # Try to remove a PNG file once again, already done that...
        with pytest.raises(KeyError, match="No PNG file is associated to the \\[My best datafile\\] datafile."):
            del df[FileType.PNG_FILE]

        # Invalid FileType in getter
        with pytest.raises(KeyError, match="Datafile 'key_1' key is not a valid FileType index."):
            f = df["key_1"]

        # FileType key not found in getter
        with pytest.raises(KeyError, match="No PNG file is associated to the \\[My best datafile\\] datafile."):
            f = df[FileType.PNG_FILE]

        jpeg = df[FileType.JPEG_FILE]
        assert jpeg.filename == "irfu_simple.jpg" and isinstance(jpeg, image.JpegImageFile)
        json_file = df[FileType.JSON_FILE]
        assert json_file.filename == "test_header_249.json" and isinstance(json_file, file.JsonFile)

    def test_datafile_associated_file_export(self, tmp_path, caplog):
        """
        Tests exporting associated file back into external file

        Parameters
        ----------
        tmp_path: temporary path  PyTest fixture
        caplog: captured log PyTest fixture
        """
        df = Datafile(name="My best datafile")

        # Add pickle file and export it, check modification time and perform diff comparison
        orig_pkl_fpath = os.path.join(os.path.dirname(__file__), "io", "datafiles", "dict_saved.pkl")
        df[FileType.PICKLE_FILE] = orig_pkl_fpath
        # Valid but should log an info message
        tmp_fpath = str(tmp_path / df[FileType.PICKLE_FILE].filename)
        fpath = df[FileType.PICKLE_FILE].save_to_disk(tmp_fpath)
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.INFO,
                                            "File '{tfp:s}' saved.".format(tfp=tmp_fpath))
        assert DatetimeUtil.utc_from_timestamp(FileUtil.last_modification_timestamp(fpath)) == \
               df[FileType.PICKLE_FILE].last_modified
        assert filecmp.cmp(fpath, orig_pkl_fpath, shallow=False)

        # Add tar.gz file and export it, check modification time and perform diff comparison
        orig_tar_gz_fpath = os.path.join(os.path.dirname(__file__), "io", "datafiles", "archive.tar.gz")
        df[FileType.TARGZ_FILE] = orig_tar_gz_fpath
        tmp_fpath = str(tmp_path / df[FileType.TARGZ_FILE].filename)
        fpath = df[FileType.TARGZ_FILE].save_to_disk(tmp_fpath)
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.INFO,
                                            "File '{tfp:s}' saved.".format(tfp=tmp_fpath))
        assert DatetimeUtil.utc_from_timestamp(FileUtil.last_modification_timestamp(fpath)) == \
               df[FileType.TARGZ_FILE].last_modified
        assert filecmp.cmp(fpath, orig_tar_gz_fpath, shallow=False)

        # Add png file and export it, check modification time and perform diff comparison
        orig_png_fpath = os.path.join(os.path.dirname(__file__), "io", "datafiles", "CEA.png")
        df[FileType.PNG_FILE] = orig_png_fpath
        tmp_fpath = str(tmp_path / df[FileType.PNG_FILE].filename)
        fpath = df[FileType.PNG_FILE].save_to_disk(tmp_fpath)
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.INFO,
                                            "File '{tfp:s}' saved.".format(tfp=tmp_fpath))
        assert DatetimeUtil.utc_from_timestamp(FileUtil.last_modification_timestamp(fpath)) == \
               df[FileType.PNG_FILE].last_modified
        assert filecmp.cmp(fpath, orig_png_fpath, shallow=False)

    def test_datafile_equality(self):
        """
        Tests Datafile rich-comparison method Datafile.__eq__()
        """
        df = Datafile(name="Most important datafile",
                      description="This is the best plot ever in the history of Science")

        # Different UUID => not equals
        assert df != Datafile(name=df.name, description=df.description)

        # Different name => not equals
        assert df != Datafile(name="Other name", description=df.description, uid=df.uid)

        # Different description => not equals
        assert df != Datafile(name=df.name, description="Other description", uid=df.uid)

        # Identical datafiles
        df2 = Datafile(name=df.name, description=df.description, uid=df.uid)
        assert df2 == df

        # Plot info comparison
        df.plot_info = PlotInfo(plot_type=PlotType.LINE_PLOT, xaxis_values=N.array([10.0, 20.0, 30.0]),
                                yaxis_values=N.array([1.2, 35.2, 14.9]))
        df2.plot_info = PlotInfo(plot_type=PlotType.HISTOGRAM, xaxis_values=N.array([5.0, 15.0, 25.0, 35.0]),
                                 yaxis_values=N.array([1.25, 5.12, 4.79]))
        assert df != df2
        df.plot_info = df2.plot_info
        assert df == df2

        # Add associated files
        jpeg_fpath = os.path.join(os.path.dirname(__file__), "io", "datafiles", "irfu_simple.jpg")
        png_fpath = os.path.join(os.path.dirname(__file__), "io", "datafiles", "CEA.png")
        df[FileType.PNG_FILE] = image.PngImageFile.load_file(png_fpath)
        df2[FileType.JPEG_FILE] = jpeg_fpath
        assert df != df2
        df[FileType.JPEG_FILE] = image.JpegImageFile.load_file(jpeg_fpath)
        assert df != df2
        df2[FileType.PNG_FILE] = png_fpath
        assert df == df2

    def test_datafile_galactica_validity_checks(self, caplog):
        """
        Tests datafile Galactica validity checks

        Parameters
        ----------
        caplog: captured log PyTest fixture
        """
        df = Datafile(name="Most important datafile")

        # No name defined => should never happen
        # [...]

        # Datafile name too long
        df.name = "This is an overkill long name for the most important datafile ever. xxxxxxxxxxxxxxxxxxxxxxxxxxxx " \
                  "yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"
        df.galactica_validity_check()
        assert caplog.record_tuples[-1] == ('astrophysix.simdm', logging.WARNING,
                                            "[This is an overkill long name for the most important datafile ever. xx"
                                            "xxxxxxxxxxxxxxxxxxxxxxxxxx yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy] "
                                            "datafile name is too long for Galactica (max. 128 characters).")

    def test_datafile_hdf5_io(self, tmp_path):
        """
        Tests saving/loading Datafile from HDF5 file

        Parameters
        ----------
        tmp_path: temporary path  PyTest fixture
        """
        # Dummy project
        ramses = SimulationCode(name="Ramses 3 (MHD)", code_name="Ramses")
        simu = Simulation(simu_code=ramses, name="My simu énorme")
        proj = Project(category=ProjectCategory.GalacticDynamics, project_title="My project")
        proj.simulations.add(simu)

        res = GenericResult(name="Key result !")
        simu.generic_results.add(res)
        df = res.datafiles.add(Datafile(name="My datafile"))

        # Add tar.gz file
        targz_fpath = os.path.join(os.path.dirname(__file__), "io", "datafiles", "archive.tar.gz")
        df[FileType.TARGZ_FILE] = targz_fpath
        # Add png file
        png_fpath = os.path.join(os.path.dirname(__file__), "io", "datafiles", "CEA.png")
        df[FileType.PNG_FILE] = png_fpath

        # Save study
        fname = str(tmp_path / "study.h5")
        study = SimulationStudy(project=proj)
        study.save_HDF5(fname)

        # Reload study
        study_loaded = SimulationStudy.load_HDF5(fname)
        simu_loaded = study_loaded.project.simulations[simu.name]

        # Compare datafiles
        res_loaded = simu_loaded.generic_results[res.name]
        df_loaded = res_loaded.datafiles[df.name]
        assert df == df_loaded

        # Export associated files and perform diff comparison
        tmp_fpath_targz = str(tmp_path / df_loaded[FileType.TARGZ_FILE].filename)
        fpath = df_loaded[FileType.TARGZ_FILE].save_to_disk(tmp_fpath_targz)
        assert DatetimeUtil.utc_from_timestamp(FileUtil.last_modification_timestamp(fpath)) == \
               df[FileType.TARGZ_FILE].last_modified
        assert filecmp.cmp(fpath, targz_fpath, shallow=False)
        tmp_fpath_png = str(tmp_path / df_loaded[FileType.PNG_FILE].filename)
        fpath = df_loaded[FileType.PNG_FILE].save_to_disk(tmp_fpath_png)
        assert DatetimeUtil.utc_from_timestamp(FileUtil.last_modification_timestamp(fpath)) == \
               df[FileType.PNG_FILE].last_modified
        assert filecmp.cmp(fpath, png_fpath, shallow=False)

        # ------------------------------------------------------------------------------------------------------------ #
        # Try to add a new JPEG associated file in the loaded study and saves it again
        jpeg_fpath = os.path.join(os.path.dirname(__file__), "io", "datafiles", "irfu_simple.jpg")
        df_loaded[FileType.JPEG_FILE] = jpeg_fpath
        fname2 = str(tmp_path / "study_saved_again.h5")
        study_loaded.save_HDF5(fname2)

        # Now reloads the study once again and compare datafiles
        study_reloaded = SimulationStudy.load_HDF5(fname2)
        df_reloaded = study_reloaded.project.simulations[simu.name].generic_results[res.name].datafiles[df.name]
        assert df_loaded == df_reloaded

        # Try to edit the PNG associated file in the loaded study and saves it again
        png_fpath_black = os.path.join(os.path.dirname(__file__), "io", "datafiles", "CEA_black.png")  # Different CEA logo with black letters
        df_loaded[FileType.PNG_FILE] = png_fpath_black
        study_loaded.save_HDF5(fname2)

        # Now reloads the study once again and compare datafiles
        study_reloaded = SimulationStudy.load_HDF5(fname2)

        df_reloaded = study_reloaded.project.simulations[simu.name].generic_results[res.name].datafiles[df.name]
        assert df_loaded == df_reloaded

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Finally, compare exported files with the original one ~~~~~~~~~~~~~~~~~~~~~~~~ #
        # --> First TARGZ file saved in the first ever saved study
        fpath_targz = df_reloaded[FileType.TARGZ_FILE].save_to_disk(str(tmp_path / df_reloaded[FileType.TARGZ_FILE].filename))
        assert DatetimeUtil.utc_from_timestamp(FileUtil.last_modification_timestamp(fpath_targz)) == \
               df[FileType.TARGZ_FILE].last_modified
        assert filecmp.cmp(fpath_targz, targz_fpath, shallow=False)

        # --> Second, the PNG file edited on the study loaded once
        fpath_png = df_reloaded[FileType.PNG_FILE].save_to_disk(str(tmp_path / df_reloaded[FileType.PNG_FILE].filename))
        # assert DatetimeUtil.utc_from_timestamp(FileUtil.last_modification_timestamp(fpath_png)) != \
        #        df[FileType.PNG_FILE].last_modified
        assert not filecmp.cmp(fpath_png, png_fpath, shallow=False)
        assert DatetimeUtil.utc_from_timestamp(FileUtil.last_modification_timestamp(fpath_png)) == \
               df_loaded[FileType.PNG_FILE].last_modified
        assert filecmp.cmp(fpath_png, png_fpath_black, shallow=False)

        # --> Third, the JPEG file saved on the study loaded once
        fpath_jpg = df_reloaded[FileType.JPEG_FILE].save_to_disk(str(tmp_path / df_reloaded[FileType.JPEG_FILE].filename))
        # assert DatetimeUtil.utc_from_timestamp(FileUtil.last_modification_timestamp(fpath_jpg)) == \
        #        df_loaded[FileType.JPEG_FILE].last_modified
        assert filecmp.cmp(fpath_jpg, jpeg_fpath, shallow=False)
        # ------------------------------------------------------------------------------------------------------------ #

        new_study = SimulationStudy(project=study_reloaded.project)
        new_study.save_HDF5(str(tmp_path / "test_rewrite.h5"))


class TestPlotType(object):
    def test_from_key_exceptions(self):
        """
        Tests exceptions raised by PlotType.from_alias(method)
        """
        # Check unknown plot type
        with pytest.raises(ValueError, match="No PlotType defined with the alias 'PLOUC'."):
            pt = PlotType.from_alias("PLOUC")

    def test_init(self):
        """
        Tests valid PlotType initialisation from aliases
        """
        assert PlotType.from_alias("line") == PlotType.LINE_PLOT
        assert PlotType.from_alias("hist") == PlotType.HISTOGRAM
        assert PlotType.from_alias("2d_hist") == PlotType.HISTOGRAM_2D
        assert PlotType.from_alias("scatter") == PlotType.SCATTER_PLOT
        assert PlotType.from_alias("img") == PlotType.IMAGE
        assert PlotType.from_alias("2d_map") == PlotType.MAP_2D

        # PlotType display name
        assert PlotType.HISTOGRAM_2D.display_name == "2D histogram"

        # PlotType number of dimensions
        assert PlotType.HISTOGRAM_2D.ndimensions == 2
        assert PlotType.LINE_PLOT.ndimensions == 1
        assert PlotType.LINE_PLOT.axis_size_offset == 0
        assert PlotType.MAP_2D.axis_size_offset == 1


class TestPlotInfo(object):
    def test_plot_info_init(self):
        """
        Tests PlotInfo object initialisation
        """
        # 1D histogram
        pinfo = PlotInfo(plot_type=PlotType.HISTOGRAM, yaxis_values=N.array([1.0e3, 2.0e4]),
                         xaxis_values=N.array([1.2, 2.4, 3.6]), xaxis_log_scale=False, yaxis_log_scale=True,
                         xlabel="my label for x", ylabel="my label for y", title="My plot", xaxis_unit="Myr",
                         yaxis_unit="kpc")

        assert pinfo.title == "My plot"
        assert pinfo.plot_type == PlotType.HISTOGRAM
        assert (pinfo.yaxis_values == N.array([1.0e3, 2.0e4])).all()
        assert (pinfo.xaxis_values == N.array([1.2, 2.4, 3.6])).all()
        assert pinfo.xlabel == "my label for x"
        assert pinfo.ylabel == "my label for y"
        assert not pinfo.xaxis_log_scale
        assert pinfo.yaxis_log_scale
        assert pinfo.xaxis_unit == U.Myr
        assert pinfo.yaxis_unit == U.kpc

        # 2D histogram
        pinfo_2d = PlotInfo(plot_type=PlotType.HISTOGRAM_2D, yaxis_values=N.array([10.0, 20.0, 30.0]), title="My plot2",
                            xaxis_values=N.array([1.0, 2.0, 3.0]), values=N.array([[1.2e3, 5.5e4], [2.4e4, 9.1e3]]),
                            xaxis_log_scale=False, yaxis_log_scale=False, values_log_scale=True,
                            xlabel="my label for x", ylabel="my label for y", values_label="total mass",
                            xaxis_unit="kpc", yaxis_unit="pc", values_unit=U.Msun)

        assert pinfo_2d.title == "My plot2"
        assert pinfo_2d.plot_type == PlotType.HISTOGRAM_2D
        assert (pinfo_2d.xaxis_values == N.array([1.0, 2.0, 3.0])).all()
        assert (pinfo_2d.yaxis_values == N.array([10.0, 20.0, 30.0])).all()
        assert (pinfo_2d.values == N.array([[1.2e3, 5.5e4], [2.4e4, 9.1e3]])).all()
        assert pinfo_2d.xlabel == "my label for x"
        assert pinfo_2d.ylabel == "my label for y"
        assert pinfo_2d.values_label == "total mass"
        assert not pinfo.xaxis_log_scale
        assert not pinfo_2d.yaxis_log_scale
        assert pinfo_2d.values_log_scale
        assert pinfo_2d.xaxis_unit == U.kpc
        assert pinfo_2d.yaxis_unit == U.pc
        assert pinfo_2d.values_unit == U.Msun

    def test_setting_plot_info_type(self):
        """
        Tests PlotInfo object creation with valid /invalid 'plot_type' attribute
        """
        # PlotInfo defined without 'plot_type' mandatory attribute => Exception
        with pytest.raises(AttributeError, match="PlotInfo 'plot_type' attribute is not defined \\(mandatory\\)."):
            pi = PlotInfo()

        # Tests invalid plot_type property initialisation exception
        with pytest.raises(AttributeError, match="No PlotType defined with the alias 'TRICOT'."):
            PlotInfo(plot_type="TRICOT")  # Unknown plot type

        with pytest.raises(AttributeError, match="PlotInfo 'plot_type' attribute is not a valid PlotType enum value."):
            PlotInfo(plot_type=(3, "Strawberries"))  # Invalid plot_type

    def test_plot_info_data(self):
        """
        Tests PlotInfo instance data setup with PlotInfo.set_data() method
        """
        with pytest.raises(AttributeError, match="PlotInfo 'xaxis_values' attribute is not defined \\(mandatory\\)."):
            pi = PlotInfo(plot_type=PlotType.LINE_PLOT)
        with pytest.raises(AttributeError, match="PlotInfo 'yaxis_values' attribute is not defined \\(mandatory\\)."):
            pi = PlotInfo(plot_type=PlotType.LINE_PLOT, xaxis_values=N.array([1., 2., 3., 4.]))

        # Invalid yaxis_values attribute
        values_1d_arr_error = "'yaxis_values' PlotInfo attribute must be a 1-dimensional array."
        with pytest.raises(AttributeError, match=values_1d_arr_error):
            pi = PlotInfo(plot_type=PlotType.LINE_PLOT, yaxis_values=N.array([[1., 2.], [3., 4.]]),  # 2D array here !
                          xaxis_values=N.array([10., 20., 30., 40.]))
        with pytest.raises(AttributeError, match=values_1d_arr_error):
            pi = PlotInfo(plot_type=PlotType.LINE_PLOT, yaxis_values={"a": [1, 2, 3, 4]},  # A dict here !
                          xaxis_values=N.array([10., 20., 30., 40.]))

        # Invalid xaxis_values attribute
        xaxis_values_1d_arr_error = "'xaxis_values' PlotInfo attribute must be a 1-dimensional array."
        with pytest.raises(AttributeError, match=xaxis_values_1d_arr_error):
            pi = PlotInfo(plot_type=PlotType.LINE_PLOT, yaxis_values=N.array([1., 2., 3., 4.]),
                          xaxis_values={3.5: [2.3, 4.5]})  # Adict here !
        with pytest.raises(AttributeError, match=xaxis_values_1d_arr_error):
            pi = PlotInfo(plot_type=PlotType.LINE_PLOT, yaxis_values=N.array([1., 2., 3., 4.]),
                          xaxis_values=N.array([[10., 20.], [30., 40.]]))  # 2D array here !

        # Array size mismatch (1D plots)
        arr_size_mismatch_err = "Array size mismatch : 'yaxis_values' coordinate array size should be 5 \\(x-axis " \
                                "coordinate array size=5\\) for 'Line plot'."
        with pytest.raises(AttributeError, match=arr_size_mismatch_err):
            pi = PlotInfo(plot_type=PlotType.LINE_PLOT, yaxis_values=N.array([1., 2., 3., 4.]),
                          xaxis_values=N.array([10., 20., 30., 40., 50.]))
        arr_size_mismatch_err = "Array size mismatch : 'yaxis_values' coordinate array size should be 3 \\(x-axis " \
                                "coordinate array size=4\\) for 'Histogram'."
        with pytest.raises(AttributeError, match=arr_size_mismatch_err):
            pi = PlotInfo(plot_type=PlotType.HISTOGRAM, yaxis_values=N.array([1., 2., 3., 4.]),
                          xaxis_values=N.array([10., 20., 30., 40.]))

        # Invalid 'values' attribute (2D plots)
        with pytest.raises(AttributeError, match="PlotInfo 'values' attribute is not defined \\(mandatory for 2D "
                                                 "plots\\)."):
            pi = PlotInfo(plot_type=PlotType.HISTOGRAM_2D, xaxis_values=N.array([10., 20., 30.]),
                          yaxis_values=N.array([10., 20., 30.]))  # Missing values attribute
        values_1d_arr_error = "PlotInfo 'values' attribute must be a 2-dimensional array."
        with pytest.raises(AttributeError, match=values_1d_arr_error):
            pi = PlotInfo(plot_type=PlotType.HISTOGRAM_2D, xaxis_values=N.array([10., 20., 30.]),
                          yaxis_values=N.array([10., 20., 30.]), values={1: 'a'})  # A dict here !
        with pytest.raises(AttributeError, match=values_1d_arr_error):
            pi = PlotInfo(plot_type=PlotType.HISTOGRAM_2D, xaxis_values=N.array([10., 20., 30.]),
                          yaxis_values=N.array([10., 20., 30.]), values=N.array([10.0, 20.0, 30.0, 40.0]))  # 1D array here !

        # Array size mismatch
        arr_size_mismatch_err = "Array size mismatch : 'values' array \\(shape=\\(2, 2\\)\\) should have a shape " \
                                "\\(2, 3\\) \\(x-axis coordinate array size=3 ; y-axis coordinate array size=4\\) " \
                                "for '2D histogram'."
        with pytest.raises(AttributeError, match=arr_size_mismatch_err):
            pi = PlotInfo(plot_type=PlotType.HISTOGRAM_2D, values=N.array([[1., 2.], [3., 4.]]),
                          xaxis_values=N.array([10., 20., 30.]), yaxis_values=N.array([10.0, 20.0, 30.0, 40.0]))

        # Should be ok
        pi = PlotInfo(plot_type=PlotType.HISTOGRAM_2D, values=N.array([[1., 2.], [3., 4.]]),
                      xaxis_values=N.array([10., 20., 30.]), yaxis_values=N.array([10.0, 20.0, 30.0]))
        pi.set_data(N.array([1.0, 2.0, 3.0, 4.0]), N.array([1.0, 2.0, 3.0, 4.0]),
                    values=N.array([[1.5, 6.2, 32.1], [6.4, 8.1, 0.6], [4.7, 22.1, 15.4]]))

    def test_plot_info_unavailable_attrs_1d_plots(self):
        """
        Tests unavailable PlotInfo attributes for 1D plots (only available for 2D plots)
        """
        pinfo = PlotInfo(plot_type=PlotType.SCATTER_PLOT, yaxis_values=N.array([1.0e3, 2.0e4, 4.5e5]),
                         xaxis_values=N.array([1.2, 2.4, 3.6]))

        with pytest.raises(AttributeError, match="PlotInfo object does not have a 'values' property."):
            v = pinfo.values

        # Values log-scale flag  property (gettter + setter)
        err_log_scale = "PlotInfo object does not have a 'values_log_scale' property."
        with pytest.raises(AttributeError, match=err_log_scale):
            vls = pinfo.values_log_scale
        with pytest.raises(AttributeError, match=err_log_scale):
            pinfo.values_log_scale = True

        # Values unit  property (gettter + setter)
        err_values_unit = "PlotInfo object does not have a 'values_unit' property."
        with pytest.raises(AttributeError, match=err_values_unit):
            vu = pinfo.values_unit
        with pytest.raises(AttributeError, match=err_values_unit):
            pinfo.values_unit = U.Msun

        err_values_label = "PlotInfo object does not have a 'values_label' property."
        with pytest.raises(AttributeError, match=err_values_label):
            vl = pinfo.values_label
        with pytest.raises(AttributeError, match=err_values_label):
            pinfo.values_label = "my label"

    def test_plot_info_units(self):
        """
        Tests PlotInfo unit setup (x-axis/y-axis/values)
        """
        pi = PlotInfo(plot_type=PlotType.HISTOGRAM_2D, values=N.array([[1., 2.], [3., 4.]]),
                      xaxis_values=N.array([10., 20., 30.]), yaxis_values=N.array([10.0, 20.0, 30.0]))

        # Invalid x-axis unit values
        inv_unit_err = "PlotInfo 'xaxis_unit' property is not a valid \\(non-empty\\) string."
        with pytest.raises(AttributeError, match=inv_unit_err):
            pi.xaxis_unit = ""
        with pytest.raises(AttributeError, match=inv_unit_err):
            pi.xaxis_unit = 153.25
        with pytest.raises(AttributeError, match="PlotInfo 'xaxis_unit' property error : Unknown unit name 'Smurf'."):
            pi.xaxis_unit = "Smurf"

        # Invalid y-axis unit values
        inv_unit_err = "PlotInfo 'yaxis_unit' property is not a valid \\(non-empty\\) string."
        with pytest.raises(AttributeError, match=inv_unit_err):
            pi.yaxis_unit = ""
        with pytest.raises(AttributeError, match=inv_unit_err):
            pi.yaxis_unit = 153.25
        with pytest.raises(AttributeError, match="PlotInfo 'yaxis_unit' property error : Unknown unit name 'Pluto'."):
            pi.yaxis_unit = "Pluto"

        # Invalid x-axis unit values
        inv_unit_err = "PlotInfo 'values_unit' property is not a valid \\(non-empty\\) string."
        with pytest.raises(AttributeError, match=inv_unit_err):
            pi.values_unit = ""
        with pytest.raises(AttributeError, match=inv_unit_err):
            pi.values_unit = 153.25
        with pytest.raises(AttributeError, match="PlotInfo 'values_unit' property error : Unknown unit name 'Mickey'."):
            pi.values_unit = "Mickey"

        # Ok
        pi.xaxis_unit = U.Myr
        pi.yaxis_unit = U.kpc
        pi.values_unit = U.Msun

    def test_plot_info_title_labels(self):
        """
        Tests PlotInfo label setup (x-axis/y-axis/value) and title setup
        """
        pi = PlotInfo(plot_type=PlotType.HISTOGRAM_2D, values=N.array([[1., 2.], [3., 4.]]),
                      xaxis_values=N.array([10., 20., 30.]), yaxis_values=N.array([10.0, 20.0, 30.0]))

        # Invalid x-axis label
        inv_label_err = "PlotInfo 'xlabel' property is not a valid string."
        with pytest.raises(AttributeError, match=inv_label_err):
            pi.xlabel = 123.5

        # Invalid y-axis label
        inv_label_err = "PlotInfo 'ylabel' property is not a valid string."
        with pytest.raises(AttributeError, match=inv_label_err):
            pi.ylabel = 123.5

        # Invalid x-axis label
        inv_label_err = "PlotInfo 'values_label' property is not a valid string."
        with pytest.raises(AttributeError, match=inv_label_err):
            pi.values_label = 123.5

        # Invalid plot title
        inv_label_err = "PlotInfo 'title' property is not a valid string."
        with pytest.raises(AttributeError, match=inv_label_err):
            pi.title = 123.5

    def test_plot_info_log_scale(self):
        """
        Tests PlotInfo log scale flags (x-axis/y-axis/value)
        """
        pi = PlotInfo(plot_type=PlotType.HISTOGRAM_2D, values=N.array([[1., 2.], [3., 4.]]),
                      xaxis_values=N.array([10., 20., 30.]), yaxis_values=N.array([10.0, 20.0, 30.0]))

        with pytest.raises(AttributeError, match="'xaxis_log_scale' PlotInfo property must be a boolean value."):
            pi.xaxis_log_scale = 0.5
        pi.xaxis_log_scale = True
        with pytest.raises(AttributeError, match="'yaxis_log_scale' PlotInfo property must be a boolean value."):
            pi.yaxis_log_scale = 0.5
        pi.yaxis_log_scale = False
        with pytest.raises(AttributeError, match="'values_log_scale' PlotInfo property must be a boolean value."):
            pi.values_log_scale = 0.5
        pi.values_log_scale = True

    def test_plot_info_equality(self):
        """
        Tests PlotInfo instance equality
        """
        # 2D histogram
        pi = PlotInfo(plot_type=PlotType.HISTOGRAM_2D, yaxis_values=N.array([10.0, 20.0, 30.0]),
                      xaxis_values=N.array([1.0, 2.0, 3.0]), values=N.array([[1.2e3, 5.5e4], [2.4e4, 9.1e3]]))

        # Different UUID => not equals
        assert pi != PlotInfo(plot_type=pi.plot_type, yaxis_values=pi.yaxis_values, xaxis_values=pi.xaxis_values,
                              values=pi.values)

        # Different type => not equals
        assert pi != PlotInfo(plot_type=PlotType.LINE_PLOT, yaxis_values=pi.yaxis_values, xaxis_values=pi.xaxis_values,
                              values=pi.values, uid=pi.uid)

        # Different title => not equals
        pi2 = PlotInfo(plot_type=pi.plot_type, yaxis_values=pi.yaxis_values, xaxis_values=pi.xaxis_values,
                       values=pi.values, uid=pi.uid)
        assert pi == pi2
        pi.title = "My plot"
        pi2.title = "Test"
        assert pi != pi2
        pi2.title = pi.title
        assert pi == pi2

        # Different axis/value labels => not equals
        pi.xlabel = "x-axis label"
        pi2.xlabel = "dummy"
        assert pi != pi2
        pi2.xlabel = pi.xlabel
        assert pi == pi2
        pi.ylabel = "y-axis label"
        pi2.ylabel = "dummy"
        assert pi != pi2
        pi2.ylabel = pi.ylabel
        assert pi == pi2
        pi.values_label = "value label"
        pi2.values_label = "dummy"
        assert pi != pi2
        pi2.values_label = pi.values_label
        assert pi == pi2

        # Different axis/value log-scale flags => not equals
        pi.xaxis_log_scale = True
        pi2.xaxis_log_scale = False
        assert pi != pi2
        pi2.xaxis_log_scale = pi.xaxis_log_scale
        assert pi == pi2
        pi.yaxis_log_scale = True
        pi2.yaxis_log_scale = False
        assert pi != pi2
        pi2.yaxis_log_scale = pi.yaxis_log_scale
        assert pi == pi2
        pi.values_log_scale = True
        pi2.values_log_scale = False
        assert pi != pi2
        pi2.values_log_scale = pi.values_log_scale
        assert pi == pi2

        # Unit not equals => not equals
        pi.xaxis_unit = U.kpc
        pi2.xaxis_unit = 1.0E3*U.pc
        assert pi != pi2
        pi2.xaxis_unit = U.kpc
        assert pi == pi2
        pi.yaxis_unit = U.kpc
        pi2.yaxis_unit = 1.0E3 * U.pc
        assert pi != pi2
        pi2.yaxis_unit = U.kpc
        assert pi == pi2
        pi.values_unit = U.Msun
        pi2.values_unit = U.kg
        assert pi != pi2
        pi2.values_unit = U.Msun
        assert pi == pi2

        # Different data and MD5sums
        pi2.set_data(pi.xaxis_values, pi.yaxis_values, pi.values-1.0)
        assert pi != pi2
        pi2.set_data(pi.xaxis_values, pi.yaxis_values-1.0, pi.values)
        assert pi != pi2
        pi2.set_data(pi.xaxis_values-1.0, pi.yaxis_values, pi.values)
        assert pi != pi2
        pi2.set_data(pi.xaxis_values, pi.yaxis_values, pi.values)
        assert pi == pi2

    def test_plot_info_hdf5_io(self, tmp_path):
        """
        Tests saving/loading PlotInfo from HDF5 file

        Parameters
        ----------
        tmp_path: temporary path PyTest fixture
        """
        # Dummy project
        proj = Project(category=ProjectCategory.GalacticDynamics, project_title="My project")
        ramses = SimulationCode(name="Ramses 3 (MHD)", code_name="Ramses")
        simu = proj.simulations.add(Simulation(simu_code=ramses, name="My simu énorme"))
        res = simu.generic_results.add(GenericResult(name="Key result !"))
        df = res.datafiles.add(Datafile(name="My datafile"))
        df.plot_info = PlotInfo(plot_type=PlotType.HISTOGRAM_2D, yaxis_values=N.array([10.0, 20.0, 30.0]), title="plot",
                                xaxis_values=N.array([1.0, 2.0, 3.0]), values=N.array([[1.2e3, N.nan], [2.4e4, 9.1e3]]),
                                xaxis_log_scale=True, yaxis_log_scale=True, values_log_scale=True,
                                xlabel="my label for x", ylabel="my label for y", values_label="total mass",
                                xaxis_unit=U.kpc, yaxis_unit=U.Mpc, values_unit=U.Msun)

        # Save study
        fname = str(tmp_path / "study.h5")
        study = SimulationStudy(project=proj)
        study.save_HDF5(fname)

        # Reload study
        study_loaded = SimulationStudy.load_HDF5(fname)
        simu_loaded = study_loaded.project.simulations[simu.name]

        # Compare PlotInfo objects
        res_loaded = simu_loaded.generic_results[res.name]
        df_loaded = res_loaded.datafiles[df.name]
        assert df.plot_info == df_loaded.plot_info


__all__ = ["TestFileType", "TestDatafile", "TestPlotType", "TestPlotInfo"]
