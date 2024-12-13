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
import numpy as N
import hashlib


class NumpyUtil(object):
    """
    Numpy ndarray object utility abstract class
    """

    @classmethod
    def check_is_array(cls, a, ndim=None):
        """
        Checks that an object is a valid numpy.ndarray object, optionally with a given number of dimensions

        Parameters
        ----------
        a: :obj:`numpy.ndarray`
            array to check
        ndim: :obj:`int`` or None
            number of dimensions to check, if not None
        """
        if not isinstance(a, N.ndarray):
            raise AttributeError("'a' is not a valid numpy.ndarray object")

        if ndim is not None:
            if a.ndim != ndim:
                raise AttributeError("'a' does not have {n!s} dimensions.".format(n=ndim))

    @classmethod
    def check_dtype(cls, a):
        """
        Check numpy.ndarray datatype

        Parameters
        ----------
        a: :obj:`numpy.ndarray`
            array

        Returns
        -------
        k: :obj:`string`
            array datatype kind
        """
        dtk = a.dtype.kind
        if dtk in ["U", "S"]:
            return "s"
        elif dtk == "f":
            return "f"
        elif dtk == "i":
            return "i"
        elif dtk == 'b':
            return "b"
        return None

    @classmethod
    def md5sum(cls, a):
        """
        Compute the md5 checksum of a given array

        Parameter
        ---------
        a: `numpy.ndarray`
            Numpy arrray
        """
        cls.check_is_array(a)
        hash_md5 = hashlib.md5()
        hash_md5.update(a)
        return hash_md5.hexdigest()


__all__ = ["NumpyUtil"]
