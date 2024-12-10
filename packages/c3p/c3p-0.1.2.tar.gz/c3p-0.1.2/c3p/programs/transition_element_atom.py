"""
Classifies: CHEBI:27081 transition element atom
"""
from rdkit import Chem

# Define the atomic numbers for transition elements
TRANSITION_ELEMENT_ATOMIC_NUMBERS = list(range(21, 31)) + list(range(39, 49)) + list(range(71, 81)) + list(range(103, 113))

def is_transition_element_atom(smiles: str):
    """
    Determines if a molecule is a transition element atom.

    A transition element atom is defined as an element whose atom has an incomplete d sub-shell,
    or which can give rise to cations with an incomplete d sub-shell.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a transition element atom, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule is a single atom
    if mol.GetNumAtoms() != 1:
        return False, "Molecule is not a single atom"

    atom = mol.GetAtomWithIdx(0)

    # Get the atomic number and symbol
    atomic_num = atom.GetAtomicNum()
    symbol = atom.GetSymbol()

    if atomic_num in TRANSITION_ELEMENT_ATOMIC_NUMBERS:
        return True, f"{symbol} is a transition element atom"

    return False, f"{symbol} is not a transition element atom"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:27081',
                          'name': 'transition element atom',
                          'definition': 'An element whose atom has an '
                                        'incomplete d sub-shell, or which can '
                                        'give rise to cations with an '
                                        'incomplete d sub-shell.',
                          'parents': ['CHEBI:33521']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: 'PeriodicGroup'",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 5,
    'num_false_positives': 68,
    'num_true_negatives': 183781,
    'num_false_negatives': 3,
    'num_negatives': None,
    'precision': 0.0684931506849315,
    'recall': 0.625,
    'f1': 0.12345679012345677,
    'accuracy': 0.9996138303137765}