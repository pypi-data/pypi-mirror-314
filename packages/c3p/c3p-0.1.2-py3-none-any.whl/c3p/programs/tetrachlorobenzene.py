"""
Classifies: CHEBI:26888 tetrachlorobenzene
"""
from rdkit import Chem

def is_tetrachlorobenzene(smiles: str):
    """
    Determines if a molecule is a tetrachlorobenzene (any chlorobenzene carrying four chloro groups).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a tetrachlorobenzene, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Count the number of chlorine atoms
    num_cl = sum(atom.GetSymbol() == 'Cl' for atom in mol.GetAtoms())

    # Check for exactly four chlorine atoms
    if num_cl != 4:
        return False, "The molecule does not contain exactly four chlorine atoms"

    # Check for at least one aromatic ring
    if mol.GetRingInfo().NumAromaticRings() < 1:
        return False, "The molecule does not contain an aromatic ring"

    # Check if all non-chlorine atoms are carbon or hydrogen
    for atom in mol.GetAtoms():
        symbol = atom.GetSymbol()
        if symbol != 'C' and symbol != 'H' and symbol != 'Cl':
            return False, "The molecule contains atoms other than carbon, hydrogen, and chlorine"

    return True, "The molecule is a tetrachlorobenzene"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26888',
                          'name': 'tetrachlorobenzene',
                          'definition': 'Any member of the class of '
                                        'chlorobenzenes carrying four chloro '
                                        'groups at unspecified positions.',
                          'parents': ['CHEBI:23132']},
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
    'success': False,
    'best': True,
    'error': "'RingInfo' object has no attribute 'NumAromaticRings'",
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': None}