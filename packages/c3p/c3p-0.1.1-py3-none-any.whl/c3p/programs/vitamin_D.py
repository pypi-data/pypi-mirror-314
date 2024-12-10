"""
Classifies: CHEBI:27300 vitamin D
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_vitamin_D(smiles: str):
    """
    Determines if a molecule is a vitamin D compound.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a vitamin D compound, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of hydroxyl groups
    num_hydroxyl_groups = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O' and atom.GetIsAromatic() == False)
    if num_hydroxyl_groups < 1:
        return False, "No hydroxyl groups found"

    # Check for the presence of a seco-steroid skeleton
    seco_steroid_skeleton = False
    rings = mol.GetRingInfo().AtomRings()
    for ring in rings:
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if all(atom.GetSymbol() == 'C' for atom in atoms):
                seco_steroid_skeleton = True
                break

    if not seco_steroid_skeleton:
        return False, "No seco-steroid skeleton found"

    # Check for the presence of a conjugated triene system
    conjugated_triene = False
    for bond in mol.GetBonds():
        begin_atom = bond.GetBeginAtom()
        end_atom = bond.GetEndAtom()
        begin_idx = begin_atom.GetIdx()
        end_idx = end_atom.GetIdx()
        bond_type = bond.GetBondType()
        if bond_type == Chem.BondType.DOUBLE:
            neighbors_begin = [neighbor.GetIdx() for neighbor in begin_atom.GetNeighbors()]
            neighbors_end = [neighbor.GetIdx() for neighbor in end_atom.GetNeighbors()]
            if any(mol.GetBondBetweenAtoms(begin_idx, neighbor).GetBondType() == Chem.BondType.DOUBLE for neighbor in neighbors_begin) and \
               any(mol.GetBondBetweenAtoms(end_idx, neighbor).GetBondType() == Chem.BondType.DOUBLE for neighbor in neighbors_end):
                conjugated_triene = True
                break

    if not conjugated_triene:
        return False, "No conjugated triene system found"

    return True, "Molecule is a vitamin D compound"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:27300',
                          'name': 'vitamin D',
                          'definition': 'Any member of a group of fat-soluble '
                                        'hydroxy seco-steroids that exhibit '
                                        'biological activity against vitamin D '
                                        'deficiency. Vitamin D  can be '
                                        'obtained from sun exposure, food and '
                                        'supplements and is biologically '
                                        'inactive and converted into the '
                                        'biologically active calcitriol via '
                                        'double hydroxylation in the body.',
                          'parents': ['CHEBI:36853']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': 'Attempt failed: cannot unpack non-iterable Bond object',
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 25,
    'num_false_positives': 100,
    'num_true_negatives': 109,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.2,
    'recall': 1.0,
    'f1': 0.33333333333333337,
    'accuracy': 0.5726495726495726}