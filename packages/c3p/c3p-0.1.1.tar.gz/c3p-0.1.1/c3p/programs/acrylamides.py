"""
Classifies: CHEBI:22216 acrylamides
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_acrylamides(smiles: str):
    """
    Determines if a molecule is an acrylamide or a derivative of acrylamide.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an acrylamide, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find all amide bonds
    amide_bonds = []
    for bond in mol.GetBonds():
        begin_atom = mol.GetAtomWithIdx(bond.GetBeginAtomIdx())
        end_atom = mol.GetAtomWithIdx(bond.GetEndAtomIdx())
        if begin_atom.GetSymbol() == 'N' and end_atom.GetSymbol() == 'C' and begin_atom.GetIsAromatic() is False and end_atom.GetIsAromatic() is False:
            if begin_atom.GetTotalNumHs() == 0 and end_atom.GetTotalNumHs() == 0:
                amide_bonds.append(bond.GetBeginAtomIdx())
                amide_bonds.append(bond.GetEndAtomIdx())

    if not amide_bonds:
        return False, "No amide bonds found"

    # Find all alkene bonds
    alkene_bonds = []
    for bond in mol.GetBonds():
        if bond.GetBondType() == Chem.BondType.DOUBLE:
            begin_atom = mol.GetAtomWithIdx(bond.GetBeginAtomIdx())
            end_atom = mol.GetAtomWithIdx(bond.GetEndAtomIdx())
            if begin_atom.GetHybridization() == Chem.HybridizationType.SP2 and end_atom.GetHybridization() == Chem.HybridizationType.SP2:
                alkene_bonds.append(bond.GetBeginAtomIdx())
                alkene_bonds.append(bond.GetEndAtomIdx())

    if not alkene_bonds:
        return False, "No alkene bonds found"

    # Check if any alkene is adjacent to an amide
    for alkene_idx in alkene_bonds:
        alkene_atom = mol.GetAtomWithIdx(alkene_idx)
        for neighbor in alkene_atom.GetNeighbors():
            if neighbor.GetIdx() in amide_bonds:
                return True, "Molecule is an acrylamide"

    return False, "Molecule is not an acrylamide"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22216',
                          'name': 'acrylamides',
                          'definition': 'An enamide which is acrylamide or a '
                                        'derivative of acrylamide obtained by '
                                        'replacement of one or more of its '
                                        'hydrogens.',
                          'parents': ['CHEBI:51751']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: type object 'BondType' has no attribute "
               "'AMIDE'",
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 100,
    'num_true_negatives': 686,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 1.0,
    'f1': 0.0196078431372549,
    'accuracy': 0.8729351969504447}