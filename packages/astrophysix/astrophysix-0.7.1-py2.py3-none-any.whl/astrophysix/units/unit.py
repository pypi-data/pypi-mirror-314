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

.. autoclass:: astrophysix.units.unit.Unit
   :members: UNKNOWN_PHYSICAL_TYPE, name, coeff, description, latex, dimensions, physical_type, appropriate_unit,
             equivalent_unit_list, express, from_name, identical, info, is_base_unit, iterate_units, __eq__, create_unit
   :undoc-members:

"""
from __future__ import print_function, unicode_literals, division
from future.builtins import dict, list
from numpy import isscalar, array, abs, isclose, argmin, log10
import sys
import warnings


class UnitError(Exception):
    pass


class Unit(object):
    """
    Dimensional physical unit class

    Parameters
    ----------
    name : :obj:`string`
        Unit name
    base_unit : :class:`~astrophysix.units.unit.Unit` instance
        Composite unit from which this instance should be initialised
    coeff  : :obj:`float`
        dimensionless value of the unit instance.
    dims : 8-:obj:`tuple` of :obj:`int`
        dimension of the unit object expressed in the international unit system (``kg``, ``m``, ``s``, ``K``, ``A``, ``mol``, ``rad``, ``cd``)
    descr : :obj:`string` or **None**
        Unit description
    latex: :obj:`string` or **None**
        Unit displayed name (latex format)

    Examples
    --------

        >>> cs_m_s = Unit(name="cs", coeff=340.0, dims=(0, 1, -1, 0, 0, 0, 0, 0), descr="sound speed unit")
        >>> print("sound speed = {v:g} m/h".format(v=cs_m_s.express(km/hour)))
        sound speed = 1224 km/h
        >>>
        >>> dens = Unit(name="Msun/kpc^3", base_unit=Msun/kpc**3, descr="Solar mass per cubic kiloparsec",
                        latex="{u1:s}.{u2:s}^{{-3}}".format(u1=Msun.latex, u2=kpc.latex))
        >>> print(dens)
        (6.76957356533e-29 m^-3.kg)
    """
    _phystype_unit_mapping = dict()
    UNKNOWN_PHYSICAL_TYPE = 'unknown'
    _unit_registry = dict()
    _unit_system = list(["kg", "m", "s", "K", "A", "mol", "rad", "cd"])

    def __new__(cls, name="", base_unit=None, coeff=1.0, dims=None, descr=None, latex=None):
        # Tries to create a named Unit instance with a name already present in the registry
        if name != "" and name in cls._unit_registry:
            # Get registry corresponding Unit
            u = cls._unit_registry[name]

            # Check if the new Unit is identical to the existing one in the registry
            duplicate_entry = False
            if base_unit is not None:
                if not isinstance(base_unit, Unit):
                    raise AttributeError("'base_unit' parameter must be a a 'Unit' instance.")

                # Different Unit with identical name ?
                if base_unit.coeff != u.coeff or ((base_unit.dimensions - u.dimensions) != 0).any():
                    duplicate_entry = True
            elif dims is not None:
                if len(dims) != len(cls._unit_system):
                    raise AttributeError("Wrong dimensions : must be a tuple of length " + str(len(cls._unit_system)))
                adims = array(dims, 'i')

                # Different Unit with identical name ?
                if ((u.dimensions - adims) != 0).any() or coeff != u.coeff:
                    duplicate_entry = True

            if duplicate_entry:
                warnings.warn("Warning ! a different unit with identical name '{uname:s}' already exist in Unit "
                              "registry. Registry Unit instance is used...".format(uname=name))
            else:  # Registry Unit is identical, check description/latex differences
                if descr is not None and descr != u.description:
                    warnings.warn("Warning ! a identical unit with name '{uname:s}' already exist in Unit registry with"
                                  " a different description. Registry Unit instance is used...".format(uname=name))
                elif latex is not None and latex != u.latex:
                    warnings.warn("Warning ! a identical unit with name '{uname:s}' already exist in Unit registry with"
                                  " a different LaTex formula. Registry Unit instance is used...".format(uname=name))
            return u

        return super(Unit, cls).__new__(cls)

    def __init__(self, name="", base_unit=None, coeff=1.0, dims=None, descr=None, latex=None):
        # Already initialised Unit instance (in the registry)
        if name != "" and name in self._unit_registry and self is self._unit_registry[name]:
            return

        super(Unit, self).__init__()

        # Unit name + laTex displayed name
        self._name = name
        self._latex = latex

        if base_unit is not None:
            if not isinstance(base_unit, Unit):
                raise AttributeError("'base_unit' parameter must be a a 'Unit' instance.")
            self._dimensions = array(base_unit._dimensions, 'i')
            self._coeff = base_unit._coeff
        elif dims is None:
            raise AttributeError("'dims' attribute is mandatory to define a 'Unit' object.")
        else:
            if len(dims) != len(Unit._unit_system):
                raise AttributeError("Wrong dimensions : must be a tuple of length " + str(len(Unit._unit_system)))
            self._dimensions = array(dims, 'i')
            self._coeff = coeff

        if descr is None:
            self._descr = ""
        else:
            self._descr = descr

    @classmethod
    def from_name(cls, unit_name):
        """
        Get a :class:`~astrophysix.units.unit.Unit` from its name in the ``astrophysix`` unit registry.

        Parameters
        ----------
        unit_name: :obj:`string`
            name of the unit to search.

        Raises
        ------
        AttributeError
            if `unit_name` attribute does not correspond to any unit in the ``astrophysix`` unit registry.
        """
        if unit_name not in cls._unit_registry:
            raise AttributeError("Unknown unit name '%s'" % unit_name)

        return cls._unit_registry[unit_name]

    @classmethod
    def create_unit(cls, name="", base_unit=None, coeff=1.0, dims=None, descr=None, latex=None):
        """
        Add a new Unit instance to the registry

        Parameters
        ----------
        name : :obj:`string`
            Unit name
        base_unit : :class:`~astrophysix.units.unit.Unit` instance
            Composite unit from which this instance should be initialised
        coeff  : :obj:`float`
            dimensionless value of the unit instance.
        dims : 8-:obj:`tuple` of :obj:`int`
            dimension of the unit object expressed in the international unit system (``kg``, ``m``, ``s``, ``K``, ``A``, ``mol``, ``rad``, ``cd``)
        descr : :obj:`string` or **None**
            Unit description
        latex: :obj:`string` or **None**
            Unit displayed name (latex format)

        Raises
        ------
        ValueError
            If the provided `name` already corresponds to a unit in the registry.
        """
        if name in cls._unit_registry:
            raise ValueError("{unm:s} Unit is already defined as {regunit!s}".format(unm=name,
                                                                                     regunit=cls._unit_registry[name]))

        u = Unit(name=name, base_unit=base_unit, coeff=coeff, dims=dims, descr=descr, latex=latex)
        cls._unit_registry[name] = u
        return u

    def __eq__(self, other):
        """
        Checks Unit instance equality

        Parameters
        ----------
        other: :class:`~astrophysix.units.unit.Unit`
            other unit instance to compare to

        Returns
        -------
        e: :obj:`bool`
            True if :attr:`Unit.coeff` and :attr:`Unit.dimensions` are identical, otherwise False.
        """
        if not isclose(self._coeff, other.coeff, rtol=1.0e-6):
            return False
        if ((self._dimensions - other.dimensions) != 0).any():
            return False
        return True

    def __ne__(self, other):
        """
        Not an implied relationship between "rich comparison" equality methods in Python 2.X but only in Python 3.X
        see https://docs.python.org/2.7/reference/datamodel.html#object.__ne__

        other: other instance to compare to
        """
        # --------------------------------------------- Python 2 ----------------------------------------------------- #
        #  There are no implied relationships among the comparison operators. The truth of x==y does not imply that
        #  x!=y is false. Accordingly, when defining __eq__(), one should also define __ne__() so that the operators
        #  will behave as expected.
        # --------------------------------------------- Python 3 ----------------------------------------------------- #
        # By default, __ne__() delegates to __eq__() and inverts the result unless it is NotImplemented. There are no
        # other implied relationships among the comparison operators, for example, the truth of (x<y or x==y) does not
        # imply x<=y.
        # ------------------------------------------------------------------------------------------------------------ #
        return not self.__eq__(other)

    def identical(self, other_unit):
        """
        Strict unit instance comparison method

        Parameters
        ----------
        other_unit: :class:`~astrophysix.units.unit.Unit`
            other unit to compare to.

        Returns
        -------
        e: :obj:`bool`
            True only if `other_unit` is equals to `self` AND has identical name/description/LaTex formula.
            Otherwise returns False.
        """
        # Strict value equality
        if self._coeff != other_unit.coeff or ((self._dimensions - other_unit.dimensions) != 0).any():
            return False

        if self._name != other_unit.name or self.latex != other_unit.latex or self._descr != other_unit.description:
            return False

        return True

    @property
    def name(self):
        """
        Unit name
        """
        return self._name

    @property
    def latex(self):
        """
        Unit displayed name (LaTex format)
        """
        if self._latex is not None:
            return self._latex
        return self._name

    @property
    def dimensions(self):
        """
        Unit dimension array
        """
        return self._dimensions

    @property
    def description(self):
        """
        Unit description
        """
        return self._descr

    @property
    def coeff(self):
        """
        Constant value of this unit
        """
        return self._coeff

    def is_base_unit(self):
        """
        Checks whether the Unit is a base SI Unit (kg, m, s, K, A, mol, rad, cd).

        Returns
        -------
        b: :obj:`bool`
            True only if unit is a base SI unit(kg, m, s, K, A, mol, rad, cd). Otherwise returns False.
        """
        if self._coeff != 1.0:
            return False

        msk = (self._dimensions != 0)
        n = msk.sum()
        if n == 0:  # Dimensionless unit
            return True
        elif n == 1:
            if self._dimensions[msk][0] == 1:
                return True

        return False

    def info(self):
        """
        Print information about this unit. If any, print the name and description of this unit, then print the value of
        this unit and the list of equivalent unit contained in the built-in unit registry associated with their
        conversion factor.

        Example
        -------
            >>> U.kpc.info()
            Unit : kpc
            ----------
            Kiloparsec
            Value
            -----
            3.0856775814671917e+19 m
            Equivalent units
            ----------------
            * m            :    3.24078e-20 kpc
            * um           :    3.24078e-26 kpc
            * mm           :    3.24078e-23 kpc
            * cm           :    3.24078e-22 kpc
            * nm           :    3.24078e-29 kpc
            * km           :    3.24078e-17 kpc
            * Angstrom     :    3.24078e-30 kpc
            * au           :    4.84814e-09 kpc
            * pc           :          0.001 kpc
            * Mpc          :           1000 kpc
            * Gpc          :          1e+06 kpc
            * Rsun         :    2.25399e-11 kpc
            * ly           :    0.000306601 kpc
        """
        s = ""
        if self._name != "":
            title = "Unit : {uname:s}".format(uname=self._name)
            l = len(title)
            s += title + "\n" + (l * "-") + "\n"

        # Description
        if len(self._descr) > 0:
            s += self._descr + "\n\n"

        s += "Value\n" \
             "-----\n" + str(self._coeff) + " " + self._decompose_base_units() + "\n\n"

        s += "Equivalent units\n" \
             "----------------\n" + ""

        for u in self.equivalent_unit_list():
            s += " * {equname:12s} : {f:14g} {uname:s}\n".format(equname=u.name, f=u.express(self), uname=self._name)

        print(s)

    def equivalent_unit_list(self):
        """
        Get the equivalent unit list (with same physical type)

        Example
        -------
            >>> print(U.kg.equivalent_unit_list())
            [g : (0.001 kg), t : (1000 kg), mH : (1.66e-27 kg), Msun : (1.9889e+30 kg), Mearth : (5.9722e+24 kg)]
        """
        l = list()
        t = self.physical_type
        for u in self._unit_registry.values():
            if self == u:
                continue
            if u.physical_type == t:
                l.append(u)

        return l

    def appropriate_unit(self, nearest_log10=1.0):
        """
        Try to find the better suited unit (among available equivalent units to represent this unit).

        Parameters
        ----------
        nearest_log10: :obj:`float`
            log of the nearest value to round to. Default 1.0.

        Example
        -------
            >>> u = 2426.2 * U.ly
            >>> bv, bu = u.appropriate_unit()
            >>> print("Appropriate unit : 2426.2 ly = {v:g} {bu:s}".format(v=bv, bu=bu.name))
            Appropriate unit : 2426.2 ly = 0.743876 kpc
        """
        eq_units = self.equivalent_unit_list()
        if len(eq_units) == 0:
            return self

        tlist = [(eq_unit, self.express(eq_unit)) for eq_unit in eq_units]
        imin = argmin(array([abs(log10(t[1]) - nearest_log10) for t in tlist]))
        best_unit, ph_val = tlist[imin]
        return ph_val, best_unit

    @classmethod
    def create_phystype(cls, unit, phys_type_name):
        """
        Adds a new physical unit mapping.

        Parameters
        ----------
        unit : :class:`~astrophysix.units.unit.Unit`
            The unit to map from.

        phys_type_name : :obj:`string`
            The physical quantity name of the unit.
        """
        d = tuple(unit.dimensions)
        if d in cls._phystype_unit_mapping:
            raise ValueError("{u!s} is already defined as '{ptype_name:s}' physical quantity "
                             "type".format(u=cls._phystype_unit_mapping[d], ptype_name=phys_type_name))
        cls._phystype_unit_mapping[d] = phys_type_name

    @property
    def physical_type(self):
        """
        Get the unit physical type (dimensioned physical quantity).

        Returns
        -------
        t : :obj:`string`
            The name of the physical quantity, or :attr:`Unit.UNKNOWN_PHYSICAL_TYPE` if the physical quantity is unknown.
        """
        d = tuple(self._dimensions)
        return self._phystype_unit_mapping.get(d, self.UNKNOWN_PHYSICAL_TYPE)

    def __div__(self, other):
        r"""
        Returns the result of the division of `self` by `other`

        """
        if isscalar(other):
            newdims = self._dimensions
            newval = self._coeff / other
            return Unit(coeff=newval, dims=newdims)
        elif isinstance(other, Unit):
            newdims = self._dimensions - other._dimensions
            newval = self._coeff / other._coeff
            return Unit(coeff=newval, dims=newdims)
        else:
            raise UnitError("Unable to divide a Unit instance by something which is neither a Unit object nor a "
                            "scalar.")

    def __truediv__(self, other):
        r"""
        Returns the result of the future division of `self` by `other`

        """
        return self.__div__(other)

    def __rdiv__(self, other):
        r"""
        Returns the result of the division of `other` by `self`

        """
        if isscalar(other):
            newdims = -self._dimensions
            newval = other / self._coeff
            return Unit(coeff=newval, dims=newdims)
        elif isinstance(other, Unit):
            newdims = other._dimensions - self._dimensions
            newval = other._coeff / self._coeff
            return Unit(coeff=newval, dims=newdims)
        else:
            raise UnitError("Unable to divide something which is neither a Unit object nor a scalar by a Unit "
                            "instance.")

    def __rtruediv__(self, other):
        r"""
        Returns the result of the future division of `other` by `self`

        """
        return self.__rdiv__(other)

    def __mul__(self, other):
        r"""
        Returns the result of the multiplication of `self` with `other`

        """
        if isscalar(other):
            newdims = self._dimensions
            newval = self._coeff * other
            return Unit(coeff=newval, dims=newdims)
        elif isinstance(other, Unit):
            newdims = self._dimensions + other._dimensions
            newval = self._coeff * other._coeff
            return Unit(coeff=newval, dims=newdims)
        else:
            raise UnitError("Unable to multiply a Unit instance by something which is neither a Unit object nor a "
                            "scalar.")

    def __rmul__(self, other):
        r"""
        Returns the result of the multiplication of `other` with `self`

        """
        return self * other

    def __pow__(self, n):
        r"""
        Returns the result of the exponentiation of `self` by `n`

        """
        return Unit(coeff=self._coeff ** n, dims=n * self._dimensions)

    def _decompose_base_units(self):
        s = ""

        d = array(self._dimensions)
        for i in range(len(Unit._unit_system)):
            if d[i] != 0:
                if (d[0:i] != 0).any():
                    s += "."
                s += Unit._unit_system[i]
                if d[i] != 1:
                    s += "^" + str(d[i])
        return s

    if sys.version_info[0] >= 3:  # Python 3
        def __str__(self):
            return self.__unicode__()
    else:  # Python 2
        def __str__(self):
            return self.__unicode__().encode('utf8')

    def __unicode__(self):
        strrep = ""

        # Name & value
        if len(self._name) > 0:
            strrep += self._name + " : "

        strrep += "({coeff:g} {base_units:s})".format(coeff=self._coeff, base_units=self._decompose_base_units())
        return strrep

    def __repr__(self):
        return self.__str__()

    @classmethod
    def iterate_units(cls, phys_type=None):
        """
        Unit iterator method. Iterates over all units in the ``astrophysix`` unit registry.

        Parameters
        ----------
        phys_type: :obj:`string`
            Name of the physical quantity type of the units to iterate over. Default **None** (all physical quantities).

        Yields
        ------
        u: :class:`~astrophysix.units.unit.Unit`
            unit of the required physical quantity type, if any given.
        """
        if phys_type is None:
            for u in cls._unit_registry.values():
                yield u
        else:
            if phys_type not in cls._phystype_unit_mapping.values():
                raise AttributeError("Unknown physical quantity type '{pt!s}'.".format(pt=phys_type))
            for u in cls._unit_registry.values():
                if u.physical_type == phys_type:
                    yield u

    def express(self, unit):
        """
        Unit conversion method. Gives the conversion factor of this :class:`~astrophysix.units.unit.Unit`
        expressed into another (dimension-compatible) given :class:`~astrophysix.units.unit.Unit`.

        Checks that :

        * the **unit** param. is also a :class:`~astrophysix.units.unit.Unit` instance
        * the **unit** param. is dimension-compatible.

        Parameters
        ----------
        unit : :class:`~astrophysix.units.unit.Unit`
            unit in which the conversion is made

        Returns
        -------
        fact : :obj:`float`
            conversion factor of this unit expressed in **unit**

        Examples
        --------
        * Conversion of a kpc expressed in light-years :

            >>> factor = kpc.express(ly)
            >>> print("1 kpc = {fact:f} ly".format(fact=factor))
            1 kpc = 3261.563777 ly

        * Conversion of :math:`1 M_{\odot}` into kpc/Myr :

            >>> print(Msun.express(kpc/Myr))
            UnitError: Incompatible dimensions between :
            - Msun : (1.9889e+30 kg) (type: mass) and
            - (977792 m.s^-1) (type: velocity)
        """
        if not isinstance(unit, Unit):
            raise AttributeError("'unit' attribute must be a 'Unit' instance.")

        dmax = len(Unit._unit_system) - 1
        if tuple(self._dimensions[0:dmax]) != tuple(unit._dimensions[0:dmax]):
            raise UnitError("Incompatible dimensions between :\n"
                            "- {me!s} (type: {ptype:s}) and\n"
                            "- {unit!s} (type: {uptype:s})".format(me=self, ptype=self.physical_type, unit=unit,
                                                                   uptype=unit.physical_type))

        return (self / unit)._coeff


__all__ = ["Unit", "UnitError"]
