"""
Classifies: CHEBI:16110 1,2-diacyl-sn-glycero-3-phosphocholine(1+)
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_1_2_diacyl_sn_glycero_3_phosphocholine_1__(smiles: str):
    """
    Determines if a molecule is a 1,2-diacyl-sn-glycero-3-phosphocholine(1+).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a 1,2-diacyl-sn-glycero-3-phosphocholine(1+), False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of a phosphorus atom
    p_atom = None
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'P':
            p_atom = atom
            break
    if p_atom is None:
        return False, "No phosphorus atom found"

    # Check for the presence of a choline group
    choline_group = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'N' and atom.GetFormalCharge() == 1:
            choline_group = True
            break
    if not choline_group:
        return False, "No choline group found"

    # Check for the presence of two acyl chains
    acyl_chains = 0
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C' and atom.GetDegree() == 1 and atom.GetIsAromatic() is False:
            env = Chem.FindAtomEnvironmentOfRadiusN(mol, 4, atom.GetIdx())
            if 'O=C' in ''.join([mol.GetAtomWithIdx(i).GetSymbol() for i in env]):
                acyl_chains += 1
    if acyl_chains != 2:
        return False, f"Found {acyl_chains} acyl chains instead of 2"

    # Check for the glycerol backbone
    glycerol_backbone = False
    for bond in mol.GetBonds():
        atom1 = mol.GetAtomWithIdx(bond.GetBeginAtomIdx())
        atom2 = mol.GetAtomWithIdx(bond.GetEndAtomIdx())
        if atom1.GetSymbol() == 'O' and atom2.GetSymbol() == 'P':
            glycerol_backbone = True
            break
    if not glycerol_backbone:
        return False, "No glycerol backbone found"

    return True, "This molecule is a 1,2-diacyl-sn-glycero-3-phosphocholine(1+)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:16110',
                          'name': '1,2-diacyl-sn-glycero-3-phosphocholine(1+)',
                          'definition': 'A phosphatidylcholine that is a '
                                        'glycerol phosphatide '
                                        '(phosphoglyceride, '
                                        'glycerophospholipid) in which the '
                                        'hydroxy group of choline is '
                                        'esterified with the phosphate group '
                                        'of phosphatidic acid.',
                          'parents': ['CHEBI:49183']},
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
    'error': 'Range Error\n'
             '\tidx\n'
             '\tViolation occurred on line 209 in file '
             'Code/GraphMol/ROMol.cpp\n'
             '\tFailed Expression: 22 < 22\n'
             '\tRDKIT: 2024.03.6\n'
             '\tBOOST: 1_85\n',
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