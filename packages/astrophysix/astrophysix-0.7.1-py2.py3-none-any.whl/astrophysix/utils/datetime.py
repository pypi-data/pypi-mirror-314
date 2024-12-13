# -*- coding: utf-8 -*-
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
from future.builtins import str
import sys
import logging
import datetime
if sys.version_info.major == 2:
    import pytz

log = logging.getLogger("astrophysix.simdm")


class DatetimeUtil(object):
    @staticmethod
    def utc_now():
        """Returns a UTC timezone-aware datetime corresponding to now"""
        if sys.version_info.major > 2:  # Python 3.+
            return datetime.datetime.now(datetime.timezone.utc)
        else:  # Python 2
            return datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)

    @staticmethod
    def utc_from_timestamp(tms):
        """Get UTC timezone-aware datetime corresponding to a given timestamp"""
        if sys.version_info.major > 2:  # Python 3.+
            return datetime.datetime.utcfromtimestamp(tms).replace(tzinfo=datetime.timezone.utc)
        else:  # Python 2
            return datetime.datetime.utcfromtimestamp(tms).replace(tzinfo=pytz.UTC)

    @staticmethod
    def utc_to_timestamp(dt):
        """
        Get the POSIX timestamp corresponding to a datetime instance
        see also : https://docs.python.org/3.3/library/datetime.html#datetime.datetime.timestamp

        Parameters
        ----------
        dt: ``datetime.datetime``
            UTC timezone-aware datetime object to convert

        Returns
        -------
        ts: ``float``
            POSIX timestamp corresponding to dt
        """
        if sys.version_info.major > 3 or (sys.version_info.major == 3 and sys.version_info.minor >= 3):  # Python 3.3+
            return dt.timestamp()
        else:
            ts = (dt - datetime.datetime(1970, 1, 1, tzinfo=pytz.UTC)).total_seconds()
            return ts

    @staticmethod
    def utc_from_string(s, fmt):
        """Returns a UTC timezone-aware datetime corresponding to a given string and a given format"""
        if sys.version_info.major > 2:  # Python 3.+
            return datetime.datetime.strptime(s, fmt).replace(tzinfo=datetime.timezone.utc)
        else:  # Python 2
            return datetime.datetime.strptime(s, fmt).replace(tzinfo=pytz.UTC)


__all__ = ["DatetimeUtil"]
