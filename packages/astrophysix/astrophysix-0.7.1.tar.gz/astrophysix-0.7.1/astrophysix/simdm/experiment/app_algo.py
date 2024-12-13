# -*- coding: utf-8 -*-
#   This file is part of Horus.
#
#   Horus is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Horus is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Horus.  If not, see <http://www.gnu.org/licenses/>.
"""

.. autoclass:: astrophysix.simdm.experiment.AppliedAlgorithm
    :members:
    :undoc-members:
    :inherited-members:
    :exclude-members: open_h5file, is_type_string, hsp_save_to_h5, cast_string, hsp_load_from_h5,
                      INVALID_ALIAS_ERROR_MESSAGE, VALID_ALIAS_REGEX

"""
from __future__ import absolute_import, unicode_literals
from future.builtins import str
import uuid
import logging

from astrophysix.utils.persistency import Hdf5StudyPersistent
from astrophysix.utils.strings import Stringifiable
from ..protocol import Algorithm
from ..utils import GalacticaValidityCheckMixin


log = logging.getLogger("astrophysix.simdm")


class AppliedAlgorithm(Hdf5StudyPersistent, GalacticaValidityCheckMixin, Stringifiable):
    """
    Experiment applied algorithm class

    Parameters
    ----------
    algorithm: :class:`~astrophysix.simdm.protocol.Algorithm`
        protocol algorithm (mandatory).
    details: :obj:`string`
        implementation details.
    """
    def __init__(self, **kwargs):
        super(AppliedAlgorithm, self).__init__(**kwargs)

        # Protocol associated algorithm
        if "algorithm" not in kwargs:
            raise AttributeError("AppliedAlgorithm 'algorithm' attribute is not defined (mandatory).")
        algo = kwargs["algorithm"]
        if not isinstance(algo, Algorithm):
            raise AttributeError("AppliedAlgorithm 'algorithm' attribute is not a valid Algorithm object.")
        self._algorithm = algo

        # Applied algorithm implementation details
        self._details = ""
        if "details" in kwargs:
            self.implementation_details = kwargs["details"]

    def __eq__(self, other):
        """
        AppliedAlgorithm comparison method

        other: :class:`~astrophysix.simdm.experiment.AppliedAlgorithm`
            applied algorithm to compare to
        """
        if not super(AppliedAlgorithm, self).__eq__(other):
            return False

        if self._algorithm != other.algorithm:
            return False

        if self._details != other.implementation_details:
            return False

        return True

    @property
    def algorithm(self):
        """Experiment protocol's :class:`~astrophysix.simdm.protocol.Algorithm`. Cannot be edited after applied algorithm
        initialisation."""
        return self._algorithm

    @property
    def algo_name(self):
        """:class:`~astrophysix.simdm.protocol.Algorithm` name. Cannot be edited."""
        return self._algorithm.name

    @property
    def implementation_details(self):
        """Applied algorithm implementation details (:obj:`string`). Can be edited."""
        return self._details

    @implementation_details.setter
    def implementation_details(self, new_details):
        try:
            self._details = Stringifiable.cast_string(new_details)
        except TypeError:
            err_msg = "{cname:s} 'implementation_details' property is not a valid string.".format(cname=self.__class__.__name__)
            log.error(err_msg)
            raise AttributeError(err_msg)

    @classmethod
    def _hsp_valid_attributes(cls):
        """List of valid kwargs in __init__() method"""
        return ["algorithm", "details"]

    def _hsp_write(self, h5group, **kwargs):
        """
        Serialize an AppliedAlgorithm object into a HDF5 file.

        Parameters
        ----------
        h5group: ``h5py.Group``
            Main group to write the AppliedAlgorithm into.
        kwargs: ``dict``
            keyword argument dictionary.
        """
        # Call to parent class _hsp_write() : write UUID, etc.
        super(AppliedAlgorithm, self)._hsp_write(h5group, **kwargs)

        # Write algorithm UUID
        self._hsp_write_attribute(h5group, ('algorithm_uid', self._algorithm.uid), **kwargs)

        # Write applied algorithm implementation details, if defined
        self._hsp_write_attribute(h5group, ('details', self._details), **kwargs)

    @classmethod
    def _hsp_read(cls, h5group, version, dependency_objdict=None):
        """
        Read an AppliedAlgorithm object from a HDF5 file (*.h5).

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
        app_algo: ``AppliedAlgorithm``
            Read AppliedAlgorithm instance
        """
        # Handle different versions here

        # Fetch Hdf5StudyPersistent object UUID
        uid = super(AppliedAlgorithm, cls)._hsp_read(h5group, version, dependency_objdict=dependency_objdict)

        # Read algorithm UUID
        algo_uid = uuid.UUID(cls._hsp_read_attribute(h5group, 'algorithm_uid', "algorithm UUID"))
        protocol = list(dependency_objdict.values())[0]
        found_algo = protocol.algorithms.find_by_uid(algo_uid)
        if found_algo is None:
            err_msg = "Unknown algorithm UUID '{auid!s}' in the {proto!s}.".format(auid=algo_uid, proto=protocol)
            log.error(err_msg)
            raise IOError(err_msg)

        # Create applied algorithm object
        app_algo = cls(uid=uid, algorithm=found_algo)

        # Read applied algorithm implementation details, if defined
        algo_details = cls._hsp_read_attribute(h5group, 'details', "algorithm implementation details",
                                               raise_error_if_not_found=False)
        if algo_details is not None:
            app_algo.implementation_details = algo_details

        return app_algo

    def __unicode__(self):
        """
        String representation of the instance
        """
        s = "[{appalgo_name:s}] applied algorithm".format(appalgo_name=self._algorithm.name)
        return s


__all__ = ["AppliedAlgorithm"]
