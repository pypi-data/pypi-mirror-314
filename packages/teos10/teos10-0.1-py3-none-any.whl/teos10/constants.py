# teos10: unofficial Python implementation of the TEOS-10 properties of water.
# Copyright (C) 2020-2024  Matthew Paul Humphreys  (GNU GPLv3)
"""Constants from IAPWS08 Table 1."""

pressure_n = 101_325  # normal pressure in Pa
pressure_st = 1e8  # reducing pressure in Pa
temperature_zero = 273.15  # Celcius zero point in K
temperature_st = 40.0  # reducing temperature in K
salinity_n = 0.035_165_04  # normal salinity in kg/kg
salinity_st = salinity_n * 40 / 35  # reducing salinity in kg/kg
gas_constant = 8.314_472  # molar gas constant in J/(mol*kg)
salt_mass = 31.403_821_8  # molar mass of sea salt in g/mol
dbar_to_Pa = 10_000
salinity_to_salt = 1e-3
