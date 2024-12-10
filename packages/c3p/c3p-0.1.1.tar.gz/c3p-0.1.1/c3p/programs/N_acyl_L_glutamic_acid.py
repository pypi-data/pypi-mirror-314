"""
Classifies: CHEBI:21650 N-acyl-L-glutamic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_N_acyl_L_glutamic_acid(smiles: str):
    """
    Determines if a molecule is an N-acyl-L-glutamic acid (any optically active N-acylglutamic acid having L-configuration).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an N-acyl-L-glutamic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for amide functional group
    amide_atom_idx = None
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'N' and atom.GetDegree() == 3:
            neighbors = [mol.GetAtomWithIdx(n).GetSymbol() for n in atom.GetNeighbors()]
            if 'C' in neighbors and 'O' in neighbors:
                amide_atom_idx = atom.GetIdx()
                break
    if amide_atom_idx is None:
        return False, "No amide functional group found"

    # Check for glutamic acid backbone
    backbone_atoms = []
    for bond in mol.GetBonds():
        if bond.GetBondType() == Chem.BondType.SINGLE:
            atom1 = mol.GetAtomWithIdx(bond.GetBeginAtomIdx())
            atom2 = mol.GetAtomWithIdx(bond.GetEndAtomIdx())
            if atom1.GetSymbol() == 'C' and atom2.GetSymbol() == 'C':
                backbone_atoms.append(atom1.GetIdx())
                backbone_atoms.append(atom2.GetIdx())
    if len(backbone_atoms) != 4:
        return False, "Glutamic acid backbone not found"

    # Check for carboxyl groups
    carboxyl_count = 0
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C' and atom.GetDegree() == 3:
            neighbors = [mol.GetAtomWithIdx(n).GetSymbol() for n in atom.GetNeighbors()]
            if 'O' in neighbors and 'O' in neighbors:
                carboxyl_count += 1
    if carboxyl_count != 2:
        return False, "Two carboxyl groups not found"

    # Check for L-configuration
    chiral_centers = Chem.FindMolChiralCenters(mol)
    if len(chiral_centers) != 1:
        return False, "Single chiral center not found"
    chiral_atom_idx = chiral_centers[0][0]
    chiral_atom = mol.GetAtomWithIdx(chiral_atom_idx)
    if chiral_atom.GetProp('_ChiralityPossible') != 'Yes':
        return False, "Chiral center not optically active"
    if chiral_atom.GetProp('_CIPCode') != 'S':
        return False, "Chiral center not L-configuration"

    return True, "N-acyl-L-glutamic acid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:21650',
                          'name': 'N-acyl-L-glutamic acid',
                          'definition': 'Any optically active N-acylglutamic '
                                        'acid having L-configuration.',
                          'parents': [   'CHEBI:21658',
                                         'CHEBI:48927',
                                         'CHEBI:83982']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.0,
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
    'error': 'Python argument types in\n'
             '    Mol.GetAtomWithIdx(Mol, Atom)\n'
             'did not match C++ signature:\n'
             '    GetAtomWithIdx(RDKit::ROMol {lvalue} self, unsigned int idx)',
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0,
    'f1': 0,
    'accuracy': None}