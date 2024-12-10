"""
Classifies: CHEBI:26961 thiophenes
"""
from rdkit import Chem
from rdkit.Chem import rdchem

def is_thiophene(smiles: str):
    """
    Determines if a molecule contains at least one thiophene ring.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule contains at least one thiophene ring, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains a thiophene ring
    thiophene_ring = Chem.MolFromSmarts('c1cccs1')
    thiophene_matches = mol.GetSubstructMatches(thiophene_ring)

    if thiophene_matches:
        return True, "Molecule contains at least one thiophene ring"
    else:
        return False, "Molecule does not contain a thiophene ring"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26961',
                          'name': 'thiophenes',
                          'definition': 'Compounds containing at least one '
                                        'thiophene ring.',
                          'parents': ['CHEBI:38106']},
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
    'num_true_positives': 33,
    'num_false_positives': 100,
    'num_true_negatives': 10697,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.24812030075187969,
    'recall': 1.0,
    'f1': 0.3975903614457831,
    'accuracy': 0.9907663896583564}