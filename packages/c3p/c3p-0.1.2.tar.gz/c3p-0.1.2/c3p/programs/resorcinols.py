"""
Classifies: CHEBI:33572 resorcinols
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_resorcinol(smiles: str):
    """
    Determines if a molecule is a resorcinol (benzenediol with hydroxy groups meta to each other).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a resorcinol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule has a single benzene ring
    ring_info = mol.GetRingInfo()
    aromatic_rings = [ring for ring in ring_info.AtomRings() if all(mol.GetAtomWithIdx(idx).GetIsAromatic() for idx in ring)]
    benzene_rings = [ring for ring in aromatic_rings if len(ring) == 6]

    if len(benzene_rings) != 1:
        return False, "Molecule does not have a single benzene ring"

    # Check if the benzene ring has two hydroxy substituents
    benzene_ring = benzene_rings[0]
    hydroxy_atoms = []
    for idx in benzene_ring:
        atom = mol.GetAtomWithIdx(idx)
        if atom.GetSymbol() == 'O' and atom.GetTotalNumHs() == 1:
            hydroxy_atoms.append(atom)

    if len(hydroxy_atoms) != 2:
        return False, "Benzene ring does not have exactly two hydroxy substituents"

    # Check if the hydroxy groups are meta to each other
    distance_matrix = Chem.GetDistanceMatrix(mol)
    hydroxy_idxs = [hydroxy_atom.GetIdx() for hydroxy_atom in hydroxy_atoms]
    distance = distance_matrix[hydroxy_idxs[0], hydroxy_idxs[1]]

    if distance != 3:
        return False, "Hydroxy groups are not meta to each other"

    return True, "Molecule is a resorcinol"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33572',
                          'name': 'resorcinols',
                          'definition': 'Any benzenediol in which the two '
                                        'hydroxy groups are meta to one '
                                        'another.',
                          'parents': ['CHEBI:33570']},
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
    'error': "name 'is_resorcinols' is not defined",
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