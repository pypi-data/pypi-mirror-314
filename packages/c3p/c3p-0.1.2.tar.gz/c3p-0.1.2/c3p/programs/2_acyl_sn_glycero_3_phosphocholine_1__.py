"""
Classifies: CHEBI:16728 2-acyl-sn-glycero-3-phosphocholine(1+)
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_2_acyl_sn_glycero_3_phosphocholine_1__(smiles: str):
    """
    Determines if a molecule is a 2-acyl-sn-glycero-3-phosphocholine(1+).
    A 2-acylglycerophosphocholine in which the glycerol moiety has sn stereochemistry and
    which has an unspecified acyl group attached at the 2-position.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a 2-acyl-sn-glycero-3-phosphocholine(1+), False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for phosphocholine moiety
    phosphocholine_present = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'P' and atom.GetDegree() == 4:
            neighbors = [mol.GetAtomWithIdx(n.GetIdx()).GetSymbol() for n in atom.GetNeighbors()]
            if 'O' in neighbors and 'N' in neighbors and 'C' in neighbors:
                phosphocholine_present = True
                break

    if not phosphocholine_present:
        return False, "Phosphocholine moiety not found"

    # Check for glycerol moiety with sn stereochemistry
    sn_glycerol_present = False
    for bond in mol.GetBonds():
        if bond.GetBondType() == Chem.BondType.SINGLE and bond.GetIsAcyclic():
            atom1 = mol.GetAtomWithIdx(bond.GetBeginAtomIdx())
            atom2 = mol.GetAtomWithIdx(bond.GetEndAtomIdx())
            if (atom1.GetSymbol() == 'C' and atom2.GetSymbol() == 'C' and
                    atom1.GetDegree() == 4 and atom2.GetDegree() == 4):
                for neighbor1 in atom1.GetNeighbors():
                    if neighbor1.GetSymbol() == 'O':
                        for neighbor2 in atom2.GetNeighbors():
                            if neighbor2.GetSymbol() == 'O':
                                sn_glycerol_present = True
                                break
                if sn_glycerol_present:
                    break

    if not sn_glycerol_present:
        return False, "sn-glycerol moiety not found"

    # Check for acyl group at the 2-position
    acyl_present = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C' and atom.GetDegree() == 3 and atom.GetTotalNumHs() == 0:
            neighbors = [mol.GetAtomWithIdx(n.GetIdx()).GetSymbol() for n in atom.GetNeighbors()]
            if 'C' in neighbors and 'O' in neighbors and 'O' in neighbors:
                acyl_present = True
                break

    if not acyl_present:
        return False, "Acyl group at the 2-position not found"

    return True, "Molecule is a 2-acyl-sn-glycero-3-phosphocholine(1+)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:16728',
                          'name': '2-acyl-sn-glycero-3-phosphocholine(1+)',
                          'definition': 'A  2-acylglycerophosphocholine in '
                                        'which the glycerol moiety has sn '
                                        'stereochemistry and which has an '
                                        'unspecified acyl group attached at '
                                        'the 2-position.',
                          'parents': ['CHEBI:11502']},
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
    'error': "'Bond' object has no attribute 'GetIsAcyclic'",
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