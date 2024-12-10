"""
Classifies: CHEBI:28966 chlorophyll
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_chlorophyll(smiles: str):
    """
    Determines if a molecule is a chlorophyll based on the presence of a fifth ring
    beyond the four pyrrole-like rings, and the presence of a magnesium atom.
    The function also checks for the presence of a long phytol chain.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a chlorophyll, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Count the number of rings
    ring_info = mol.GetRingInfo()
    num_rings = len(ring_info.AtomRings())

    if num_rings < 5:
        return False, "Less than 5 rings found"

    # Check for the presence of a magnesium atom
    has_mg = any(atom.GetSymbol() == 'Mg' for atom in mol.GetAtoms())
    if not has_mg:
        return False, "No magnesium atom found"

    # Check for the presence of a phytol chain
    phytol_pattern = Chem.MolFromSmarts('C=CC(C)(CCC=C(C)C)')
    has_phytol = mol.HasSubstructMatch(phytol_pattern)

    if has_phytol:
        return True, "Chlorophyll with phytol chain"
    else:
        return True, "Chlorophyll without phytol chain"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:28966',
                          'name': 'chlorophyll',
                          'definition': 'A family of magnesium porphyrins, '
                                        'defined by the presence of a fifth '
                                        'ring beyond the four pyrrole-like '
                                        'rings. The rings can have various '
                                        'side chains which usually include a '
                                        'long phytol chain.',
                          'parents': ['CHEBI:25111']},
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
    'num_true_positives': 4,
    'num_false_positives': 62,
    'num_true_negatives': 183832,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.06060606060606061,
    'recall': 1.0,
    'f1': 0.1142857142857143,
    'accuracy': 0.9996628565835409}