"""
Classifies: CHEBI:26893 tetracyclic triterpenoid
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_tetracyclic_triterpenoid(smiles: str):
    """
    Determines if a molecule is a tetracyclic triterpenoid.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a tetracyclic triterpenoid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule has 30 carbon atoms
    if rdMolDescriptors.CalcMolFormula(mol).count('C') != 30:
        return False, "Molecule does not have 30 carbon atoms"

    # Count the number of rings
    ring_info = mol.GetRingInfo()
    num_rings = ring_info.NumRings()

    # Check if the molecule has exactly 4 rings
    if num_rings != 4:
        return False, f"Molecule has {num_rings} rings, expected 4"

    # Check if all rings are fused
    fused_rings = set()
    for ring in ring_info.AtomRings():
        ring_atoms = set(ring)
        for other_ring in ring_info.AtomRings():
            if len(ring_atoms & set(other_ring)) > 0:
                fused_rings.add(tuple(sorted(ring)))
                fused_rings.add(tuple(sorted(other_ring)))

    if len(fused_rings) != 4:
        return False, "Rings are not fused into a tetracyclic system"

    return True, "The molecule is a tetracyclic triterpenoid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26893',
                          'name': 'tetracyclic triterpenoid',
                          'definition': 'Any triterpenoid consisting of a '
                                        'tetracyclic skeleton.',
                          'parents': ['CHEBI:177333', 'CHEBI:36615']},
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
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 183684,
    'num_false_negatives': 25,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9998639152137347}