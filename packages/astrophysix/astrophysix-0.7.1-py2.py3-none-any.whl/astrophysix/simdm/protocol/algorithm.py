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
Algorithm type
^^^^^^^^^^^^^^

.. autoclass:: astrophysix.simdm.protocol.AlgoType
   :members:
   :undoc-members:

Algorithm
^^^^^^^^^

.. autoclass:: astrophysix.simdm.protocol.Algorithm
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


class AlgoType(Enum):
    """
    Algorithm type enum

    Example
    -------
        >>> t = AlgoType.PoissonMultigrid
        >>> t.name
        "Multigrid Poisson solver"
    """
    StructuredGrid = ("struct_grid", "Structured grid method")
    AdaptiveMeshRefinement = ("AMR", "Adaptive mesh refinement")
    SmoothParticleHydrodynamics = ("SPH", "Smooth particle hydrodynamics")
    SpectralMethod = ("spectr_meth", "Spectral method")
    VoronoiMovingMesh = ("Voronoi_MM", "Voronoi tesselation-based moving mesh")
    Godunov = ("Godunov", "Godunov scheme")
    PoissonMultigrid = ("Poisson_MG", "Multigrid Poisson solver")
    PoissonConjugateGradient = ("Poisson_CG", "Conjugate Gradient Poisson solver")
    ParticleMesh = ("PM", "Particle-mesh solver")
    NBody = ("nbody", "N-body method")
    FriendOfFriend = ("FOF", "Friend-of-friend")
    HLLCRiemann = ("HLLC",  "Harten-Lax-van Leer-Contact Riemann solver")
    RayTracer = ("ray_tracer", "Ray-tracer")
    RadiativeTransfer = ("rad_transfer", "Radiative transfer")
    RungeKutta = ("runge_kutta", "Runge-Kutta method")

    def __init__(self, key, name):
        self._key = key
        self._name = name

    @property
    def key(self):
        """Algorithm type indexing key"""
        return self._key

    @property
    def name(self):
        """Algorithm type verbose name"""
        return self._name

    @classmethod
    def from_key(cls, key):
        """
        Parameters
        ----------
        key: :obj:`string`
            algorithm type key

        Returns
        -------
        t: :class:`~astrophysix.simdm.protocol.AlgoType`
            Algorithm type matching the requested key.

        Raises
        ------
        ValueError
            if requested key does not match any algorithm type.

        Example
        -------
            >>> t = AlgoType.from_key("FOF")
            >>> t.name
            "Friend-of-friend"
            >>> t2 = AlgoType.from_key("MY_UNKNOWN_ALGO_TYPE")
            ValuerError: No AlgoType defined with the key 'MY_UNKNOWN_ALGO_TYPE'.
        """
        for algotype in cls:
            if algotype.key == key:
                return algotype
        raise ValueError("No AlgoType defined with the key '{k:s}'.".format(k=key))


class Algorithm(Hdf5StudyPersistent, GalacticaValidityCheckMixin, Stringifiable):
    """
    Protocol algorithm

    Parameters
    ----------
    algo_type: :class:`~astrophysix.simdm.protocol.AlgoType` or :obj:`string`
        AlgoType enum value or AlgoType valid key (mandatory).
    description: :obj:`string`
        algorithm description
    """
    def __init__(self, **kwargs):
        super(Algorithm, self).__init__(**kwargs)

        self._algo_type = AlgoType.AdaptiveMeshRefinement
        self._description = ""

        if "algo_type" not in kwargs:
            raise AttributeError("Algorithm 'algo_type' attribute is not defined (mandatory).")
        atype = kwargs["algo_type"]
        try:
            satype = Stringifiable.cast_string(atype)
            self._algo_type = AlgoType.from_key(satype)
        except ValueError as ve:
            log.error(str(ve))
            raise AttributeError(str(ve))
        except TypeError:  # Not a valid string
            if not isinstance(atype, AlgoType):
                err_msg = "Algorithm 'algo_type' attribute is not a valid AlgoType enum value."
                log.error(err_msg)
                raise AttributeError(err_msg)
            self._algo_type = atype

        if "description" in kwargs:
            self.description = kwargs["description"]

    def __eq__(self, other):
        """
        Algorithm comparison method

        other: :class:`~astrophysix.simdm.protocol.Algorithm`
            algorithm to compare to
        """
        if not super(Algorithm, self).__eq__(other):
            return False

        if self._algo_type != other.algo_type:
            return False

        if self._description != other.description:
            return False

        return True

    @property
    def algo_type(self):
        """Algorithm type (:class:`~astrophysix.simdm.protocol.AlgoType`)"""
        return self._algo_type

    @property
    def name(self):
        """Algorithm name"""
        return self._algo_type.name

    @property
    def description(self):
        """Algorithm description"""
        return self._description

    @description.setter
    def description(self, new_descr):
        try:
            self._description = Stringifiable.cast_string(new_descr)
        except TypeError:  # Not a valid string
            raise AttributeError("Algorithm 'description' property is not a valid string.")

    @classmethod
    def _hsp_valid_attributes(cls):
        """List of valid kwargs in __init__() method"""
        return ["algo_type", "description"]

    def _hsp_write(self, h5group, **kwargs):
        """
        Serialize an Algorithm object into a HDF5 file.

        Parameters
        ----------
        h5group: ``h5py.Group``
            Main group to write the Algorithm into.
        kwargs: ``dict``
            keyword argument dictionary.
        """
        # Call to parent class _hsp_write() : write UUID, etc.
        super(Algorithm, self)._hsp_write(h5group, **kwargs)

        # Write algorithm type key
        self._hsp_write_attribute(h5group, ('algo_type', self._algo_type.key), **kwargs)

        # Write algorithm description, if defined
        self._hsp_write_attribute(h5group, ('description', self._description), **kwargs)

    @classmethod
    def _hsp_read(cls, h5group, version, dependency_objdict=None):
        """
        Read an Algorithm object from a HDF5 file (*.h5).

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
        algo: ``Algorithm``
            Read Algorithm instance
        """
        # Handle different versions here

        # Fetch Hdf5StudyPersistent object UUID
        uid = super(Algorithm, cls)._hsp_read(h5group, version, dependency_objdict=dependency_objdict)

        # Read algorithm type
        algotype_key = cls._hsp_read_attribute(h5group, 'algo_type', "algorithm type")

        # Create algorithm object
        algo = cls(uid=uid, algo_type=algotype_key)

        # Read algorithm description, if defined
        algo_descr = cls._hsp_read_attribute(h5group, 'description', "algorithm description",
                                             raise_error_if_not_found=False)
        if algo_descr is not None:
            algo.description = algo_descr

        return algo

    def __unicode__(self):
        """
        String representation of the instance
        """
        return "'{algo_typename:s}' algorithm".format(algo_typename=self._algo_type.name)


__all__ = ["Algorithm", "AlgoType"]
