"""
Classifies: CHEBI:22557 anhydrohexose
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_anhydrohexose(smiles: str):
    """
    Determines if a molecule is an anhydrohexose (any anhydro sugar formally arising by elimination
    of water from two hydroxy groups of a single molecule of a hexose or hexose derivative).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an anhydrohexose, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule has an anhydride group
    anhydride_ring = Chem.GetSSSR(mol)
    if not any(len(ring) == 5 and sum(mol.GetAtomWithIdx(idx).GetHybridization() == Chem.HybridizationType.SP2 for idx in ring) == 4 for ring in anhydride_ring):
        return False, "No anhydride ring found"

    # Check if the molecule has a hexose backbone
    ring_atoms = set()
    for ring in anhydride_ring:
        if len(ring) == 5:
            ring_atoms.update(ring)
    hexose_backbone = False
    for atom_idx in ring_atoms:
        atom = mol.GetAtomWithIdx(atom_idx)
        neighbors = [mol.GetAtomWithIdx(neighbor.GetIdx()) for neighbor in atom.GetNeighbors()]
        if sum(neighbor.GetSymbol() == 'O' and neighbor.GetDegree() == 1 for neighbor in neighbors) == 1:
            hexose_backbone = True
            break

    if not hexose_backbone:
        return False, "No hexose backbone found"

    return True, "Molecule is an anhydrohexose"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22557',
                          'name': 'anhydrohexose',
                          'definition': 'Any anhydro sugar formally arising by '
                                        'elimination of water from two hydroxy '
                                        'groups of a single molecule of a '
                                        'hexose or hexose derivative.',
                          'parents': ['CHEBI:22558']},
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
    'num_false_positives': 100,
    'num_true_negatives': 3944,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9750309023485785}