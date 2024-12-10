"""
Classifies: CHEBI:32952 amine
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_amine(smiles: str):
    """
    Determines if a molecule is an amine, defined as a compound formally derived from ammonia
    by replacing one, two, or three hydrogen atoms by hydrocarbyl groups.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an amine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find all nitrogen atoms
    nitrogen_atoms = [atom for atom in mol.GetAtoms() if atom.GetAtomicNum() == 7]

    # Check if any nitrogen atoms have at least one hydrogen atom attached
    for n_atom in nitrogen_atoms:
        has_hydrogen = False
        for neighbor in n_atom.GetNeighbors():
            if neighbor.GetAtomicNum() == 1:
                has_hydrogen = True
                break
        if has_hydrogen:
            # Check if the nitrogen atom has 1, 2, or 3 carbon substituents
            carbon_substituents = 0
            for neighbor in n_atom.GetNeighbors():
                if neighbor.GetAtomicNum() == 6:
                    carbon_substituents += 1
            if carbon_substituents in [1, 2, 3]:
                return True, "Molecule contains an amine group"

    return False, "Molecule does not contain an amine group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:32952',
                          'name': 'amine',
                          'definition': 'A compound formally derived from '
                                        'ammonia by replacing one, two or '
                                        'three hydrogen atoms by hydrocarbyl '
                                        'groups.',
                          'parents': ['CHEBI:50047']},
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
    'num_false_positives': 6,
    'num_true_negatives': 183063,
    'num_false_negatives': 86,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9994976932106686}