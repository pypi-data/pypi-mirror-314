"""
Classifies: CHEBI:27922 sorbose
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_sorbose(smiles: str):
    """
    Determines if a molecule is a sorbose (a ketohexose often involved in the commercial production of vitamin C,
    and found to occur naturally in grapes).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a sorbose, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule has 6 carbon atoms
    if Descriptors.HeavyAtomCount(mol) != 12:
        return False, "Molecule does not have 12 heavy atoms (not a hexose)"

    # Check if the molecule has 6 oxygen atoms
    if Descriptors.HeavyAtomCount(mol) - Descriptors.NumHeteroatoms(mol) != 6:
        return False, "Molecule does not have 6 carbon atoms (not a hexose)"

    # Check if the molecule has a keto group
    keto_smarts = Chem.MolFromSmarts('C=O')
    matches = mol.GetSubstructMatches(keto_smarts)
    if not matches:
        return False, "Molecule does not contain a keto group"

    # Check if the molecule is a pyranose
    pyranose_smarts = Chem.MolFromSmarts('OC1OCCOC1')
    matches = mol.GetSubstructMatches(pyranose_smarts)
    if not matches:
        return False, "Molecule is not a pyranose"

    return True, "Molecule is a sorbose (a ketohexose)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:27922',
                          'name': 'sorbose',
                          'definition': 'A ketohexose often involved in the '
                                        'commercial production of vitamin C. '
                                        'It has been found to occur naturally '
                                        'in grapes.',
                          'parents': ['CHEBI:24973']},
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