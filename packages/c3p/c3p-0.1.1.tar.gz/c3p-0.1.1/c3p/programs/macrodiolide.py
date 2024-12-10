"""
Classifies: CHEBI:145556 macrodiolide
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_macrodiolide(smiles: str):
    """
    Determines if a molecule is a macrodiolide (a macrocyclic polyester with two ester linkages in the ring).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a macrodiolide, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for macrocyclic ring
    rings = mol.GetRingInfo().AtomRings()
    if not rings:
        return False, "No rings found"

    macrocyclic_ring = None
    for ring in rings:
        if len(ring) >= 8:  # Macrocyclic rings typically have at least 8 atoms
            macrocyclic_ring = ring
            break

    if macrocyclic_ring is None:
        return False, "No macrocyclic ring found"

    # Count the number of ester linkages in the macrocyclic ring
    ester_count = 0
    for atom_idx in macrocyclic_ring:
        atom = mol.GetAtomWithIdx(atom_idx)
        if atom.GetSymbol() == 'O' and atom.GetFormalCharge() == 0:
            neighbors = list(atom.GetNeighbors())
            if len(neighbors) == 2:
                neighbor1, neighbor2 = neighbors
                if neighbor1.GetSymbol() == 'C' and neighbor2.GetSymbol() == 'C':
                    if neighbor1.GetDegree() == 3 and neighbor2.GetDegree() == 3:
                        ester_count += 1

    if ester_count == 2:
        return True, "Macrodiolide with two ester linkages in the macrocyclic ring"
    else:
        return False, f"Not a macrodiolide (found {ester_count} ester linkages in the macrocyclic ring)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:145556',
                          'name': 'macrodiolide',
                          'definition': 'A macropolylide which contains two '
                                        'ester linkages in one macrocyclic '
                                        'ring.',
                          'parents': ['CHEBI:145555']},
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
    'num_true_negatives': 34320,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 1.0,
    'f1': 0.0196078431372549,
    'accuracy': 0.9970947967810349}