"""
Classifies: CHEBI:33576 sulfur-containing carboxylic acid
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_sulfur_containing_carboxylic_acid(smiles: str):
    """
    Determines if a molecule is a sulfur-containing carboxylic acid.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a sulfur-containing carboxylic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for sulfur atoms
    has_sulfur = any(atom.GetSymbol() == 'S' for atom in mol.GetAtoms())
    if not has_sulfur:
        return False, "No sulfur atom found"

    # Check for carboxylic acid group
    carboxylic_acid_smarts = "[$(C(=O)O)]"
    carboxylic_acid_pattern = Chem.MolFromSmarts(carboxylic_acid_smarts)
    carboxylic_acid_matches = mol.GetSubstructMatches(carboxylic_acid_pattern)

    if carboxylic_acid_matches:
        return True, "Molecule is a sulfur-containing carboxylic acid"
    else:
        return False, "No carboxylic acid group found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33576',
                          'name': 'sulfur-containing carboxylic acid',
                          'definition': 'Any carboxylic acid having a sulfur '
                                        'substituent.',
                          'parents': ['CHEBI:33261', 'CHEBI:33575']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: module 'rdkit.Chem.AllChem' has no attribute "
               "'EnumerateTautomers'",
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 15,
    'num_false_positives': 100,
    'num_true_negatives': 1835,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.13043478260869565,
    'recall': 1.0,
    'f1': 0.23076923076923078,
    'accuracy': 0.9487179487179487}