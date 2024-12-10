"""
Classifies: CHEBI:137348 dihydroxydocosahexaenoic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_dihydroxydocosahexaenoic_acid(smiles: str):
    """
    Determines if a molecule is a dihydroxydocosahexaenoic acid.

    A docosanoid that consists of any docosahexaenoic acid carrying two hydroxy substituents
    at unspecified positions.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a dihydroxydocosahexaenoic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule has 22 carbon atoms
    if Descriptors.HeavyAtomCount(mol) != 24:
        return False, "Molecule does not have 22 carbon atoms"

    # Check if the molecule has 6 double bonds
    if Descriptors.NumHeteroatomicDoubleBonds(mol) != 6:
        return False, "Molecule does not have 6 double bonds"

    # Check if the molecule has 2 hydroxy groups
    if Descriptors.NHOHCount(mol) != 2:
        return False, "Molecule does not have 2 hydroxy groups"

    # Check if the molecule has a carboxylic acid group
    if Descriptors.NHOHCount(mol) != 1:
        return False, "Molecule does not have a carboxylic acid group"

    return True, "Molecule is a dihydroxydocosahexaenoic acid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:137348',
                          'name': 'dihydroxydocosahexaenoic acid',
                          'definition': 'A docosanoid that consists of any '
                                        'docosahexaenoic acid carrying two '
                                        'hydroxy substituents at unspecified '
                                        'positions.',
                          'parents': [   'CHEBI:131863',
                                         'CHEBI:140345',
                                         'CHEBI:35972']},
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
    'error': "module 'rdkit.Chem.Descriptors' has no attribute "
             "'NumHeteroatomicDoubleBonds'",
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