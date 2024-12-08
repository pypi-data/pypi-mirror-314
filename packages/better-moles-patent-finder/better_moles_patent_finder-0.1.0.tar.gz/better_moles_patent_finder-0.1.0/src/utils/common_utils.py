import pandas as pd
from rdkit import Chem
from rdkit import RDLogger

from utils.common_types import SmilesQuery

RDLogger.DisableLog('rdApp.*')


def cast_smiles_for_query(smiles: str) -> SmilesQuery:
    """
    Casts a SMILES string to its canonical form and generates an InChIKey.

    Args:
        smiles (str): The SMILES string to canonicalize.

    Returns:
        SmilesQuery: A dataclass containing the canonical SMILES and the InChIKey.

    Raises:
        ValueError: If the SMILES string is invalid or cannot be processed.
    """
    if smiles == "":
        raise ValueError(f"Error processing SMILES string.")
    try:
        # Canonicalize SMILES
        molecule = Chem.MolFromSmiles(smiles)
        if molecule is None:
            raise ValueError(f"Invalid SMILES string: {smiles}")

        query_smiles = Chem.MolToSmiles(molecule)
        query_mol = Chem.MolFromSmiles(query_smiles)
        query_inchikey = Chem.MolToInchiKey(query_mol)

        return SmilesQuery(smiles=query_smiles, inchikey=query_inchikey)
    except Exception as e:
        raise ValueError(f"Error processing SMILES string.")


def load_data_from_csv(file_path: str) -> list:
    assert file_path is not None, "File path cannot be None"
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        raise e
    return df


def add_patents_to_df(df: pd.DataFrame, patents: list[list[str]]) -> pd.DataFrame:
    """
    Adds a column containing lists of patent IDs to a DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame, expected to contain the original data (e.g., SMILES strings).
        patents (list[list[str]]): A list of lists, where each sublist contains patent IDs corresponding to the rows in the DataFrame.

    Returns:
        pd.DataFrame: A new DataFrame with an additional column named 'patent_ids' containing the patent IDs.
    """
    if len(df) != len(patents):
        raise ValueError("The length of the DataFrame and the patents list must match.")

    # Add the patent IDs as a new column
    df_with_patents = df.copy()
    df_with_patents['patent_ids'] = patents
    return df_with_patents


def save_df_to_csv(df: pd.DataFrame, file_path: str) -> None:
    """
    Saves a DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        file_path (str): The file path where the CSV will be saved.

    Returns:
        None
    """
    try:
        df.to_csv(file_path, index=False)
        print(f"DataFrame successfully saved to {file_path}")
    except Exception as e:
        raise IOError(f"An error occurred while saving the DataFrame to {file_path}: {e}")
