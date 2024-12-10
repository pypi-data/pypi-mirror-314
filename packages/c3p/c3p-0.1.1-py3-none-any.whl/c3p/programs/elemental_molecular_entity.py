"""
Classifies: CHEBI:33259 elemental molecular entity
"""
from rdkit import Chem

def is_elemental_molecular_entity(smiles: str):
    """
    Determines if a molecule is an elemental molecular entity (all atoms have the same atomic number).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an elemental molecular entity, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Get the list of atomic numbers present in the molecule
    atomic_nums = set(atom.GetAtomicNum() for atom in mol.GetAtoms())

    # Check if there is only one unique atomic number
    if len(atomic_nums) == 1:
        return True, f"All atoms have the same atomic number: {list(atomic_nums)[0]}"
    else:
        return False, "Molecule contains atoms with different atomic numbers"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33259',
                          'name': 'elemental molecular entity',
                          'definition': 'A molecular entity all atoms of which '
                                        'have the same atomic number.',
                          'parents': ['CHEBI:23367']},
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
    'num_true_positives': 24,
    'num_false_positives': 100,
    'num_true_negatives': 10826,
    'num_false_negatives': 4,
    'num_negatives': None,
    'precision': 0.1935483870967742,
    'recall': 0.8571428571428571,
    'f1': 0.3157894736842105,
    'accuracy': 0.9905057513237173}