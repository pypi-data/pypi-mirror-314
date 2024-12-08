from dataclasses import dataclass


@dataclass
class SmilesQuery:
    """
    SmilesQuery: A class for representing a SMILES query.
    Attributes:
        smiles: str
        inchikey: str
    """
    smiles: str
    inchikey: str
