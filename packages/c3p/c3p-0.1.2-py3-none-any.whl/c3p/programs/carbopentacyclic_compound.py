"""
Classifies: CHEBI:177356 carbopentacyclic compound
"""
from rdkit import Chem

def is_carbopentacyclic_compound(smiles: str):
    """
    Determines if a molecule is a carbopentacyclic compound, which is defined as a carbopolycyclic compound
    comprising of five carbocyclic rings.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a carbopentacyclic compound, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Get the ring information
    ring_info = mol.GetRingInfo()

    # Count the number of carbocyclic rings
    carbocyclic_rings = 0
    for ring in ring_info.AtomRings():
        atoms = [mol.GetAtomWithIdx(idx) for idx in ring]
        if all(atom.GetSymbol() == 'C' for atom in atoms) and len(ring) > 2:
            carbocyclic_rings += 1

    if carbocyclic_rings == 5:
        return True, "The compound contains five carbocyclic rings"
    else:
        return False, f"The compound does not contain exactly five carbocyclic rings (found {carbocyclic_rings})"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:177356',
                          'name': 'carbopentacyclic compound',
                          'definition': 'A carbopolyclic compound comprising '
                                        'of five carbocyclic rings.',
                          'parents': ['CHEBI:177357', 'CHEBI:35294']},
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
    'num_true_negatives': 6926,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 1.0,
    'f1': 0.0196078431372549,
    'accuracy': 0.9857691760352925}