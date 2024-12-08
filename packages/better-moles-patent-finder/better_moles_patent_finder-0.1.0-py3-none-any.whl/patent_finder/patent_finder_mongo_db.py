from concurrent.futures import ThreadPoolExecutor
from pymongo.collection import Collection
import pandas as pd
from mongo.mongo_connector import MongoConnector
from utils.common_types import SmilesQuery
from utils.common_utils import cast_smiles_for_query


class PatentFinderMongoDB:
    def __init__(self, smiles_df: pd.DataFrame, mongo_connector: MongoConnector):
        self.smiles_df = smiles_df
        self.smiles_list = list(smiles_df['smiles'])
        self.patents_ids = [[] for _ in range(len(self.smiles_list))]
        self.mongo_connector = mongo_connector

    @staticmethod
    def get_smiles_patents_ids(query: SmilesQuery, collection: Collection) -> list[str]:
        try:
            # Query the database by SMILES and InChIKey using regex for batch processing
            results = collection.find({
                "$or": [
                    {"molecule.smiles": {"$regex": query.smiles, "$options": "i"}},
                    {"molecule.inchikey": query.inchikey}
                ]
            })

            patent_ids = []
            for result in results:
                patents = result.get('patents', [])
                if isinstance(patents, list):
                    patent_ids.extend(patent.get('id') for patent in patents if 'id' in patent)
                elif isinstance(patents, dict):
                    patent_ids.append(patents.get('id'))
            return patent_ids
        except Exception as e:
            print(f"Error processing query: {query}\n{e}")
            return []

    def find_all_patents(self) -> list[list[str]]:
        """
        Find all patent IDs in parallel for the SMILES strings.
        """
        with ThreadPoolExecutor() as executor:
            # Process all SMILES in parallel
            results = list(executor.map(self._find_patents_for_smiles, self.smiles_list))
        return results

    def _find_patents_for_smiles(self, smiles: str) -> list[str]:
        """
        A helper method to handle the query for a single SMILES string.
        """
        try:
            query = cast_smiles_for_query(smiles)
            return self.get_smiles_patents_ids(query, self.mongo_connector.collection)
        except ValueError:
            print(f"Error processing SMILES: {smiles}")
            return []  # Return empty list for invalid SMILES
