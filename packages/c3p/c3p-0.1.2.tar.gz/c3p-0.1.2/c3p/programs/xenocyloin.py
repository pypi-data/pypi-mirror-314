"""
Classifies: CHEBI:156365 xenocyloin
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_xenocyloin(smiles: str):
    """
    Determines if a molecule is a xenocyloin, a member of the class of indoles that is 1-H indole
    with the hydrogen at position 3 substituted with a 2'-hydroxy-3'-alkoxy-4'-alkyl group.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a xenocyloin, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of an indole ring
    indole_ring = mol.GetSubstructMatches(Chem.MolFromSmarts('c1ccc2n[nH]cc2c1'))
    if not indole_ring:
        return False, "No indole ring found"

    # Check for the presence of a hydrogen at position 1 of the indole ring
    indole_ring_atoms = [mol.GetAtomWithIdx(idx) for idx in indole_ring[0]]
    if not any(atom.GetSymbol() == 'H' and atom.GetTotalNumHs() == 1 for atom in indole_ring_atoms):
        return False, "No hydrogen at position 1 of the indole ring"

    # Check for the 2'-hydroxy-3'-alkoxy-4'-alkyl substituent at position 3
    indole_ring_atom_3 = mol.GetAtomWithIdx(indole_ring[0][2])
    neighbors = indole_ring_atom_3.GetNeighbors()

    if len(neighbors) != 1:
        return False, "Substituent at position 3 is incorrect"

    # Check for the 2'-hydroxy group
    neighbor_atom = neighbors[0]
    if neighbor_atom.GetTotalNumHs() != 1:
        return False, "2'-hydroxy group not found"

    # Check for the 3'-alkoxy group
    neighbor_neighbors = neighbor_atom.GetNeighbors()
    if len(neighbor_neighbors) != 2:
        return False, "3'-alkoxy group not found"

    # Check for the 4'-alkyl group
    alkyl_group = [n for n in neighbor_neighbors if n.GetTotalNumHs() == 0 and n.GetIsAromatic() is False]
    if len(alkyl_group) != 1:
        return False, "4'-alkyl group not found"

    return True, "Molecule is a xenocyloin"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:156365',
                          'name': 'xenocyloin',
                          'definition': 'A member of the class of indoles that '
                                        'is 1-H indole with the hydrogen at '
                                        'position 3 substituted with a '
                                        "2'-hydroxy-3'-alkoxy-4'-alkyl group. "
                                        'It is an antiinsectan compound found '
                                        'in the nematode parasite Xenorhabdus '
                                        'bovienii.',
                          'parents': ['CHEBI:17087', 'CHEBI:24828']},
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
    'num_true_negatives': 183925,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999945630307842}