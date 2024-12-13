# teos10: unofficial Python implementation of the TEOS-10 properties of water.
# Copyright (C) 2020-2024  Matthew Paul Humphreys  (GNU GPLv3)
"""Gibbs energy functions."""

import itertools
from collections import namedtuple

from jax import numpy as np

from . import constants

GibbsValidity = namedtuple("GibbsValidity", ("total", "temperature", "pressure"))


def validity(temperature, pressure):
    """Validity checker for input temperature and pressure values.

    The validity ranges are:
        100 < pressure_Pa < 1e8 Pa
       (270.5 - pressure_Pa*7.43e-8) < temperature < 313.15 K
    where pressure_Pa = pressure * 10000.

    Parameters
    ----------
    temperature : float
        Temperature in K.
    pressure : float
        Pressure in dbar.

    Returns
    -------
    GibbsValidity (namedtuple)
        Whether the input temperature(s) and pressure(s) are valid, separated into the
        component fields:
            total : bool
                Whether both temperature and pressure are valid.
            temperature : bool
                Whether the temperature is valid.
            pressure : bool
                Whether the pressure is valid.
    """
    pressure_Pa = pressure * constants.dbar_to_Pa
    vt = ((270.5 - pressure_Pa * 7.43e-8) < temperature) & (temperature <= 313.15)
    vp = (100 <= pressure_Pa) & (pressure_Pa <= 1e8)
    valid = vt & vp
    return GibbsValidity(valid, vt, vp)


def water(temperature, pressure):
    """Gibbs energy of pure water in J/kg.

    Source: http://www.teos-10.org/pubs/IAPWS-2009-Supplementary.pdf (IAPWS09).

    Validity:
        100 < pressure_Pa < 1e8 Pa
       (270.5 - pressure_Pa*7.43e-8) < temperature < 313.15 K
    where pressure_Pa = pressure * 10000.

    Parameters
    ----------
    temperature : float
        Temperature in K.
    pressure : float
        Pressure in dbar.

    Returns
    -------
    float
        The Gibbs energy in J/kg.
    """
    # Coefficients of the Gibbs function as defined in IAPWS09 Table 2
    Gdict = {
        (0, 0): +0.101_342_743_139_674 * 10**3,
        (3, 2): +0.499_360_390_819_152 * 10**3,
        (0, 1): +0.100_015_695_367_145 * 10**6,
        (3, 3): -0.239_545_330_654_412 * 10**3,
        (0, 2): -0.254_457_654_203_630 * 10**4,
        (3, 4): +0.488_012_518_593_872 * 10**2,
        (0, 3): +0.284_517_778_446_287 * 10**3,
        (3, 5): -0.166_307_106_208_905 * 10,
        (0, 4): -0.333_146_754_253_611 * 10**2,
        (4, 0): -0.148_185_936_433_658 * 10**3,
        (0, 5): +0.420_263_108_803_084 * 10,
        (4, 1): +0.397_968_445_406_972 * 10**3,
        (0, 6): -0.546_428_511_471_039,
        (4, 2): -0.301_815_380_621_876 * 10**3,
        (1, 0): +0.590_578_347_909_402 * 10,
        (4, 3): +0.152_196_371_733_841 * 10**3,
        (1, 1): -0.270_983_805_184_062 * 10**3,
        (4, 4): -0.263_748_377_232_802 * 10**2,
        (1, 2): +0.776_153_611_613_101 * 10**3,
        (5, 0): +0.580_259_125_842_571 * 10**2,
        (1, 3): -0.196_512_550_881_220 * 10**3,
        (5, 1): -0.194_618_310_617_595 * 10**3,
        (1, 4): +0.289_796_526_294_175 * 10**2,
        (5, 2): +0.120_520_654_902_025 * 10**3,
        (1, 5): -0.213_290_083_518_327 * 10,
        (5, 3): -0.552_723_052_340_152 * 10**2,
        (2, 0): -0.123_577_859_330_390 * 10**5,
        (5, 4): +0.648_190_668_077_221 * 10,
        (2, 1): +0.145_503_645_404_680 * 10**4,
        (6, 0): -0.189_843_846_514_172 * 10**2,
        (2, 2): -0.756_558_385_769_359 * 10**3,
        (6, 1): +0.635_113_936_641_785 * 10**2,
        (2, 3): +0.273_479_662_323_528 * 10**3,
        (6, 2): -0.222_897_317_140_459 * 10**2,
        (2, 4): -0.555_604_063_817_218 * 10**2,
        (6, 3): +0.817_060_541_818_112 * 10,
        (2, 5): +0.434_420_671_917_197 * 10,
        (7, 0): +0.305_081_646_487_967 * 10,
        (3, 0): +0.736_741_204_151_612 * 10**3,
        (7, 1): -0.963_108_119_393_062 * 10,
        (3, 1): -0.672_507_783_145_070 * 10**3,
    }
    # Convert units
    pressure_Pa = pressure * constants.dbar_to_Pa
    # Reduce temperature and pressure
    ctau = (temperature - constants.temperature_zero) / constants.temperature_st
    cpi = (pressure_Pa - constants.pressure_n) / constants.pressure_st
    # Initialise with zero and increment following Eq. (1)
    Gpure = np.zeros_like(temperature)
    for j, k in itertools.product(range(8), range(7)):
        if (j, k) in Gdict.keys():
            Gpure = Gpure + Gdict[(j, k)] * ctau**j * cpi**k
    return Gpure


def salt(temperature, pressure, salinity):
    """Saline part of the Gibbs energy of seawater in J/kg.

    Source: http://www.teos-10.org/pubs/IAPWS-08.pdf (IAPWS08).

    Validity:
        100 < pressure_Pa < 1e8 Pa
        (270.5 - pressure_Pa*7.43e-8) < temperature < 313.15 K
     where pressure_Pa = pressure * 10000.

    Parameters
    ----------
    temperature : float
        Temperature in K.
    pressure : float
        Pressure in dbar.
    salinity : float
        Reference-composition salinity in g/kg.

    Returns
    -------
    float
        The Gibbs energy in J/kg.
    """
    # Coefficients of the Gibbs function as defined in IAPWS08 Table 2
    Gdict = {
        (1, 0, 0): +0.581_281_456_626_732 * 10**4,
        (2, 2, 1): -0.860_764_303_783_977 * 10**3,
        (2, 0, 0): +0.141_627_648_484_197 * 10**4,
        (3, 2, 1): +0.383_058_066_002_476 * 10**3,
        (3, 0, 0): -0.243_214_662_381_794 * 10**4,
        (2, 3, 1): +0.694_244_814_133_268 * 10**3,
        (4, 0, 0): +0.202_580_115_603_697 * 10**4,
        (3, 3, 1): -0.460_319_931_801_257 * 10**3,
        (5, 0, 0): -0.109_166_841_042_967 * 10**4,
        (2, 4, 1): -0.297_728_741_987_187 * 10**3,
        (6, 0, 0): +0.374_601_237_877_840 * 10**3,
        (3, 4, 1): +0.234_565_187_611_355 * 10**3,
        (7, 0, 0): -0.485_891_069_025_409 * 10**2,
        (2, 0, 2): +0.384_794_152_978_599 * 10**3,
        (1, 1, 0): +0.851_226_734_946_706 * 10**3,
        (3, 0, 2): -0.522_940_909_281_335 * 10**2,
        (2, 1, 0): +0.168_072_408_311_545 * 10**3,
        (4, 0, 2): -0.408_193_978_912_261 * 10,
        (2, 1, 2): -0.343_956_902_961_561 * 10**3,
        (3, 1, 0): -0.493_407_510_141_682 * 10**3,
        (4, 1, 0): +0.543_835_333_000_098 * 10**3,
        (3, 1, 2): +0.831_923_927_801_819 * 10**2,
        (5, 1, 0): -0.196_028_306_689_776 * 10**3,
        (2, 2, 2): +0.337_409_530_269_367 * 10**3,
        (6, 1, 0): +0.367_571_622_995_805 * 10**2,
        (3, 2, 2): -0.541_917_262_517_112 * 10**2,
        (2, 2, 0): +0.880_031_352_997_204 * 10**3,
        (2, 3, 2): -0.204_889_641_964_903 * 10**3,
        (3, 2, 0): -0.430_664_675_978_042 * 10**2,
        (2, 4, 2): +0.747_261_411_387_560 * 10**2,
        (4, 2, 0): -0.685_572_509_204_491 * 10**2,
        (2, 0, 3): -0.965_324_320_107_458 * 10**2,
        (2, 3, 0): -0.225_267_649_263_401 * 10**3,
        (3, 0, 3): +0.680_444_942_726_459 * 10**2,
        (3, 3, 0): -0.100_227_370_861_875 * 10**2,
        (4, 0, 3): -0.301_755_111_971_161 * 10**2,
        (4, 3, 0): +0.493_667_694_856_254 * 10**2,
        (2, 1, 3): +0.124_687_671_116_248 * 10**3,
        (2, 4, 0): +0.914_260_447_751_259 * 10**2,
        (3, 1, 3): -0.294_830_643_494_290 * 10**2,
        (3, 4, 0): +0.875_600_661_808_945,
        (2, 2, 3): -0.178_314_556_207_638 * 10**3,
        (4, 4, 0): -0.171_397_577_419_788 * 10**2,
        (3, 2, 3): +0.256_398_487_389_914 * 10**2,
        (2, 5, 0): -0.216_603_240_875_311 * 10**2,
        (2, 3, 3): +0.113_561_697_840_594 * 10**3,
        (4, 5, 0): +0.249_697_009_569_508 * 10,
        (2, 4, 3): -0.364_872_919_001_588 * 10**2,
        (2, 6, 0): +0.213_016_970_847_183 * 10,
        (2, 0, 4): +0.158_408_172_766_824 * 10**2,
        (2, 0, 1): -0.331_049_154_044_839 * 10**4,
        (3, 0, 4): -0.341_251_932_441_282 * 10,
        (2, 1, 4): -0.316_569_643_860_730 * 10**2,
        (3, 0, 1): +0.199_459_603_073_901 * 10**3,
        (4, 0, 1): -0.547_919_133_532_887 * 10**2,
        (2, 2, 4): +0.442_040_358_308_000 * 10**2,
        (5, 0, 1): +0.360_284_195_611_086 * 10**2,
        (2, 3, 4): -0.111_282_734_326_413 * 10**2,
        (2, 1, 1): +0.729_116_529_735_046 * 10**3,
        (2, 0, 5): -0.262_480_156_590_992 * 10,
        (3, 1, 1): -0.175_292_041_186_547 * 10**3,
        (2, 1, 5): +0.704_658_803_315_449 * 10,
        (4, 1, 1): -0.226_683_558_512_829 * 10**2,
        (2, 2, 5): -0.792_001_547_211_682 * 10,
    }
    # Convert units
    pressure_Pa = pressure * constants.dbar_to_Pa
    salinity_s = salinity * constants.salinity_to_salt
    # Reduce temperature, pressure and salinity
    ctau = (temperature - constants.temperature_zero) / constants.temperature_st
    cpi = (pressure_Pa - constants.pressure_n) / constants.pressure_st
    cxi = np.sqrt(salinity_s / constants.salinity_st)
    cxi2_lncxi = cxi**2 * np.log(cxi)
    # Initialise with zero and increment following Eq. (4)
    Gsalt = np.zeros_like(temperature)
    for j, k in itertools.product(range(7), range(6)):
        addG = np.zeros_like(temperature)
        if (1, j, k) in Gdict:
            addG = Gdict[(1, j, k)] * cxi2_lncxi
        for i in range(2, 8):
            if (i, j, k) in Gdict:
                addG = addG + Gdict[(i, j, k)] * cxi**i
        Gsalt = Gsalt + addG * ctau**j * cpi**k
    return Gsalt


def seawater(temperature, pressure_Pa, salinity):
    """Gibbs energy of seawater in J/kg.

    Parameters
    ----------
    temperature : float
        Temperature in K.
    pressure : float
        Pressure in dbar.
    salinity : float
        Reference-composition salinity in g/kg.

    Returns
    -------
    float
        The Gibbs energy in J/kg.
    """
    return water(temperature, pressure_Pa) + salt(temperature, pressure_Pa, salinity)
