"""
Classifies: CHEBI:33573 tetrol
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_tetrol(smiles: str):
    """
    Determines if a molecule is a tetrol (a polyol containing 4 hydroxy groups).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a tetrol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Count the number of hydroxy groups
    num_hydroxy = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O' and atom.GetTotalNumHs() == 1)

    if num_hydroxy == 4:
        return True, "Molecule contains 4 hydroxy groups"
    else:
        return False, f"Molecule contains {num_hydroxy} hydroxy groups (not 4)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33573',
                          'name': 'tetrol',
                          'definition': 'A polyol that contains 4 hydroxy '
                                        'groups.',
                          'parents': ['CHEBI:26191']},
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
    'num_true_positives': 8,
    'num_false_positives': 100,
    'num_true_negatives': 1799,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.07407407407407407,
    'recall': 0.8,
    'f1': 0.13559322033898305,
    'accuracy': 0.9465688842325825}