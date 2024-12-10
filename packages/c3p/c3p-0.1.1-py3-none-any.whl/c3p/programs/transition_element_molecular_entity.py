"""
Classifies: CHEBI:33497 transition element molecular entity
"""
from rdkit import Chem

# List of atomic numbers for transition elements
transition_elements = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103]

def is_transition_element_molecular_entity(smiles: str):
    """
    Determines if a molecular entity contains one or more atoms of a transition element.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule contains a transition element, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    atoms = mol.GetAtoms()
    for atom in atoms:
        atomic_number = atom.GetAtomicNum()
        if atomic_number in transition_elements:
            element_symbol = atom.GetSymbol()
            return True, f"Molecule contains the transition element {element_symbol} (atomic number {atomic_number})"

    return False, "No transition elements found in the molecule"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33497',
                          'name': 'transition element molecular entity',
                          'definition': 'A molecular entity containing one or '
                                        'more atoms of a transition element.',
                          'parents': ['CHEBI:23367']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': 'Attempt failed: unterminated string literal (detected at line '
               '1) (<string>, line 1)',
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 72,
    'num_false_positives': 100,
    'num_true_negatives': 44649,
    'num_false_negatives': 4,
    'num_negatives': None,
    'precision': 0.4186046511627907,
    'recall': 0.9473684210526315,
    'f1': 0.5806451612903226,
    'accuracy': 0.9976798661461238}