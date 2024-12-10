"""
Classifies: CHEBI:27093 tricarboxylic acid
"""
from rdkit import Chem
from rdkit.Chem import Descriptors

def is_tricarboxylic_acid(smiles: str):
    """
    Determines if a molecule is a tricarboxylic acid.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a tricarboxylic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of three carboxylic acid groups
    carboxylic_acid_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O' and
                                 sum(1 for neighbor in atom.GetNeighbors() if neighbor.GetSymbol() == 'C' and
                                     len([n for n in neighbor.GetNeighbors() if n.GetSymbol() == 'O' and n.GetFormalCharge() == -1]) == 1) == 2)
    if carboxylic_acid_count != 3:
        return False, "Does not contain three carboxylic acid groups"

    # Check for the presence of a carbonyl group
    carbonyl_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O' and
                          sum(1 for neighbor in atom.GetNeighbors() if neighbor.GetSymbol() == 'C' and
                              len([n for n in neighbor.GetNeighbors() if n.GetSymbol() == 'O' and n.GetFormalCharge() == 0]) == 1) == 1)
    if carbonyl_count == 0:
        return True, "Tricarboxylic acid"
    else:
        return True, "Tricarboxylic acid with a carbonyl group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:27093',
                          'name': 'tricarboxylic acid',
                          'definition': 'An oxoacid containing three carboxy '
                                        'groups.',
                          'parents': ['CHEBI:33575']},
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
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 183813,
    'num_false_negatives': 12,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999347205222359}