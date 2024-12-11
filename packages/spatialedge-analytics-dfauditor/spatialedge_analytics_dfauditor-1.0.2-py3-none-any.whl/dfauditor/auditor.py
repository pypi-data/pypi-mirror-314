import logging
from multiprocessing import Pool, cpu_count

import pandas as pd
import psutil

import dfauditor.app_logger
import dfauditor.extractor

log = dfauditor.app_logger.get(log_level=logging.INFO)


def profile_number_columns(series_items):
    log.debug('name: {}; row.count: {}; used: {}% free: {:.2f}GB'.format(series_items[0],
                                                                         len(series_items[1].index),
                                                                         psutil.virtual_memory().percent,
                                                                         float(
                                                                             psutil.virtual_memory().free) / 1024 ** 3))
    return dfauditor.extractor.numeric(series_items[1]).__dict__


def profile_string_columns(series_items):
    log.debug('name: {}; row.count: {}; used: {}% free: {:.2f}GB'.format(series_items[0],
                                                                         len(series_items[1].index),
                                                                         psutil.virtual_memory().percent,
                                                                         float(
                                                                             psutil.virtual_memory().free) / 1024 ** 3))
    return dfauditor.extractor.string(series_items[1]).__dict__


def profile_proba_bins(series, size):
    log.debug('name: {}; row.count: {}; used: {}% free: {:.2f}GB'.format(series.name,
                                                                         len(series.index),
                                                                         psutil.virtual_memory().percent,
                                                                         float(psutil.virtual_memory().free) / 1024 ** 3))
    return dfauditor.extractor.bins(series, size=size).__dict__

def profile_col_bins(series_items, lower_bound, upper_bound, bins):
    log.debug('name: {}; row.count: {}; used: {}% free: {:.2f}GB'.format(series_items.name,
                                                                         len(series_items),
                                                                         psutil.virtual_memory().percent,
                                                                         float(
                                                                             psutil.virtual_memory().free) / 1024 ** 3))
    return dfauditor.extractor.bins(series_items, lower_bound=lower_bound, upper_bound=upper_bound, size=bins).__dict__


def audit_dataframe(dataframe, nr_processes=None, proba_col_bins=[], col_bins=[]):
    """
    produce a profile of the dataframe 
    :param dataframe: a pandas dataframe 
    :param nr_processes: a integer value specifying the number of processes to use (ideally #{processes}<#{cpus}) 
    :param proba_col_bins: a list of tuples (column_name, nr_of_bins) - e.g. ('score', 10) 
        would give you ten bins on the score column. This should be used only on series ranging 0 to 1
    :param col_bins: a list of tuples (column_name, lower_bound, upper_bound, nr_of_bins) for columns
        that should be binned to custom values
    :return: a json body containing the derived metrics
    """
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError('Currently only supports panda dataframes')

    #If num processors not supplied default to the min of series count or CPU count
    if not nr_processes:
        nr_processes = min(dataframe.shape[1], cpu_count())
    else:
        nr_processes = min(nr_processes, cpu_count())

    with Pool(nr_processes) as pool:
        columns = dataframe.columns
        log.debug('auditing dataframe with {} rows and {} columns'.format(
            len(dataframe.index),
            len(columns)))
        # using generic numpy type labels
        number_df = dataframe.select_dtypes(include=['number'])
        string_df = dataframe.select_dtypes(include=['object'])

        res_list = pool.map(profile_number_columns, number_df.items())
        res_list += pool.map(profile_string_columns, string_df.items())
        if proba_col_bins:
            # change the shape of list of tuples [(name_i, bins_i),...] to
            #   [(name_0, ..., name_n), (bins_0, ..., bins_n)]
            proba_col_bins_t = list(zip(*proba_col_bins))
            res_list += pool.starmap(profile_proba_bins, [(series, size) for series, size in zip(proba_col_bins_t[0], proba_col_bins_t[1])])

        if col_bins and len(col_bins) > 0:
            col_bins_t = []
            for bin_conf in col_bins:
                col_bins_t.append(
                    (
                        dataframe[bin_conf[0]],
                        bin_conf[1],
                        bin_conf[2],
                        bin_conf[3],
                    )
                )

            res_list += pool.starmap(profile_col_bins, col_bins_t)

        return res_list