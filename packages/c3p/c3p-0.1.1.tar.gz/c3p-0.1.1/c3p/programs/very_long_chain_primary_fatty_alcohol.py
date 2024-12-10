"""
Classifies: CHEBI:138741 very long-chain primary fatty alcohol
"""
from rdkit import Chem
from rdkit.Chem import Descriptors

def is_very_long_chain_primary_fatty_alcohol(smiles: str):
    """
    Determines if a molecule is a very long-chain primary fatty alcohol (C23-C27).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a very long-chain primary fatty alcohol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains an -OH group
    if not any(atom.GetSymbol() == 'O' and sum(atom.GetNeighbors()) == 1 for atom in mol.GetAtoms()):
        return False, "Molecule does not contain a primary alcohol group"

    # Get the number of carbon atoms in the longest chain
    chain_length = Descriptors.GetLongestChain(mol)

    if chain_length < 23 or chain_length > 27:
        return False, f"Chain length is {chain_length}, not between C23 and C27"

    return True, f"Very long-chain primary fatty alcohol with {chain_length} carbon atoms"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:138741',
                          'name': 'very long-chain primary fatty alcohol',
                          'definition': 'Any primary fatty alcohol with a '
                                        'chain length between C23 and C27.',
                          'parents': ['CHEBI:142622']},
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
    'success': False,
    'best': True,
    'error': "unsupported operand type(s) for +: 'int' and 'Atom'",
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': None}