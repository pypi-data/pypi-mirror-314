"""
Classifies: CHEBI:27136 triol
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_triol(smiles: str):
    """
    Determines if a molecule is a triol (a compound containing three hydroxy groups).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a triol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Count the number of hydroxy groups
    num_hydroxy_groups = rdMolDescriptors.CalcNumHydroxyGroups(mol)

    if num_hydroxy_groups == 3:
        return True, "The molecule contains three hydroxy groups"
    else:
        return False, f"The molecule contains {num_hydroxy_groups} hydroxy groups (expected 3)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:27136',
                          'name': 'triol',
                          'definition': 'A chemical compound containing three '
                                        'hydroxy groups.',
                          'parents': ['CHEBI:26191']},
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
    'error': "module 'rdkit.Chem.rdMolDescriptors' has no attribute "
             "'CalcNumHydroxyGroups'",
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