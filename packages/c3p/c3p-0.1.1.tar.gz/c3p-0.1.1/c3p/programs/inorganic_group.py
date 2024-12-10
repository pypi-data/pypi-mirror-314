"""
Classifies: CHEBI:33246 inorganic group
"""
from rdkit import Chem

def is_inorganic_group(smiles: str):
    """
    Determines if a molecule is an inorganic group (any substituent group which does not contain carbon).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is an inorganic group, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains carbon atoms
    has_carbon = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C':
            has_carbon = True
            break

    if has_carbon:
        return False, "Molecule contains carbon atoms"

    # Check if the molecule is a valid group
    if not mol.GetNumAtoms() > 1:
        return False, "Molecule is not a valid group"

    # Check if at least one atom is marked as an attachment point
    has_attachment_point = False
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() == 0:
            has_attachment_point = True
            break

    if not has_attachment_point:
        return False, "Molecule does not have an attachment point"

    return True, "Inorganic group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33246',
                          'name': 'inorganic group',
                          'definition': 'Any substituent group which does not '
                                        'contain carbon.',
                          'parents': ['CHEBI:24433']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: type object 'Mol' has no attribute "
               "'HasSubstructMatchError'",
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 6,
    'num_false_positives': 100,
    'num_true_negatives': 110242,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.05660377358490566,
    'recall': 1.0,
    'f1': 0.10714285714285715,
    'accuracy': 0.9990937760539385}