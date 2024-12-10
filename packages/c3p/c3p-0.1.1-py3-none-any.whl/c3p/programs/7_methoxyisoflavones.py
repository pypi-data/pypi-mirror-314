"""
Classifies: CHEBI:140356 7-methoxyisoflavones
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_7_methoxyisoflavone(smiles: str):
    """
    Determines if a molecule is a 7-methoxyisoflavone.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a 7-methoxyisoflavone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find the isoflavone moiety
    isoflavone_pattern = Chem.MolFromSmarts('C1=C(C(=O)C2=C(C=C1)C(=O)C3=C(C=C(C=C3)O)O2)O')
    matches = mol.GetSubstructMatches(isoflavone_pattern)

    if not matches:
        return False, "Molecule does not contain an isoflavone moiety"

    # Check for a methoxy group at the 7-position
    for match in matches:
        ring_atoms = list(match)
        ring_atoms.sort()  # Ensure consistent ordering
        ring_info = mol.GetRingInfo().AtomRings()[ring_atoms.index(tuple(ring_atoms))]

        # Find the 7-position atom
        for i, atom_idx in enumerate(ring_info):
            atom = mol.GetAtomWithIdx(atom_idx)
            if atom.GetSymbol() == 'O' and atom.GetTotalNumHs() == 0:
                break
        else:
            continue

        neighbor = atom.GetNeighbors()[0]
        if neighbor.GetSymbol() == 'C' and neighbor.GetTotalNumHs() == 0:
            methoxy_neighbor = neighbor.GetNeighbors()[0]
            if methoxy_neighbor.GetSymbol() == 'O' and methoxy_neighbor.GetTotalNumHs() == 1:
                return True, "Molecule is a 7-methoxyisoflavone"

    return False, "Molecule does not have a methoxy group at the 7-position of the isoflavone moiety"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:140356',
                          'name': '7-methoxyisoflavones',
                          'definition': 'Any methoxyisoflavone that has a '
                                        'methoxy group at the 7-position of '
                                        'the isoflavone moiety.',
                          'parents': ['CHEBI:38756']},
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
    'error': "name 'is_7_methoxyisoflavones' is not defined",
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