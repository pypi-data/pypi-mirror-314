"""
Classifies: CHEBI:33677 f-block molecular entity
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_f_block_molecular_entity(smiles: str):
    """
    Determines if a molecule is an f-block molecular entity, containing one or more atoms of an f-block element.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an f-block molecular entity, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Get the atomic numbers of all atoms in the molecule
    atomic_numbers = [atom.GetAtomicNum() for atom in mol.GetAtoms()]

    # Check if any atom is an f-block element (atomic number between 58 and 71 or between 90 and 103)
    has_f_block_element = any(58 <= atomic_num <= 71 or 90 <= atomic_num <= 103 for atomic_num in atomic_numbers)

    if has_f_block_element:
        f_block_elements = [AllChem.GetAtomicSymbol(atomic_num) for atomic_num in atomic_numbers if
                            58 <= atomic_num <= 71 or 90 <= atomic_num <= 103]
        return True, f"Molecule contains the following f-block elements: {', '.join(f_block_elements)}"
    else:
        return False, "Molecule does not contain any f-block elements"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33677',
                          'name': 'f-block molecular entity',
                          'definition': 'A molecular entity containing one or '
                                        'more atoms of an f-block element.',
                          'parents': ['CHEBI:33497']},
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
    'success': False,
    'best': True,
    'error': "module 'rdkit.Chem.AllChem' has no attribute 'GetAtomicSymbol'",
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0,
    'f1': 0,
    'accuracy': None}