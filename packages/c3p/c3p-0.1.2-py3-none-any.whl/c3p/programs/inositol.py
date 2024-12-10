"""
Classifies: CHEBI:24848 inositol
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_inositol(smiles: str):
    """
    Determines if a molecule is an inositol (any cyclohexane-1,2,3,4,5,6-hexol).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an inositol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Count the number of rings
    ring_info = mol.GetRingInfo()
    rings = ring_info.AtomRings()
    if len(rings) != 1:
        return False, "Molecule does not contain exactly one ring"

    # Check if the ring is a 6-membered ring
    ring = rings[0]
    if len(ring) != 6:
        return False, "Molecule does not contain a 6-membered ring"

    # Check if all ring atoms are carbon
    ring_atoms = [mol.GetAtomWithIdx(idx) for idx in ring]
    if not all(atom.GetSymbol() == 'C' for atom in ring_atoms):
        return False, "Ring contains non-carbon atoms"

    # Check if all ring atoms are bound to a hydroxy group
    for atom in ring_atoms:
        hydroxy_groups = sum(1 for neighbor in atom.GetNeighbors() if neighbor.GetSymbol() == 'O' and neighbor.GetTotalNumHs() == 1)
        if hydroxy_groups != 1:
            return False, "Ring atom not bound to a single hydroxy group"

    return True, "Molecule is an inositol (cyclohexane-1,2,3,4,5,6-hexol)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24848',
                          'name': 'inositol',
                          'definition': 'Any cyclohexane-1,2,3,4,5,6-hexol.',
                          'parents': ['CHEBI:23451', 'CHEBI:37206']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': 'Attempt failed: Python argument types in\n'
               '    Mol.GetAtomWithIdx(Mol, Atom)\n'
               'did not match C++ signature:\n'
               '    GetAtomWithIdx(RDKit::ROMol {lvalue} self, unsigned int '
               'idx)',
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 2,
    'num_true_negatives': 183923,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.3333333333333333,
    'recall': 1.0,
    'f1': 0.5,
    'accuracy': 0.9999891260615682}