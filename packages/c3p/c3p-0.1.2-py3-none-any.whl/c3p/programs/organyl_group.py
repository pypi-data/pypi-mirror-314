"""
Classifies: CHEBI:33249 organyl group
"""
from rdkit import Chem
from rdkit.Chem import Descriptors

def is_organyl_group(smiles: str):
    """
    Determines if a given SMILES string represents an organyl group.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is an organyl group, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for presence of a free valence at a carbon atom
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C' and atom.GetTotalNumHs() < atom.GetTotalValence():
            # Found a carbon atom with a free valence
            break
    else:
        return False, "No free valence found at a carbon atom"

    # Check if the molecule is organic
    if not all(atom.GetSymbol() in ['C', 'H', 'O', 'N', 'S', 'P', 'F', 'Cl', 'Br', 'I'] for atom in mol.GetAtoms()):
        return False, "Molecule contains inorganic atoms"

    return True, "Organyl group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33249',
                          'name': 'organyl group',
                          'definition': 'Any organic substituent group, '
                                        'regardless of functional type, having '
                                        'one free valence at a carbon atom.',
                          'parents': ['CHEBI:51447']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: 'FragmentMatcher' object has no attribute "
               "'AddFragmentSmarts'",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 100,
    'num_true_negatives': 5,
    'num_false_negatives': 20,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 0.047619047619047616,
    'f1': 0.01639344262295082,
    'accuracy': 0.047619047619047616}