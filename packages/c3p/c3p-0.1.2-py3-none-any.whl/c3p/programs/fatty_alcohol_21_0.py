"""
Classifies: CHEBI:197491 fatty alcohol 21:0
"""
from rdkit import Chem

def is_fatty_alcohol_21_0(smiles: str):
    """
    Determines if a molecule is a fatty alcohol with 21 carbon atoms.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a fatty alcohol 21:0, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Count the number of carbon atoms
    num_carbons = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')

    # Check if there is exactly one oxygen atom
    num_oxygens = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O')
    if num_oxygens != 1:
        return False, "Molecule does not contain exactly one oxygen atom"

    # Check if the molecule is aliphatic (no rings)
    if not mol.GetRingInfo().IsAtomInRingOfSize(0, 3) and \
       not mol.GetRingInfo().IsAtomInRingOfSize(0, 4) and \
       not mol.GetRingInfo().IsAtomInRingOfSize(0, 5) and \
       not mol.GetRingInfo().IsAtomInRingOfSize(0, 6) and \
       not mol.GetRingInfo().IsAtomInRingOfSize(0, 7):
        if num_carbons == 21:
            return True, "Molecule is a fatty alcohol 21:0"
        else:
            return False, f"Molecule has {num_carbons} carbon atoms (should be 21)"
    else:
        return False, "Molecule contains a ring"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:197491',
                          'name': 'fatty alcohol 21:0',
                          'definition': 'Any fatty alcohol containing 21 '
                                        'carbons.',
                          'parents': ['CHEBI:17135']},
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
    'num_true_negatives': 60787,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 1.0,
    'f1': 0.0196078431372549,
    'accuracy': 0.998357640257522}