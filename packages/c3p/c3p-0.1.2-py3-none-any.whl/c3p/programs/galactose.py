"""
Classifies: CHEBI:28260 galactose
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_galactose(smiles: str):
    """
    Determines if a molecule is galactose (an aldohexose that is the C-4 epimer of glucose).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is galactose, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule has 6 carbons and an aldehyde group
    if mol.GetRingInfo().NumRings() == 1 and mol.HasSubstructMatch(Chem.MolFromSmarts('[C@H]1[C@H]([C@@H]([C@@H]([C@@H]([C@@H]1O)O)O)O)O')):
        # Check if the molecule is the C-4 epimer of glucose
        glucose = Chem.MolFromSmiles('OC[C@H]1O[C@@H](O)[C@H](O)[C@@H](O)[C@@H]1O')
        if mol.HasSubstructMatch(AllChem.MolFromSmarts('OC[C@@H]1O[C@H](O)[C@H](O)[C@@H](O)[C@@H]1O')):
            return True, "This is alpha-L-galactose, an aldohexose that is the C-4 epimer of glucose"
        elif mol.HasSubstructMatch(AllChem.MolFromSmarts('OC[C@H]1O[C@@H](O)[C@@H](O)[C@@H](O)[C@@H]1O')):
            return True, "This is beta-L-galactose, an aldohexose that is the C-4 epimer of glucose"
        else:
            return False, "This molecule is an aldohexose but not the C-4 epimer of glucose"
    else:
        return False, "This molecule is not an aldohexose"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:28260',
                          'name': 'galactose',
                          'definition': 'An aldohexose that is the C-4 epimer '
                                        'of glucose.',
                          'parents': ['CHEBI:33917']},
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
    'num_true_negatives': 183921,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.999994562912539}