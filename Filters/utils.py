import numpy
import pandas as pd
import datetime
import os
import matplotlib.pyplot as plt

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
    
def icsd_finder(icsd_true, nov_mat):
    """
    Matches novel materials with their corresponding ICSD (Inorganic Crystal Structure Database) IDs 
    and updates the novel materials DataFrame with the matched ICSD IDs.
    Args:
        icsd_true (pandas.DataFrame): A DataFrame containing the true ICSD data. 
            It must have at least the following columns:
            - 'pretty_formula': The chemical formula of the material.
            - 'icsd_ids': The corresponding ICSD IDs for the material.
        nov_mat (pandas.DataFrame): A DataFrame containing novel materials to be matched.
            It must have the following column:
            - 'Novel Material': The chemical formula of the novel material.
    Returns:
        tuple:
            - pandas.DataFrame: The updated `nov_mat` DataFrame with an additional column:
                - 'icsd_ids': A list of matched ICSD IDs for each novel material.
            - int: The count of true positive matches (number of novel materials found in `icsd_true`).
    Notes:
        - If a novel material matches multiple ICSD IDs, they are concatenated into a single string, 
          separated by commas.
        - If no match is found for a novel material, its 'icsd_ids' entry will remain empty.
    """

    icsd_ids = numpy.empty(len(nov_mat['Novel Material']), dtype=object)  # Initialize with dtype=object for strings
    matches = icsd_true[icsd_true['pretty_formula'].isin(nov_mat['Novel Material']) == True]
    matches = matches[['pretty_formula', 'icsd_ids']]
    true_positive = len(matches['pretty_formula'])
    for idx, materials in enumerate(matches['pretty_formula']):
        icsd = matches['icsd_ids'].iloc[idx]
        for idy, mat_new in enumerate(nov_mat['Novel Material']):
            if materials == mat_new:
                if icsd_ids[idy] is None or icsd_ids[idy] == '':
                    #icsd_ids[idy] = [','.join(map(str, icsd))]
                    icsd_ids[idy] = ','.join(map(str, icsd))
                else:
                    icsd_ids[idy] = [icsd_ids[idy] + ',' + ','.join(map(str, icsd))]   
    nov_mat['icsd_ids'] = icsd_ids
    return nov_mat, true_positive

def p_syn(nov_mat, true_positive):
    """
    Calculate the percentage of true positives in a dataset of novel materials 
    and generate a pie chart visualization.
    Args:
        nov_mat (dict): A dictionary containing a key 'Novel Material' which maps 
                        to a list of novel materials.
        true_positive (int): The number of true positive cases identified.
    Returns:
        float: The percentage of true positives in the dataset.
    Side Effects:
        Generates a pie chart using the `pie_chart` function to visualize the 
        proportion of true positives and false positives.
    """
    
    p_syn = true_positive*100/ (len(nov_mat['Novel Material']))
    pie_chart(true_positive, len(nov_mat['Novel Material'])-true_positive, p_syn)
    return p_syn


def add_details_to_csv(nov_mat, details):
    """
    Adds details to a given DataFrame or dictionary-like object.
    This function takes a matrix or dictionary-like object (`nov_mat`) and a dictionary of details (`details`).
    It adds each key from `details` as a new column or key in `nov_mat` and assigns the corresponding value
    from `details` to the first element of the newly added column or key.
    Args:
        nov_mat (dict or pandas.DataFrame): The matrix or dictionary-like object to which details will be added.
        details (dict): A dictionary containing key-value pairs to be added to `nov_mat`.
    Returns:
        dict or pandas.DataFrame: The updated `nov_mat` with the added details.
    Note:
        - This function assumes that `nov_mat` supports item assignment and indexing.
        - The first element of each new column or key in `nov_mat` is set to the corresponding value from `details`.
    """

    for items in details:
        print(items, details[items])
        if isinstance(details[items], (int, float)):  # Corrected isinstance usage
            nov_mat.loc[0, items] = details[items]

        elif isinstance(details[items], dict):  # Corrected isinstance usage
            idx = 0
            for keys in details[items].keys():
                nov_mat.loc[idx, items + "args"] = keys
                idx += 1
            idy = 0
            for values in details[items].values():
                nov_mat.loc[idy, items] = values
                idy += 1
            
        else:  # Corrected isinstance usage
            rows = len(details[items])
            for row in range(rows):  # Fixed variable name conflict
                nov_mat.loc[row, items] = details[items][row]
    return nov_mat

def pie_chart(true_positive, false_positive, p_syn):
    """
    Generates and saves a pie chart visualizing the proportions of true positives and false positives.
    Args:
        true_positive (int or float): The count or proportion of true positive values.
        false_positive (int or float): The count or proportion of false positive values.
        p_syn (float): A percentage value representing P-Syn, used in the chart title and filename.
    Behavior:
        - Creates a pie chart with two slices: 'True Positive' and 'False Positive'.
        - Uses custom colors and an exploded view for better visualization.
        - Displays the percentage of each slice on the chart.
        - Saves the chart as a PNG file in the "./Results/" directory with a filename based on the `p_syn` value.
        - Displays the chart in a pop-up window.
    Note:
        - Ensure the "./Results/" directory exists before calling this function to avoid file-saving errors.
        - The `p_syn` value is formatted to two decimal places in the chart title and filename.
    Returns:
        None
    """

    labels = ['True Positive', 'False Positive']
    sizes = [true_positive, false_positive]
    colors = ['#66c2a5', '#fc8d62']
    explode = (0.1, 0.1)  # explode the 1st slice
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=140)
    plt.title(f'P-Syn: {p_syn:.2f}%', fontsize=14)
    plt.savefig(f"./Results/pie_chart{p_syn}.png")
    plt.show()



