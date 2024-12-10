"""
Classifies: CHEBI:33313 polonium atom
"""
from rdkit import Chem

def is_polonium_atom(smiles: str):
    """
    Determines if a molecule is a polonium atom.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a polonium atom, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if there is only one atom
    if mol.GetNumAtoms() != 1:
        return False, "Not a single atom"

    # Check if the atom is polonium
    atom = mol.GetAtomWithIdx(0)
    atomic_num = atom.GetAtomicNum()
    if atomic_num != 84:
        return False, "Not a polonium atom"

    isotope = atom.GetIsotope()
    if isotope == 0:
        return False, "Not a specific polonium isotope"
    else:
        return True, f"Polonium-{isotope} atom"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33313',
                          'name': 'polonium atom',
                          'definition': 'A radioactive metallic element '
                                        'discovered in 1898 by Marie '
                                        'Sklodowska Curie and named after her '
                                        'home country, Poland (Latin Polonia).',
                          'parents': ['CHEBI:33303', 'CHEBI:33521']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': 'Attempt failed: invalid syntax (<string>, line 1)',
    'attempt': 4,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 2,
    'num_false_positives': 0,
    'num_true_negatives': 183906,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 1.0,
    'recall': 1.0,
    'f1': 1.0,
    'accuracy': 1.0}