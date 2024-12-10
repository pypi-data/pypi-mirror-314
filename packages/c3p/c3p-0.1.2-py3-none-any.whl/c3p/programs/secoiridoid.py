"""
Classifies: CHEBI:139166 secoiridoid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdFMCS

def is_secoiridoid(smiles: str):
    """
    Determines if a molecule is a secoiridoid (an iridoid monoterpenoid in which a bond in the cyclopentane ring has been cleaved).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a secoiridoid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Define the SMARTS pattern for the iridoid core
    iridoid_core = "[C@H]1[C@H]([C@@H]([C@@H]([C@H](O1)CO)O)O)O"
    pattern = Chem.MolFromSmarts(iridoid_core)

    matches = mol.GetSubstructMatches(pattern)

    if not matches:
        return False, "Iridoid core not found"

    # Check for cleaved cyclopentane ring
    ring_info = mol.GetRingInfo()
    rings = ring_info.AtomRings()
    acyclic = any(len(ring) > 5 for ring in rings)

    if acyclic:
        return True, "Secoiridoid (cleaved cyclopentane ring in iridoid core)"
    else:
        return False, "Iridoid core found, but cyclopentane ring is intact"

# Example usage
smiles = "[C@@H]1([C@@H]([C@H]([C@@H]([C@H](O1)CO)O)O)O)O[C@H]2/C(/[C@](C(=CO2)C(=O)OC)([H])CC(=O)OCCC=3C=CC(=CC3)O)=C/C"
result, reason = is_secoiridoid(smiles)
print(f"Is a secoiridoid? {result}")
print(f"Reason: {reason}")


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:139166',
                          'name': 'secoiridoid',
                          'definition': 'An iridoid monoterpenoid in which a '
                                        'bond in the cyclopentane ring has '
                                        'been cleaved.',
                          'parents': ['CHEBI:50563']},
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
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 100,
    'num_true_negatives': 868,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 1.0,
    'f1': 0.0196078431372549,
    'accuracy': 0.8968008255933952}