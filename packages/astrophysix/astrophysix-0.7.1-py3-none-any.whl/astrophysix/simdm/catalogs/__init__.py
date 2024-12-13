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
 +_ My Project
  + Target Objects
   +_ 'Spiral galaxy' target object
   +_ 'Elliptic galaxy' target object
    + Object properties
     +_ 'pos_x' property
     +_ 'pos_y' property
     +_ 'pos_z' property
     +_ 'mass' property

    + Object property groups
     +_ 'Position' property group
      +_ 'pos_x' property
      +_ 'pos_y' property
      +_ 'pos_z' property

  +_ Cosmological simulation
   + Generic results
    +_ Generic Result #1
     + Catalogs
      +_ [Spiral galaxy] catalog #1
      +_ [Elliptic galaxy] catalog #2
       + Tabulated data
        +_ 'pos_x' value series
        +_ 'pos_y' value series
        +_ 'pos_z' values series
        +_ 'mass' value series

@endwbs

@startuml

Result "1" *-d- "many" Catalog : contains
Catalog "1" *-r- "many" CatalogField : contains
TargetObject "1" *-d- "many" ObjectProperty : contains
TargetObject "1" *-d- "many" ObjectPropertyGroup : contains
ObjectPropertyGroup "1" *-d- "many" ObjectProperty : contains
CatalogField "1" *-d- "1" ObjectProperty : refers to

class Result {
    +catalogs : ObjectList

}

Catalog "1" *-r- "1" TargetObject : refers to

class Catalog {
    +nobjects : int
    +Catalog_fields : ObjectList
}

class CatalogField {
    +field_values : 1D numpy.ndarray
    +object_property: ObjectProperty
}

class TargetObject {
    +name : string
    +object_properties : ObjectList
    +property_groups : ObjectList
}

class ObjectProperty {
    +property_name : string
}

class ObjectPropertyGroup {
    +group_name : string
}

@enduml

"""
from .field import CatalogField  # Import before Catalog to avoid circular import errors
from .catalog import Catalog
from .targobj import TargetObject, ObjectProperty, ObjectPropertyGroup, PropertySortFlag, PropertyFilterFlag

__doc__ = """

Target object and their properties
----------------------------------

*New in version 0.5.0*

.. autoclass:: astrophysix.simdm.catalogs.targobj.TargetObject
    :members:
    :undoc-members:
    :inherited-members:
    :exclude-members: open_h5file, is_type_string, hsp_save_to_h5, cast_string, hsp_load_from_h5, 
                      INVALID_ALIAS_ERROR_MESSAGE, VALID_ALIAS_REGEX


.. autoclass:: astrophysix.simdm.catalogs.targobj.ObjectProperty
    :members:
    :undoc-members:
    :inherited-members:
    :exclude-members: open_h5file, is_type_string, hsp_save_to_h5, cast_string, hsp_load_from_h5, 
                      INVALID_ALIAS_ERROR_MESSAGE, VALID_ALIAS_REGEX


.. autoclass:: astrophysix.simdm.catalogs.targobj.ObjectPropertyGroup
    :members:
    :undoc-members:
    :inherited-members:
    :exclude-members: open_h5file, is_type_string, hsp_save_to_h5, cast_string, hsp_load_from_h5, 
                      INVALID_ALIAS_ERROR_MESSAGE, VALID_ALIAS_REGEX


.. autoclass:: astrophysix.simdm.catalogs.targobj.PropertySortFlag
   :members:
   :undoc-members:


.. autoclass:: astrophysix.simdm.catalogs.targobj.PropertyFilterFlag
   :members:
   :undoc-members:

Object catalogs and catalog fields
----------------------------------

*New in version 0.5.0*

.. autoclass:: astrophysix.simdm.catalogs.catalog.Catalog
    :members:
    :undoc-members:
    :inherited-members:
    :exclude-members: open_h5file, is_type_string, hsp_save_to_h5, cast_string, hsp_load_from_h5, 
                      INVALID_ALIAS_ERROR_MESSAGE, VALID_ALIAS_REGEX


.. autoclass:: astrophysix.simdm.catalogs.field.CatalogField
    :members:
    :undoc-members:
    :inherited-members:
    :exclude-members: open_h5file, is_type_string, hsp_save_to_h5, cast_string, hsp_load_from_h5, 
                      INVALID_ALIAS_ERROR_MESSAGE, VALID_ALIAS_REGEX

"""

__all__ = ["Catalog", "CatalogField", "TargetObject", "ObjectProperty", "ObjectPropertyGroup", "PropertySortFlag",
           "PropertyFilterFlag"]
