"""
Classifies: CHEBI:197468 nonadecanol
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors

def is_nonadecanol(smiles: str):
    """
    Determines if a molecule is a nonadecanol (a fatty alcohol consisting of a hydroxy function
    at any position of an unbranched saturated chain of nineteen carbon atoms).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a nonadecanol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for 19 carbon atoms
    if Descriptors.HeavyAtomCount(mol) != 20:
        return False, "Not a nonadecanol (incorrect number of atoms)"

    # Check for a single hydroxyl group
    if Descriptors.AlcoholCount(mol) != 1:
        return False, "Not a nonadecanol (incorrect number of hydroxyl groups)"

    # Check for a single unbranched chain
    if not is_unbranched_chain(mol):
        return False, "Not a nonadecanol (branched chain)"

    return True, "Nonadecanol"

def is_unbranched_chain(mol):
    """
    Determines if a molecule is an unbranched chain.

    Args:
        mol (rdkit.Chem.Mol): RDKit molecule object

    Returns:
        bool: True if the molecule is an unbranched chain, False otherwise
    """
    for atom in mol.GetAtoms():
        if atom.GetDegree() > 2 and atom.GetSymbol() != 'O':
            return False
    return True


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:197468',
                          'name': 'nonadecanol',
                          'definition': 'A fatty alcohol consisting of a '
                                        'hydroxy function at any position of '
                                        'an unbranched saturated chain of '
                                        'nineteen carbon atoms.',
                          'parents': [   'CHEBI:134179',
                                         'CHEBI:197469',
                                         'CHEBI:50584']},
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
    'error': "module 'rdkit.Chem.Descriptors' has no attribute 'AlcoholCount'",
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