from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
from pymongo.synchronous.collection import Collection

from utils.common_types import SmilesQuery
from mongo.mongo_connector import MongoConnector
from patent_finder.patent_finder_mongo_db import PatentFinderMongoDB


# Mock the `cast_smiles_for_query` function
@pytest.fixture
def mock_cast_smiles_for_query():
    with patch("utils.common_utils.cast_smiles_for_query") as mock:
        yield mock


# Mock MongoConnector
@pytest.fixture
def mock_mongo_connector():
    mock_connector = MagicMock(spec=MongoConnector)
    mock_connector.collection = MagicMock(spec=Collection)
    return mock_connector


@pytest.fixture
def smiles_dataframe():
    # Sample DataFrame
    return pd.DataFrame({
        'smiles': ['CCO', 'C1CCCCC1']
    })


@pytest.mark.parametrize(
    "mocked_results, expected_patent_ids",
    [
        (
                [
                    {"molecule": {"smiles": "CCO", "inchikey": "LFQSCWFLJHTTHZ-UHFFFAOYSA-N"},
                     "patents": [{"id": "patent1"}, {"id": "patent2"}]},
                    {"molecule": {"smiles": "CCO", "inchikey": "LFQSCWFLJHTTHZ-UHFFFAOYSA-N"},
                     "patents": {"id": "patent3"}}
                ],
                ["patent1", "patent2", "patent3"]
        ),
        (
                [
                    {"molecule": {"smiles": "C1CCCCC1", "inchikey": "XDTMQSROBMDMFD-UHFFFAOYSA-N"},
                     "patents": []}
                ],
                []
        ),
        (
                [],
                []
        )
    ],
)
def test_get_smiles_patents_ids(mock_mongo_connector, mock_cast_smiles_for_query, mocked_results, expected_patent_ids):
    # Mock the MongoDB collection behavior
    mock_mongo_connector.collection.find.return_value = mocked_results

    # Mock cast_smiles_for_query
    mock_cast_smiles_for_query.return_value = SmilesQuery(smiles="CCO", inchikey="LFQSCWFLJHTTHZ-UHFFFAOYSA-N")

    # Instantiate the class
    patent_finder = PatentFinderMongoDB(pd.DataFrame({'smiles': ["CCO"]}), mock_mongo_connector)

    # Test `get_smiles_patents_ids`
    query = SmilesQuery(smiles="CCO", inchikey="LFQSCWFLJHTTHZ-UHFFFAOYSA-N")
    results = patent_finder.get_smiles_patents_ids(query, mock_mongo_connector.collection)

    assert results == expected_patent_ids


def test_find_all_patents_with_invalid_smiles(smiles_dataframe, mock_mongo_connector):
    # Mock MongoDB responses
    mock_mongo_connector.collection.find.side_effect = [
        [
            {"molecule": {"smiles": "CCO", "inchikey": "LFQSCWFLJHTTHZ-UHFFFAOYSA-N"},
             "patents": [{"id": "patent1"}, {"id": "patent2"}]},
        ],
        [
            {"molecule": {"smiles": "C1CCCCC1", "inchikey": "XDTMQSROBMDMFD-UHFFFAOYSA-N"},
             "patents": []},
        ],
    ]

    # Instantiate the class
    patent_finder = PatentFinderMongoDB(smiles_dataframe, mock_mongo_connector)

    # Test `find_all_patents`
    results = patent_finder.find_all_patents()

    # Expected results
    expected_results = [
        ["patent1", "patent2"],  # For "CCO"
        [],  # For "C1CCCCC1"
    ]

    assert results == expected_results


if __name__ == '__main__':
    pytest.main()
