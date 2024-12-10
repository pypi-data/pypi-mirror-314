"""
Classifies: CHEBI:33247 organic group
"""
from rdkit import Chem

def is_organic_group(smiles: str):
    """
    Determines if a molecule is an organic group.
    Organic group is defined as 'Any substituent group or skeleton containing carbon.'

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an organic group, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains carbon
    has_carbon = any(atom.GetSymbol() == 'C' for atom in mol.GetAtoms())

    if has_carbon:
        return True, "Molecule contains carbon"
    else:
        return False, "Molecule does not contain carbon"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33247',
                          'name': 'organic group',
                          'definition': 'Any substituent group or skeleton '
                                        'containing carbon.',
                          'parents': ['CHEBI:24433']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.0,
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
    'num_true_positives': 166,
    'num_false_positives': 100,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.6240601503759399,
    'recall': 1.0,
    'f1': 0.7685185185185186,
    'accuracy': 0.6240601503759399}