"""
Classifies: CHEBI:20873 CDP-sugar
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_CDP_sugar(smiles: str):
    """
    Determines if a molecule is a CDP-sugar (A pyrimidine nucleotide-sugar having CDP as the nucleotide component
    attached to an unspecified sugar via an anomeric diphosphate linkage).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a CDP-sugar, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of the CDP moiety
    cdp_smarts = "[N]1=C([N]=C(N)C(=O)N1)[C@H]2O[C@@H]([C@H]([C@H]2O)O)[P@@](=O)(O)[P@](=O)(O)O"
    cdp_pattern = Chem.MolFromSmarts(cdp_smarts)
    if not mol.HasSubstructMatch(cdp_pattern):
        return False, "CDP moiety not found"

    # Check for the presence of a sugar moiety
    sugar_smarts = "[C@H]1[C@H]([C@@H]([C@H]([C@@H](O1)O)O)O)O"
    sugar_pattern = Chem.MolFromSmarts(sugar_smarts)
    if not mol.HasSubstructMatch(sugar_pattern):
        return False, "Sugar moiety not found"

    # Check for the presence of an anomeric diphosphate linkage
    anomeric_linkage_smarts = "[C@H]1[C@@H]([C@H]([C@@H]([C@H](O1)O)O)O)O[P@@](=O)(O)[P@](=O)(O)[N]1=C([N]=C(N)C(=O)N1)[C@@H]2O[C@H]([C@@H]([C@H]2O)O)O"
    anomeric_linkage_pattern = Chem.MolFromSmarts(anomeric_linkage_smarts)
    if not mol.HasSubstructMatch(anomeric_linkage_pattern):
        return False, "Anomeric diphosphate linkage not found"

    return True, "Molecule is a CDP-sugar"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:20873',
                          'name': 'CDP-sugar',
                          'definition': 'A pyrimidine nucleotide-sugar having '
                                        'CDP as the nucleotide component '
                                        'attached to an unspecified sugar via '
                                        'an anomeric diphosphate linkage.',
                          'parents': ['CHEBI:61109']},
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
    'num_true_negatives': 183919,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9999945628534145}