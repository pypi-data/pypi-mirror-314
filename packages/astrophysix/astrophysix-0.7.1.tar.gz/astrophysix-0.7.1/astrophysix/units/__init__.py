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
from __future__ import absolute_import
from numpy import pi, tan, radians, array
from .unit import Unit, UnitError


# --------------------------------------------------------------------------------------------------------------------#
# Dimensionless units
none = Unit.create_unit('none',       dims=(0, 0, 0, 0, 0, 0, 0, 0), descr="Unscaled dimensionless unit")
percent = Unit.create_unit('percent', base_unit=0.01 * none, descr="One hundredth of unity", latex="\\%")


# --------------------------------------------------------------------------------------------------------------------#
# Time units
s = Unit.create_unit('s',             dims=(0, 0, 1, 0, 0, 0, 0, 0), descr="Second : base time unit")
min = Unit.create_unit('min',         base_unit=60. * s,         descr="Minute", latex="\\textrm{min}")
hour = Unit.create_unit('hour',       base_unit=3600. * s,       descr="Hour", latex="\\textrm{h}")
day = Unit.create_unit('day',         base_unit=24. * hour,      descr="Day", latex="\\textrm{day}")
sid_day = Unit.create_unit('sid_day', base_unit=86164.09053 * s, descr="Sidereal day : Earth full rotation time",
                                                                 latex="\\textrm{T}_{\\textrm{sid}}")
year = Unit.create_unit('year',       base_unit=365.25 * day,    descr="Year", latex="\\textrm{yr}")
kyr = Unit.create_unit('kyr',         base_unit=1.0E3 * year,    descr="kyr : millenium", latex="\\textrm{kyr}")
Myr = Unit.create_unit('Myr',         base_unit=1.0E6 * year,    descr="Megayear : million years", latex="\\textrm{Myr}")
Gyr = Unit.create_unit('Gyr',         base_unit=1.0E9 * year,    descr="Gigayear : trillion years", latex="\\textrm{Gyr}")


# --------------------------------------------------------------------------------------------------------------------#
# Distance units
m = Unit.create_unit('m',               dims=(0, 1, 0, 0, 0, 0, 0, 0), descr="Meter : base length unit")
um = Unit.create_unit('um',             base_unit=1.0E-6 * m,         descr="Micron", latex="\\mu m")
mm = Unit.create_unit('mm',             base_unit=1.0E-3 * m,         descr="Millimeter", latex="\\textrm{mm}")
cm = Unit.create_unit('cm',             base_unit=1.0E-2 * m,         descr="Centimeter", latex="\\textrm{cm}")
nm = Unit.create_unit('nm',             base_unit=1.0E-9 * m,         descr="Nanometer", latex="\\textrm{nm}")
km = Unit.create_unit('km',             base_unit=1000.0 * m,         descr="Kilometer", latex="\\textrm{km}")
Angstrom = Unit.create_unit('Angstrom', base_unit=1.0E-10 * m,        descr="Angstrom: 10**-10 m", latex="\\AA")
au = Unit.create_unit('au',             base_unit=1.495978707e8 * km, descr="Astronomical unit", latex="\\textrm{au}")
pc = Unit.create_unit('pc',             base_unit=au / tan(radians(1. / 3600.)), descr="Parsec", latex="\\textrm{pc}")  # 3.085677e16 * m
kpc = Unit.create_unit('kpc',           base_unit=1.0E3 * pc,         descr="Kiloparsec", latex="\\textrm{kpc}")
Mpc = Unit.create_unit('Mpc',           base_unit=1.0E6 * pc,         descr="Megaparsec", latex="\\textrm{Mpc}")
Gpc = Unit.create_unit('Gpc',           base_unit=1.0E9 * pc,         descr="Gigaparsec", latex="\\textrm{Gpc}")
Rsun = Unit.create_unit('Rsun',         base_unit=6.95508E5 * km,     descr="Solar radius", latex="\\textrm{R}_{\\odot}")


# ------------------------------------------------------------------------------------------------------------------- #
# Volume units
cm3 = Unit.create_unit('cm3',           base_unit=cm**3,              descr="Cubic centimeter", latex="\\textrm{cm}^{3}")
m3 = Unit.create_unit('m3',             base_unit=m**3,               descr="Cubic meter", latex="\\textrm{m}^{3}")
pc3 = Unit.create_unit('pc3',           base_unit=pc**3,              descr="Cubic parsec", latex="\\textrm{pc}^{3}")
kpc3 = Unit.create_unit('kpc3',         base_unit=pc**3,              descr="Cubic kiloparsec", latex="\\textrm{kpc}^{3}")


# ------------------------------------------------------------------------------------------------------------------- #
# Frequency units
Hz = Unit.create_unit('Hz', base_unit=1.0 / s, descr="Hertz : frequency unit", latex="\\textrm{Hz}")
kHz = Unit.create_unit('kHz', base_unit=1.0E3 * Hz, descr="kilo-Hertz : frequency unit", latex="\\textrm{kHz}")
MHz = Unit.create_unit('MHz', base_unit=1.0E6 * Hz, descr="mega-Hertz : frequency unit", latex="\\textrm{MHz}")
GHz = Unit.create_unit('GHz', base_unit=1.0E9 * Hz, descr="giga-Hertz : frequency unit", latex="\\textrm{GHz}")


# ------------------------------------------------------------------------------------------------------------------- #
# Surface units
barn = Unit.create_unit('barn', 1.0E-28 * m**2, descr="barn: surface unit used in HEP", latex="\\textrm{barn}")


# ------------------------------------------------------------------------------------------------------------------- #
# Velocity units
m_s = Unit.create_unit('m_s',           base_unit=m /s,        descr="Meters per second",
                                                               latex="\\textrm{m}\\cdot\\textrm{s}^{-1}")
km_s = Unit.create_unit('km_s',         base_unit=1.0e3 * m_s, descr="kilometers per second",
                                                               latex="\\textrm{km}\\cdot\\textrm{s}^{-1}")


# --------------------------------------------------------------------------------------------------------------------#
# Mass units
kg = Unit.create_unit('kg',         coeff=1.0, dims=(1, 0, 0, 0, 0, 0, 0, 0), descr="Kilogram : base mass unit", latex="\\textrm{kg}")
g = Unit.create_unit('g',           base_unit=1.0E-3 * kg,    descr="Gram")
t = Unit.create_unit('t',           base_unit=1.0E3 * kg,     descr="Metric ton")
mH = Unit.create_unit('mH',         base_unit=1.66E-24 * g,   descr="Hydrogen atomic mass", latex="m_{\\textrm{H}}")
Msun = Unit.create_unit('Msun',     base_unit=1.9889E30 * kg, descr="Solar mass", latex="\\textrm{M}_{\\odot}")
Mearth = Unit.create_unit('Mearth', base_unit=5.9722E24 * kg, descr="Earth mass", latex="\\textrm{M}_{\\oplus}")


# ------------------------------------------------------------------------------------------------------------------- #
# Angular measurements
rad = Unit.create_unit('rad', dims=(0, 0, 0, 0, 0, 0, 1, 0),
                       descr="radian: angular measurement (ratio lengh / radius of an arc)", latex="\\textrm{rad}")
degree = Unit.create_unit('deg',          base_unit=(pi / 180.0) * rad, latex="^{\\circ}",
                          descr="degree: angular measurement corresponding to 1/360 of a full rotation")
hourangle = Unit.create_unit('hourangle', base_unit=15.0 * degree,
                             descr="hour angle: angular measurement with 24 in a full circle")
arcmin = Unit.create_unit('arcmin',       base_unit=degree / 60.0, descr="arc minute: 1/60 of a hour angle", latex="'")
arcsec = Unit.create_unit('arcsec',       base_unit=degree/3600.0, descr="arc second: 1/60 of an arcminute", latex="\"")
sr = Unit.create_unit('sr',               base_unit=rad ** 2, descr="Steradian: solid angle (SI) unit")

# --------------------------------------------------------------------------------------------------------------------#
# Force units
N = Unit.create_unit('N',       base_unit=kg * m / s ** 2, descr="Newton : (SI) force unit")
dyne = Unit.create_unit('dyne', base_unit=g * cm / s ** 2, descr="dyne : (CGS) force unit", latex="\\textrm{dyne}")

# --------------------------------------------------------------------------------------------------------------------#
# Temperature unit
K = Unit.create_unit('K', dims=(0, 0, 0, 1, 0, 0, 0, 0), descr="Kelvin : base temperature unit")


# --------------------------------------------------------------------------------------------------------------------#
# Energy units
J = Unit.create_unit('J',     base_unit=kg * (m / s)**2,   descr="Joule : (SI) energy unit")
W = Unit.create_unit('W',     base_unit=J / s,             descr="Watt")
erg = Unit.create_unit('erg', base_unit=g * (cm / s) ** 2, descr="erg : (CGS) energy unit", latex="\\textrm{erg}")

# --------------------------------------------------------------------------------------------------------------------#
# Pressure unit
barye = Unit.create_unit('barye', base_unit=g / (cm * s**2), descr="Barye: (CGS) pressure unit")
Pa = Unit.create_unit('Pa',       base_unit=J * m ** -3,     descr="Pascal: (SI) pressure unit", latex="\\textrm{Pa}")
hPa = Unit.create_unit('hPa',     base_unit=1.0E2 * Pa,      descr="Hectopascal", latex="\\textrm{hPa}")
kPa = Unit.create_unit('kPa',     base_unit=1.0E3 * Pa,      descr="Kilopascal", latex="\\textrm{kPa}")
bar = Unit.create_unit('bar',     base_unit=1.0E5 * Pa,      descr="Bar", latex="\\textrm{bar}")
atm = Unit.create_unit('atm',     base_unit=1.01325 * bar,   descr="atm: atmospheric pressure (101 3525 Pa)", latex="\\textrm{atm}")


# --------------------------------------------------------------------------------------------------------------------#
# Electrical units
A = Unit.create_unit('A',     dims=(0, 0, 0, 0, 1, 0, 0, 0), descr="Ampere : electric intensity base unit")
C = Unit.create_unit('C',     base_unit=A * s,               descr="Coulomb")
e = Unit.create_unit('e',     base_unit=1.602176565e-19 * C, descr="e : elementary electric charge carried by a proton")
V = Unit.create_unit('V',     base_unit=J / C,               descr="Volt")
Ohm = Unit.create_unit('Ohm', base_unit=V * s / C,           descr="Ohm", latex="\\Omega")
S = Unit.create_unit('S',     base_unit=C / (V * s),         descr="Siemens")
F = Unit.create_unit('F',     base_unit=C / V,               descr="Farad")


# --------------------------------------------------------------------------------------------------------------------#
# Magnetical units
T = Unit.create_unit('T',           base_unit=V * s / m**2,   descr="Tesla")
Gauss = Unit.create_unit('Gauss',   base_unit=1.0E-4 * T,     descr="Gauss", latex="\\textrm{G}")
mGauss = Unit.create_unit('mGauss', base_unit=1.0E-3 * Gauss, descr="Milligauss", latex="\\textrm{mG}")
uGauss = Unit.create_unit('uGauss', base_unit=1.0E-6 * Gauss, descr="Microgauss", latex="\\mu \\textrm{G}")
Henry = Unit.create_unit('Henry',   base_unit=T * m**2 / A,   descr="Henry",      latex="\\textrm{H}")


# ------------------------------------------------------------------------------------------------------------------- #
# Amount of substance
mol = Unit.create_unit('mol', dims=(0, 0, 0, 0, 0, 1, 0, 0), descr="mole: amount of a chemical substance base unit")


# ------------------------------------------------------------------------------------------------------------------- #
# Illumination
cd = Unit.create_unit('cd',     dims=(0, 0, 0, 0, 0, 0, 0, 1), descr="Candela: base luminous intensity unit")
lm = Unit.create_unit('lm',     base_unit=cd * sr,             descr="Lumen")
lx = Unit.create_unit('lx',     base_unit=lm / m**2,           descr="Lux")
Lsun = Unit.create_unit('Lsun', base_unit=3.846E26 * W,        descr="Solar luminosity", latex="\\textrm{L}_{\\odot}")


# ------------------------------------------------------------------------------------------------------------------- #
# Spectral density
Jy = Unit.create_unit('Jy', base_unit=1.0E-26 * W / (m**2 * Hz), descr="Jansky")


# --------------------------------------------------------------------------------------------------------------------#
# Composite units
c = Unit.create_unit('c',       base_unit=2.99792458E8 * m / s,          descr="Speed of light in vacuum")
ly = Unit.create_unit('ly',     base_unit=c * year,                      descr="Light year")
eV = Unit.create_unit('eV',     base_unit=e * V,                         descr="electron-Volt")
G = Unit.create_unit('G',       base_unit=6.67428e-11 * m ** 3 / kg / (s ** 2), descr="Graviational constant")
kB = Unit.create_unit('kB',     base_unit=1.3806504E-23 * J / K,         descr="Boltzmann constant", latex="k_{\\textrm{B}}")
H = Unit.create_unit('H',       base_unit=70.0 * km / s / Mpc,           descr="Hubble's constant")
rhoc = Unit.create_unit('rhoc', base_unit=3.0 * H ** 2 / (8.0 * pi * G), descr="Friedmann's universe critical density",
                                                                         latex="\\rho_{c}")
H_cc = Unit.create_unit('H_cc', base_unit=mH / cm ** 3 / 0.76,           descr="Atoms per cubic centimeter",
                                                                         latex="\\textrm{H}/\\textrm{cc}")
g_cc = Unit.create_unit('g_cc', base_unit=g / cm ** 3,                   descr="Gram per cubic centimeter",
                                                                         latex="\\textrm{g}/\\textrm{cc}")


# --------------------------------------------------------------------------------------------------------------------#
# Planck constant
h = Unit.create_unit('h',       base_unit=6.62606957E-34 * J * s, descr="Planck Constant")
hbar = Unit.create_unit('hbar', base_unit=h / (2*pi),             descr="Reduced Planck constant", latex="\\bar{h}")

# --------------------------------------------------------------------------------------------------------------------#
# Stefan-Boltzmann constants
sigmaSB = Unit.create_unit('sigmaSB', base_unit=(2 * pi**5 * kB**4) / (15 * h**3 * c**2), descr="Stefan-Boltzmann constant",
                                                                                          latex="\\sigma_{\\textrm{SB}}")
a_R = Unit.create_unit('a_r',         base_unit=4 * sigmaSB / c, descr="Radiation constant", latex="a_{R}")


# ----- Physical type creation ----- #
Unit.create_phystype(none, 'dimensionless')
Unit.create_phystype(m, 'length')
Unit.create_phystype(m**2, 'area')
Unit.create_phystype(m3, 'volume')
Unit.create_phystype(s, 'time')
Unit.create_phystype(rad, 'angle')
Unit.create_phystype(sr, 'solid angle')
Unit.create_phystype(m_s, 'velocity')
Unit.create_phystype(m / s**2, 'acceleration')
Unit.create_phystype(Hz, 'frequency')
Unit.create_phystype(g, 'mass')
Unit.create_phystype(mol, 'amount of substance')
Unit.create_phystype(K, 'temperature')
Unit.create_phystype(N, 'force')
Unit.create_phystype(J, 'energy')  # or 'torque'
Unit.create_phystype(J/K, 'entropy')
Unit.create_phystype(J/s/m**2, 'energy flux density')
Unit.create_phystype(J/kg, 'specific energy')
Unit.create_phystype(Pa, 'pressure')  # or 'energy density'
Unit.create_phystype(W, 'power')  # or 'energy flux'
Unit.create_phystype(W/(m*K), 'thermal conductivity')
Unit.create_phystype(kg / m**3, 'volume density')
Unit.create_phystype(kg / m**2, 'surface density')
Unit.create_phystype(kg / m, 'linear density')
Unit.create_phystype(m**3 / kg, 'specific volume')
Unit.create_phystype(mol / m**3, 'molar volume')
Unit.create_phystype(kg * m / s, 'momentum/impulse')
Unit.create_phystype(kg*m**2, "moment of inertia")
Unit.create_phystype(kg * m**2 / s, 'angular momentum')
Unit.create_phystype(rad / s, 'angular velocity')
Unit.create_phystype(rad / s**2, 'angular acceleration')
Unit.create_phystype(g / (m * s), 'dynamic viscosity')
Unit.create_phystype(m ** 2 / s, 'kinematic viscosity')
Unit.create_phystype(m**-1, 'wavenumber')
Unit.create_phystype(A, 'electric current')
Unit.create_phystype(C, 'electric charge')
Unit.create_phystype(V, 'electric potential')
Unit.create_phystype(Ohm, 'electric resistance')
Unit.create_phystype(Ohm*m, 'electric resistivity')
Unit.create_phystype(S, 'electric conductance')
Unit.create_phystype(S/m, 'electric conductivity')
Unit.create_phystype(F, 'electric capacitance')
Unit.create_phystype(C * m, 'electric dipole moment')
Unit.create_phystype(A / m**2, 'electric current density')
Unit.create_phystype(V / m, 'electric field strength')
Unit.create_phystype(C / m**2, 'electric flux density')  # or 'electric displacement'
Unit.create_phystype(C / m**3, 'electric charge density')
Unit.create_phystype(F / m, 'permittivity')
Unit.create_phystype(T, 'magnetic flux density')
Unit.create_phystype(T * m**2, 'magnetic flux')
Unit.create_phystype(A / m, 'magnetic field strength')
Unit.create_phystype(Henry / m, 'magnetic permeability')
Unit.create_phystype(Henry, 'inductance')
Unit.create_phystype(cd, 'luminous intensity')
Unit.create_phystype(lm, 'luminous flux')
Unit.create_phystype(lx, 'luminous emittence')
Unit.create_phystype(W / sr, 'radiant intensity')
Unit.create_phystype(cd / m**2, 'luminance')
Unit.create_phystype(Jy, 'spectral flux density')

del pi, tan, radians


# ------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------- Rich docstring ---------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------- #
_mod_doc = """

Base units
^^^^^^^^^^

    +-----------+-------------------------------------------------------------------+
    |   Name    |                      Description                                  |
    +===========+===================================================================+
"""
_ns = locals()
_sk = _ns.keys()
_sk = sorted(_sk)
_su = []
for _k in _sk:
    _v = _ns[_k]
    if isinstance(_v, Unit) and _v.is_base_unit():
        _su.append(_k)

for _k in _su:
    _v = _ns[_k]
    _mod_doc += "    |%10s | %65s | \n"% (_v._name, _v._descr)
    _mod_doc += "    +-----------+-------------------------------------------------------------------+\n"

_mod_doc += """

.. seealso:: `Wikipedia : SI base unit <https://en.wikipedia.org/wiki/SI_base_unit>`_


.. _phys_constants:

Constants and common units
^^^^^^^^^^^^^^^^^^^^^^^^^^

    +-----------+---------------+-----------------------------+---------------------------------------------------""" +\
    """---------------------+
    |   Name    |      Value    | Decomposition in base units |                         Description               """ +\
    """                     |
    +===========+===============+=============================+===================================================""" +\
    """=====================+
"""

_su = []
for _k in _sk:
    _v = _ns[_k]
    if isinstance(_v, Unit) and not _v.is_base_unit():
        _su.append(_k)

for _k in _su:
    _v = _ns[_k]
    _mod_doc += "    |%10s |%14g | %27s | %70s | \n"% (_v._name, _v._coeff, _v._decompose_base_units(), _v._descr)
    _mod_doc += "    +-----------+---------------+-----------------------------+" \
                "------------------------------------------------------------------------+\n"

_rpqd = {qty: d for d, qty in Unit._phystype_unit_mapping.items()}
_pq = Unit._phystype_unit_mapping.values()
_spq = sorted(_pq)

_mod_doc += """

.. _phys_qties:

Physical quantities
^^^^^^^^^^^^^^^^^^^

    +-------------------------------+---------------------------------+
    |  Quantity                     |   Decomposition in base units   |
    +===============================+=================================+
"""
for _q in _spq:
    _d = _rpqd[_q]
    _u = Unit(dims=_d)
    _mod_doc += "    | {qty:29s} | {bu:31s} |\n".format(qty=_q, bu=_u._decompose_base_units())
    _mod_doc += "    +-------------------------------+---------------------------------+\n"

_mod_doc += "\n"

__doc__ = _mod_doc

del _mod_doc, _su, _sk, _ns
# ------------------------------------------------------------------------------------------------------------------- #


__all__ = ["Unit", "UnitError"]
