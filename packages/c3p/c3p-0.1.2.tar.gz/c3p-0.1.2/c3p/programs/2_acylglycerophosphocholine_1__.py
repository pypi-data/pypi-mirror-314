"""
Classifies: CHEBI:11502 2-acylglycerophosphocholine(1+)
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_2_acylglycerophosphocholine_1__(smiles: str):
    """
    Determines if a molecule is a 2-acylglycerophosphocholine(1+) based on its SMILES string.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a 2-acylglycerophosphocholine(1+), False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of a phosphorus atom
    if mol.GetAtomWithAtomicNum(15) is None:
        return False, "No phosphorus atom found"

    # Check for the presence of a quaternary ammonium group
    quat_ammonium_found = False
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() == 7 and atom.GetTotalDegree() == 4 and atom.GetFormalCharge() == 1:
            quat_ammonium_found = True
            break
    if not quat_ammonium_found:
        return False, "No quaternary ammonium group found"

    # Check for the presence of an ester group
    ester_found = False
    for bond in mol.GetBonds():
        if bond.GetBondType() == Chem.BondType.DOUBLE and \
           bond.GetBeginAtom().GetAtomicNum() == 8 and \
           bond.GetEndAtom().GetAtomicNum() == 6:
            ester_found = True
            break
    if not ester_found:
        return False, "No ester group found"

    # Check for the presence of a glycerol backbone
    glycerol_atoms = []
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() == 8 and atom.GetTotalDegree() == 2:
            glycerol_atoms.append(atom)
    if len(glycerol_atoms) != 3:
        return False, "No glycerol backbone found"

    return True, "Molecule is a 2-acylglycerophosphocholine(1+)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:11502',
                          'name': '2-acylglycerophosphocholine(1+)',
                          'definition': 'A glycerophosphocholine having an '
                                        'unspecified acyl group attached at '
                                        'the 2-position.',
                          'parents': ['CHEBI:35267']},
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
    'error': "'Mol' object has no attribute 'GetAtomWithAtomicNum'",
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