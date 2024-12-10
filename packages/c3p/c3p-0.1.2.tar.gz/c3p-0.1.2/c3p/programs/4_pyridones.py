"""
Classifies: CHEBI:20485 4-pyridones
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_4_pyridones(smiles: str):
    """
    Determines if a molecule is a 4-pyridone or its derivative.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a 4-pyridone or its derivative, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains a pyridin-4-one substructure
    pyridin4one_smi = 'c1cc(=O)nc[nH]1'
    pyridin4one_query = Chem.MolFromSmarts(pyridin4one_smi)
    if mol.HasSubstructMatch(pyridin4one_query):
        return True, "The molecule contains a pyridin-4-one substructure"
    else:
        return False, "The molecule does not contain a pyridin-4-one substructure"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:20485',
                          'name': '4-pyridones',
                          'definition': 'Any pyridone that is pyridin-4-one or '
                                        'its derivatives by substitution of '
                                        'one of more of the hydrogens.',
                          'parents': ['CHEBI:38183']},
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
    'num_false_positives': 100,
    'num_true_negatives': 42187,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9976116155883465}