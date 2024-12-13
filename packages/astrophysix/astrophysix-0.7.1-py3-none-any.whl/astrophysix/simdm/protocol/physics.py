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
Physics
^^^^^^^

.. autoclass:: astrophysix.simdm.protocol.Physics
   :members:
   :undoc-members:


Physical process
^^^^^^^^^^^^^^^^

.. autoclass:: astrophysix.simdm.protocol.PhysicalProcess
    :members:
    :undoc-members:
    :inherited-members:
    :exclude-members: open_h5file, is_type_string, hsp_save_to_h5, cast_string, hsp_load_from_h5,
                      INVALID_ALIAS_ERROR_MESSAGE, VALID_ALIAS_REGEX
"""
from __future__ import absolute_import, unicode_literals
from future.builtins import str, list, dict
import logging
from enum import Enum

from astrophysix.simdm.utils import GalacticaValidityCheckMixin
from astrophysix.utils.strings import Stringifiable
from astrophysix.utils.persistency import Hdf5StudyPersistent

log = logging.getLogger("astrophysix.simdm")


class Physics(Enum):
    """
    Physics enum

    Example
    -------
        >>> ph = Physics.MHD
        >>> ph.name
        "Magnetohydrodynamics"
    """
    SelfGravity = ("self_gravity", "Self-gravity")
    ExternalGravity = ("ext_gravity", "External gravity")
    Hydrodynamics = ("hydro",  "Hydrodynamics")
    MHD = ("mhd", "Magnetohydrodynamics")
    StarFormation = ("star_form", "Star formation")
    SupernovaeFeedback = ("sn_feedback", "Supernovae feedback")
    SupermassiveBlackHoleFeedback = ("smbh_feedback", "SMBH feedback")
    StellarIonisingRadiation = ("stell_ion_rad", "Stellar ionising radiation")
    StellarUltravioletRadiation = ("stell_uv_rad", "Stellar ultraviolet radiation")
    StellarInfraredRadiation = ("stell_ir_rad", "Stellar infrared radiation")
    AGNFeedback = ("AGN_feedback", "AGN feedback")
    ProtostellarJetFeedback = ("psjet_feedback", "Protostellar jet feedback")
    Chemistry = ("chemistry", "Chemistry")
    DustCooling = ("dust_cooling", "Dust cooling")
    MolecularCooling = ("mol_cooling", "Molecular cooling")
    AtomicCooling = ("atomic_cooling", "Atomic cooling")
    TurbulentForcing = ("turb_forcing", "Turbulent forcing")
    RadiativeTransfer = ("rad_transfer", "Radiative transfer")

    def __init__(self, key, name):
        self._key = key
        self._name = name

    @property
    def key(self):
        """Physics indexing key"""
        return self._key

    @property
    def name(self):
        """PHysics verbose name"""
        return self._name

    @classmethod
    def from_key(cls, key):
        """
        Parameters
        ----------
        key: :obj:`string`
            physics key

        Returns
        -------
        t: :class:`~astrophysix.simdm.protocol.Physics`
            Physics matching the requested key.

        Raises
        ------
        ValueError
            if requested key does not match any physics.

        Example
        -------
            >>> ph = Physics.from_key("star_from")
            >>> ph.name
            "Star formation"
            >>> ph2 = Physics.from_key("MY_UNKNOWN_PHYSICS")
            ValuerError: No Physics defined with the key 'MY_UNKNOWN_PHYSICS'.
        """
        for ph in cls:
            if ph.key == key:
                return ph
        raise ValueError("No Physics defined with the key '{k:s}'.".format(k=key))


class PhysicalProcess(Hdf5StudyPersistent, GalacticaValidityCheckMixin, Stringifiable):
    """
    Simulation code physical process

    Parameters
    ----------
    physics: :class:`~astrophysix.simdm.protocol.Physics` or :obj:`string`
        Physics enum value or Physics valid key. (mandatory)
    description: :obj:`string`
        physics description
    """
    def __init__(self, **kwargs):
        super(PhysicalProcess, self).__init__(**kwargs)

        self._physics = Physics.StarFormation
        self._description = ""

        if "physics" not in kwargs:
            raise AttributeError("PhysicalProcess 'physics' attribute is not defined (mandatory).")
        ph = kwargs["physics"]
        try:
            sph = Stringifiable.cast_string(ph)
            self._physics = Physics.from_key(sph)
        except ValueError as ve:
            log.error(str(ve))
            raise AttributeError(str(ve))
        except TypeError:
            if not isinstance(ph, Physics):
                err_msg = "PhysicalProcess 'physics' attribute is not a valid Physics enum value."
                log.error(err_msg)
                raise AttributeError(err_msg)
            self._physics = ph

        if "description" in kwargs:
            self.description = kwargs["description"]

    def __eq__(self, other):
        """
        PhysicalProcess comparison method

        other: :class:`~astrophysics.simdm.protocol.PhysicalProcess`
            physical process to compare to
        """
        if not super(PhysicalProcess, self).__eq__(other):
            return False

        if self._physics != other.physics:
            return False

        if self._description != other.description:
            return False

        return True

    @property
    def physics(self):
        """Prrocess type (:class:`~astrophysix.simdm.protocol.Physics`)"""
        return self._physics

    @property
    def name(self):
        """Physical process name"""
        return self._physics.name

    @property
    def description(self):
        """Physical process description"""
        return self._description

    @description.setter
    def description(self, new_descr):
        try:
            self._description = Stringifiable.cast_string(new_descr)
        except TypeError:
            raise AttributeError("PhysicalProcess 'description' property is not a valid string.")

    @classmethod
    def _hsp_valid_attributes(cls):
        """List of valid kwargs in __init__() method"""
        return ["physics", "description"]

    def _hsp_write(self, h5group, **kwargs):
        """
        Serialize a PhysicalProcess object into a HDF5 file.

        Parameters
        ----------
        h5group: ``h5py.Group``
            Main group to write the PhysicalProcess into.
        kwargs: ``dict``
            keyword argument dictionary.
        """
        # Call to parent class _hsp_write() : write UUID, etc.
        super(PhysicalProcess, self)._hsp_write(h5group, **kwargs)

        # Write physics type key
        self._hsp_write_attribute(h5group, ('phys_type', self._physics.key), **kwargs)

        # Write physical process description, if  defined
        self._hsp_write_attribute(h5group, ('description', self._description), **kwargs)

    @classmethod
    def _hsp_read(cls, h5group, version, dependency_objdict=None):
        """
        Read a PhysicalProcess object from a HDF5 file (*.h5).

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
        exp: ``PhysicalProcess``
            Read PhysicalProcess instance
        """
        # Handle different versions here

        # Fetch Hdf5StudyPersistent object UUID
        uid = super(PhysicalProcess, cls)._hsp_read(h5group, version, dependency_objdict=dependency_objdict)

        # Read physics type
        phys_key = cls._hsp_read_attribute(h5group, 'phys_type', "physical process type")

        # Create physical process object
        pproc = cls(uid=uid, physics=phys_key)

        # Read physical process description, if defined
        pp_desc = cls._hsp_read_attribute(h5group, 'description', "physical process description",
                                          raise_error_if_not_found=False)
        if pp_desc is not None:
            pproc.description = pp_desc

        return pproc

    def __unicode__(self):
        """
        String representation of the instance
        """
        return "'{phys:s}' physical process".format(phys=self._physics.name)


__all__ = ["PhysicalProcess", "Physics"]
