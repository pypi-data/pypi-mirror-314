"""
Classifies: CHEBI:145952 4-formyl steroid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_4_formyl_steroid(smiles: str):
    """
    Determines if a molecule is a 4-formyl steroid, which is any steroid substituted by a formyl group at position 4.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a 4-formyl steroid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Get the ring info for the molecule
    rings = mol.GetRingInfo()

    # Check for at least one 4-membered ring (steroidal backbone)
    if not any(len(ring) == 4 for ring in rings.AtomRings()):
        return False, "No 4-membered rings found (steroidal backbone not present)"

    # Find the 4-membered ring (steroidal backbone)
    steroidal_backbone = None
    for ring in rings.AtomRings():
        if len(ring) == 4:
            steroidal_backbone = ring
            break

    # Check if a formyl group is attached to the steroidal backbone
    formyl_position = None
    for atom_idx in steroidal_backbone:
        atom = mol.GetAtomWithIdx(atom_idx)
        if atom.GetSymbol() == 'C':
            for neighbor in atom.GetNeighbors():
                if neighbor.GetSymbol() == 'C' and neighbor.GetDegree() == 2 and neighbor.GetTotalNumHs() == 0:
                    formyl_atom = neighbor
                    for formyl_neighbor in formyl_atom.GetNeighbors():
                        if formyl_neighbor.GetSymbol() == 'O' and formyl_neighbor.GetDegree() == 1:
                            formyl_position = formyl_atom.GetIdx()
                            break

    if formyl_position is None:
        return False, "No formyl group found attached to the steroidal backbone"

    # Check if the formyl group is at position 4
    if formyl_position not in steroidal_backbone:
        return False, "Formyl group not attached at position 4 of the steroidal backbone"

    return True, "Molecule is a 4-formyl steroid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:145952',
                          'name': '4-formyl steroid',
                          'definition': 'A steroid aldehyde that is any '
                                        'steroid which is substituted by a '
                                        'formyl group at position 4.',
                          'parents': ['CHEBI:131565']},
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
    'num_true_negatives': 183923,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999945629716622}