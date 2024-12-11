# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""
5 statistical stationarity tests for forecasting.
"""

import statsmodels.tsa.stattools as stattools
from arch import unitroot
import numpy as np
from azureml.automl.runtime.featurizer.transformer.timeseries import forecasting_heuristic_utils


def adf_test(series, **kw):
    """
    Wrapper for the augmented Dickey-Fuller test. Allows users to set the lag order.
    :param series: series to test
    :return: dictionary of results
    """
    try:
        if "lags" in kw.keys():
            statistic, pval, critval, resstore = stattools.adfuller(
                series, maxlag=kw["lags"], autolag=kw["autolag"], store=kw["store"]
            )
        else:
            statistic, pval, critval, resstore = stattools.adfuller(
                series, autolag=kw["IC"], store=kw["store"]
            )
    except ValueError as e:
        forecasting_heuristic_utils._log_warn_maybe("adf_test is failed", e)
        return None

    output = {
        "statistic": statistic,
        "pval": pval,
        "critical": critval,
        "resstore": resstore,
    }
    return output


def kpss_test(series, **kw):
    """
    Wrapper for the KPSS test. Allows users to set the lag order.
    :param series: series to test
    :return: dictionary of results
    """
    try:
        if kw["store"]:
            statistic, p_value, critical_values, rstore = stattools.kpss(
                series, regression=kw["reg_type"], nlags=kw["lags"], store=kw["store"]
            )
        else:
            statistic, p_value, lags, critical_values = stattools.kpss(
                series, regression=kw["reg_type"], nlags=kw["lags"]
            )
    except ValueError as e:
        forecasting_heuristic_utils._log_warn_maybe("kpss_test is failed", e)
        return None

    output = {
        "statistic": statistic,
        "pval": p_value,
        "critical": critical_values,
        "nlags": rstore.lags if kw["store"] else lags,
    }

    if kw["store"]:
        output.update({"resstore": rstore})
    return output


def unit_root_test_helper(test_dict):
    """
    Helper function to analyze if the data is nonStationary based on 5 unit root tests.
    :param test_dict: dictionary contains the unit root tests.
    :return: isStationary based on majority of unit root tests.
    """

    test_sum = {}
    for test_name, test in test_dict.items():
        # Check if the test failed by trying to extract the test statistic
        if test_name in ("ADF", "KPSS"):
            try:
                test["statistic"]
            except BaseException as e:
                forecasting_heuristic_utils._log_warn_maybe("test is failed", e)
                test = None
        else:
            try:
                test.stat
            except BaseException as e:
                forecasting_heuristic_utils._log_warn_maybe("test is failed", e)
                test = None

        # Here, we skip the current test since it failed to get test stats.
        if test is None:
            continue

        if test_name in ("ADF", "KPSS"):
            p_val = test["pval"]
        else:
            p_val = test.pvalue

        if test_name != "KPSS":
            stationary = "yes" if p_val < 0.05 else "not"
        else:
            stationary = "yes" if p_val > 0.05 else "not"
        test_sum[test_name] = stationary

    # decision based on the majority rule
    if len(test_sum) > 0:
        ratio = len([x for x in test_sum if test_sum[x] == "yes"]) / len(test_sum)
    else:
        ratio = 1  # all tests fail, assume the series is stationary

    # Majority rule. If the ratio is more than 0.5, assume the series in stationary.
    isStationary = True if(ratio > 0.5) else False

    return isStationary


def unit_root_test_wrapper(series, lags=None):
    np.random.seed(2014)
    """
    Main function to run multiple stationarity tests. Runs five tests and returns a summary table + decision
    based on the majority rule. If the number of tests that determine a series is stationary equals to the
    number of tests that deem it non-stationary, we assume the series is non-stationary.
        * Augmented Dickey-Fuller (ADF),
        * KPSS,
        * ADF using GLS,
        * Phillips-Perron (PP),
        * Zivot-Andrews (ZA)
    :param lags: (optional) parameter that allows user to run a series of tests for a specific lag value.
    :param series: series to test
    :return: isNonStationary
    """
    # setting for ADF and KPSS tests
    adf_settings = {"IC": "AIC", "store": True}
    kpss_settings = {"reg_type": "c", "lags": "auto", "store": True}

    # settings for PP, ADF GLS and ZA tests
    arch_test_settings = {}

    if lags is not None:
        adf_settings.update({"lags": lags, "autolag": None})
        kpss_settings.update({"lags:": lags})
        arch_test_settings = {"lags": lags}

    # Run individual tests
    adf = adf_test(series, **adf_settings)  # ADF test
    kpss = kpss_test(series, **kpss_settings)  # KPSS test
    pp = unitroot.PhillipsPerron(series, **arch_test_settings)  # Phillips-Perron test
    adfgls = unitroot.DFGLS(series, **arch_test_settings)  # ADF using GLS test
    za = unitroot.ZivotAndrews(series, **arch_test_settings)  # Zivot-Andrews test

    test_dict = {
        "ADF": adf,
        "KPSS": kpss,
        "PP": pp,
        "ADF GLS": adfgls,
        "ZA": za,
    }

    isStationary = unit_root_test_helper(test_dict)
    return isStationary
