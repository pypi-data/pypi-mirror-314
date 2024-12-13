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
@startwbs

+ Simulation study
 + Project
  + Target objects
   +_ Spiral galaxy
   +_ Elliptical galaxy
  + Simulation codes
   +_ RAMSES
   +_ AREPO
  + Simulations
   +_ [RAMSES] Simulation #1
    + Generic results
     +_ Generic Result #1
      + Datafiles
       +_ Star formation history plot
     +_ Result #2
    + Snapshots
     +_ Snapshot #234
      + Datafiles
       +_ Gas density 2D map
        +_ 'rho_dens.png' PNG file
        +_ 'rho_slice.fits' FITS file
       +_ Star formation radial 1D profile
      + Catalogs
       +_ [Spiral galaxy] Galaxy catalog (Z=2.0)
     +_ Snapshot #587
  + Post-processing runs
   + Post-processing codes
    +_ RadMC
   +_ [RadMC] Post-pro. run #1 (Simulation #2)
    + Generic results
     +_ Synthetic observed map
      + Datafiles
       +_ Map #1
        +_ 'map.jpeg' JPEG file
   +_ [AREPO] Simulation #2

@endwbs
"""
from __future__ import print_function, unicode_literals, division, absolute_import  # Python 2 and 3 compatibility

from enum import Enum

from future.builtins import str, list
import logging

from astrophysix.utils.persistency import Hdf5StudyPersistent
from .datafiles import PngImageFile, JpegImageFile
from .datafiles.image import ImageFile
from .utils import ObjectList, GalacticaValidityCheckMixin
from .catalogs.targobj import TargetObject
from astrophysix.utils.strings import Stringifiable
from .experiment import Simulation
from .protocol import SimulationCode, PostProcessingCode, InputParameter


__doc__ = """

.. autoclass:: astrophysix.simdm.ProjectCategory
   :members:
   :undoc-members:

.. autoclass:: astrophysix.simdm.Project
   :members:
   :undoc-members:

"""

from ..utils import FileUtil, FileType

log = logging.getLogger("astrophysix.simdm")


class ProjectCategory(Enum):
    """
    Project category enum

    Example
    -------
        >>> cat = ProjectCategory.PlanetaryAtmospheres
        >>> cat.verbose_name
        "Planetary atmospheres"
    """
    SolarPhysics = ("SOLAR_PHYSICS", "Solar Physics")
    PlanetaryAtmospheres = ("PLANET_ATMO", "Planetary atmospheres")
    StellarEnvironments = ("STELLAR_ENVS", "Stellar environments")
    StarPlanetInteractions = ("STAR_PLANET_INT", "Star-planet interactions")
    StarFormation = ("STAR_FORM", "Star formation")
    StellarPhysics = ("STELLAR_PHYSICS", "Stellar physics")
    InterstellarMedium = ("ISM", "Interstellar medium")
    Magnetohydrodynamics = ("MHD", "Magnetohydrodynamics")
    Supernovae = ("SUPERNOVAE", "Supernovae")
    HighEnergyAstrophysics = ("HIGH_ENERGY", "High-energy astrophysics")
    GalacticDynamics = ("GALAXIES", "Galactic dynamics")
    Cosmology = ("COSMOLOGY", "Cosmology")

    def __init__(self, alias, verbose):
        self._alias = alias
        self._verbose = verbose

    @property
    def alias(self):
        """Project category alias"""
        return self._alias

    @property
    def verbose_name(self):
        """Project category verbose name"""
        return self._verbose

    @classmethod
    def from_alias(cls, alias):
        """

        Parameters
        ----------
        alias: :obj:`string`
            project category alias

        Returns
        -------
        c: :class:`~astrophysix.simdm.ProjectCategory`
            Project category matching the requested alias.

        Raises
        ------
        ValueError
            if requested alias does not match any project category.

        Example
        -------
            >>> c = ProjectCategory.from_alias("STAR_FORM")
            >>> c.verbose_name
            "Star formation"
            >>> c2 = ProjectCategory.from_alias("MY_UNKNOWN_CATEGORY")
            ValuerError: No ProjectCategory defined with the alias 'MY_UNKNOWN_CATEGORY'.
        """
        for cat in cls:
            if cat.alias == alias:
                return cat
        raise ValueError("No ProjectCategory defined with the alias '{a:s}'.".format(a=alias))


class Project(Hdf5StudyPersistent, GalacticaValidityCheckMixin, Stringifiable):
    """
    Numerical study project (Simulation data model)

    Parameters
    ----------
    category: :class:`~astrophysix.simdm.project.ProjectCategory` or :obj:`string`
        project category or project category alias (mandatory)
    project_title: :obj:`string`
        project title (mandatory)
    alias: :obj:`string`
        Project alias (if defined, 16 max characters is recommended)
    short_description: :obj:`string`
        project short description
    general_description: :obj:`string`
        (long) project description
    data_description: :obj:`string`
        available data description in the project
    acknowledgement: :obj:`string`
        Project acknowledgement text. describes how to acknowledge the work presented in this project in any
        publication.
    directory_path: :obj:`string`
        project directory path
    thumbnail_image: :obj:`string` or :class:`~astrophysix.simdm.datafiles.image.ImageFile`
        project image thumbnail for fancy display on the Galactica simulation database.
        
    Example
    -------

        >>> # Define a new project
        >>> proj = Project(project_title="My M51 galaxy interaction model", category=ProjectCategory.GalaxyMergers,
        ...                alias="M51_SIM2022", short_description="M51 interacting galaxy model at 10 pc scale with" 
        ...                "low-efficiency star formation", general_description=gen_descr, data_description=data_descr,
        ...                directory_path="/raid/data/PROJS/M51_M/", thumbnail_image="~/Pictures/M51_M/thumb_M51.png",
        ...                acknowledgement="Please cite Bournaud et al. 2022 (in prep.) if you use data from this project.")
        >>>
        >>> # Set the project in a study
        >>> study = SimulationStudy(project=proj)
    """
    # _hsp_version = 2  # Project with target objects + acknowledgement property
    # _hsp_version = 3  # Project with thumbnail PNG/JPEG image file (optional)
    _hsp_version = 4  # Project with simulation datatable parameter list
    def __init__(self, *args, **kwargs):
        uid = kwargs.pop("uid", None)
        super(Project, self).__init__(uid=uid, **kwargs)

        self._category = ProjectCategory.StarFormation
        self._title = ""
        self._short_description = ""
        self._general_description = ""
        self._data_description = ""
        self._alias = ""
        self._how_to_acknowledge = ""
        self._directory_path = ""
        self._thumbnail_img = None

        self._simulations = ObjectList(Simulation, "name",
                                       object_addition_delhandler=(self._can_delete_input_param,
                                                                   ["simulation_code", "input_parameters"]))
        self._simu_dt_params = ObjectList(InputParameter, 'name')
        self._simu_dt_params.add_validity_check_method(self._check_valid_simu_input_param)

        if "category" not in kwargs:
            raise AttributeError("Project 'category' attribute is not defined (mandatory).")
        self.category = kwargs["category"]

        if "project_title" not in kwargs:
            raise AttributeError("Project 'project_title' attribute is not defined (mandatory).")
        self.project_title = kwargs["project_title"]

        if "alias" in kwargs:
            self.alias = kwargs["alias"]

        if "short_description" in kwargs:
            self.short_description = kwargs["short_description"]

        if "general_description" in kwargs:
            self.general_description = kwargs["general_description"]

        if "data_description" in kwargs:
            self.data_description = kwargs["data_description"]

        if "acknowledgement" in kwargs:
            self._how_to_acknowledge = kwargs["acknowledgement"]

        if "directory_path" in kwargs:
            self.directory_path = kwargs["directory_path"]

        if "thumbnail_image" in kwargs:
            self.thumbnail_image = kwargs["thumbnail_image"]

    def __eq__(self, other):
        """
        Project comparison method

        other: :class:`~astrophysix.simdm.Project`
            project to compare to.
        """
        if not super(Project, self).__eq__(other):
            return False

        if self._category != other.category:
            return False

        if self._title != other.project_title:
            return False

        if self._alias != other.alias:
            return False

        if self._short_description != other.short_description:
            return False

        if self._general_description != other.general_description:
            return False

        if self._data_description != other.data_description:
            return False

        if self._how_to_acknowledge != other.acknowledgement:
            return False

        if self._directory_path != other.directory_path:
            return False

        if self._simulations != other.simulations:
            return False

        if self._thumbnail_img != other.thumbnail_image:
            return False

        if self._simu_dt_params != other.simu_datatable_params:
            return False

        return True

    def __ne__(self, other):  # Not an implied relationship between "rich comparison" equality methods in Python 2.X
        return not self.__eq__(other)

    @property
    def category(self):
        """
        :class:`~astrophysix.simdm.ProjectCategory` or
        :attr:`ProjectCategory.alias <astrophysix.simdm.ProjectCategory.alias>` (:obj:`string`). Can be edited."""
        return self._category

    @category.setter
    def category(self, new_cat):
        try:
            scat = Stringifiable.cast_string(new_cat)
            self._category = ProjectCategory.from_alias(scat)
        except ValueError as  ve:
            log.error(str(ve))
            raise AttributeError(str(ve))
        except TypeError:
            if not isinstance(new_cat, ProjectCategory):
                err_msg = "Project 'category' attribute is not a valid ProjectCategory enum value."
                log.error(err_msg)
                raise AttributeError(err_msg)
            self._category = new_cat

    @property
    def project_title(self):
        """Project title"""
        return self._title

    @project_title.setter
    def project_title(self, new_title):
        try:
            self._title = Stringifiable.cast_string(new_title, valid_empty=False)
        except TypeError:
            err_msg = "Project 'project_title' property is not a valid (non empty) string."
            log.error(err_msg)
            raise AttributeError(err_msg)

    @property
    def alias(self):
        """Project alias"""
        return self._alias

    @alias.setter
    def alias(self, new_alias):
        try:
            self._alias = Stringifiable.cast_string(new_alias)
        except TypeError:
            err_msg = "Project 'alias' property is not a valid string"
            log.error(err_msg)
            raise AttributeError(err_msg)

    @property
    def short_description(self):
        """Short description of the project"""
        return self._short_description

    @short_description.setter
    def short_description(self, new_descr):
        try:
            self._short_description = Stringifiable.cast_string(new_descr)
        except TypeError:
            err_msg = "Project 'short_description' property is not a valid string"
            log.error(err_msg)
            raise AttributeError(err_msg)

    @property
    def general_description(self):
        """General description of the project"""
        return self._general_description

    @general_description.setter
    def general_description(self, new_descr):
        try:
            self._general_description = Stringifiable.cast_string(new_descr)
        except TypeError:
            err_msg = "Project 'general_description' property is not a valid string"
            log.error(err_msg)
            raise AttributeError(err_msg)

    @property
    def data_description(self):
        """Data description available in this project"""
        return self._data_description

    @data_description.setter
    def data_description(self, new_descr):
        try:
            self._data_description = Stringifiable.cast_string(new_descr)
        except TypeError:
            err_msg = "Project 'data_description' property is not a valid string"
            log.error(err_msg)
            raise AttributeError(err_msg)

    @property
    def acknowledgement(self):
        """How to acknowledge this project.

        *New in version 0.5.0*.
        """
        return self._how_to_acknowledge

    @acknowledgement.setter
    def acknowledgement(self, ack):
        try:
            self._how_to_acknowledge = Stringifiable.cast_string(ack)
        except TypeError:
            err_msg = "Project 'acknowledgement' property is not a valid string"
            log.error(err_msg)
            raise AttributeError(err_msg)

    @property
    def directory_path(self):
        """Project data directory path"""
        return self._directory_path

    @directory_path.setter
    def directory_path(self, new_path):
        try:
            self._directory_path = Stringifiable.cast_string(new_path)
        except TypeError:
            err_msg = "Project 'directory_path' property is not a valid string"
            log.error(err_msg)
            raise AttributeError(err_msg)

    @property
    def thumbnail_image(self):
        """Thumbnail image for the project"""
        return self._thumbnail_img

    @thumbnail_image.setter
    def thumbnail_image(self, new_thimg):
        """Set new thumbnail image for the current project (for display in the project thumbnail panel on the Galactica
        project category listing

        *New in version 0.7.0*."""
        if new_thimg is None:
            self._thumbnail_img = None
        elif Stringifiable.is_type_string(new_thimg):
            ftype = FileUtil.get_file_type(new_thimg)
            img_file_types = [img_file_class.FILE_TYPE for img_file_class in ImageFile.__subclasses__()]
            if ftype not in img_file_types:
                img_ftypes_str = "/".join([ftype.alias for ftype in img_file_types])
                err_msg = "Only image ({ift:s}) image file paths can be set in {cname:s} as thumbnail " \
                          "images.".format(cname=self.__class__.__name__, kname=ImageFile.__name__, ift=img_ftypes_str)
                log.error(err_msg)
                raise ValueError(err_msg)
            if ftype == FileType.JPEG_FILE:
                self.thumbnail_image = JpegImageFile.load_file(new_thimg)
            elif ftype == FileType.PNG_FILE:
                self._thumbnail_img = PngImageFile.load_file(new_thimg)
            else:
                raise NotImplementedError("Only JPEG and PNG files are accepted as project thumbnail images.")
        elif isinstance(new_thimg, ImageFile):
            self._thumbnail_img = new_thimg
        else:
            err_msg = "Only image (JPEG/PNG) image file paths or {kname:s} objects can be set in {cname:s} as " \
                      "thumbnail images.".format(cname=self.__class__.__name__, kname=ImageFile.__name__)
            log.error(err_msg)
            raise ValueError(err_msg)
        return

    @property
    def simulations(self):
        """Project :class:`~astrophysix.simdm.experiment.Simulation` list
        (:class:`~astrophysix.simdm.utils.ObjectList`)"""
        return self._simulations

    @property
    def simu_datatable_params(self):
        """List of :class:`~astrophysix.simdm.protocol.input_parameters.InputParameter` objects coming from the
        project :class:`~astrophysix.simdm.experiment.Simulation` associated :class:`~astrophysix.simdm.protocol.base.SimulationCode`.
        These input parameters can be used in parametric studies to display the project simulations in a datatable
        (instead of a list) on the Galactica project page, (:class:`~astrophysix.simdm.utils.ObjectList`)

        *New in version 0.7.0*.

        Example
        -------
        >>> proj = Project(category="COSMOLOGY", project_title="Reionisation of the universe",
        ...                alias="REIO_4")
        >>> ramses = protocol.SimulationCode(name="Ramses 3.0 (Hydro)", code_name="RAMSES", alias="RAMSES_CODE")
        >>> # Add input parameters
        >>> dx_min = InputParameter(key="max_res", name="dx_min",
        ...                         description="min. spatial resolution")
        >>> ramses.input_parameters.add(dx_min)
        >>> used_mhd_solver = InputParameter(key="with_mhd", name="MHD solver used",
        ...                                  description="Pure hydro or MHD run ?")
        >>> ramses.input_parameters.add(used_mhd_solver)
        >>>
        >>> # Define parameter settings
        >>> dx_min_lores = ParameterSetting(input_param=dx_min, value=100.0, unit=U.kpc)
        >>> dx_min_hires = ParameterSetting(input_param=dx_min, value=10.0, unit=U.kpc)
        >>> use_hydro = ParameterSetting(input_param=used_mhd_solver, value=False)
        >>> use_mhd = ParameterSetting(input_param=used_mhd_solver, value=True)
        >>>
        >>> # Add simulations with defined parameter settings in project
        >>> simu_hydro_lores = experiment.Simulation(ramses, name="My simu low-res (hydro)",
        ...                                          alias="SIMU_HYDRO_LOW", execution_time=exe_time)
        >>> simu_hydro_lores.parameter_settings.add(dx_min_lores)
        >>> simu_hydro_lores.parameter_settings.add(use_hydro)
        >>> proj.simulations.add(simu_hydro_lores)
        >>>
        >>> simu_hydro_hires = experiment.Simulation(ramses, name="My simu high-res (hydro)",
        ...                                          alias="SIMU_HYDRO_HIGH", execution_time=exe_time))
        >>> simu_hydro_hires.parameter_settings.add(dx_min_hires)
        >>> simu_hydro_hires.parameter_settings.add(use_hydro)
        >>> proj.simulations.add(simu_hydro_hires)
        >>>
        >>> simu_mhd_lores = experiment.Simulation(ramses, name="My simu low-res (MHD)",
        ...                                        alias="SIMU_MHD_LOW", execution_time=exe_time)
        >>> simu_mhd_lores.parameter_settings.add(dx_min_lores)
        >>> simu_mhd_lores.parameter_settings.add(use_mhd)
        >>> proj.simulations.add(simu_mhd_lores)
        >>>
        >>> simu_mhd_hires = experiment.Simulation(ramses, name="My simu high-res (MHD)",
        ...                                        alias="SIMU_MHD_HIGH", execution_time=exe_time)
        >>> simu_mhd_hires.parameter_settings.add(dx_min_hires)
        >>> simu_mhd_hires.parameter_settings.add(use_mhd)
        >>> proj.simulations.add(simu_mhd_hires)
        >>>
        >>> # Add input parameters in project simulation datatable parameter list
        >>> proj.simu_datatable_params.add(dx_min)
        >>> proj.simu_datatable_params.add(used_mhd_solver)
        """
        return self._simu_dt_params

    def _simu_codes(self):
        """Simulation codes iterator"""
        puid_list = []
        for simu in self._simulations:
            p = simu.simulation_code
            if p.uid not in puid_list:
                puid_list.append(p.uid)
                yield p

    def _post_pro_codes(self):
        """Post-processing codes iterator"""
        ppcode_uid_list = []
        for simu in self._simulations:
            for pprun in simu.post_processing_runs:
                p = pprun.postpro_code
                if p.uid not in ppcode_uid_list:
                    ppcode_uid_list.append(p.uid)
                    yield p

    def _target_objects(self):
        """Target object iterator"""
        to_uid_list = []
        for simu in self._simulations:  # Loop over simulations
            for sn in simu.snapshots:  # Loop over simulation snapshots
                for cat in sn.catalogs:  # Loop over catalogs
                    if cat.target_object.uid not in to_uid_list:
                        to_uid_list.append(cat.target_object.uid)
                        yield cat.target_object
            for res in simu.generic_results:  # Loop over simulation generic results
                for cat in res.catalogs:  # Loop over catalogs
                    if cat.target_object.uid not in to_uid_list:
                        to_uid_list.append(cat.target_object.uid)
                        yield cat.target_object

            for pprun in simu.post_processing_runs:
                for sn in pprun.snapshots:  # Loop over post-processing run snapshots
                    for cat in sn.catalogs:  # Loop over catalogs
                        if cat.target_object.uid not in to_uid_list:
                            to_uid_list.append(cat.target_object.uid)
                            yield cat.target_object
                for res in pprun.generic_results:  # Loop over post-processing run generic results
                    for cat in res.catalogs:  # Loop over catalogs
                        if cat.target_object.uid not in to_uid_list:
                            to_uid_list.append(cat.target_object.uid)
                            yield cat.target_object

    def _check_valid_simu_input_param(self, input_param):
        """
        Checks that a given input parameter can be added into this project's aimulation datatable input parameter list.
        Verifies that the input parameter belongs to any of the project experiment protocol's input parameter list.
        Raises an AttributeError if not.

        Parameters
        ----------
        input_param: ``astrophysix.simdm.protocol.input_parameter.InputParameter``
            input parameter to add into the simulation datatable parameter list
        """
        for simu_code in self._simu_codes():
            if input_param not in simu_code.input_parameters:
                err_msg = "{cname:s} '{ip!s}' does not refer to any input parameter of the project's simulation " \
                          "codes.".format(cname=self.__class__.__name__, ip=input_param)
                log.error(err_msg)
                raise AttributeError(err_msg)

    def _can_delete_input_param(self, inp_param):
        """
        Checks if an input parameter does not belong to the project simulation's datatable parameter list and can be
        safely deleted. Returns None if it can be deleted, otherwise returns a string.

        Parameters
        ----------
        inp_param: ``astrophysix.simdm.protocol.input_parameters.InputParameter``
            input parameter about to be deleted

        Returns
        -------
        o: str or None
        """
        for ip in self._simu_dt_params:
            if ip is inp_param:  # Reference identity, not equality ??? Should work
                return "Simulation datatable {ip!s}".format(s=self, ip=inp_param)
        return None

    @classmethod
    def _hsp_valid_attributes(cls):
        """List of valid kwargs in __init__() method"""
        return ["category", "project_title", "alias", "short_description", "general_description", "data_description",
                "data_description", "acknowledgement", "directory_path", "thumbnail_image"]

    def _hsp_write(self, h5group, **kwargs):
        """
        Serialize a Project object into a HDF5 file.

        Parameters
        ----------
        h5group: ``h5py.Group``
            Main group to write the Project into.
        kwargs: ``dict``
            keyword argument dictionary.
        """
        # Call to parent class _hsp_write() : write UUID, etc.
        super(Project, self)._hsp_write(h5group, **kwargs)

        # If necessary, call callback function with project name
        self._hsp_write_callback(str(self), **kwargs)

        # Write project title
        self._hsp_write_attribute(h5group, ('title', self._title), **kwargs)

        # Write project category alias
        self._hsp_write_attribute(h5group, ('category', self._category.alias), **kwargs)

        # Write project Galactica alias, if defined
        self._hsp_write_attribute(h5group, ('galactica_alias', self._alias), **kwargs)

        # Write project directory path, if defined
        self._hsp_write_attribute(h5group, ('project_directory', self._directory_path), **kwargs)

        # Write project short/general/data description/ acknowledgement
        self._hsp_write_attribute(h5group, ('short_description', self._short_description), **kwargs)
        self._hsp_write_attribute(h5group, ('general_description', self._general_description), **kwargs)
        self._hsp_write_attribute(h5group, ('data_description', self._data_description), **kwargs)
        self._hsp_write_attribute(h5group, ('acknowledgement', self._how_to_acknowledge), **kwargs)

        # Write project thumbnail image into HDF5 file
        if not kwargs.get("dry_run", False) and not kwargs.get("new_file", True):  # Old HDF5 file being modified (not a dry run)
            # Delete thumbnail image from HDF5 group if not present anymore in the Project
            if "thumbnail_img" in h5group and self.thumbnail_image is None:
                del h5group["thumbnail_img"]

        self._hsp_write_object(h5group, "thumbnail_img", self._thumbnail_img, **kwargs)

        # Write protocol directory
        if kwargs.get("from_project", False):  # Write protocol list in project subgroup (not in each experiment)
            proto_group = self._hsp_get_or_create_h5group(h5group, "PROTOCOLS", **kwargs)
            self._hsp_write_object_list(proto_group, "SIMU_CODES", self._simu_codes, "simu_code_", **kwargs)
            self._hsp_write_object_list(proto_group, "PPRUN_CODES", self._post_pro_codes, "pprun_code_", **kwargs)

        # Write all target objects
        if kwargs.get("from_project", False): # Write target object list in project subgroup (not in each catalog)
            self._hsp_write_object_list(h5group, "TARGET_OBJECTS", self._target_objects, "targobj_", **kwargs)

        # Write all simulations
        self._hsp_write_object_list(h5group, "SIMULATIONS", self._simulations, "simu_", **kwargs)

        # Write simulation datatable parameters
        self._hsp_write_object_list(h5group, "SIMU_DT_PARAMS", self._simu_dt_params, "simu_dt_param_", **kwargs)

    @classmethod
    def _hsp_read(cls, h5group, version, dependency_objdict=None):
        """
        Read a Project object from a HDF5 file (*.h5).

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
        proj: ``Project``
            Read Project instance
        """
        # Handle different versions here

        # Fetch Hdf5StudyPersistent object UUID
        uid = super(Project, cls)._hsp_read(h5group, version, dependency_objdict=dependency_objdict)

        # Create Project instance with mandatory attributes
        t = cls._hsp_read_attribute(h5group, "title", "project title")
        cat = cls._hsp_read_attribute(h5group, "category", "project category")
        proj = cls(uid=uid, category=cat, project_title=t)

        # ------------------------------------------ Optional attributes --------------------------------------------- #
        # Read Galactica alias
        alias = cls._hsp_read_attribute(h5group, "galactica_alias", "project Galactica alias",
                                        raise_error_if_not_found=False)
        if alias is  not None:
            proj.alias = alias
        # Read project directory
        dpath = cls._hsp_read_attribute(h5group, "project_directory", "project directory",
                                        raise_error_if_not_found=False)
        if dpath is not None:
            proj.directory_path = dpath

        # -------------------------- Read project short/general/data description --------------------------- #
        ddescr = cls._hsp_read_attribute(h5group, "data_description", "project data description",
                                         raise_error_if_not_found=False)
        if ddescr is not None:
            proj.data_description = ddescr
        gdescr = cls._hsp_read_attribute(h5group, "general_description", "project general description",
                                         raise_error_if_not_found=False)
        if gdescr is not None:
            proj.general_description = gdescr

        sdescr = cls._hsp_read_attribute(h5group, "short_description", "project short description",
                                         raise_error_if_not_found=False)
        if sdescr is not None:
            proj.short_description = sdescr
        # --------------------------------------------------------------------------------------------------- #
        # ------------------------------------------------------------------------------------------------------------ #

        # Build dependency object dictionary indexed by their class name
        dod = {}
        if "PROTOCOLS" in h5group:
            protgroup = h5group["PROTOCOLS"]
            # Build simulation code dictionary indexed by their UUID
            if "SIMU_CODES" in protgroup:
                simu_code_dict = {}
                for simu_code in SimulationCode._hsp_read_object_list(protgroup, "SIMU_CODES", "simu_code_",
                                                                      "simulation code"):
                    simu_code_dict[simu_code.uid] = simu_code

                dod[SimulationCode.__name__] = simu_code_dict

            # Build post-processing code dictionary indexed by their UUID
            if "PPRUN_CODES" in protgroup:
                pprun_code_dict = {}
                for pprun_code in PostProcessingCode._hsp_read_object_list(protgroup, "PPRUN_CODES", "pprun_code_",
                                                                           "post-processing code"):
                    pprun_code_dict[pprun_code.uid] = pprun_code

                dod[PostProcessingCode.__name__] = pprun_code_dict

        if version >= 2:  # and "TARGET_OBJECTS" in h5group:
            # Build target object dictionary indexed by their UUID
            tobj_dict = {}
            for tobj in TargetObject._hsp_read_object_list(h5group, "TARGET_OBJECTS", "targobj_", "target object",
                                                           dependency_objdict=dod):
                tobj_dict[tobj.uid] = tobj
            dod[TargetObject.__name__] = tobj_dict

            # Read project acknowledgement text
            ackn = cls._hsp_read_attribute(h5group, "acknowledgement", "project acknowledgement",
                                           raise_error_if_not_found=False)
            if ackn is not None:
                proj.acknowledgement = ackn

        if version >= 3:
            # Read project thumbnail image file
            if "thumbnail_img" in h5group:
                proj.thumbnail_image = ImageFile._hsp_read_object(h5group, "thumbnail_img", "thumbnail image file")

        # Build simulation list and add each simulation into project
        if "SIMULATIONS" in h5group:
            for simu in Simulation._hsp_read_object_list(h5group, "SIMULATIONS", "simu_", "project simulation",
                                                         dependency_objdict=dod):
                proj.simulations.add(simu)

        if version >= 4:
            if "SIMU_DT_PARAMS" in h5group:
                for simudt_param in InputParameter._hsp_read_object_list(h5group, "SIMU_DT_PARAMS", "simu_dt_param_",
                                                                         "project's simulation datatable parameter",
                                                                         dependency_objdict=dod):
                    proj.simu_datatable_params.add(simudt_param)

        return proj

    def galactica_validity_check(self, **kwargs):
        """
        Perform validity checks on this  instance and eventually log warning messages.

        Parameters
        ----------
        kwargs: `dict`
            keyword arguments (optional)
        """
        # Check project alias
        if len(self.alias) == 0:
            log.warning("{p!s} Galactica alias is missing.".format(p=self))
        elif len(self._alias) > 16:
            log.warning("{p!s} Galactica alias is too long (max. 16 characters).".format(p=self))
        else:
            err_msg = self.galactica_valid_alias(self._alias)
            if err_msg is not None:
                log.warning("{p!s} Galactica alias is not valid ({m:s})".format(p=self, m=err_msg))

        # Check project title
        if len(self._title) == 0:
            log.warning("{p!s} Galactica project title is missing.".format(p=self))
        elif len(self._title) > 128:
            log.warning("{p!s} Galactica project title is too long (max. 128 characters).".format(p=self))

        # Check project short description
        if len(self._short_description) == 0:
            log.warning("{p!s} Galactica short description is missing.".format(p=self))
        elif len(self._short_description) > 256:
            log.warning("{p!s} Galactica short description is too long (max. 256 characters).".format(p=self))

        # Check project post-processing/simulation code validity + protocol alias unicity
        code_names = {}
        for scode in self._simu_codes():
            scode.galactica_validity_check()
            if len(scode.alias) > 0:
                if scode.alias in code_names:
                    log.warning("{c1!s} and {c2!s} protocols share the same alias. They must be "
                                "unique.".format(c1=code_names[scode.alias], c2=scode))
                else:
                    code_names[scode.alias] = scode
        for pcode in self._post_pro_codes():
            pcode.galactica_validity_check()
            if len(pcode.alias) > 0:
                if pcode.alias in code_names:
                    log.warning("{c1!s} and {c2!s} protocols share the same alias. They must be "
                                "unique.".format(c1=code_names[pcode.alias], c2=pcode))
                else:
                    code_names[pcode.alias] = pcode

        # Check project post-processing runs/simulations validity + experiment alias unicity
        experiments = {}
        for srun in self._simulations:
            srun.galactica_validity_check()
            if len(srun.alias) > 0:
                if srun.alias in experiments:
                    log.warning("{r1!s} and {r2!s} experiments share the same alias. They must be "
                                "unique.".format(r1=experiments[srun.alias], r2=srun))
                else:
                    experiments[srun.alias] = srun

            for prun in srun.post_processing_runs:
                prun.galactica_validity_check()
                if len(prun.alias) > 0:
                    if prun.alias in experiments:
                        log.warning("{r1!s} and {r2!s} experiments share the same alias. They must be "
                                    "unique.".format(r1=experiments[prun.alias], r2=prun))
                    else:
                        experiments[prun.alias] = prun

        # Check target object validity + object name unicity in the project
        targobj_names = {}
        for targobj in self._target_objects():
            targobj.galactica_validity_check()
            if targobj.name in targobj_names:
                log.warning("{r1!s} and {r2!s} share the same name. They must be "
                            "unique.".format(r1=targobj_names[targobj.name], r2=targobj))
            else:
                targobj_names[targobj.name] = targobj

    def __unicode__(self):
        """
        String representation of the instance
        """
        strrep = "[{category:s}]".format(category=self._category.verbose_name)

        # Title and short description
        if len(self._title) > 0:
            strrep += " '{ptitle:s}' project".format(ptitle=self._title)

        return strrep


__all__ = ["Project", "ProjectCategory"]
