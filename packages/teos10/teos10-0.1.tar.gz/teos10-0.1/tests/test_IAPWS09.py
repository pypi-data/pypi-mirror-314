import numpy as np

import teos10

# Check values from IAPWS09 Table 6
temperature_water = np.array([273.15, 273.15, 313.15])
pressure_water = np.array([101_325, 1e8, 101_325]) / teos10.constants.dbar_to_Pa
check_water = {
    "gibbs": [0.101_342_743e3, 0.977_303_868e5, -0.116_198_898e5],  # J kg-1
    "dG_dT": [0.147_644_587, 0.851_506_346e1, -0.572_365_181e3],  # J kg-1 K-1
    "dG_dp": [0.100_015_695e-2, 0.956_683_354e-3, 0.100_784_471e-2],  # m3 kg-1
    "d2G_dT2": [-0.154_472_324e2, -0.142_970_174e2, -0.133_463_968e2],  # J kg-1 K-2
    "d2G_dTdp": [-0.677_459_513e-7, 0.199_088_060e-6, 0.388_499_694e-6],  # m3 kg-1 K-1
    "d2G_dp2": [
        -0.508_915_308e-12,
        -0.371_527_164e-12,
        -0.445_841_077e-12,
    ],  # m3 kg-1 Pa-1
    "enthalpy": [0.610_136_242e2, 0.954_044_973e5, 0.167_616_267e6],  # J kg-1
    "helmholtz_energy": [0.183_980_891e-2, 0.206_205_140e4, -0.117_220_097e5],  # J kg-1
    "internal_energy": [-0.403_272_791e2, -0.263_838_183e3, 0.167_514_147e6],  # J kg-1
    "entropy": [-0.147_644_587, -0.851_506_346e1, 0.572_365_181e3],  # J kg-1 K-1
    "density": [0.999_843_071e3, 0.104_527_793e4, 0.992_216_354e3],  # kg m-3
    "heat_capacity": [0.421_941_153e4, 0.390_523_030e4, 0.417_942_416e4],  # J kg-1 K-1
    "sound_speed": [0.140_240_099e4, 0.157_543_089e4, 0.152_891_242e4],  # m s-1
}


def factor_sigfig(x):
    return 10.0 ** np.ceil(np.log10(np.abs(x)))


def sigfig(x, sf):
    """Return `x` to `sf` significant figures."""
    factor = 10.0 ** np.ceil(np.log10(np.abs(x)))
    return factor * np.round(x / factor, decimals=sf)


def formatter(values):
    return ("{:.8e} " * len(values)).format(*sigfig(values, 9))


def test_gibbs_water():
    """Compare pure water Gibbs energy with check values from IAPWS09."""
    test_values = []
    for t, p in zip(temperature_water, pressure_water):
        test_values.append(teos10.gibbs.water(t, p))
    assert formatter(check_water["gibbs"]) == formatter(test_values)


def test_dG_dT_water():
    """Compare temperature derivative of pure water Gibbs energy with check values from
    IAPWS09.
    """
    test_values = []
    for t, p in zip(temperature_water, pressure_water):
        test_values.append(teos10.properties.dG_dT(teos10.gibbs.water)(t, p))
    assert formatter(check_water["dG_dT"]) == formatter(test_values)


def test_dG_dp_water():
    """Compare pressure derivative of pure water Gibbs energy with check values from
    IAPWS09.
    """
    test_values = []
    for t, p in zip(temperature_water, pressure_water):
        test_values.append(teos10.properties.dG_dp(teos10.gibbs.water)(t, p))
    assert formatter(check_water["dG_dp"]) == formatter(test_values)


def test_d2G_dT2_water():
    """Compare second temperature derivative of pure water Gibbs energy with check
    values from IAPWS09.
    """
    test_values = []
    for t, p in zip(temperature_water, pressure_water):
        test_values.append(teos10.properties.d2G_dT2(teos10.gibbs.water)(t, p))
    assert formatter(check_water["d2G_dT2"]) == formatter(test_values)


def test_d2G_dTdp_water():
    """Compare temperature-pressure derivative of pure water Gibbs energy with check
    values from IAPWS09.
    """
    test_values = []
    for t, p in zip(temperature_water, pressure_water):
        test_values.append(teos10.properties.d2G_dTdp(teos10.gibbs.water)(t, p))
    assert formatter(check_water["d2G_dTdp"]) == formatter(test_values)


def test_d2G_dp2_water():
    """Compare temperature-pressure derivative of pure water Gibbs energy with check
    values from IAPWS09.
    """
    test_values = []
    for t, p in zip(temperature_water, pressure_water):
        test_values.append(teos10.properties.d2G_dp2(teos10.gibbs.water)(t, p))
    assert formatter(check_water["d2G_dp2"]) == formatter(test_values)


def test_enthalpy_water():
    """Compare pure water enthalpy with check values from IAPWS09."""
    test_values = []
    for t, p in zip(temperature_water, pressure_water):
        test_values.append(teos10.enthalpy(t, p, gfunc=teos10.gibbs.water))
    assert formatter(check_water["enthalpy"]) == formatter(test_values)


def test_helmholtz_energy_water():
    """Compare pure water Helmholtz energy with check values from IAPWS09."""
    test_values = []
    for t, p in zip(temperature_water, pressure_water):
        test_values.append(teos10.helmholtz_energy(t, p, gfunc=teos10.gibbs.water))
    assert formatter(check_water["helmholtz_energy"]) == formatter(test_values)


def test_internal_energy_water():
    """Compare pure water internal energy with check values from IAPWS09."""
    test_values = []
    for t, p in zip(temperature_water, pressure_water):
        test_values.append(teos10.internal_energy(t, p, gfunc=teos10.gibbs.water))
    assert formatter(check_water["internal_energy"]) == formatter(test_values)


def test_entropy_water():
    """Compare pure water entropy with check values from IAPWS09."""
    test_values = []
    for t, p in zip(temperature_water, pressure_water):
        test_values.append(teos10.entropy(t, p, gfunc=teos10.gibbs.water))
    assert formatter(check_water["entropy"]) == formatter(test_values)


def test_density_water():
    """Compare pure water density with check values from IAPWS09."""
    test_values = []
    for t, p in zip(temperature_water, pressure_water):
        test_values.append(teos10.density(t, p, gfunc=teos10.gibbs.water))
    assert formatter(check_water["density"]) == formatter(test_values)


def test_heat_capacity_water():
    """Compare pure water heat capacity with check values from IAPWS09."""
    test_values = []
    for t, p in zip(temperature_water, pressure_water):
        test_values.append(teos10.heat_capacity(t, p, gfunc=teos10.gibbs.water))
    assert formatter(check_water["heat_capacity"]) == formatter(test_values)


def test_sound_speed_water():
    """Compare pure water sound speed with check values from IAPWS09."""
    test_values = []
    for t, p in zip(temperature_water, pressure_water):
        test_values.append(teos10.sound_speed(t, p, gfunc=teos10.gibbs.water))
    assert formatter(check_water["sound_speed"]) == formatter(test_values)
