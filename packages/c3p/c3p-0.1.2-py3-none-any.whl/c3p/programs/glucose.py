"""
Classifies: CHEBI:17234 glucose
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_glucose(smiles: str):
    """
    Determines if a molecule is glucose (an aldohexose used as a source of energy and metabolic intermediate).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is glucose, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of a glucose-like ring
    ring_info = mol.GetRingInfo()
    rings = ring_info.AtomRings()
    glucose_ring = None
    for ring in rings:
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(idx) for idx in ring]
            if all(atom.GetSymbol() == 'C' for atom in atoms):
                glucose_ring = ring
                break

    if glucose_ring is None:
        return False, "No glucose-like ring found"

    # Check for the presence of an aldehyde group
    aldehyde_atom = None
    for atom_idx in glucose_ring:
        atom = mol.GetAtomWithIdx(atom_idx)
        if atom.GetTotalNumHs() == 0 and sum(mol.GetAtomWithIdx(neighbor).GetTotalNumHs() for neighbor in atom.GetNeighbors()) == 1:
            aldehyde_atom = atom_idx
            break

    if aldehyde_atom is None:
        return False, "No aldehyde group found"

    # Check for the presence of five hydroxyl groups
    hydroxyl_count = 0
    for atom_idx in glucose_ring:
        atom = mol.GetAtomWithIdx(atom_idx)
        if atom.GetSymbol() == 'O' and atom.GetTotalNumHs() == 1:
            hydroxyl_count += 1

    if hydroxyl_count != 5:
        return False, f"Incorrect number of hydroxyl groups (found {hydroxyl_count}, expected 5)"

    return True, "The molecule is glucose"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17234',
                          'name': 'glucose',
                          'definition': 'An aldohexose used as a source of '
                                        'energy and metabolic intermediate.',
                          'parents': ['CHEBI:33917']},
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
    'success': False,
    'best': True,
    'error': 'Python argument types in\n'
             '    Mol.GetAtomWithIdx(Mol, Atom)\n'
             'did not match C++ signature:\n'
             '    GetAtomWithIdx(RDKit::ROMol {lvalue} self, unsigned int idx)',
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': None}