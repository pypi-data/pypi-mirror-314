"""
Classifies: CHEBI:27207 univalent carboacyl group
"""
from rdkit import Chem

def is_univalent_carboacyl_group(smiles: str):
    """
    Determines if a molecule is a univalent carboacyl group.

    A univalent carboacyl group is a group formed by loss of OH from the carboxy group of a carboxylic acid.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a univalent carboacyl group, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find the carbonyl carbon atom
    carbonyl_carbon = None
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C' and atom.GetTotalNumHs() == 0 and atom.GetFormalCharge() == 0 and atom.GetTotalDegree() == 3:
            neighbors = [mol.GetAtomWithIdx(nbr_idx).GetSymbol() for nbr_idx in atom.GetNeighbors()]
            if 'O' in neighbors and 'O' in neighbors:
                carbonyl_carbon = atom
                break

    if carbonyl_carbon is None:
        return False, "No carbonyl carbon found"

    # Check if the carbonyl carbon is connected to an asterisk (*)
    asterisk_neighbor = None
    for nbr_idx in carbonyl_carbon.GetNeighbors():
        atom = mol.GetAtomWithIdx(nbr_idx)
        if atom.GetSymbol() == '*':
            asterisk_neighbor = atom
            break

    if asterisk_neighbor is None:
        return False, "Carbonyl carbon is not connected to an asterisk (*)"

    return True, "Molecule is a univalent carboacyl group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:27207',
                          'name': 'univalent carboacyl group',
                          'definition': 'A univalent carboacyl group is a '
                                        'group formed by loss of OH from the '
                                        'carboxy group of a carboxylic acid.',
                          'parents': ['CHEBI:37838']},
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
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': None}