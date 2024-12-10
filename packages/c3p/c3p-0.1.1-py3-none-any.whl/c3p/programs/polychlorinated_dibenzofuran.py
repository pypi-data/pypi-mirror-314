"""
Classifies: CHEBI:134046 polychlorinated dibenzofuran
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_polychlorinated_dibenzofuran(smiles: str):
    """
    Determines if a molecule is a polychlorinated dibenzofuran (a member of the class of benzofurans that is benzofuran in which two or more of the hydrogens have been replaced by chlorines).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a polychlorinated dibenzofuran, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains a benzofuran substructure
    benzofuran_pattern = Chem.MolFromSmarts('c1coc2ccccc12')
    if not mol.HasSubstructMatch(benzofuran_pattern):
        return False, "Molecule does not contain a benzofuran substructure"

    # Count the number of chlorine atoms
    num_chlorines = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'Cl')

    if num_chlorines < 2:
        return False, "Molecule does not have at least two chlorine atoms"

    return True, f"Polychlorinated dibenzofuran with {num_chlorines} chlorine atoms"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:134046',
                          'name': 'polychlorinated dibenzofuran',
                          'definition': 'A member of the class of benzofurans '
                                        'that is benzofuran in which two or '
                                        'more of the hydrogens have reen '
                                        'replaced by chlorines.',
                          'parents': [   'CHEBI:134045',
                                         'CHEBI:36683',
                                         'CHEBI:38922']},
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
    'num_false_positives': 14,
    'num_true_negatives': 183911,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.06666666666666667,
    'recall': 1.0,
    'f1': 0.125,
    'accuracy': 0.9999238824309776}