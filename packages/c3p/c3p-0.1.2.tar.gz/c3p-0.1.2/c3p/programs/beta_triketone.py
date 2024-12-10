"""
Classifies: CHEBI:140323 beta-triketone
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_beta_triketone(smiles: str):
    """
    Determines if a molecule is a beta-triketone.

    A beta-triketone is a triketone in which each ketone functionality
    is located beta- to the other two.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a beta-triketone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find all carbonyl groups
    carbonyls = []
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C' and atom.GetTotalNumHs() == 0:
            neighbors = [mol.GetAtomWithIdx(n).GetSymbol() for n in atom.GetNeighbors()]
            if 'O' in neighbors and len([x for x in neighbors if x != 'O']) == 2:
                carbonyls.append(atom.GetIdx())

    # Check if there are exactly three carbonyl groups
    if len(carbonyls) != 3:
        return False, "The molecule does not contain exactly three carbonyl groups"

    # Check if each carbonyl group is beta to the other two
    for i in range(len(carbonyls)):
        c1 = mol.GetAtomWithIdx(carbonyls[i])
        for j in range(i + 1, len(carbonyls)):
            c2 = mol.GetAtomWithIdx(carbonyls[j])
            if not AllChem.PathExistsBetweenAtoms(mol, c1.GetIdx(), c2.GetIdx(), 4):
                return False, "The carbonyl groups are not all beta to each other"

    return True, "The molecule is a beta-triketone"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:140323',
                          'name': 'beta-triketone',
                          'definition': 'A triketone in which the each ketone '
                                        'functionality is located beta- to the '
                                        'other two.',
                          'parents': ['CHEBI:140322']},
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