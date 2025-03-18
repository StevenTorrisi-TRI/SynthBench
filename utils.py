import numpy
import pandas as pd
import datetime
import os

def save(filter_name, df, df_name=None):
    """
    Saves the input DataFrame to a CSV file.

    Args:
    filter_name (str): The name of the filter.
    df (pandas.DataFrame): The DataFrame to be saved.

    Returns:
    None
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    if df_name is None:
        df_name = "df"
        filename = f"{df_name}_{timestamp}_{filter_name}.csv"
    else:
        filename = f"{df_name}_{timestamp}_{filter_name}.csv"
    results_dir = "Results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    filename = os.path.join(results_dir, filename)
    df.to_csv(filename, index=False)
    