"""
Classifies: CHEBI:32863 secondary amine
"""
from rdkit import Chem
from rdkit.Chem import Descriptors

def is_secondary_amine(smiles: str):
    """
    Determines if a molecule is a secondary amine.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a secondary amine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Get the number of nitrogen atoms
    num_n_atoms = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 7)

    # Check if there is exactly one nitrogen atom
    if num_n_atoms != 1:
        return False, "Molecule does not contain exactly one nitrogen atom"

    # Get the nitrogen atom
    n_atom = next(atom for atom in mol.GetAtoms() if atom.GetAtomicNum() == 7)

    # Count the number of hydrogen atoms bonded to the nitrogen
    num_h_bonds = sum(1 for neighbor in n_atom.GetNeighbors() if neighbor.GetAtomicNum() == 1)

    # Check if the nitrogen atom has exactly one hydrogen bond
    if num_h_bonds != 1:
        return False, "Nitrogen atom does not have exactly one hydrogen bond"

    # Check if the nitrogen atom has exactly two non-hydrogen neighbors
    non_h_neighbors = [neighbor for neighbor in n_atom.GetNeighbors() if neighbor.GetAtomicNum() != 1]
    if len(non_h_neighbors) != 2:
        return False, "Nitrogen atom does not have exactly two non-hydrogen neighbors"

    return True, "Molecule is a secondary amine"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:32863',
                          'name': 'secondary amine',
                          'definition': 'A compound formally derived from '
                                        'ammonia by replacing two hydrogen '
                                        'atoms by hydrocarbyl groups.',
                          'parents': ['CHEBI:32952', 'CHEBI:50995']},
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
    'num_true_negatives': 183883,
    'num_false_negatives': 5,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999728095362395}