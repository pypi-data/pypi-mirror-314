"""
Classifies: CHEBI:228171 pentacosanol
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors

def is_pentacosanol(smiles: str):
    """
    Determines if a molecule is a pentacosanol (a fatty alcohol with an unbranched saturated chain of twenty-five carbon atoms and a hydroxy function at any position).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a pentacosanol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for 25 carbon atoms
    num_carbons = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if num_carbons != 25:
        return False, "Number of carbon atoms is not 25"

    # Check for a single hydroxy group
    num_oxygens = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O')
    if num_oxygens != 1:
        return False, "There is not exactly one hydroxy group"

    # Check that the carbon chain is unbranched and saturated
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C':
            if atom.GetDegree() > 4:
                return False, "Carbon chain is branched"
            if atom.GetHybridization() != Chem.HybridizationType.SP3:
                return False, "Carbon chain is unsaturated"

    return True, "The molecule is a pentacosanol"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:228171',
                          'name': 'pentacosanol',
                          'definition': 'A fatty alcohol consisting of a '
                                        'hydroxy function at any position of '
                                        'an unbranched saturated chain of '
                                        'twenty-five carbon atoms.',
                          'parents': [   'CHEBI:134179',
                                         'CHEBI:228172',
                                         'CHEBI:50584']},
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
    'num_false_positives': 5,
    'num_true_negatives': 183917,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.16666666666666666,
    'recall': 1.0,
    'f1': 0.2857142857142857,
    'accuracy': 0.9999728147105038}