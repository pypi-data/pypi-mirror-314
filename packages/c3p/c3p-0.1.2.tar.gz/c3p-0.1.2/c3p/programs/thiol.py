"""
Classifies: CHEBI:29256 thiol
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_thiol(smiles: str):
    """
    Determines if a molecule is a thiol, i.e., an organosulfur compound with a thiol group (-SH)
    attached to a carbon atom of any aliphatic or aromatic moiety.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a thiol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find all sulfur atoms
    sulfur_atoms = [atom.GetIdx() for atom in mol.GetAtoms() if atom.GetSymbol() == 'S']

    # Check if any sulfur atom has a hydrogen attached
    thiol_groups = []
    for sulfur_idx in sulfur_atoms:
        sulfur_atom = mol.GetAtomWithIdx(sulfur_idx)
        for neighbor in sulfur_atom.GetNeighbors():
            if neighbor.GetSymbol() == 'H':
                thiol_groups.append(sulfur_idx)
                break

    if not thiol_groups:
        return False, "No thiol group (-SH) found"

    # Check if thiol group is attached to a carbon atom
    for thiol_idx in thiol_groups:
        thiol_atom = mol.GetAtomWithIdx(thiol_idx)
        is_attached_to_carbon = False
        for neighbor in thiol_atom.GetNeighbors():
            if neighbor.GetSymbol() == 'C':
                is_attached_to_carbon = True
                break
        if not is_attached_to_carbon:
            return False, "Thiol group not attached to a carbon atom"

    return True, "Molecule contains a thiol group (-SH) attached to a carbon atom"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:29256',
                          'name': 'thiol',
                          'definition': 'An organosulfur compound in which a '
                                        'thiol group, -SH, is attached to a '
                                        'carbon atom of any aliphatic or '
                                        'aromatic moiety.',
                          'parents': ['CHEBI:33261']},
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
    'num_true_negatives': 183807,
    'num_false_negatives': 12,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999347183914612}