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
import sys

from future.builtins import str


class Stringifiable(object):
    if sys.version_info.major > 2:  # Python 3.+
        def __str__(self):
            return self.__unicode__()
    else:  # Python 2
        def __str__(self):
            return self.__unicode__().encode('utf8')

    def __unicode__(self):
        """
        String representation of the instance
        """
        raise NotImplementedError()

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def is_type_string(s):
        """
        If the object is not a string object (basestring in Python 2, str in Python 3), returns False. Otherwise returns
        True.

        Parameters
        ----------
        s: object to test.
        """
        if sys.version_info.major > 2:  # Python 3.+
            return isinstance(s, str)
        else:  # Python 2
            return isinstance(s, basestring)

    @staticmethod
    def cast_string(s, valid_empty=True):
        """
        Tries to cast an object into a Python 3 compatible unicode string. If the object is not a string object
        (basestring in Python 2, str in Python 3), or if the string is empty and 'valid_empty' is False, raises a
        TypeError.

        Parameters
        ----------
        s: object to cast into a Python 3 compatible string
        valid_empty: Are empty strings valid ? Default true.

        Returns
        -------
        p3s: Python 3 compatible unicode str
        """
        if sys.version_info.major > 2:  # Python 3.+
            if not isinstance(s, str) or (not valid_empty and len(s) == 0):
                raise TypeError("Invalid string")
            return s
        else:  # Python 2
            if not isinstance(s, basestring) or (not valid_empty and len(s) == 0):
                raise TypeError("Invalid string")
            # Cast to Python 3 unicode str
            return str(s)


__all__ = ["Stringifiable"]
