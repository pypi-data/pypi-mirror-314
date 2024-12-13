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
from __future__ import unicode_literals, print_function
from future.builtins import str
import pytest
from astrophysix import units as U


class TestUnit(object):
    def test_express_exceptions(self):
        """
        Test exceptions raised by Unit.express(method)
        """
        # Check incompatible types
        with pytest.raises(U.UnitError) as e:
            f = U.Msun.express(U.kpc/U.Myr)
        assert str(e.value) == "Incompatible dimensions between :\n- Msun : (1.9889e+30 kg) (type: mass) and\n" \
                               "- (977792 m.s^-1) (type: velocity)"

        # Check Unit instance
        with pytest.raises(AttributeError) as e:
            f = U.Myr.express(3.9)
        assert str(e.value) == "'unit' attribute must be a 'Unit' instance."

    def test_express_valid_value(self):
        """
        Test conversion factor returned by Unit.express() method
        """
        f = U.kpc.express(U.ly)
        assert f == 3261.56377714188

    def test_unit_multiplication_error(self):
        """
        Test Unit instance multiplication raises UnitError
        """
        with pytest.raises(U.UnitError) as e:
            a = U.hour * ("Apple", 1, "Dog")
        assert str(
            e.value) == "Unable to multiply a Unit instance by something which is neither a Unit object nor a " \
                        "scalar."

    def test_unit_multiplication(self):
        """
        Test Unit instance multiplication
        """
        # Check left/right multiplication yields identical results
        a = U.c * U.Myr
        s = "{unit!s}".format(unit=a)  # call to __str__() here
        assert s == "(9.46073e+21 m)"
        assert a == U.Myr * U.c

        # Check real value multiplication
        a = 1000.0 * U.pc
        assert a == U.kpc

        # Check coefficient approximation
        a = 1000.0011 * U.pc  # More than 1.0E-6 relative tolerance on equality !
        assert a != U.kpc

    def test_unit_equality_identity(self):
        """
        Tests Unit instance equality and (strict) identity
        """
        assert U.km_s == U.km/U.s
        assert not U.km_s.identical(U.km/U.s)
        u = U.Unit.create_unit(name="Msun_pc2", base_unit=U.Msun/U.pc**2, descr="Solar mass per square parsec",
                               latex="\\textrm{M}_{\\odot}\\cdot\\textrm{pc}^{-2}")
        assert not u.identical(U.Msun/U.pc**2)
        assert U.Unit.from_name("Msun_pc2") == U.Msun/U.pc**2
        assert u.description == "Solar mass per square parsec"

    def test_unit_division(self):
        """
        Test Unit instance division
        """
        v = U.km / U.s
        s = "{unit!s}".format(unit=v)  # call to __str__() here
        assert s == "(1000 m.s^-1)"
        assert v != U.s / U.km  # Left/right division should not yield identical results !

    def test_unit_division_error(self):
        """
        Test Unit instance division raises UnitError
        """
        with pytest.raises(U.UnitError) as e:
            a = U.hour / ("Apple", 1, "Dog")
        assert str(e.value) == "Unable to divide a Unit instance by something which is neither a Unit object nor a " \
                               "scalar."

    def test_unit_power(self):
        """
        Test Unit instance to a given exponent
        """
        a = (10.0 * U.km) ** 3
        s = "{unit!s}".format(unit=a)  # call to __str__() here
        assert s == "(1e+12 m^3)"

    def test_base_SI_unit(self):
        """
        Test Unit.is_base_unit() method
        """
        assert U.kg.is_base_unit()
        assert not U.kpc.is_base_unit()
        assert U.m.is_base_unit()
        assert not U.Msun.is_base_unit()

    def test_physical_type(self):
        """
        Test Unit instance physical types
        """
        assert U.km.physical_type == "length"
        assert U.mGauss.physical_type == "magnetic flux density"
        assert U.Msun.physical_type == "mass"

        a = U.kg / U.km ** 3
        assert a.physical_type == "volume density"

        H = U.T * U.m ** 2 / U.A  # Henry
        assert H.physical_type == "inductance"

        a = U.mGauss / U.V / U.kg ** 2  # Really exotic physical quantity
        assert a.physical_type == U.Unit.UNKNOWN_PHYSICAL_TYPE

    def test_unit_instance_pickup_from_registry(self):
        """
        Test Unit instance retrieval from base Unit registry
        """
        assert U.Unit.from_name("Msun") is U.Msun

    def test_unit_iterator(self):
        """
        Test Unit registry iteration method
        """
        assert len(list(U.Unit.iterate_units())) == 91  # 91 units defined in Unit registry
        assert len(list(U.Unit.iterate_units(phys_type=U.kg.physical_type))) == 6  # 6 mass units defined in Unit registry
        assert U.kpc in U.Unit.iterate_units(phys_type=U.m.physical_type)
        assert U.Msun not in U.Unit.iterate_units(phys_type=U.W.physical_type)


__all__ = ["TestUnit"]
