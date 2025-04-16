import pandas as pd
import utils
import os

def read_csv():
    """
    Reads a CSV file containing material data and returns it as a pandas DataFrame.
    The function ensures that the script works regardless of the current working directory
    by constructing the path to the CSV file relative to the script's location. It expects
    the CSV file to be located in a "Materials" subdirectory and named "extracted_table.csv".
    Raises:
        FileNotFoundError: If the CSV file does not exist at the specified path.
    Returns:
        pandas.DataFrame: A DataFrame containing the data from the CSV file.
    """

    # Ensure the script works regardless of the current working directory
    script_dir = os.path.dirname(__file__)
    csv_path = os.path.join(script_dir, "Materials", "extracted_table.csv")
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found at path: {csv_path}")
    elem_db = pd.read_csv(csv_path)
    return elem_db

def unpack_target(elem_prop:dict)-> tuple:
    """
    Extracts and returns the element, coordination, and charge information 
    from a given dictionary representing element properties.
    Parameters:
    elem_prop (dict): A dictionary containing the following keys:
        - 'element' (str): The name or symbol of the element.
        - 'coordination' (int): The coordination number of the element.
        - 'charge' (int or float): The charge associated with the element.
    Returns:
    tuple: A tuple containing:
        - element (str): The name or symbol of the element.
        - element_coordination (int): The coordination number of the element.
        - element_charge (int or float): The charge associated with the element.
    """

    element = elem_prop['element']
    element_coordination = elem_prop['coordination']
    element_charge = elem_prop['charge']
    return element, element_coordination, element_charge


def unpack_conditions(conditions, condtion_value):
    """
    Unpacks specific condition values from the provided dictionaries.
    This function extracts the values for 'charge', 'coordination', and 
    'Hume-Rothery' conditions from the input dictionaries. If a condition 
    is not present, its corresponding value is set to None.
    Args:
        conditions (list): A list of condition names to check for, such as 
            'charge', 'coordination', or 'Hume-Rothery'.
        condtion_value (dict): A dictionary containing the values for the 
            specified conditions.
    Returns:
        tuple: A tuple containing the following elements:
            - charge (any or None): The value associated with the 'charge' 
              condition, or None if not present.
            - coordination (any or None): The value associated with the 
              'coordination' condition, or None if not present.
            - target_property (any or None): The value associated with the 
              'target_property' key under 'Hume-Rothery', or None if not present.
            - target_percentage (any or None): The value associated with the 
              'target_percentage' key under 'Hume-Rothery', or None if not present.
    """

    if 'charge' in conditions: 
        charge = condtion_value['charge']
    else:
        charge = None
    if 'coordination' in conditions:
        coordination = condtion_value['coordination']
    else:
        coordination = None
    if 'Hume-Rothery' in conditions:
        target_property = condtion_value['target_property']
        target_percentage = condtion_value['target_percentage']
    else:
        target_property = None
        target_percentage = None
    return charge, coordination, target_property, target_percentage    

def find_substitutes(element, conditions, elem_db, charge, coordination, target_property, target_lb, target_ub):
    """
    Identifies potential substitute elements based on specified conditions and properties.
    Parameters:
        element (str): The element for which substitutes are being searched.
        conditions (list): A list of conditions to filter substitutes. Possible values include:
            - 'coordination': Filters substitutes based on coordination number.
            - 'Hume-Rothery': Filters substitutes based on a target property range.
        elem_db (pandas.DataFrame): A database of elements containing their properties.
        charge (int): The charge state of the element to match.
        coordination (int): The coordination number to match (used if 'coordination' is in conditions).
        target_property (str): The property name to filter substitutes (used if 'Hume-Rothery' is in conditions).
        target_lb (float): The lower bound of the target property range (used if 'Hume-Rothery' is in conditions).
        target_ub (float): The upper bound of the target property range (used if 'Hume-Rothery' is in conditions).
    Returns:
        pandas.DataFrame: A filtered DataFrame containing potential substitute elements that meet the specified conditions.
    """
    
    substitutes = elem_db[elem_db['Charge'] == charge]
    if 'coordination' in conditions:
        substitutes = substitutes[substitutes['Coordination'] == coordination]
    if 'Hume-Rothery' in conditions:
        substitutes = substitutes[(substitutes[target_property] >= target_lb) & (substitutes[target_property] <= target_ub)]
    if element in substitutes['Ion'].values:
        substitutes = substitutes[substitutes['Ion'] != element]
    return substitutes

def hume_rothery_rule(percentage, target_value):
    """
    Calculate the lower and upper bounds of a target value based on a given percentage.
    This function applies the Hume-Rothery rule to determine the range of values 
    (lower bound and upper bound) around a target value by adding and subtracting 
    a percentage of the target value.
    Parameters:
    -----------
    percentage : float
        The percentage value used to calculate the bounds. Should be a positive number.
    target_value : float
        The target value around which the bounds are calculated.
    Returns:
    --------
    tuple
        A tuple containing two float values:
        - target_lb: The lower bound of the target value.
        - target_ub: The upper bound of the target value.
    Example:
    --------
    >>> hume_rothery_rule(10, 100)
    (90.0, 110.0)
    """

    target_lb = target_value - (target_value*percentage/100)
    target_ub = target_value + (target_value*percentage/100)
    return target_lb, target_ub
    

def main(icsd_true, comp, elem_prop, conditions, condition_value):
    """
    Main function to identify novel materials based on substitution rules and evaluate their properties.
    Args:
        icsd_true (str): Path to the ICSD database file containing true positive materials.
        comp (str): Composition of the target material.
        elem_prop (tuple): Tuple containing the target element, its coordination, and charge.
        conditions (list): List of conditions to apply for substitution (e.g., "Hume-Rothery").
        condition_value (float): Value associated with the condition (e.g., percentage for Hume-Rothery rule).
    Returns:
        tuple: A tuple containing:
            - nov_mat_db (pd.DataFrame): DataFrame of novel materials with their properties and ICSD matches.
            - true_positive (int): Count of true positive matches with the ICSD database.
            - p_syn (float): Synthetic p-value calculated based on the matches.
    Workflow:
        1. Unpacks the target element properties and substitution conditions.
        2. Reads the element database and filters the target element based on its properties.
        3. If "Hume-Rothery" condition is specified, calculates the target property bounds.
        4. Identifies potential substitute elements based on the conditions.
        5. Generates novel material formulas using the substitutes.
        6. Matches the novel materials with the ICSD database to find true positives.
        7. Calculates the synthetic p-value and adds details to the results.
        8. Saves the results to a CSV file.
    Notes:
        - The function relies on several utility functions (e.g., `utils.icsd_finder`, `utils.p_syn`, `utils.save`) 
          and assumes the presence of a CSV file containing element properties.
        - The generated CSV file contains detailed information about the novel materials and their matches.
    """

    element, element_coordination, element_charge = unpack_target(elem_prop)
    charge, coordination, target_property, target_percentage = unpack_conditions(conditions, condition_value)
    print("Conditions")
    print("----------------------------------------------------------------")
    print("charge:", charge)
    print("coordination:", coordination)
    print("target_property:", target_property)
    print("target_percentage:", target_percentage)
    print("----------------------------------------------------------------")
  
    elem_db = read_csv()
    target_element = elem_db[(elem_db['Ion'] == element) & (elem_db['Charge'] == element_charge) 
                             &  (elem_db['Coordination'] == element_coordination)]
    print("----------------------------------------------------------------")
    print("Properties of the Target element")
    print("----------------------------------------------------------------")
    print(target_element[['Ion', 'Coordination', 'Charge', 'Ionic Radius']])
    print("----------------------------------------------------------------")

    if "Hume-Rothery" in conditions:
        target_value = target_element[target_property].values[0]
        print(f"{target_property} of {element}: {target_value}")
        target_lb, target_ub = hume_rothery_rule(target_percentage, target_value)
    else:
        target_lb = None
        target_ub = None

    elem_sub = find_substitutes(element, conditions, elem_db, charge, coordination, target_property, target_lb, target_ub)
    elem_sub = elem_sub.drop_duplicates(subset=['Ion'])
    novel_mat = []
    novel_mat.extend([f"Cs{substitute}I3" for substitute in elem_sub['Ion']])
    # Combine elem_sub and novel_mat into a new DataFrame
    elem_sub.loc[:, 'Novel Material'] = novel_mat

    #find the matches with ICSD
    nov_mat_db, true_positive = utils.icsd_finder(icsd_true, elem_sub)
    nov_mat_db = nov_mat_db[['Ion', 'Coordination', 'Charge', 'Ionic Radius', 'Novel Material', 'icsd_ids']].reset_index(drop=True)
    nov_mat_db = nov_mat_db.rename(columns={'Ion': 'Substituted Element'})
    
    #calculate the true positive and false positive and the synthetic p_value
    p_syn = utils.p_syn(nov_mat_db, true_positive)
    details = {
        'True Positive': true_positive,
        'Synthetic P-Value': p_syn,
        'Conditions': conditions,
        'Condition Value': condition_value
    }
    nov_mat_db = utils.add_details_to_csv(nov_mat_db, details)
    
    # Save the DataFrame to a CSV file
    utils.save('isovalenet_generator', nov_mat_db, df_name="novel_materials")

    return nov_mat_db, true_positive, p_syn



if __name__ == "__main__":
    h5_filename = 'all_materials_9June2022.h5'  # Replace with the actual HDF5 file name
    h5_file_path = os.path.join('Materials', h5_filename)

    # Read the HDF5 file
    mat_db = pd.read_hdf(h5_file_path)

    # Find the materials with ICSD ID
    icsd_true = mat_db[mat_db['icsd_ids'].apply(lambda x: len(x) != 0)]
    elem_prob = {'element': 'Pb', 'coordination': 'VIII', 'charge': 2}
    conditions = ['charge', 'coordination','Hume-Rothery']
    condition_value = {'charge': 2, 'coordination': 'VIII', 'target_property': 'Ionic Radius', 'target_percentage': 15}
    main(icsd_true = icsd_true , comp="CsPbI3", elem_prop = elem_prob, conditions=conditions, condition_value=condition_value)