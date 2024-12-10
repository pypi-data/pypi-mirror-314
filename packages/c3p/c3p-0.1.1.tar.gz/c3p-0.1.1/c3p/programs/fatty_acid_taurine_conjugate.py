"""
Classifies: CHEBI:132474 fatty acid-taurine conjugate
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_fatty_acid_taurine_conjugate(smiles: str):
    """
    Determines if a molecule is a fatty acid-taurine conjugate.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a fatty acid-taurine conjugate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find the taurine moiety
    taurine_pattern = Chem.MolFromSmarts('NCCS(=O)(=O)O')
    taurine_match = mol.GetSubstructMatch(taurine_pattern)

    if not taurine_match:
        return False, "No taurine moiety found"

    # Find the fatty acid moiety
    fatty_acid_pattern = Chem.MolFromSmarts('C(=O)CCCCCCCCCCC')
    fatty_acid_match = mol.GetSubstructMatch(fatty_acid_pattern)

    if not fatty_acid_match:
        return False, "No fatty acid moiety found"

    # Check if the fatty acid and taurine moieties are connected
    taurine_idx = taurine_match[0]
    fatty_acid_idx = fatty_acid_match[0]

    if not mol.GetBondBetweenAtoms(taurine_idx, fatty_acid_idx):
        return False, "Fatty acid and taurine moieties are not connected"

    return True, "The molecule is a fatty acid-taurine conjugate"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:132474',
                          'name': 'fatty acid-taurine conjugate',
                          'definition': 'A monocarboxylic acid amide obtained '
                                        'by formal condensation of the carboxy '
                                        'group of any fatty acid with the '
                                        'amino group of taurine.',
                          'parents': ['CHEBI:29347', 'CHEBI:33551']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': 'Attempt failed: tuple index out of range',
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 86,
    'num_true_negatives': 183837,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.011494252873563218,
    'recall': 1.0,
    'f1': 0.022727272727272724,
    'accuracy': 0.9995324155629499}