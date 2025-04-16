import pandas as pd
from Filters import utils

def match_stoichimetric_combinations(icsd_true: pd.DataFrame, df: pd.DataFrame) -> pd.Series:
    """
    Checks which stoichiometries have been seen before in other material systems.

    Args:
    stoichiometry (list): The stoichiometry to be matched.
    df (pandas.DataFrame): The input DataFrame, expected to have a column named "Atoms".

    Returns:
    pandas.Series: A Series indicating whether the atoms in each row of the input DataFrame match the given stoichiometry.
    """
    # Existing Stoichioemtry
    stoichiometry = [[3, 1, 6],[3, 2, 9],[1, 1, 4],[2, 1, 6],[1, 1, 3],[1, 2, 5],[4, 1, 6],[1, 2, 7],[2, 1, 5],[3, 1, 5]]
    atoms = [eval(atom) for atom in df["Atoms"].to_list()]  # Convert string representations of lists to actual lists
    matches = [atom in stoichiometry for atom in atoms]  # Check membership using a list comprehension
    nov_mat = df[['composition', 'Atoms']][matches].copy()  # Create a new DataFrame with the selected columns where matches is True
    nov_mat = nov_mat.rename(columns={'composition': 'Novel Material', 'Atoms': 'Atoms'})

    nov_mat['icsd_ids'] = None  # Initialize the 'icsd_ids' column with None values
    
    #find the matches with ICSD
    nov_mat_db, true_positive = utils.icsd_finder(icsd_true=icsd_true, nov_mat=nov_mat)  # Call the icsd_finder function to match ICSD IDs
    
    #calculate the true positive and false positive and the synthetic p_value
    p_syn = utils.p_syn(nov_mat_db, true_positive)
    
    utils.save("stoichimetry_match", nov_mat_db, df_name='Ternary_perovskite')  # Save the DataFrame to a CSV file
    return nov_mat_db, true_positive, p_syn  # Return the updated DataFrame and the count of true positives