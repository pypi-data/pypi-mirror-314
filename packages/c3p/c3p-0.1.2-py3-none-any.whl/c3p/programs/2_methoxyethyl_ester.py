"""
Classifies: CHEBI:136838 2-methoxyethyl ester
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors

def is_2_methoxyethyl_ester(smiles: str):
    """
    Determines if a molecule is a 2-methoxyethyl ester.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a 2-methoxyethyl ester, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find all ester bonds
    ester_bonds = []
    for bond in mol.GetBonds():
        if bond.GetBondType() == Chem.BondType.ESTERS:
            ester_bonds.append(bond)

    if not ester_bonds:
        return False, "No ester bonds found"

    # Check if the ester is a 2-methoxyethyl ester
    for bond in ester_bonds:
        atom1 = mol.GetAtomWithIdx(bond.GetBeginAtomIdx())
        atom2 = mol.GetAtomWithIdx(bond.GetEndAtomIdx())

        # Check if one of the atoms is an oxygen
        if atom1.GetSymbol() == 'O':
            ester_oxygen = atom1
            ester_carbon = atom2
        elif atom2.GetSymbol() == 'O':
            ester_oxygen = atom2
            ester_carbon = atom1
        else:
            continue

        # Check if the carbon atom is connected to a methoxyethyl group
        methoxyethyl_found = False
        for neighbor in ester_carbon.GetNeighbors():
            if neighbor.GetSymbol() == 'C':
                neighbor_neighbors = [mol.GetAtomWithIdx(idx) for idx in neighbor.GetNeighborIds()]
                if any(atom.GetSymbol() == 'O' and len(atom.GetNeighbors()) == 2 for atom in neighbor_neighbors):
                    methoxyethyl_found = True
                    break

        if methoxyethyl_found:
            return True, "The molecule is a 2-methoxyethyl ester"

    return False, "The molecule is not a 2-methoxyethyl ester"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:136838',
                          'name': '2-methoxyethyl ester',
                          'definition': 'A carboxylic ester resulting from the '
                                        'formal condensation between a '
                                        'carboxylic acid and the hydroxy group '
                                        'of 2-methoxyethanol. In contrast to '
                                        'many other water-solubilising esters, '
                                        'the 2-methoxyethyl esters of many '
                                        'amino acids are crystalline, allowing '
                                        'them to be easily purified.',
                          'parents': ['CHEBI:25698', 'CHEBI:33308']},
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
    'error': "type object 'BondType' has no attribute 'ESTERS'",
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