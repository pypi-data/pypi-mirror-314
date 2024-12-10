"""
Classifies: CHEBI:138730 3'-methoxyflavones
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_3_methoxyflavones(smiles: str):
    """
    Determines if a molecule is a 3'-methoxyflavone (a methoxyflavone with a methoxy substituent at position 3').

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a 3'-methoxyflavone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if it is a flavone
    ring_info = mol.GetRingInfo()
    aromatic_rings = [ring for ring in ring_info.AtomRings() if all(mol.GetAtomWithIdx(idx).GetIsAromatic() for idx in ring)]
    if len(aromatic_rings) != 3 or not all(len(ring) in [5, 6] for ring in aromatic_rings):
        return False, "Not a flavone structure"

    # Check for methoxy group at position 3'
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O' and atom.GetDegree() == 2:
            neighbor_1 = atom.GetNeighbors()[0]
            neighbor_2 = atom.GetNeighbors()[1]
            if neighbor_1.GetSymbol() == 'C' and neighbor_2.GetSymbol() == 'C' and neighbor_1.GetDegree() == 3 and neighbor_2.GetDegree() == 3:
                if neighbor_1.GetIsAromatic() and neighbor_2.GetIsAromatic():
                    for bond in neighbor_1.GetBonds():
                        if bond.GetBondType() == Chem.BondType.SINGLE and bond.GetOtherAtom(neighbor_1).GetSymbol() == 'C':
                            methoxy_carbon = bond.GetOtherAtom(neighbor_1)
                            if len(methoxy_carbon.GetNeighbors()) == 2 and methoxy_carbon.GetDegree() == 2 and methoxy_carbon.GetIsAromatic():
                                ring = ring_info.IsBondInRingOfSize(bond.GetIdx(), 6)
                                if ring:
                                    return True, "3'-methoxyflavone structure found"

    return False, "Not a 3'-methoxyflavone structure"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:138730',
                          'name': "3'-methoxyflavones",
                          'definition': 'Any methoxyflavone with a methoxy '
                                        "substituent at position 3'.",
                          'parents': ['CHEBI:25241']},
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
    'error': "name 'is_3__methoxyflavones' is not defined",
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