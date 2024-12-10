"""
Classifies: CHEBI:197528 fatty alcohol 23:0
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors

def is_fatty_alcohol_23_0(smiles: str):
    """
    Determines if a molecule is a fatty alcohol 23:0 (contains 23 carbon atoms and one hydroxyl group).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a fatty alcohol 23:0, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule has exactly 23 carbon atoms
    num_carbon_atoms = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if num_carbon_atoms != 23:
        return False, f"Molecule does not contain exactly 23 carbon atoms (found {num_carbon_atoms})"

    # Check if the molecule has exactly one hydroxyl group
    num_hydroxyl_groups = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O' and
                               atom.GetTotalNumHs() == 1)
    if num_hydroxyl_groups != 1:
        return False, f"Molecule does not contain exactly one hydroxyl group (found {num_hydroxyl_groups})"

    return True, "Molecule is a fatty alcohol 23:0"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:197528',
                          'name': 'fatty alcohol 23:0',
                          'definition': 'Any fatty alcohol containing 23 '
                                        'carbons.',
                          'parents': ['CHEBI:197504']},
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
    'num_true_positives': 1,
    'num_false_positives': 100,
    'num_true_negatives': 7680,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 1.0,
    'f1': 0.0196078431372549,
    'accuracy': 0.9871481814676777}