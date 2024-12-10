"""
Classifies: CHEBI:28765 phosphatidylinositol phosphate
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_phosphatidylinositol_phosphate(smiles: str):
    """
    Determines if a molecule is a phosphatidylinositol phosphate.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a phosphatidylinositol phosphate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of a phosphate group
    has_phosphate = any(atom.GetAtomicNum() == 15 and atom.GetTotalDegree() == 4 for atom in mol.GetAtoms())
    if not has_phosphate:
        return False, "No phosphate group found"

    # Check for the presence of an inositol ring
    inositol_ring_info = mol.GetRingInfo().AtomRings()
    inositol_ring = None
    for ring in inositol_ring_info:
        if len(ring) == 6:
            ring_atoms = [mol.GetAtomWithIdx(idx) for idx in ring]
            if all(atom.GetAtomicNum() == 8 for atom in ring_atoms) and sum(atom.GetTotalDegree() - 2 for atom in ring_atoms) == 12:
                inositol_ring = ring
                break

    if inositol_ring is None:
        return False, "No inositol ring found"

    # Check for the presence of a glycerol backbone
    glycerol_atoms = []
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() == 8 and atom.GetTotalDegree() == 2:
            neighbors = atom.GetNeighbors()
            if all(neighbor.GetAtomicNum() == 6 and neighbor.GetTotalDegree() == 4 for neighbor in neighbors):
                glycerol_atoms.extend(neighbors)

    if len(glycerol_atoms) < 3:
        return False, "No glycerol backbone found"

    # Check for the presence of at least one acyl chain
    has_acyl_chain = False
    for atom in glycerol_atoms:
        for neighbor in atom.GetNeighbors():
            if neighbor.GetAtomicNum() == 6 and neighbor.GetTotalDegree() == 3 and neighbor.GetIsAromatic() == False:
                has_acyl_chain = True
                break

    if not has_acyl_chain:
        return False, "No acyl chain found"

    return True, "Molecule is a phosphatidylinositol phosphate"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:28765',
                          'name': 'phosphatidylinositol phosphate',
                          'definition': 'Any member of the phosphoinositide '
                                        'family of compounds, of which seven '
                                        'occur naturally.',
                          'parents': ['CHEBI:18179']},
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
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 183896,
    'num_false_negatives': 4,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999782490483958}