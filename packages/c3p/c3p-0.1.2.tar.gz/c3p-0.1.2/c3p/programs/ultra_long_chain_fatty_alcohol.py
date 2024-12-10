"""
Classifies: CHEBI:197505 ultra-long-chain fatty alcohol
"""
from rdkit import Chem
from rdkit.Chem import Descriptors

def is_ultra_long_chain_fatty_alcohol(smiles: str):
    """
    Determines if a molecule is an ultra-long-chain fatty alcohol (chain length > C27).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an ultra-long-chain fatty alcohol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains an alcohol group (-OH)
    alcohol_pattern = Chem.MolFromSmarts('O')
    if not mol.HasSubstructMatch(alcohol_pattern):
        return False, "Molecule does not contain an alcohol group (-OH)"

    # Calculate the length of the longest carbon chain
    longest_chain = Descriptors.Lipinski.LongestChain(mol)
    chain_length = len(longest_chain)

    if chain_length > 27:
        return True, f"Ultra-long-chain fatty alcohol with chain length C{chain_length}"
    else:
        return False, f"Fatty alcohol with chain length C{chain_length}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:197505',
                          'name': 'ultra-long-chain fatty alcohol',
                          'definition': 'Any fatty alcohol which has a chain '
                                        'length greater than C27.',
                          'parents': ['CHEBI:24026']},
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
    'error': "module 'rdkit.Chem.Descriptors' has no attribute 'Lipinski'",
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