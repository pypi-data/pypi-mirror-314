"""
Classifies: CHEBI:228187 hexacosanol
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors

def is_hexacosanol(smiles: str):
    """
    Determines if a molecule is a hexacosanol (a fatty alcohol consisting of a hydroxy function
    at any position of an unbranched saturated chain of twenty-six carbon atoms).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a hexacosanol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for a single alcohol group
    alcohol_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8 and atom.GetTotalNumHs() == 1)
    if alcohol_count != 1:
        return False, "Molecule does not contain exactly one alcohol group"

    # Check for linear chain
    if not Descriptors.Descriptors.Descriptors.Descriptors.Descriptors.Descriptors.Descriptors.Descriptors.Descriptors.Descriptors.Descriptors.Descriptors().Has0DDescriptor(mol):
        return False, "Molecule is not linear"

    # Check for 26 carbon atoms
    if sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6) != 26:
        return False, "Molecule does not contain 26 carbon atoms"

    # Check for saturated chain
    if not Descriptors.Descriptors.Descriptors.Descriptors.Descriptors.Descriptors.Descriptors.Descriptors.Descriptors.Descriptors.Descriptors.Descriptors().IsNsaturatedHetero(mol):
        return False, "Molecule contains unsaturated bonds or heteroatoms"

    return True, "Molecule is a hexacosanol"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:228187',
                          'name': 'hexacosanol',
                          'definition': 'A fatty alcohol consisting of a '
                                        'hydroxy function at any position of '
                                        'an unbranched saturated chain of '
                                        'twenty-six carbon atoms.',
                          'parents': [   'CHEBI:134179',
                                         'CHEBI:50584',
                                         'CHEBI:78143']},
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
    'success': False,
    'best': True,
    'error': "module 'rdkit.Chem.Descriptors' has no attribute 'Descriptors'",
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0,
    'f1': 0,
    'accuracy': None}