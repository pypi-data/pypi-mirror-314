"""
Classifies: CHEBI:33640 polycyclic cage
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
from rdkit.Chem import AllChem
from collections import defaultdict

def is_polycyclic_cage(smiles: str):
    """
    Determines if a molecule is a polycyclic cage compound.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a polycyclic cage compound, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Calculate ring information
    ring_info = mol.GetRingInfo()
    rings = ring_info.AtomRings()

    if not rings:
        return False, "No rings found"

    # Check for cage structure
    atoms_in_rings = set()
    for ring in rings:
        atoms_in_rings.update(ring)

    if len(atoms_in_rings) != len(mol.GetAtoms()):
        return False, "Not all atoms are part of a ring (not a cage structure)"

    # Check for polycyclic structure
    atom_rings = defaultdict(list)
    for atom_idx in atoms_in_rings:
        atom_rings[atom_idx] = [ring for ring in rings if atom_idx in ring]

    if any(len(rings) == 1 for rings in atom_rings.values()):
        return False, "Contains monocyclic components (not polycyclic)"

    return True, "Polycyclic cage compound"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33640',
                          'name': 'polycyclic cage',
                          'definition': 'A polycyclic compound having the '
                                        'shape of a cage.',
                          'parents': ['CHEBI:35990']},
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
    'num_true_positives': 2,
    'num_false_positives': 40,
    'num_true_negatives': 183846,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.047619047619047616,
    'recall': 0.5,
    'f1': 0.08695652173913042,
    'accuracy': 0.999771602588504}