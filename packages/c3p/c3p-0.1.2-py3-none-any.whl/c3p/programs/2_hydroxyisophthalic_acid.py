"""
Classifies: CHEBI:19643 2-hydroxyisophthalic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import BRICS

def is_2_hydroxyisophthalic_acid(smiles: str):
    """
    Determines if a molecule is a 2-hydroxyisophthalic acid.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a 2-hydroxyisophthalic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Identify the ring system
    ring_info = mol.GetRingInfo()
    ring_atoms = set()
    for ring in ring_info.AtomRings():
        if len(ring) == 6:
            ring_atoms.update(ring)
            break
    else:
        return False, "No 6-membered ring found"

    # Check if the ring is aromatic
    aromatic_ring = all(mol.GetAtomWithIdx(idx).GetIsAromatic() for idx in ring_atoms)
    if not aromatic_ring:
        return False, "Ring is not aromatic"

    # Check if the ring contains only carbon atoms
    if not all(mol.GetAtomWithIdx(idx).GetSymbol() == 'C' for idx in ring_atoms):
        return False, "Ring contains non-carbon atoms"

    # Check for the carboxylic acid groups
    carboxyl_count = sum(Chem.Mol.GetBondBetweenAtoms(mol, idx1, idx2).GetBondType() == Chem.BondType.DOUBLE
                         and mol.GetAtomWithIdx(idx2).GetSymbol() == 'O'
                         and mol.GetAtomWithIdx(idx2).GetIsAromatic() is False
                         and mol.GetAtomWithIdx(idx2).GetTotalDegree() == 1
                         for idx1 in ring_atoms for idx2 in mol.GetAtomWithIdx(idx1).GetNeighbors())
    if carboxyl_count != 2:
        return False, "Molecule does not have two carboxylic acid groups"

    # Check for the hydroxy group at position 2
    hydroxy_idx = None
    for idx in ring_atoms:
        if mol.GetAtomWithIdx(idx).GetTotalNumHs() == 1:
            hydroxy_idx = idx
            break
    if hydroxy_idx is None:
        return False, "No hydroxy group found on the ring"

    # Check if the hydroxy group is at position 2
    brics = BRICS.BRICSDecomposition(mol)
    brics_smarts = brics.GetBrics()
    if 'O=C1OCC=2C1=C(O)C(=CC2C(=O)O)' not in brics_smarts:
        return False, "Hydroxy group is not at position 2"

    return True, "Molecule is a 2-hydroxyisophthalic acid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:19643',
                          'name': '2-hydroxyisophthalic acid',
                          'definition': 'A hydroxybenzoic acid that is '
                                        'isophthalic acid in which the '
                                        'hydrogen at position 2 is substituted '
                                        'by a hydroxy group.',
                          'parents': ['CHEBI:24676', 'CHEBI:33853']},
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
    'error': 'Python argument types in\n'
             '    Mol.GetBondBetweenAtoms(Mol, int, Atom)\n'
             'did not match C++ signature:\n'
             '    GetBondBetweenAtoms(RDKit::ROMol {lvalue} self, unsigned int '
             'idx1, unsigned int idx2)',
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