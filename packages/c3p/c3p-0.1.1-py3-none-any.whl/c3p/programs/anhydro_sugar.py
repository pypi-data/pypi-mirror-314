"""
Classifies: CHEBI:22558 anhydro sugar
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_anhydro_sugar(smiles: str):
    """
    Determines if a molecule is an anhydro sugar.

    Anhydro sugars are intramolecular ethers formally arising by elimination
    of water from two hydroxy groups of a single molecule of a monosaccharide
    (aldose or ketose) or monosaccharide derivative.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an anhydro sugar, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains oxygen atoms
    if not [atom for atom in mol.GetAtoms() if atom.GetSymbol() == 'O']:
        return False, "No oxygen atoms found"

    # Check for the presence of ether bonds
    ether_bonds = [bond for bond in mol.GetBonds() if bond.GetBondType() == Chem.BondType.ETHER]
    if not ether_bonds:
        return False, "No ether bonds found"

    # Check for intramolecular ether bonds
    intramolecular_ethers = []
    for bond in ether_bonds:
        atom1 = mol.GetAtomWithIdx(bond.GetBeginAtomIdx())
        atom2 = mol.GetAtomWithIdx(bond.GetEndAtomIdx())
        ring_info = mol.GetRingInfo()
        if not ring_info.IsBondInRingOfSize(bond.GetIdx(), 3):
            continue
        intramolecular_ethers.append((atom1.GetIdx(), atom2.GetIdx()))

    if not intramolecular_ethers:
        return False, "No intramolecular ether bonds found"

    # Check if the molecule is a monosaccharide or monosaccharide derivative
    mw = rdMolDescriptors.CalcExactMolWt(mol)
    if mw < 100 or mw > 300:
        return False, "Molecular weight outside the typical range for monosaccharides"

    return True, "Molecule classified as an anhydro sugar"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22558',
                          'name': 'anhydro sugar',
                          'definition': 'Intramolecular ethers formally '
                                        'arising by elimination of water from '
                                        'two hydroxy groups of a single '
                                        'molecule of a monosaccharide (aldose '
                                        'or ketose) or monosaccharide '
                                        'derivative.',
                          'parents': ['CHEBI:35381']},
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
    'error': "type object 'BondType' has no attribute 'ETHER'",
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