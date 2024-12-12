import logging
import dfauditor.metrics
import dfauditor.response
import pandas as pd
import numpy as np

import dfauditor.app_logger

log = dfauditor.app_logger.get(log_level=logging.INFO)

class BinConfigException(Exception):
    pass

"""
take a pandas series and extract stats according to column type
"""

def numeric(series):
    stats = dfauditor.response.Numeric()
    stats.attr = series.name
    stats.mean = series.mean()
    stats.std = series.std()
    stats.variance = series.var()
    stats.min = series.min()
    stats.max = series.max()
    stats.range = stats.max - stats.min
    stats.median, stats.iqr = dfauditor.metrics.median_iqr(series)
    stats.kurtosis = series.kurt()
    stats.skewness = series.skew()
    stats.mad = np.abs(series - series.mean()).mean()
    stats.p_zeros = float(series[series == 0].count()) / len(series.index) * 100
    stats.p_nan = float(series.isna().sum()) / len(series.index) * 100
    return stats


def string(series, head=3):
    # Only run if at least 1 non-missing value
    stats = dfauditor.response.String()
    stats.attr = series.name
    value_counts = series.value_counts(dropna=False)
    distinct = value_counts.count()
    stats.distinct = distinct
    for n, v in zip(value_counts.index[0:head], value_counts.iloc[0:head].values):
        stats.freq.append({'name': n, 'value': v})
    return stats

def round_bin_range(bin_range, decimal_places):
    if bin_range.startswith('['):
        # print(f"Processing bin_range: {bin_range}")
        parts = bin_range.strip('[]()').split(', ')
        rounded_parts = [str(round(float(part), decimal_places)) for part in parts]
        # print(f"Rounded parts: {rounded_parts}")
        return f"[{rounded_parts[0]}, {rounded_parts[1]}]"
    elif bin_range.startswith('('):
        # print(f"Processing bin_range: {bin_range}")
        parts = bin_range.strip('[]()').split(', ')
        rounded_parts = [str(round(float(part), decimal_places)) for part in parts]
        # print(f"Rounded parts: {rounded_parts}")
        return f"({rounded_parts[0]}, {rounded_parts[1]}]"
    else:
        return bin_range

def bins(series, lower_bound=0, upper_bound=1, size=10):
    """
    apply binning to a domain (x)
    :param series:
    :param lower_bound: The lower boundary to use for bin size calc, default: 0.
    :param upper_bound: The upper boundary to use for bin size calc, default: 1
    :param size: number of bins
    :return: size
    """

    series_min = series.min()
    series_max = series.max()
    if lower_bound == 0 and upper_bound == 1 and (series_min < lower_bound or series_max > upper_bound):
        raise BinConfigException("The series bounds fall outside the supplied lower/upper bounds of 0 and 1")

    resp_data = dfauditor.response.Bins(size=size, lower_bound=lower_bound, upper_bound=upper_bound)
    resp_data.attr = series.name

    vc = pd.cut(series, bins=resp_data.bin_config.tolist(), include_lowest=True).value_counts()
    resp_data.load(counts=vc)

    decimal_places = 3
    bin_ranges_dict = {'bin_range_' + str(i): str(bin_range) for i, bin_range in enumerate(vc.index)}
    bin_ranges = {
        key: '[' + str(round_bin_range(value, decimal_places)).strip('(]') + ']' if list(bin_ranges_dict.keys()).index(key) == 0 else round_bin_range(value, decimal_places)
        for key, value in bin_ranges_dict.items()}
    bin_counts_dict = {f"bin_count_{i}": count for i, count in enumerate(vc)}

    for key, value in bin_counts_dict.items():
        setattr(resp_data, key, value)
    for key, value in bin_ranges.items():
        setattr(resp_data, key, value)

    return resp_data