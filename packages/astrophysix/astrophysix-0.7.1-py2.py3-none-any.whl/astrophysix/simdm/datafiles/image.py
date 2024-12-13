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

.. autoclass:: astrophysix.simdm.datafiles.image.PngImageFile
    :members: filename, last_modified, load_file, save_to_disk, pil_image, raw_file_data
    :show-inheritance: AssociatedFile

.. autoclass:: astrophysix.simdm.datafiles.image.JpegImageFile
    :members: filename, last_modified, load_file, save_to_disk, pil_image, raw_file_data
    :show-inheritance: AssociatedFile

"""
from __future__ import print_function, unicode_literals, division, absolute_import  # Python 2 and 3 compatibility
from future.builtins import str, list, int
import logging
import io
from PIL import Image

from astrophysix.utils.file import FileType
from .file import AssociatedFile


log = logging.getLogger("astrophysix.simdm")


class ImageFile(AssociatedFile):
    @property
    def pil_image(self):
        """
        Pillow image (JPEG/PNG) image property getter. Implements lazy I/O.
        """
        # Force read from HDF5 file if necessary
        self._hsp_lazy_read()

        return Image.open(io.BytesIO(self._raw_file_data.tobytes()))

    def __unicode__(self):
        """
        String representation of the ImageFile instance
        """
        s = "[{fname:s}] datafile associated {ft:s} image file".format(fname=self._filename, ft=self.FILE_TYPE.alias)
        return s


class PngImageFile(ImageFile):
    """
    Datafile associated :attr:`~astrophysix.utils.file.FileType.PNG_FILE` image file class.
    """
    FILE_TYPE = FileType.PNG_FILE


class JpegImageFile(ImageFile):
    """
    Datafile associated :attr:`~astrophysix.utils.file.FileType.JPEG_FILE` image file class.
    """
    FILE_TYPE = FileType.JPEG_FILE


__all__ = ["ImageFile", "JpegImageFile", "PngImageFile"]
