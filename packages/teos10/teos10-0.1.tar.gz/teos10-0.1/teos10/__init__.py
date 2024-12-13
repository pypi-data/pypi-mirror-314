# teos10: unofficial Python implementation of the TEOS-10 properties of water.
# Copyright (C) 2020-2024  Matthew Paul Humphreys  (GNU GPLv3)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Unofficial Python implementation of the TEOS-10 properties of (sea)water.

Based on
    "Release on the IAPWS Formulation 2008 for the Thermodynamic Properties of Seawater"
    (IAPWS, 2008), and
    "Supplementary Release on a Computationally Efficient Thermodynami Formulation for
    Liquid Water for Oceanographic Use" (IAPWS, 2009).

All functions have the following inputs:
    temperature
        Temperature in K.
    pressure
        Total pressure in dbar.
    salinity
        Absolute salinity in g / kg.

By default, properties are calculated for seawater.  This can be changed by providing
a different Gibbs energy function to the optional ``gfunc`` kwarg.

Functions
---------
gibbs.water
    Gibbs energy of the pure water component in J / kg.
gibbs.salt
    Gibbs energy of the salt component in J / kg.
gibbs.seawater
    Gibbs energy of seawater (water + salt) in J / kg.
adiabatic_lapse_rate
    Isentropic temperature-pressure coefficient, adiabatic lapse rate in K / Pa.
chemical_potential_relative
    Relative chemical potential in J / kg.
chemical_potential_salt
    Chemical potential of the salt component in J / kg.
chemical_potential_water
    Chemical potential of the pure water component in J / kg.
density
    Density in kg / m**3.
enthalpy
    Specific enthalpy in J / kg.
entropy
    Specific entropy in J / (kg * K).
haline_contraction
    Haline contraction coefficient in kg / kg.
heat_capacity
    Specific isobaric heat capacity in J / (kg * K).
helmholtz_energy
    Specific Helmholtz energy in J / kg.
internal_energy
    Specific internal energy in J / kg.
isenotropic_compressibility
    Isenotropic compressibility in 1 / Pa.
isothermal_compressibility
    Isothermal compressibility in 1 / Pa.
molality_seawater
    Molality of seawater in mol / kg.
osmotic
    Osmotic coefficient.
sound_speed
    Sound speed in m / s.
thermal_expansion
    Thermal expansion coefficient in 1 / K.
validity
    Validity checker for input temperature and pressure values.
"""

from . import (
    constants,
    gibbs,
    properties,
)
from .gibbs import validity
from .properties import (
    adiabatic_lapse_rate,
    chemical_potential_relative,
    chemical_potential_salt,
    chemical_potential_water,
    density,
    enthalpy,
    entropy,
    haline_contraction,
    heat_capacity,
    helmholtz_energy,
    internal_energy,
    isenotropic_compressibility,
    isothermal_compressibility,
    molality_seawater,
    osmotic,
    sound_speed,
    thermal_expansion,
)

__all__ = [
    "constants",
    "gibbs",
    "properties",
    "adiabatic_lapse_rate",
    "chemical_potential_relative",
    "chemical_potential_salt",
    "chemical_potential_water",
    "density",
    "enthalpy",
    "entropy",
    "haline_contraction",
    "heat_capacity",
    "helmholtz_energy",
    "internal_energy",
    "isenotropic_compressibility",
    "isothermal_compressibility",
    "molality_seawater",
    "osmotic",
    "sound_speed",
    "thermal_expansion",
    "validity",
]
__author__ = "Humphreys, Matthew P."
__version__ = "0.1"
