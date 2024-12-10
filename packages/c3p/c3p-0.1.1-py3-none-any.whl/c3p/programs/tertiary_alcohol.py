"""
Classifies: CHEBI:26878 tertiary alcohol
"""
from rdkit import Chem
from rdkit.Chem import rdchem

def is_tertiary_alcohol(smiles: str):
    """
    Determines if a molecule contains a tertiary alcohol group.

    A tertiary alcohol is a compound in which a hydroxy group, -OH, is attached
    to a saturated carbon atom which has three other carbon atoms attached to it.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule contains a tertiary alcohol group, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    atoms = mol.GetAtoms()
    for atom in atoms:
        if atom.GetSymbol() == "O" and atom.GetHybridization() == rdchem.HybridizationType.SP3:
            neighbors = atom.GetNeighbors()
            if len(neighbors) == 1:
                carbon = neighbors[0]
                if carbon.GetSymbol() == "C" and carbon.GetHybridization() == rdchem.HybridizationType.SP3:
                    carbon_neighbors = carbon.GetNeighbors()
                    carbon_neighbors_symbols = [n.GetSymbol() for n in carbon_neighbors]
                    if "C" in carbon_neighbors_symbols and carbon_neighbors_symbols.count("C") == 3:
                        return True, "The molecule contains a tertiary alcohol group"

    return False, "The molecule does not contain a tertiary alcohol group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26878',
                          'name': 'tertiary alcohol',
                          'definition': 'A tertiary alcohol is a compound in '
                                        'which a hydroxy group, -OH, is '
                                        'attached to a saturated carbon atom '
                                        'which has three other carbon atoms '
                                        'attached to it.',
                          'parents': ['CHEBI:30879']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': None,
    'attempt': 0,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 106,
    'num_false_positives': 100,
    'num_true_negatives': 1580,
    'num_false_negatives': 3,
    'num_negatives': None,
    'precision': 0.5145631067961165,
    'recall': 0.9724770642201835,
    'f1': 0.673015873015873,
    'accuracy': 0.9424259362772499}