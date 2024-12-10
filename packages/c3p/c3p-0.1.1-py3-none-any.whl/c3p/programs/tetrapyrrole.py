"""
Classifies: CHEBI:26932 tetrapyrrole
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_tetrapyrrole(smiles: str):
    """
    Determines if a molecule is a tetrapyrrole, defined as a natural pigment containing four pyrrole rings
    joined by one-carbon units linking position 2 of one pyrrole ring to position 5 of the next.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a tetrapyrrole, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find all rings
    rings = mol.GetRingInfo().AtomRings()

    # Check for four pyrrole rings
    pyrrole_rings = []
    for ring in rings:
        atoms = [mol.GetAtomWithIdx(i) for i in ring]
        if len(ring) == 4:
            num_n = sum(atom.GetAtomicNum() == 7 for atom in atoms)
            if num_n == 4:  # All atoms in the ring are nitrogen
                pyrrole_rings.append(ring)

    if len(pyrrole_rings) != 4:
        return False, "Not exactly four pyrrole rings found"

    # Check if the pyrrole rings are connected by one-carbon units
    connected_rings = set()
    for i, ring1 in enumerate(pyrrole_rings):
        for j, ring2 in enumerate(pyrrole_rings):
            if i != j:
                for atom1_idx in ring1:
                    atom1 = mol.GetAtomWithIdx(atom1_idx)
                    for atom2_idx in ring2:
                        atom2 = mol.GetAtomWithIdx(atom2_idx)
                        if atom1.GetIdx() in atom2.GetNeighbors():
                            connected_rings.add((i, j))

    if len(connected_rings) != 4:
        return False, "Pyrrole rings are not correctly connected by one-carbon units"

    return True, "Molecule is a tetrapyrrole"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26932',
                          'name': 'tetrapyrrole',
                          'definition': 'A natural pigment containing four '
                                        'pyrrole rings joined by one-carbon '
                                        'units linking position 2 of one '
                                        'pyrrole ring to position 5 of the '
                                        'next.',
                          'parents': ['CHEBI:33833', 'CHEBI:38077']},
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
    'num_true_negatives': 183622,
    'num_false_negatives': 31,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9998312034107801}