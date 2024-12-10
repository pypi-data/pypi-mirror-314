"""
Classifies: CHEBI:28802 flavonols
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_flavonols(smiles: str):
    """
    Determines if a molecule is a flavonol, defined as a hydroxyflavone with a hydroxy group
    at position 3 of the heterocyclic ring.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a flavonol, False otherwise
        str: Reason for the classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find the heterocyclic ring with oxygen
    heterocyclic_ring = None
    for ring in mol.GetRingInfo().AtomRings():
        atoms = [mol.GetAtomWithIdx(idx) for idx in ring]
        if any(atom.GetAtomicNum() == 8 for atom in atoms) and len(ring) == 6:
            heterocyclic_ring = ring
            break

    if heterocyclic_ring is None:
        return False, "No heterocyclic ring with oxygen found"

    # Check if the ring has a hydroxy group at position 3
    ring_atoms = [mol.GetAtomWithIdx(idx) for idx in heterocyclic_ring]
    position_3_atom = ring_atoms[2]

    if position_3_atom.GetAtomicNum() != 8 or position_3_atom.GetTotalNumHs() != 1:
        return False, "No hydroxy group at position 3 of the heterocyclic ring"

    # Check if the structure contains a carbonyl group in the heterocyclic ring
    carbonyl_group_found = False
    for atom in ring_atoms:
        if atom.GetAtomicNum() == 8 and atom.GetFormalCharge() == 0 and atom.GetImplicitValence() == 2:
            carbonyl_group_found = True
            break

    if not carbonyl_group_found:
        return False, "No carbonyl group found in the heterocyclic ring"

    return True, "The molecule is a flavonol"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:28802',
                          'name': 'flavonols',
                          'definition': 'Any hydroxyflavone in which is the '
                                        'ring hydrogen at position 3 of the '
                                        'heterocyclic ring is replaced by a '
                                        'hydroxy group.',
                          'parents': ['CHEBI:192499', 'CHEBI:24698']},
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
    'num_true_negatives': 183854,
    'num_false_negatives': 8,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999564891059599}