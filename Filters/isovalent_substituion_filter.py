import pandas as pd

def match_stoichimetric_combinations(df: pd.DataFrame):
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

    atoms = pd.Series(df["Atoms"])
    matches = atoms.isin(stoichiometry)
    return matches