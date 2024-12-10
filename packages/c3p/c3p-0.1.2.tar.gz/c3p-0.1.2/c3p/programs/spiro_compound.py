"""
Classifies: CHEBI:33599 spiro compound
"""
from rdkit import Chem
from rdkit.Chem import rdchem

def is_spiro_compound(smiles: str):
    """
    Determines if a molecule is a spiro compound.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a spiro compound, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find all rings in the molecule
    rings = mol.GetRingInfo().AtomRings()

    # Check if any pair of rings share only one common atom
    for i, ring1 in enumerate(rings):
        for ring2 in rings[i + 1:]:
            common_atoms = set(ring1) & set(ring2)
            if len(common_atoms) == 1:
                common_atom = mol.GetAtomWithIdx(list(common_atoms)[0])
                return True, f"Spiro compound with common atom {common_atom.GetSymbol()} (index {common_atom.GetIdx()})"

    return False, "Not a spiro compound"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33599',
                          'name': 'spiro compound',
                          'definition': 'A compound having one atom as the '
                                        'only common member of two rings.',
                          'parents': ['CHEBI:33635']},
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
    'num_true_positives': 40,
    'num_false_positives': 100,
    'num_true_negatives': 2005,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.2857142857142857,
    'recall': 1.0,
    'f1': 0.4444444444444445,
    'accuracy': 0.9533799533799534}