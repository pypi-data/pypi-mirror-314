"""
Classifies: CHEBI:33637 ortho-fused compound
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_ortho_fused_compound(smiles: str):
    """
    Determines if a molecule is an ortho-fused compound.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an ortho-fused compound, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find all rings in the molecule
    ring_info = mol.GetRingInfo()
    rings = ring_info.AtomRings()

    # Check if there are at least two rings
    if len(rings) < 2:
        return False, "Compound does not have at least two rings"

    # Find all pairs of rings that share exactly two atoms
    ortho_fused_rings = []
    for i, ring1 in enumerate(rings):
        for ring2 in rings[i+1:]:
            common_atoms = set(ring1) & set(ring2)
            if len(common_atoms) == 2:
                ortho_fused_rings.append((ring1, ring2))

    # Check if any pair of ortho-fused rings is aromatic
    for ring1, ring2 in ortho_fused_rings:
        ring1_atoms = [mol.GetAtomWithIdx(idx) for idx in ring1]
        ring2_atoms = [mol.GetAtomWithIdx(idx) for idx in ring2]
        if all(atom.GetIsAromatic() for atom in ring1_atoms) and all(atom.GetIsAromatic() for atom in ring2_atoms):
            return True, "Compound has two aromatic rings fused in an ortho configuration"

    return False, "Compound does not have any ortho-fused aromatic rings"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33637',
                          'name': 'ortho-fused compound',
                          'definition': 'A polycyclic compound in which two '
                                        'rings have two, and only two, atoms '
                                        'in common. Such compounds have n '
                                        'common faces and 2n common atoms.',
                          'parents': ['CHEBI:35293']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': 'Attempt failed: tuple index out of range',
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 5,
    'num_false_positives': 100,
    'num_true_negatives': 591,
    'num_false_negatives': 7,
    'num_negatives': None,
    'precision': 0.047619047619047616,
    'recall': 0.4166666666666667,
    'f1': 0.08547008547008546,
    'accuracy': 0.8477951635846372}