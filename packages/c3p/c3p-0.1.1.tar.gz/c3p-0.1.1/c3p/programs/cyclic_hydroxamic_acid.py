"""
Classifies: CHEBI:23445 cyclic hydroxamic acid
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_cyclic_hydroxamic_acid(smiles: str):
    """
    Determines if a molecule is a cyclic hydroxamic acid.

    A cyclic hydroxamic acid is a lactam having a hydroxy substituent
    on the amide nitrogen.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a cyclic hydroxamic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for lactam ring
    lactam_ring = None
    for ring in mol.GetRingInfo().AtomRings():
        atoms = [mol.GetAtomWithIdx(idx) for idx in ring]
        if len(atoms) > 3 and any(atom.GetSymbol() == 'N' for atom in atoms) and any(atom.GetSymbol() == 'O' for atom in atoms):
            lactam_ring = ring
            break

    if lactam_ring is None:
        return False, "No lactam ring found"

    # Check for hydroxyl group on the nitrogen
    n_atom = next((mol.GetAtomWithIdx(idx) for idx in lactam_ring if mol.GetAtomWithIdx(idx).GetSymbol() == 'N'), None)
    if n_atom is None:
        return False, "No nitrogen atom found in the lactam ring"

    n_neighbors = [mol.GetAtomWithIdx(neighbor.GetIdx()) for neighbor in n_atom.GetNeighbors()]
    if not any(neighbor.GetSymbol() == 'O' and neighbor.GetTotalNumHs() == 1 for neighbor in n_neighbors):
        return False, "No hydroxyl group found on the nitrogen atom of the lactam ring"

    return True, "Molecule is a cyclic hydroxamic acid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23445',
                          'name': 'cyclic hydroxamic acid',
                          'definition': 'A lactam having a hydroxy substituent '
                                        'on the amide nitrogen.',
                          'parents': ['CHEBI:24650', 'CHEBI:24995']},
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
    'num_true_positives': 1,
    'num_false_positives': 18,
    'num_true_negatives': 183899,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.05263157894736842,
    'recall': 1.0,
    'f1': 0.1,
    'accuracy': 0.9999021302971977}