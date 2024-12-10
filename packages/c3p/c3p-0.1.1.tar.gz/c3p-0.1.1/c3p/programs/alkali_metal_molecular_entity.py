"""
Classifies: CHEBI:33296 alkali metal molecular entity
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_alkali_metal_molecular_entity(smiles: str):
    """
    Determines if a molecule is an alkali metal molecular entity.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an alkali metal molecular entity, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    alkali_metals = ['Li', 'Na', 'K', 'Rb', 'Cs', 'Fr']
    alkali_metal_atoms = [atom for atom in mol.GetAtoms() if atom.GetSymbol() in alkali_metals]

    if not alkali_metal_atoms:
        return False, "No alkali metal atoms found"

    alkali_metal_symbols = [atom.GetSymbol() for atom in alkali_metal_atoms]
    alkali_metal_symbols_str = ', '.join(set(alkali_metal_symbols))

    return True, f"Molecule contains alkali metal atoms: {alkali_metal_symbols_str}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33296',
                          'name': 'alkali metal molecular entity',
                          'definition': 'A molecular entity containing one or '
                                        'more atoms of an alkali metal.',
                          'parents': ['CHEBI:33674']},
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
    'num_true_positives': 52,
    'num_false_positives': 100,
    'num_true_negatives': 47654,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.34210526315789475,
    'recall': 0.9811320754716981,
    'f1': 0.5073170731707317,
    'accuracy': 0.9978873386742527}