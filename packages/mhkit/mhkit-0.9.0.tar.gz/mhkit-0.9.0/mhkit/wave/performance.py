import numpy as np
import pandas as pd
import xarray as xr
import types
from scipy.stats import binned_statistic_2d as _binned_statistic_2d
from mhkit import wave
import matplotlib.pylab as plt
from os.path import join
from mhkit.utils import convert_to_dataarray


def capture_length(P, J, to_pandas=True):
    """
    Calculates the capture length (often called capture width).

    Parameters
    ------------
    P: numpy array, pandas Series, pandas DataFrame, xarray DataArray, or xarray Dataset
        Power [W]
    J: numpy array, pandas Series, pandas DataFrame, xarray DataArray, or xarray Dataset
        Omnidirectional wave energy flux [W/m]
    to_pandas: bool (optional)
        Flag to output pandas instead of xarray. Default = True.

    Returns
    ---------
    L: pandas Series or xarray DataArray
        Capture length [m]
    """
    if not isinstance(to_pandas, bool):
        raise TypeError(f"to_pandas must be of type bool. Got: {type(to_pandas)}")

    P = convert_to_dataarray(P)
    J = convert_to_dataarray(J)

    L = P / J

    if to_pandas:
        L = L.to_pandas()

    return L


def statistics(X, to_pandas=True):
    """
    Calculates statistics, including count, mean, standard
    deviation (std), min, percentiles (25%, 50%, 75%), and max.

    Note that std uses a degree of freedom of 1 in accordance with
    IEC/TS 62600-100.

    Parameters
    ------------
    X: numpy array, pandas Series, pandas DataFrame, xarray DataArray, or xarray Dataset
        Data
    to_pandas: bool (optional)
        Flag to output pandas instead of xarray. Default = True.

    Returns
    ---------
    stats: pandas Series or xarray DataArray
        Statistics
    """
    if not isinstance(to_pandas, bool):
        raise TypeError(f"to_pandas must be of type bool. Got: {type(to_pandas)}")

    X = convert_to_dataarray(X)

    count = X.count().item()
    mean = X.mean().item()
    std = _std_ddof1(X)
    q = X.quantile([0.0, 0.25, 0.5, 0.75, 1.0]).values
    variables = ["count", "mean", "std", "min", "25%", "50%", "75%", "max"]

    stats = xr.DataArray(
        data=[count, mean, std, q[0], q[1], q[2], q[3], q[4]],
        dims="index",
        coords={"index": variables},
    )

    if to_pandas:
        stats = stats.to_pandas()

    return stats


def _std_ddof1(a):
    # Standard deviation with degree of freedom equal to 1
    if len(a) == 0:
        return np.nan
    elif len(a) == 1:
        return 0
    else:
        return np.std(a, ddof=1)


def _performance_matrix(X, Y, Z, statistic, x_centers, y_centers):
    # General performance matrix function

    # Convert bin centers to edges
    xi = [np.mean([x_centers[i], x_centers[i + 1]]) for i in range(len(x_centers) - 1)]
    xi.insert(0, -np.inf)
    xi.append(np.inf)

    yi = [np.mean([y_centers[i], y_centers[i + 1]]) for i in range(len(y_centers) - 1)]
    yi.insert(0, -np.inf)
    yi.append(np.inf)

    # Override standard deviation with degree of freedom equal to 1
    if statistic == "std":
        statistic = _std_ddof1

    # Provide function to compute frequency
    def _frequency(a):
        return len(a) / len(Z)

    if statistic == "frequency":
        statistic = _frequency

    zi, x_edge, y_edge, binnumber = _binned_statistic_2d(
        X, Y, Z, statistic, bins=[xi, yi], expand_binnumbers=False
    )

    M = xr.DataArray(
        data=zi,
        dims=["x_centers", "y_centers"],
        coords={"x_centers": x_centers, "y_centers": y_centers},
    )

    return M


def capture_length_matrix(Hm0, Te, L, statistic, Hm0_bins, Te_bins, to_pandas=True):
    """
    Generates a capture length matrix for a given statistic

    Note that IEC/TS 62600-100 requires capture length matrices for
    the mean, std, count, min, and max.

    Parameters
    ------------
    Hm0: numpy array, pandas Series, pandas DataFrame, xarray DataArray, or xarray Dataset
        Significant wave height from spectra [m]
    Te: numpy array, pandas Series, pandas DataFrame, xarray DataArray, or xarray Dataset
        Energy period from spectra [s]
    L : numpy array, pandas Series, pandas DataFrame, xarray DataArray, or xarray Dataset
        Capture length [m]
    statistic: string
        Statistic for each bin, options include: 'mean', 'std', 'median',
        'count', 'sum', 'min', 'max', and 'frequency'.  Note that 'std' uses
        a degree of freedom of 1 in accordance with IEC/TS 62600-100.
    Hm0_bins: numpy array
        Bin centers for Hm0 [m]
    Te_bins: numpy array
        Bin centers for Te [s]
    to_pandas: bool (optional)
        Flag to output pandas instead of xarray. Default = True.

    Returns
    ---------
    LM: pandas DataFrame or xarray DataArray
        Capture length matrix with index equal to Hm0_bins and columns
        equal to Te_bins

    """
    Hm0 = convert_to_dataarray(Hm0)
    Te = convert_to_dataarray(Te)
    L = convert_to_dataarray(L)

    if not (isinstance(statistic, str) or callable(statistic)):
        raise TypeError(
            f"statistic must be of type str or callable. Got: {type(statistic)}"
        )
    if not isinstance(Hm0_bins, np.ndarray):
        raise TypeError(f"Hm0_bins must be of type np.ndarray. Got: {type(Hm0_bins)}")
    if not isinstance(Te_bins, np.ndarray):
        raise TypeError(f"Te_bins must be of type np.ndarray. Got: {type(Te_bins)}")
    if not isinstance(to_pandas, bool):
        raise TypeError(f"to_pandas must be of type bool. Got: {type(to_pandas)}")

    LM = _performance_matrix(Hm0, Te, L, statistic, Hm0_bins, Te_bins)

    if to_pandas:
        LM = LM.to_pandas()

    return LM


def wave_energy_flux_matrix(Hm0, Te, J, statistic, Hm0_bins, Te_bins, to_pandas=True):
    """
    Generates a wave energy flux matrix for a given statistic

    Parameters
    ------------
    Hm0: numpy array, pandas Series, pandas DataFrame, xarray DataArray, or xarray Dataset
        Significant wave height from spectra [m]
    Te: numpy array, pandas Series, pandas DataFrame, xarray DataArray, or xarray Dataset
        Energy period from spectra [s]
    J : numpy array, pandas Series, pandas DataFrame, xarray DataArray, or xarray Dataset
        Wave energy flux from spectra [W/m]
    statistic: string
        Statistic for each bin, options include: 'mean', 'std', 'median',
        'count', 'sum', 'min', 'max', and 'frequency'.  Note that 'std' uses a degree of freedom
        of 1 in accordance of IEC/TS 62600-100.
    Hm0_bins: numpy array
        Bin centers for Hm0 [m]
    Te_bins: numpy array
        Bin centers for Te [s]
    to_pandas: bool (optional)
        Flag to output pandas instead of xarray. Default = True.

    Returns
    ---------
    JM: pandas DataFrame or xarray DataArray
        Wave energy flux matrix with index equal to Hm0_bins and columns
        equal to Te_bins

    """
    Hm0 = convert_to_dataarray(Hm0)
    Te = convert_to_dataarray(Te)
    J = convert_to_dataarray(J)

    if not (isinstance(statistic, str) or callable(statistic)):
        raise TypeError(
            f"statistic must be of type str or callable. Got: {type(statistic)}"
        )
    if not isinstance(Hm0_bins, np.ndarray):
        raise TypeError(f"Hm0_bins must be of type np.ndarray. Got: {type(Hm0_bins)}")
    if not isinstance(Te_bins, np.ndarray):
        raise TypeError(f"Te_bins must be of type np.ndarray. Got: {type(Te_bins)}")
    if not isinstance(to_pandas, bool):
        raise TypeError(f"to_pandas must be of type bool. Got: {type(to_pandas)}")

    JM = _performance_matrix(Hm0, Te, J, statistic, Hm0_bins, Te_bins)

    if to_pandas:
        JM = JM.to_pandas()

    return JM


def power_matrix(LM, JM):
    """
    Generates a power matrix from a capture length matrix and wave energy
    flux matrix

    Parameters
    ------------
    LM: pandas DataFrame, xarray DataArray, or xarray Dataset
        Capture length matrix
    JM: pandas DataFrame, xarray DataArray, or xarray Dataset
        Wave energy flux matrix

    Returns
    ---------
    PM: pandas DataFrame, xarray DataArray, or xarray Dataset
        Power matrix

    """
    if not isinstance(LM, (pd.DataFrame, xr.DataArray, xr.Dataset)):
        raise TypeError(
            f"LM must be of type pd.DataFrame or xr.Dataset. Got: {type(LM)}"
        )
    if not isinstance(JM, (pd.DataFrame, xr.DataArray, xr.Dataset)):
        raise TypeError(
            f"JM must be of type pd.DataFrame or xr.Dataset. Got: {type(JM)}"
        )

    PM = LM * JM

    return PM


def mean_annual_energy_production_timeseries(L, J):
    """
    Calculates mean annual energy production (MAEP) from time-series

    Parameters
    ------------
    L: numpy array, pandas Series, pandas DataFrame, xarray DataArray, or xarray Dataset
        Capture length
    J: numpy array, pandas Series, pandas DataFrame, xarray DataArray, or xarray Dataset
        Wave energy flux

    Returns
    ---------
    maep: float
        Mean annual energy production

    """
    L = convert_to_dataarray(L)
    J = convert_to_dataarray(J)

    T = 8766  # Average length of a year (h)
    n = len(L)

    maep = T / n * (L * J).sum().item()

    return maep


def mean_annual_energy_production_matrix(LM, JM, frequency):
    """
    Calculates mean annual energy production (MAEP) from matrix data
    along with data frequency in each bin

    Parameters
    ------------
    LM: pandas DataFrame, xarray DataArray, or xarray Dataset
        Capture length
    JM: pandas DataFrame, xarray DataArray, or xarray Dataset
        Wave energy flux
    frequency: pandas DataFrame, xarray DataArray, or xarray Dataset
        Data frequency for each bin

    Returns
    ---------
    maep: float
        Mean annual energy production

    """
    LM = convert_to_dataarray(LM)
    JM = convert_to_dataarray(JM)
    frequency = convert_to_dataarray(frequency)

    if not LM.shape == JM.shape == frequency.shape:
        raise ValueError("LM, JM, and frequency must be of the same size")
    if not np.abs(frequency.sum() - 1) < 1e-6:
        raise ValueError("Frequency components must sum to one.")

    T = 8766  # Average length of a year (h)
    maep = T * np.nansum(LM * JM * frequency)

    return maep


def power_performance_workflow(
    S,
    h,
    P,
    statistic,
    frequency_bins=None,
    deep=False,
    rho=1205,
    g=9.80665,
    ratio=2,
    show_values=False,
    savepath="",
):
    """
    High-level function to compute power performance quantities of
    interest following IEC TS 62600-100 for given wave spectra.

    Parameters
    ------------
    S:  pandas Series, pandas DataFrame, xarray DataArray, or xarray Dataset
        Spectral density [m^2/Hz] indexed by frequency [Hz]
    h: float
        Water depth [m]
    P: numpy ndarray, pandas DataFrame, pandas Series, xarray DataArray, or xarray Dataset
        Power [W]
    statistic: string or list of strings
        Statistics for plotting capture length matrices,
        options include: "mean", "std", "median",
        "count", "sum", "min", "max", and "frequency".
        Note that "std" uses a degree of freedom of 1 in accordance with IEC/TS 62600-100.
        To output capture length matrices for multiple binning parameters,
        define as a list of strings: statistic = ["", "", ""]
    frequency_bins: numpy array or pandas Series (optional)
       Bin widths for frequency of S. Required for unevenly sized bins
    deep: bool (optional)
        If True use the deep water approximation. Default False. When
        False a depth check is run to check for shallow water. The ratio
        of the shallow water regime can be changed using the ratio
        keyword.
    rho: float (optional)
        Water density [kg/m^3]. Default = 1025 kg/m^3
    g: float (optional)
        Gravitational acceleration [m/s^2]. Default = 9.80665 m/s^2
    ratio: float or int (optional)
        Only applied if depth=False. If h/l > ratio,
        water depth will be set to deep. Default ratio = 2.
    show_values : bool (optional)
        Show values on the scatter diagram. Default = False.
    savepath: string (optional)
        Path to save figure. Terminate with '\'. Default="".

    Returns
    ---------
    LM: xarray dataset
        Capture length matrices

    maep_matrix: float
        Mean annual energy production
    """
    S = convert_to_dataarray(S)
    if not isinstance(h, (int, float)):
        raise TypeError(f"h must be of type int or float. Got: {type(h)}")
    P = convert_to_dataarray(P)
    if not isinstance(deep, bool):
        raise TypeError(f"deep must be of type bool. Got: {type(deep)}")
    if not isinstance(rho, (int, float)):
        raise TypeError(f"rho must be of type int or float. Got: {type(rho)}")
    if not isinstance(g, (int, float)):
        raise TypeError(f"g must be of type int or float. Got: {type(g)}")
    if not isinstance(ratio, (int, float)):
        raise TypeError(f"ratio must be of type int or float. Got: {type(ratio)}")

    # Compute the enegy periods from the spectra data
    Te = wave.resource.energy_period(S, frequency_bins=frequency_bins, to_pandas=False)

    # Compute the significant wave height from the NDBC spectra data
    Hm0 = wave.resource.significant_wave_height(
        S, frequency_bins=frequency_bins, to_pandas=False
    )

    # Compute the energy flux from spectra data and water depth
    J = wave.resource.energy_flux(
        S, h, deep=deep, rho=rho, g=g, ratio=ratio, to_pandas=False
    )

    # Calculate capture length from power and energy flux
    L = wave.performance.capture_length(P, J, to_pandas=False)

    # Generate bins for Hm0 and Te, input format (start, stop, step_size)
    Hm0_bins = np.arange(0, Hm0.values.max() + 0.5, 0.5)
    Te_bins = np.arange(0, Te.values.max() + 1, 1)

    # Create capture length matrices for each statistic based on IEC/TS 62600-100
    # Median, sum, frequency additionally provided
    LM = xr.Dataset()
    LM["mean"] = wave.performance.capture_length_matrix(
        Hm0, Te, L, "mean", Hm0_bins, Te_bins, to_pandas=False
    )
    LM["std"] = wave.performance.capture_length_matrix(
        Hm0, Te, L, "std", Hm0_bins, Te_bins, to_pandas=False
    )
    LM["median"] = wave.performance.capture_length_matrix(
        Hm0, Te, L, "median", Hm0_bins, Te_bins, to_pandas=False
    )
    LM["count"] = wave.performance.capture_length_matrix(
        Hm0, Te, L, "count", Hm0_bins, Te_bins, to_pandas=False
    )
    LM["sum"] = wave.performance.capture_length_matrix(
        Hm0, Te, L, "sum", Hm0_bins, Te_bins, to_pandas=False
    )
    LM["min"] = wave.performance.capture_length_matrix(
        Hm0, Te, L, "min", Hm0_bins, Te_bins, to_pandas=False
    )
    LM["max"] = wave.performance.capture_length_matrix(
        Hm0, Te, L, "max", Hm0_bins, Te_bins, to_pandas=False
    )
    LM["freq"] = wave.performance.capture_length_matrix(
        Hm0, Te, L, "frequency", Hm0_bins, Te_bins, to_pandas=False
    )

    # Create wave energy flux matrix using mean
    JM = wave.performance.wave_energy_flux_matrix(
        Hm0, Te, J, "mean", Hm0_bins, Te_bins, to_pandas=False
    )

    # Calculate maep from matrix
    maep_matrix = wave.performance.mean_annual_energy_production_matrix(
        LM["mean"], JM, LM["freq"]
    )

    # Plot capture length matrices using statistic
    for str in statistic:
        if str not in list(LM.data_vars):
            print("ERROR: Invalid Statistics passed")
            continue
        plt.figure(figsize=(12, 12), num="Capture Length Matrix " + str)
        ax = plt.gca()
        wave.graphics.plot_matrix(
            LM[str],
            xlabel="Te (s)",
            ylabel="Hm0 (m)",
            zlabel=str + " of Capture Length",
            show_values=show_values,
            ax=ax,
        )
        plt.savefig(join(savepath, "Capture Length Matrix " + str + ".png"))

    return LM, maep_matrix
