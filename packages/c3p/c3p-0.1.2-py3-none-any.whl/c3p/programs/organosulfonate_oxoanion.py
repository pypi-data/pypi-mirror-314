"""
Classifies: CHEBI:33554 organosulfonate oxoanion
"""
from rdkit import Chem

def is_organosulfonate_oxoanion(smiles: str):
    """
    Determines if a molecule is an organosulfonate oxoanion.

    An organosulfonate oxoanion is an organic anion obtained by deprotonation
    of the sulfonate group(s) of any organosulfonic acid.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is an organosulfonate oxoanion, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains at least one sulfonate group
    sulfonate_groups = []
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'S':
            neighbors = atom.GetNeighbors()
            if len(neighbors) == 4:
                for neighbor in neighbors:
                    if neighbor.GetSymbol() == 'O':
                        sulfonate_groups.append(neighbor.GetIdx())

    if not sulfonate_groups:
        return False, "No sulfonate groups found"

    # Check if at least one sulfonate group is deprotonated (negatively charged)
    deprotonated_sulfonate = False
    for idx in sulfonate_groups:
        atom = mol.GetAtomWithIdx(idx)
        if atom.GetFormalCharge() == -1:
            deprotonated_sulfonate = True
            break

    if not deprotonated_sulfonate:
        return False, "No deprotonated sulfonate groups found"

    # Check if the molecule is organic (contains at least one carbon atom)
    organic = any(atom.GetSymbol() == 'C' for atom in mol.GetAtoms())
    if not organic:
        return False, "Molecule does not contain any carbon atoms"

    return True, "Molecule is an organosulfonate oxoanion"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33554',
                          'name': 'organosulfonate oxoanion',
                          'definition': 'An organic anion obtained by '
                                        'deprotonation of the sufonate '
                                        'group(s) of any organosulfonic acid.',
                          'parents': ['CHEBI:25696']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.0,
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
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 22,
    'num_false_positives': 100,
    'num_true_negatives': 23824,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.18032786885245902,
    'recall': 1.0,
    'f1': 0.3055555555555556,
    'accuracy': 0.9958239371920153}