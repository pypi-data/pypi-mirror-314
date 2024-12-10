"""
Classifies: CHEBI:12777 vitamin A
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_vitamin_A(smiles: str):
    """
    Determines if a molecule is a vitamin A compound.

    A vitamin A compound is defined as any member of a group of fat-soluble retinoids
    produced via metabolism of provitamin A carotenoids that exhibit biological activity
    against vitamin A deficiency. Vitamin A is involved in immune function, vision,
    reproduction, and cellular communication.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a vitamin A compound, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of the retinoid backbone
    pattern = Chem.MolFromSmarts('[C@@H](C=C[C@H](C)C=C[C@H](C)C=C[C@@H](C)C=C[C@@H](C)C=C[C@@H](C)C=C[C@@H](C)C=C[C@@H](C)C=C[C@@H](C)C=O)')
    if not mol.HasSubstructMatch(pattern):
        return False, "Molecule does not contain the retinoid backbone"

    # Check for the presence of a carboxylic acid group
    pattern = Chem.MolFromSmarts('C(=O)O')
    if not mol.HasSubstructMatch(pattern):
        return False, "Molecule does not contain a carboxylic acid group"

    return True, "Molecule is a vitamin A compound"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:12777',
                          'name': 'vitamin A',
                          'definition': 'Any member of a group of fat-soluble '
                                        'retinoids produced via metabolism of '
                                        'provitamin A carotenoids that exhibit '
                                        'biological activity against vitamin A '
                                        'deficiency. Vitamin A is involved in '
                                        'immune function, vision, '
                                        'reproduction, and cellular '
                                        'communication.',
                          'parents': ['CHEBI:26537']},
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
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 183924,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999945630012234}