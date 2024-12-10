"""
Classifies: CHEBI:33271 aldimine
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_aldimine(smiles: str):
    """
    Determines if a molecule is an aldimine (imines derived from aldehydes, i.e. compounds having the structure RCH=NR).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an aldimine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find all imine bonds
    imine_bonds = []
    for bond in mol.GetBonds():
        if bond.GetBondType() == Chem.BondType.DOUBLE:
            begin_atom = bond.GetBeginAtom()
            end_atom = bond.GetEndAtom()
            if (begin_atom.GetSymbol() == 'N' and end_atom.GetSymbol() == 'C') or \
               (begin_atom.GetSymbol() == 'C' and end_atom.GetSymbol() == 'N'):
                imine_bonds.append(bond)

    if not imine_bonds:
        return False, "No imine bonds found"

    # Check if the imine bond is connected to an aldehyde group
    for bond in imine_bonds:
        c_atom = bond.GetBeginAtom() if bond.GetBeginAtom().GetSymbol() == 'C' else bond.GetEndAtom()
        if c_atom.GetTotalNumHs() == 1:
            n_atom = bond.GetBeginAtom() if bond.GetBeginAtom().GetSymbol() == 'N' else bond.GetEndAtom()
            if all(neighbor.GetAtomicNum() != 1 for neighbor in n_atom.GetNeighbors()):
                return True, "Molecule is an aldimine"

    return False, "Imine bond is not connected to an aldehyde group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33271',
                          'name': 'aldimine',
                          'definition': 'Imines derived from aldehydes, i.e. '
                                        'compounds having the structure '
                                        'RCH=NR.',
                          'parents': ['CHEBI:24783']},
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
               'False positives: []\n'
               "False negatives: [('OC(C(O)C(NC(=O)C)C=N)C(O)CO', 'Imine bond "
               "is not connected to an aldehyde group')]",
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 100,
    'num_true_negatives': 13682,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 1.0,
    'f1': 0.0196078431372549,
    'accuracy': 0.9927446854821157}