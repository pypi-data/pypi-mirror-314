"""
Classifies: CHEBI:30527 flavin
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_flavin(smiles: str):
    """
    Determines if a molecule is a flavin (a derivative of the dimethylisoalloxazine skeleton with a substituent on the 10 position).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a flavin, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule has the dimethylisoalloxazine core
    core_smarts = '[#7]1([#6]2=[#6](-[#6](-[#6](-[#6]2-[#6](-[#6](-[#6]1-[#6](=O)-[#7]-[#6](=O)-[#7]-[#6](-[#6])[#6])[#6])[#6])[#6])[#6])[#6])[#6]'
    core_match = mol.GetSubstructMatches(Chem.MolFromSmarts(core_smarts))
    if not core_match:
        return False, "Molecule does not contain the dimethylisoalloxazine core"

    # Check for a substituent on the 10 position
    dim_atom_idx = core_match[0][0]
    dim_atom = mol.GetAtomWithIdx(dim_atom_idx)
    if len(dim_atom.GetNeighbors()) == 3:
        return True, "Molecule is a flavin derivative"

    return False, "No substituent found on the 10 position"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:30527',
                          'name': 'flavin',
                          'definition': 'A derivative of the '
                                        'dimethylisoalloxazine '
                                        '(7,8-dimethylbenzo[g]pteridine-2,4(3H,10H)-dione) '
                                        'skeleton, with a substituent on the '
                                        '10 position.',
                          'parents': ['CHEBI:38925']},
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
    'num_true_negatives': 183904,
    'num_false_negatives': 3,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999836874072221}