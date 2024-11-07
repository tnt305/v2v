from typing import List, Dict, Union, Any
import pandas as pd
import os

def save_csv(
    data_path: str,
    new_columns: Dict[str, List[Any]],
    base_columns: List[str] = ['color short', 'color name', 'color code', 'r', 'g', 'b'],
    output_path: str = None):
    """
    Read a CSV file and add new columns with their corresponding values, then save to a new CSV.
    
    Args:
        data_path (str): Path to the input CSV file
        new_columns (Dict[str, List[Any]]): Dictionary of column names and their values
                                          e.g., {'description': descriptions_list, 'main_color': main_colors_list}
        base_columns (List[str]): List of original column names in the CSV
        output_path (str): Path to save the output CSV. If None, will append '_updated' to the input filename
        
    Returns:
        None: Saves the updated DataFrame to a CSV file
    
    """
    # Ensure data_path starts with ./ if not already
    if not data_path.startswith('./') and not data_path.startswith('../'):
        data_path = './' + data_path
        
    # Read the original CSV
    df = pd.read_csv(data_path, names=base_columns)
    
    # Validate input data lengths
    for col_name, col_data in new_columns.items():
        if len(col_data) != len(df):
            raise ValueError(
                f"Length mismatch: Column '{col_name}' has {len(col_data)} items "
                f"but DataFrame has {len(df)} rows"
            )
    
    # Add new columns
    for col_name, col_data in new_columns.items():
        df[col_name] = col_data
        
    # Generate output path if not provided
    if output_path is None:
        raise ValueError("output_path must be provided")
        
    # Save the updated DataFrame
    df.to_csv(output_path, index=False)
    print(f"Updated CSV saved to: {output_path}")


def read_csv(data_path: str, columns: List):
    return pd.read_csv(f"./{data_path}", names  = columns)