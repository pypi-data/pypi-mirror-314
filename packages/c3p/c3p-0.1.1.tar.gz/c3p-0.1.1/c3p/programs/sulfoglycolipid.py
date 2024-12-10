"""
Classifies: CHEBI:26829 sulfoglycolipid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_sulfoglycolipid(smiles: str):
    """
    Determines if a molecule is a sulfoglycolipid (a sulfate ester of a glycolipid).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a sulfoglycolipid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for presence of sulfate group
    has_sulfate = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'S' and atom.GetTotalDegree() == 4:
            neighbors = [mol.GetAtomWithIdx(n.GetIdx()).GetAtomicNum() for n in atom.GetNeighbors()]
            if sum(n == 8 for n in neighbors) == 4:
                has_sulfate = True
                break
    if not has_sulfate:
        return False, "No sulfate group found"

    # Check for presence of glycolipid
    glycosidic_bonds = []
    for bond in mol.GetBonds():
        if bond.GetBondType() == Chem.BondType.SINGLE:
            atom1 = bond.GetBeginAtom()
            atom2 = bond.GetEndAtom()
            if atom1.GetSymbol() == 'O' and atom2.GetSymbol() == 'C':
                glycosidic_bonds.append(bond)
            elif atom2.GetSymbol() == 'O' and atom1.GetSymbol() == 'C':
                glycosidic_bonds.append(bond)
    if not glycosidic_bonds:
        return False, "No glycosidic bonds found"

    # Check if sulfate group is attached to glycolipid
    for bond in glycosidic_bonds:
        atom1, atom2 = bond.GetBeginAtom(), bond.GetEndAtom()
        for neighbor in atom1.GetNeighbors() + atom2.GetNeighbors():
            if neighbor.GetSymbol() == 'S' and neighbor.GetTotalDegree() == 4:
                neighbors = [mol.GetAtomWithIdx(n.GetIdx()).GetAtomicNum() for n in neighbor.GetNeighbors()]
                if sum(n == 8 for n in neighbors) == 4:
                    return True, "Sulfate ester of a glycolipid"

    return False, "Sulfate group not attached to glycolipid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26829',
                          'name': 'sulfoglycolipid',
                          'definition': 'A sulfate ester of a glycolipid.',
                          'parents': [   'CHEBI:33563',
                                         'CHEBI:35724',
                                         'CHEBI:61384']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': 'Attempt failed: Python argument types in\n'
               '    Mol.GetAtomWithIdx(Mol, Atom)\n'
               'did not match C++ signature:\n'
               '    GetAtomWithIdx(RDKit::ROMol {lvalue} self, unsigned int '
               'idx)',
    'attempt': 4,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 4,
    'num_false_positives': 100,
    'num_true_negatives': 8561,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.038461538461538464,
    'recall': 1.0,
    'f1': 0.07407407407407407,
    'accuracy': 0.9884593190998269}