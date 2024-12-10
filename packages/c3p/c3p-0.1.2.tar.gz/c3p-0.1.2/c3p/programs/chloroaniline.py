"""
Classifies: CHEBI:23130 chloroaniline
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors

def is_chloroaniline(smiles: str):
    """
    Determines if a molecule is a chloroaniline (a substituted aniline with at least one chloro group).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a chloroaniline, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of an aniline substructure
    aniline_pattern = Chem.MolFromSmarts('c1ccc(N)cc1')
    if not mol.HasSubstructMatch(aniline_pattern):
        return False, "Molecule does not contain an aniline substructure"

    # Check for the presence of at least one chloro group
    has_chlorine = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'Cl':
            has_chlorine = True
            break

    if not has_chlorine:
        return False, "Molecule does not contain a chloro group"

    return True, "Molecule is a chloroaniline"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23130',
                          'name': 'chloroaniline',
                          'definition': 'Any  substituted aniline carrying at '
                                        'least one chloro group.',
                          'parents': ['CHEBI:23132', 'CHEBI:48975']},
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
    'num_true_positives': 1,
    'num_false_positives': 100,
    'num_true_negatives': 6614,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 1.0,
    'f1': 0.0196078431372549,
    'accuracy': 0.9851079672375279}