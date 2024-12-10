"""
Classifies: CHEBI:23133 chlorobenzoate
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors

def is_chlorobenzoate(smiles: str):
    """
    Determines if a molecule is a chlorobenzoate.
    Chlorobenzoates are benzoates in which the benzene ring is substituted by at least one chloro group.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a chlorobenzoate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for benzoate group
    benzoate_pattern = Chem.MolFromSmarts("[O-]C(=O)c")
    if not mol.HasSubstructMatch(benzoate_pattern):
        return False, "Molecule does not contain a benzoate group"

    # Check for chlorine substituents on the benzene ring
    benzene_ring = Chem.MolFromSmarts("c1ccccc1")
    matches = mol.GetSubstructMatches(benzene_ring)

    if not matches:
        return False, "Molecule does not contain a benzene ring"

    ring_atoms = set(matches[0])
    chloro_substituents = []

    for atom_idx in ring_atoms:
        atom = mol.GetAtomWithIdx(atom_idx)
        for neighbor in atom.GetNeighbors():
            if neighbor.GetIdx() not in ring_atoms and neighbor.GetSymbol() == 'Cl':
                chloro_substituents.append(neighbor.GetSymbol())

    if not chloro_substituents:
        return False, "Benzene ring does not have chloro substituents"

    return True, f"Chlorobenzoate with chloro substituents: {', '.join(chloro_substituents)}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23133',
                          'name': 'chlorobenzoate',
                          'definition': 'Any member of the class of benzoates '
                                        'in which the benzene ring is '
                                        'substituted by at least one chloro '
                                        'group.',
                          'parents': ['CHEBI:22718']},
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
    'num_false_positives': 22,
    'num_true_negatives': 183901,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.043478260869565216,
    'recall': 1.0,
    'f1': 0.08333333333333333,
    'accuracy': 0.9998803853765685}