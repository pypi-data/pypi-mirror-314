"""
Classifies: CHEBI:22929 bromoalkane
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors

def is_bromoalkane(smiles: str):
    """
    Determines if a molecule is a bromoalkane (an alkane substituted by at least one bromine atom).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a bromoalkane, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains bromine atoms
    has_bromine = any(atom.GetSymbol() == 'Br' for atom in mol.GetAtoms())
    if not has_bromine:
        return False, "No bromine atoms found"

    # Check if the molecule is an alkane
    has_multiple_bonds = any(bond.GetBondType() != Chem.BondType.SINGLE for bond in mol.GetBonds())
    if has_multiple_bonds:
        return False, "Molecule contains multiple bonds, so it is not an alkane"

    # Check if the molecule contains heteroatoms other than bromine
    heteroatoms = [atom for atom in mol.GetAtoms() if atom.GetAtomicNum() not in (1, 6, 35)]
    if heteroatoms:
        return False, "Molecule contains heteroatoms other than bromine"

    # Check if the molecule contains rings
    ring_info = mol.GetRingInfo()
    num_rings = ring_info.NumRings()
    if num_rings > 0:
        # Check if the rings are only single bonds
        for ring in ring_info.BondRings():
            for bond_idx in ring:
                bond = mol.GetBondWithIdx(bond_idx)
                if bond.GetBondType() != Chem.BondType.SINGLE:
                    return False, "Molecule contains rings with multiple bonds, so it is not an alkane"

    return True, "Bromoalkane"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22929',
                          'name': 'bromoalkane',
                          'definition': 'Any haloalkane that consists of an '
                                        'alkane substituted by at least one '
                                        'bromine atom.',
                          'parents': ['CHEBI:24469', 'CHEBI:37141']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'True positives: []\n'
               "False positives: [('[H][Br+][H]', 'Bromoalkane'), ('[Br+]', "
               "'Bromoalkane'), ('[Br-]', 'Bromoalkane'), ('[79Br]', "
               "'Bromoalkane'), ('[Br]', 'Bromoalkane'), ('Br[H]', "
               "'Bromoalkane'), ('Br[Br+]', 'Bromoalkane'), ('BrBr', "
               "'Bromoalkane'), ('BrCC(CCCCCCCCCC)C', 'Bromoalkane'), "
               "('BrC(CCC(Br)CBr)CBr', 'Bromoalkane')]\n"
               "False negatives: [('BrC1C(Br)C(Br)C(Br)C(Br)C1Br', 'Molecule "
               "contains rings, so it is not an alkane')]",
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 11,
    'num_true_negatives': 183914,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.08333333333333333,
    'recall': 1.0,
    'f1': 0.15384615384615385,
    'accuracy': 0.9999401933386253}