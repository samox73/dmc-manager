import numpy as np
from scipy.optimize import curve_fit


def exp_model(tau_, z0_, a_):
    return z0_ * np.exp(-a_ * tau_)


def fit_exp(
    grid, G_t, stats, begin=10, end=None, z_estimate=0.5, e_estimate=-1, verbose=False
):
    if end == None:
        end = stats["max_tau"]
    mu = stats["mu"]
    idx_min = np.where(grid > begin)[0][0]
    idx_max = np.where(grid < end)[0][-1]
    if verbose:
        print(f"Fitting from {grid[idx_min]} to {grid[idx_max]}")
    args, _ = curve_fit(
        exp_model,
        grid[idx_min:idx_max],
        G_t[idx_min:idx_max],
        p0=[z_estimate, e_estimate - mu],
    )
    Z0 = args[0]
    E0 = args[1] + mu
    if verbose:
        print(f"Z0 = {Z0:.5f}")
        print(f"E0 = {E0:.5f}")
    return Z0, E0


def E1(momenta_, alphas_):
    if not isinstance(momenta_, np.ndarray) and momenta_ == 0:
        return -alphas_
    else:
        return np.power(momenta_, 2) / 2 - alphas_ * np.sqrt(2) / momenta_ * np.arcsin(
            momenta_ / np.sqrt(2)
        )


def E2(momenta_=np.linspace(0, 1.6, 1000), alpha_=1):
    m_eff_ = 1 / (1 - alpha_ / 6)
    return (
        np.power(momenta_, 2) / (2 * m_eff_)
        - alpha_
        - 2 / 3 * (1 / 8 - 1 / (3 * np.pi)) * alpha_**2
    )


def Z1(alphas_):
    return 1 - alphas_ / 2
