# teos10: unofficial Python implementation of the TEOS-10 properties of water.
# Copyright (C) 2020-2024  Matthew Paul Humphreys  (GNU GPLv3)
"""Water properties based on derivatives of Gibbs energy functions."""

import jax
from jax import numpy as np

from . import constants, gibbs

default = gibbs.seawater  # which Gibbs energy function to use by default


def dG_dT(gfunc):
    """Function for the first derivative of `gfunc` w.r.t. temperature."""
    return jax.grad(gfunc)


def dG_dp(gfunc):
    """Function for the first derivative of `gfunc` w.r.t. pressure."""
    return lambda *args: jax.grad(gfunc, argnums=1)(*args) / constants.dbar_to_Pa


def dG_dS(gfunc):
    """Function for the first derivative of `gfunc` w.r.t. salinity."""
    return lambda *args: jax.grad(gfunc, argnums=2)(*args) / constants.salinity_to_salt


def d2G_dT2(gfunc):
    """Function for the second derivative of `gfunc` w.r.t. temperature."""
    return jax.grad(dG_dT(gfunc), argnums=0)


def d2G_dSdp(gfunc):
    """Function for the derivative of `gfunc` w.r.t. salinity and pressure."""
    return (
        lambda *args: jax.grad(dG_dp(gfunc), argnums=2)(*args)
        / constants.salinity_to_salt
    )


def d2G_dTdp(gfunc):
    """Function for the derivative of `gfunc` w.r.t. temperature and pressure."""
    return lambda *args: jax.grad(dG_dT(gfunc), argnums=1)(*args) / constants.dbar_to_Pa


def d2G_dp2(gfunc):
    """Function for the second derivative of `gfunc` w.r.t. pressure."""
    return lambda *args: jax.grad(dG_dp(gfunc), argnums=1)(*args) / constants.dbar_to_Pa


def density(*args, gfunc=default):
    """Density (rho) in kg/m**3.  IAPWS09 Table 3 (4)."""
    return 1.0 / dG_dp(gfunc)(*args)


def entropy(*args, gfunc=default):
    """Specific entropy (s) in J/(kg*K).  IAPWS09 Table 3 (5)."""
    return -dG_dT(gfunc)(*args)


def heat_capacity(*args, gfunc=default):
    """Specific isobaric heat capacity (c_p) in J/(kg*K).  IAPWS09 Table 3 (6)."""
    return -args[0] * d2G_dT2(gfunc)(*args)


def enthalpy(*args, gfunc=default):
    """Specific enthalpy (h) in J/kg.  IAPWS09 Table 3 (7)."""
    return gfunc(*args) + args[0] * entropy(*args, gfunc=gfunc)


def internal_energy(*args, gfunc=default):
    """Specific internal energy (u) in J/kg.  IAPWS09 Table 3 (8)."""
    pressure_Pa = args[1] * constants.dbar_to_Pa
    return enthalpy(*args, gfunc=gfunc) - pressure_Pa * dG_dp(gfunc)(*args)


def helmholtz_energy(*args, gfunc=default):
    """Specific Helmholtz energy (f) in J/kg.  IAPWS09 Table 3 (9)."""
    pressure_Pa = args[1] * constants.dbar_to_Pa
    return gfunc(*args) - pressure_Pa * dG_dp(gfunc)(*args)


def thermal_expansion(*args, gfunc=default):
    """Thermal expansion coefficient (alpha) in 1/K.  IAPWS09 Table 3 (10)."""
    return d2G_dTdp(gfunc)(*args) / dG_dp(gfunc)(*args)


def adiabatic_lapse_rate(*args, gfunc=default):
    """Isentropic temperature-pressure coefficient, adiabatic lapse rate (beta_s) in
    K/Pa.  IAPWS09 Table 3 (11)."""
    return -d2G_dTdp(gfunc)(*args) / dG_dp(gfunc)(*args)


def isothermal_compressibility(*args, gfunc=default):
    """Isothermal compressibility (kappa_T) in 1/Pa.  IAPWS09 Table 3 (12)."""
    return -d2G_dp2(gfunc)(*args) / dG_dp(gfunc)(*args)


def isenotropic_compressibility(*args, gfunc=default):
    """Isentropic compressibility (kappa_s) in 1/Pa.  IAPWS09 Table 3 (13)."""
    return (
        d2G_dTdp(gfunc)(*args) ** 2 - d2G_dT2(gfunc)(*args) * d2G_dp2(gfunc)(*args)
    ) / (dG_dp(gfunc)(*args) * dG_dT(gfunc)(*args))


def sound_speed(*args, gfunc=default):
    """Speed of sound (w) in m/s.  IAPWS09 Table 3 (14)."""
    return dG_dp(gfunc)(*args) * np.sqrt(
        d2G_dT2(gfunc)(*args)
        / (d2G_dTdp(gfunc)(*args) ** 2 - d2G_dT2(gfunc)(*args) * d2G_dp2(gfunc)(*args))
    )


def chemical_potential_relative(*args, gfunc=default):
    """Relative chemical potential (mu) in J/kg.  IAPWS08 Table 5 (25)."""
    return dG_dS(gfunc)(*args)


def chemical_potential_water(*args, gfunc=default):
    """Chemical potential of H2O (mu_W) in J/kg.  IAPWS08 Table 5 (26)."""
    if len(args) == 3:
        salinity_s = args[2] * constants.salinity_to_salt
        cpw = gfunc(*args) - salinity_s * dG_dS(gfunc)(*args)
    else:
        cpw = gfunc(*args)
    return cpw


def chemical_potential_salt(*args, gfunc=default):
    """Chemical potential of sea salt (mu_S) in J/kg.  IAPWS08 Table 5 (27)."""
    salinity_s = args[2] * constants.salinity_to_salt
    return gfunc(*args) + (1 - salinity_s) * dG_dS(gfunc)(*args)


def molality_seawater(salinity):
    """Molality of seawater from its salinity."""
    salinity_s = salinity * constants.salinity_to_salt
    return salinity_s / ((1.0 - salinity_s) * constants.salt_mass)


def osmotic(*args, gfunc=default):
    """Osmotic coefficient (phi), dimensionless.  IAPWS08 Table 5 (28)."""
    salinity_s = args[2] * constants.salinity_to_salt
    return -chemical_potential_water(*args, gfunc=default) / (
        molality_seawater(salinity_s) * constants.gas_constant * args[0]
    )


def haline_contraction(*args, gfunc=default):
    """Haline contraction coefficient (beta) in kg/kg.  IAPWS08 Table 5 (29)."""
    return -d2G_dSdp(gfunc)(*args) / dG_dp(gfunc)(*args)
