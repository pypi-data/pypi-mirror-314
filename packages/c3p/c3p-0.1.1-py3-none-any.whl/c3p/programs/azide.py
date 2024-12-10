"""
Classifies: CHEBI:22680 azide
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_azide(smiles: str):
    """
    Determines if a molecule contains an azide (-N3) group.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule contains an azide group, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of the azide group
    azide_pattern = Chem.MolFromSmarts('[N-]=[N+]=N')
    if mol.HasSubstructMatch(azide_pattern):
        return True, "Molecule contains an azide (-N3) group"
    else:
        return False, "Molecule does not contain an azide (-N3) group"

# Examples
print(is_azide('Oc1ccc(CC(=O)N=[N+]=[N-])cc1[N+]([O-])=O'))
# Output: (True, 'Molecule contains an azide (-N3) group')

print(is_azide('c1ccccc1'))
# Output: (False, 'Molecule does not contain an azide (-N3) group')


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22680',
                          'name': 'azide',
                          'definition': 'Any nitrogen molecular entity '
                                        'containing the group -N3.',
                          'parents': ['CHEBI:51143']},
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
    'num_true_positives': 1,
    'num_false_positives': 42,
    'num_true_negatives': 183874,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.023255813953488372,
    'recall': 1.0,
    'f1': 0.04545454545454545,
    'accuracy': 0.9997716361184665}