"""
Classifies: CHEBI:156208 high-mannose N-glycan group
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_high_mannose_N_glycan_group(smiles: str):
    """
    Determines if a molecule is a high-mannose N-glycan group.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a high-mannose N-glycan group, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Count the number of N-acetyl-D-glucosamine residues
    n_glcnac = 0
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'N' and atom.GetFormalCharge() == 0:
            neighbors = [mol.GetAtomWithIdx(n).GetSymbol() for n in atom.GetNeighbors()]
            if 'C' in neighbors and 'C' in neighbors and 'O' in neighbors:
                n_glcnac += 1

    if n_glcnac != 2:
        return False, "Molecule does not contain exactly two N-acetyl-D-glucosamine residues"

    # Count the number of mannose residues
    n_mannose = 0
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O' and atom.GetFormalCharge() == 0:
            neighbors = [mol.GetAtomWithIdx(n).GetSymbol() for n in atom.GetNeighbors()]
            if 'C' in neighbors and 'C' in neighbors and 'C' in neighbors and 'C' in neighbors:
                n_mannose += 1

    if n_mannose < 3:
        return False, "Molecule does not contain at least three mannose residues"

    # Check for glycosidic bonds between mannose and N-acetyl-D-glucosamine
    glycosidic_bonds = []
    for bond in mol.GetBonds():
        if bond.GetBondType() == Chem.BondType.SINGLE:
            atom1 = mol.GetAtomWithIdx(bond.GetBeginAtomIdx())
            atom2 = mol.GetAtomWithIdx(bond.GetEndAtomIdx())
            if atom1.GetSymbol() == 'O' and atom2.GetSymbol() == 'C':
                glycosidic_bonds.append(bond)
            elif atom2.GetSymbol() == 'O' and atom1.GetSymbol() == 'C':
                glycosidic_bonds.append(bond)

    if len(glycosidic_bonds) < 3:
        return False, "Molecule does not contain at least three glycosidic bonds"

    return True, "Molecule is a high-mannose N-glycan group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:156208',
                          'name': 'high-mannose N-glycan group',
                          'definition': 'An N-acetyl-D-glucosaminyl group '
                                        'obtained formally by removal of the '
                                        'hydroxy group from the hemiacetal '
                                        'function of a high-mannose N-glycan.',
                          'parents': ['CHEBI:21524']},
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
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': None}