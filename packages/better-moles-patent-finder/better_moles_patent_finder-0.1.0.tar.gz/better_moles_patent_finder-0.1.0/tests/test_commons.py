import pandas as pd
import pytest

from utils.common_types import SmilesQuery
from utils.common_utils import cast_smiles_for_query, add_patents_to_df, save_df_to_csv


@pytest.mark.parametrize(
    "input_smiles, expected_smiles, expected_inchikey",
    [
        ("CCO", "CCO", "LFQSCWFLJHTTHZ-UHFFFAOYSA-N"),  # Ethanol
        ("C1CCCCC1", "C1CCCCC1", "XDTMQSROBMDMFD-UHFFFAOYSA-N"),  # Cyclohexane
        ("c1ccccc1", "c1ccccc1", "UHOVQNZJYSORNB-UHFFFAOYSA-N"),  # Benzene
    ],
)
def test_cast_smiles_for_query_valid(input_smiles, expected_smiles, expected_inchikey):
    result = cast_smiles_for_query(input_smiles)

    assert result.smiles == expected_smiles
    assert result.inchikey == expected_inchikey
    assert isinstance(result, SmilesQuery)


@pytest.mark.parametrize(
    "invalid_smiles",
    [
        "InvalidSMILES",  # Completely invalid string
        "[C@@H",  # Mismatched parentheses
        ""  # Empty string
    ],
)
def test_cast_smiles_for_query_invalid(invalid_smiles):
    with pytest.raises(ValueError, match=f"Error processing SMILES string."):
        cast_smiles_for_query(invalid_smiles)


def test_add_patents_to_df():
    # Input DataFrame
    data = {'smiles': ['CCO', 'C1CCCCC1', 'InvalidSMILES']}
    smiles_df = pd.DataFrame(data)

    # Input patents
    patents = [['patent1', 'patent2'], [], []]

    # Expected output DataFrame
    expected_data = {
        'smiles': ['CCO', 'C1CCCCC1', 'InvalidSMILES'],
        'patent_ids': [['patent1', 'patent2'], [], []]
    }
    expected_df = pd.DataFrame(expected_data)

    # Test add_patents_to_df
    result_df = add_patents_to_df(smiles_df, patents)

    # Assert the DataFrames are equal
    pd.testing.assert_frame_equal(result_df, expected_df)


def test_add_patents_to_df_invalid_length():
    # Input DataFrame
    data = {'smiles': ['CCO', 'C1CCCCC1']}
    smiles_df = pd.DataFrame(data)

    # Input patents (mismatched length)
    patents = [['patent1', 'patent2']]

    # Test for ValueError
    with pytest.raises(ValueError, match="The length of the DataFrame and the patents list must match."):
        add_patents_to_df(smiles_df, patents)


def test_save_df_to_csv(tmp_path):
    # Input DataFrame
    data = {
        'smiles': ['CCO', 'C1CCCCC1', 'InvalidSMILES'],
        'patent_ids': [['patent1', 'patent2'], [], []]
    }
    df = pd.DataFrame(data)

    # File path for temporary CSV file
    file_path = tmp_path / "test_output.csv"

    # Test save_df_to_csv
    save_df_to_csv(df, str(file_path))

    # Read the CSV back into a DataFrame
    result_df = pd.read_csv(file_path)

    # Expected DataFrame
    expected_df = pd.DataFrame({
        'smiles': ['CCO', 'C1CCCCC1', 'InvalidSMILES'],
        'patent_ids': ["['patent1', 'patent2']", '[]', '[]']  # Lists are converted to strings in CSV
    })

    # Assert the DataFrames are equal
    pd.testing.assert_frame_equal(result_df, expected_df)


if __name__ == "__main__":
    pytest.main()
