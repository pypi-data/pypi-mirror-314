"""
Classifies: CHEBI:33639 ortho- and peri-fused compound
"""
from rdkit import Chem
from rdkit.Chem.MolToPDBResidues import UniqueFusedRingSets

def is_ortho_and_peri_fused_compound(smiles: str):
    """
    Determines if a molecule is an ortho- and peri-fused compound.

    An ortho- and peri-fused compound is defined as a polycyclic compound in which
    one ring contains two, and only two, atoms in common with each of two or more
    rings of a contiguous series of rings. Such compounds have n common faces and
    less than 2n common atoms.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an ortho- and peri-fused compound, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Get unique fused ring sets
    unique_fused_rings = UniqueFusedRingSets(mol)

    for fused_ring_set in unique_fused_rings:
        # Check if the fused ring set has more than 2 rings
        if len(fused_ring_set) > 2:
            # Count the number of common faces and common atoms
            common_faces = sum(len(ring.CanonicalBondRmAtomInRing()) for ring in fused_ring_set)
            common_atoms = sum(len(ring.Atoms()) for ring in fused_ring_set) - len(set().union(*(ring.Atoms() for ring in fused_ring_set)))

            # Check if the number of common faces is equal to the number of rings
            # and the number of common atoms is less than twice the number of common faces
            if common_faces == len(fused_ring_set) and common_atoms < 2 * common_faces:
                return True, "Molecule is an ortho- and peri-fused compound"

    return False, "Molecule is not an ortho- and peri-fused compound"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33639',
                          'name': 'ortho- and peri-fused compound',
                          'definition': 'A polycyclic compound in which one '
                                        'ring contains two, and only two, '
                                        'atoms in common with each of two or '
                                        'more rings of a contiguous series of '
                                        'rings. Such compounds have n common '
                                        'faces and less than 2n common atoms.',
                          'parents': ['CHEBI:35293']},
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
    'success': False,
    'best': True,
    'error': "No module named 'rdkit.Chem.MolToPDBResidues'",
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0,
    'f1': 0,
    'accuracy': None}