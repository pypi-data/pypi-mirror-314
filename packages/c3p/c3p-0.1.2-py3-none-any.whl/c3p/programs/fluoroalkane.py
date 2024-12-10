"""
Classifies: CHEBI:24067 fluoroalkane
"""
from rdkit import Chem

def is_fluoroalkane(smiles: str):
    """
    Determines if a molecule is a fluoroalkane (an alkane with at least one hydrogen replaced by fluorine).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a fluoroalkane, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if molecule contains fluorine and carbon
    if not any(atom.GetSymbol() == 'F' for atom in mol.GetAtoms()):
        return False, "No fluorine atoms present"
    if not any(atom.GetSymbol() == 'C' for atom in mol.GetAtoms()):
        return False, "No carbon atoms present"

    # Check if molecule contains only C, H, and F
    allowed_atoms = ['C', 'H', 'F']
    if not all(atom.GetSymbol() in allowed_atoms for atom in mol.GetAtoms()):
        return False, "Molecule contains atoms other than C, H, and F"

    # Check if molecule is an alkane
    rings = mol.GetRingInfo().AtomRings()
    if rings:
        return False, "Molecule contains rings, not an alkane"

    # Check if molecule contains at least one C-F bond
    has_c_f_bond = False
    for bond in mol.GetBonds():
        atom1 = mol.GetAtomWithIdx(bond.GetBeginAtomIdx())
        atom2 = mol.GetAtomWithIdx(bond.GetEndAtomIdx())
        if (atom1.GetSymbol() == 'C' and atom2.GetSymbol() == 'F') or (atom1.GetSymbol() == 'F' and atom2.GetSymbol() == 'C'):
            has_c_f_bond = True
            break

    if has_c_f_bond:
        return True, "Molecule is a fluoroalkane"
    else:
        return False, "Molecule does not contain a C-F bond"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24067',
                          'name': 'fluoroalkane',
                          'definition': 'A haloalkane that is an alkane in '
                                        'which at least one hydrogen atom has '
                                        'been replaced by a fluorine atom.',
                          'parents': ['CHEBI:24469', 'CHEBI:37143']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: module 'rdkit.Chem.Descriptors' has no "
               "attribute 'MolFromSmiles'",
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 10,
    'num_true_negatives': 183912,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.09090909090909091,
    'recall': 1.0,
    'f1': 0.16666666666666669,
    'accuracy': 0.9999456294210077}