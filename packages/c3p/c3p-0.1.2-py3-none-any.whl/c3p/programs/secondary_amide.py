"""
Classifies: CHEBI:33257 secondary amide
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors

def is_secondary_amide(smiles: str):
    """
    Determines if a molecule is a secondary amide, defined as a derivative of two oxoacids RkE(=O)l(OH)m (l =/= 0)
    in which two acyl groups are attached to the amino or substituted amino group.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a secondary amide, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find all amide bonds
    amide_bonds = []
    for bond in mol.GetBonds():
        begin_atom = mol.GetAtomWithIdx(bond.GetBeginAtomIdx())
        end_atom = mol.GetAtomWithIdx(bond.GetEndAtomIdx())
        if begin_atom.GetAtomicNum() == 7 and end_atom.GetAtomicNum() == 8:
            amide_bonds.append(bond)

    # Check if there are at least two amide bonds
    if len(amide_bonds) < 2:
        return False, "Less than two amide bonds found"

    # Check if the amide bonds are attached to the same nitrogen atom
    nitrogen_atoms = []
    for bond in amide_bonds:
        begin_atom = mol.GetAtomWithIdx(bond.GetBeginAtomIdx())
        end_atom = mol.GetAtomWithIdx(bond.GetEndAtomIdx())
        if begin_atom.GetAtomicNum() == 7:
            nitrogen_atoms.append(begin_atom)
        else:
            nitrogen_atoms.append(end_atom)

    if len(set(nitrogen_atoms)) != 1:
        return False, "Amide bonds are not attached to the same nitrogen atom"

    # Check if the nitrogen atom has at least one hydrogen atom
    hydrogen_count = sum(1 for atom in nitrogen_atoms[0].GetNeighbors() if atom.GetAtomicNum() == 1)
    if hydrogen_count == 0:
        return False, "Nitrogen atom does not have any hydrogen atoms"

    # Check if the acyl groups are attached to the nitrogen atom
    acyl_groups = []
    for bond in amide_bonds:
        begin_atom = mol.GetAtomWithIdx(bond.GetBeginAtomIdx())
        end_atom = mol.GetAtomWithIdx(bond.GetEndAtomIdx())
        if begin_atom.GetAtomicNum() == 8:
            acyl_groups.append(begin_atom)
        else:
            acyl_groups.append(end_atom)

    if len(acyl_groups) != 2:
        return False, "Incorrect number of acyl groups found"

    return True, "Molecule is a secondary amide"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33257',
                          'name': 'secondary amide',
                          'definition': 'A derivative of two oxoacids '
                                        'RkE(=O)l(OH)m (l =/= 0) in which two '
                                        'acyl groups are attached to the amino '
                                        'or substituted amino group.',
                          'parents': ['CHEBI:32988']},
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
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 183678,
    'num_false_negatives': 25,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.999863910769013}