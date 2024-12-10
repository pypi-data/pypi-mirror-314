"""
Classifies: CHEBI:144315 1-radyl-2-acyl-sn-glycerolipid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_1_radyl_2_acyl_sn_glycerolipid(smiles: str):
    """
    Determines if a molecule is a 1-radyl-2-acyl-sn-glycerolipid, where R1 is an alkyl or an acyl group,
    R2 is an acyl chain, and R3 can be an H, a phosphate, or a phospholipid group.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a 1-radyl-2-acyl-sn-glycerolipid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find the glycerol backbone
    patterns = (
        Chem.MolFromSmarts("[C;H2;D2]([C;H1]([C])([C]))[C]"),  # sn-glycerol backbone
        Chem.MolFromSmarts("[C;H2;D2]([C;H1]([C])([C]))[O]"),  # sn-glycerol backbone
    )

    backbone = None
    for pattern in patterns:
        match = mol.GetSubstructMatches(pattern)
        if match:
            backbone = [mol.GetAtomWithIdx(idx) for idx in match[0]]
            break

    if not backbone:
        return False, "No glycerol backbone found"

    # Check the substituents
    r1, r2, r3 = None, None, None

    for atom in backbone:
        neighbors = atom.GetNeighbors()
        for neighbor in neighbors:
            if neighbor.GetIdx() not in [atom.GetIdx() for atom in backbone]:
                if r1 is None:
                    r1 = neighbor
                elif r2 is None:
                    r2 = neighbor
                else:
                    r3 = neighbor

    if r1 is None or r2 is None:
        return False, "Missing substituents on glycerol backbone"

    # Check R1 (alkyl or acyl)
    is_alkyl = Descriptors.GetSMARTSMatch(mol, Chem.MolFromSmarts("[C;H3]"))
    is_acyl = Descriptors.GetSMARTSMatch(mol, Chem.MolFromSmarts("[C](=O)[O]"))

    if not is_alkyl(r1) and not is_acyl(r1):
        return False, "R1 is neither an alkyl nor an acyl group"

    # Check R2 (acyl chain)
    if not is_acyl(r2):
        return False, "R2 is not an acyl chain"

    # Check R3 (H, phosphate, or phospholipid)
    if r3 is None:
        return True, "R3 is H"

    is_phosphate = Descriptors.GetSMARTSMatch(mol, Chem.MolFromSmarts("[P]([O-])([O-])[O-]"))
    is_phospholipid = Descriptors.GetSMARTSMatch(mol, Chem.MolFromSmarts("[P]([O-])([O-])[OC]"))

    if is_phosphate(r3):
        return True, "R3 is a phosphate group"
    elif is_phospholipid(r3):
        return True, "R3 is a phospholipid group"
    else:
        return False, "R3 is not H, a phosphate, or a phospholipid group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:144315',
                          'name': '1-radyl-2-acyl-sn-glycerolipid',
                          'definition': 'A glycerolipid where R1 is an alkyl '
                                        'or an acyl group, R2 is an acyl chain '
                                        'and R3 can be an H, a phosphate or a '
                                        'phospholipid group.',
                          'parents': [   'CHEBI:144368',
                                         'CHEBI:17815',
                                         'CHEBI:35741',
                                         'CHEBI:50860']},
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
    'error': "module 'rdkit.Chem.Descriptors' has no attribute "
             "'GetSMARTSMatch'",
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