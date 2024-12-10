"""
Classifies: CHEBI:32876 tertiary amine
"""
from rdkit import Chem
from rdkit.Chem import Descriptors

def is_tertiary_amine(smiles: str):
    """
    Determines if a molecule is a tertiary amine.

    A tertiary amine is a compound formally derived from ammonia by replacing three
    hydrogen atoms by hydrocarbyl groups.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a tertiary amine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Get the number of nitrogen atoms in the molecule
    num_nitrogen = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 7)

    # Find the nitrogen atoms
    nitrogen_atoms = [atom for atom in mol.GetAtoms() if atom.GetAtomicNum() == 7]

    # Check if any nitrogen atom is tertiary
    for nitrogen in nitrogen_atoms:
        if nitrogen.GetTotalDegree() == 4:
            # Check if the nitrogen has three carbon neighbors
            carbon_neighbors = sum(1 for neighbor in nitrogen.GetNeighbors() if neighbor.GetAtomicNum() == 6)
            if carbon_neighbors == 3:
                return True, "Molecule contains a tertiary amine group"

    return False, "Molecule does not contain a tertiary amine group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:32876',
                          'name': 'tertiary amine',
                          'definition': 'A compound formally derived from '
                                        'ammonia by replacing three hydrogen '
                                        'atoms by hydrocarbyl groups.',
                          'parents': ['CHEBI:32952', 'CHEBI:50996']},
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
    'num_false_positives': 100,
    'num_true_negatives': 30527,
    'num_false_negatives': 10,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9964095701276234}