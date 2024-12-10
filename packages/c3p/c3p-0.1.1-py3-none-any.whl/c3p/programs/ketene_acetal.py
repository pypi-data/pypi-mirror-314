"""
Classifies: CHEBI:145408 ketene acetal
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_ketene_acetal(smiles: str):
    """
    Determines if a molecule is a ketene acetal (RR'C=C(OR'')(OR''') where R'', R''' != H).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a ketene acetal, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find all double bonds
    double_bonds = [bond for bond in mol.GetBonds() if bond.GetBondType() == Chem.BondType.DOUBLE]

    # Check for at least one double bond
    if not double_bonds:
        return False, "No double bonds found"

    for bond in double_bonds:
        atom1 = bond.GetBeginAtom()
        atom2 = bond.GetEndAtom()

        # Check for carbon atoms on both ends of the double bond
        if atom1.GetSymbol() != 'C' or atom2.GetSymbol() != 'C':
            continue

        # Check for at least one alkoxy group (RO-) on each carbon
        alkoxy_groups_atom1 = 0
        alkoxy_groups_atom2 = 0
        for neighbor in atom1.GetNeighbors():
            if neighbor.GetSymbol() == 'O' and neighbor.GetTotalNumHs() == 0:
                alkoxy_groups_atom1 += 1
        for neighbor in atom2.GetNeighbors():
            if neighbor.GetSymbol() == 'O' and neighbor.GetTotalNumHs() == 0:
                alkoxy_groups_atom2 += 1

        if alkoxy_groups_atom1 >= 1 and alkoxy_groups_atom2 >= 1:
            return True, "Molecule is a ketene acetal"

    return False, "Molecule is not a ketene acetal"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:145408',
                          'name': 'ketene acetal',
                          'definition': 'An organooxygen compound having the '
                                        "structure RR'C=C(OR'')(OR''') where "
                                        "R'', R''' =/= H. Formally, they are "
                                        'ethers of the enolic form of esters. '
                                        'They bear the same structural '
                                        'relationship to ketenes that acetals '
                                        'bear to aldehydes and ketones.',
                          'parents': ['CHEBI:36963']},
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
    'num_false_positives': 100,
    'num_true_negatives': 157964,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9993610223642172}