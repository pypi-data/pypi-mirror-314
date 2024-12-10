"""
Classifies: CHEBI:197511 docosanol
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_docosanol(smiles: str):
    """
    Determines if a molecule is a docosanol (a fatty alcohol with an unbranched saturated chain of twenty-two carbon atoms and a hydroxy group).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a docosanol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule has 22 carbon atoms
    if Descriptors.HeavyAtomCount(mol) != 23:
        return False, "Molecule does not contain 22 carbon atoms"

    # Check if the molecule is linear (unbranched)
    if not rdMolDescriptors.GetDescriptorValue(mol, 'Chi0V') == 0:
        return False, "Molecule is branched"

    # Check if the molecule is saturated
    if not Descriptors.MolToSaturationCode(mol) == 'saturated':
        return False, "Molecule is unsaturated"

    # Check if the molecule has exactly one hydroxyl group
    if not Descriptors.CountFunctionalGroups(mol, 'Alcohol') == 1:
        return False, "Molecule does not have exactly one hydroxyl group"

    return True, "Molecule is a docosanol"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:197511',
                          'name': 'docosanol',
                          'definition': 'A fatty alcohol consisting of a '
                                        'hydroxy function at any position of '
                                        'an unbranched saturated chain of '
                                        'twenty-two carbon atoms.',
                          'parents': [   'CHEBI:134179',
                                         'CHEBI:50584',
                                         'CHEBI:78140']},
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
    'error': "module 'rdkit.Chem.rdMolDescriptors' has no attribute "
             "'GetDescriptorValue'",
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