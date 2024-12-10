"""
Classifies: CHEBI:26955 thiocyanates
"""
from rdkit import Chem

def is_thiocyanates(smiles: str):
    """
    Determines if a molecule is a thiocyanate (ester of thiocyanic acid with general formula RSC#N).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a thiocyanate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find thiocyanate group (-SC#N)
    thiocyanate_pattern = Chem.MolFromSmarts("[#16]C#N")
    matches = mol.GetSubstructMatches(thiocyanate_pattern)

    if not matches:
        return False, "No thiocyanate group (-SC#N) found"

    # Check for substituents (-R)
    for match in matches:
        carbon_idx = match[0]
        carbon = mol.GetAtomWithIdx(carbon_idx)
        substituents = [neighbor.GetSymbol() for neighbor in carbon.GetNeighbors() if neighbor.GetIdx() != match[1]]

        if len(substituents) > 0:
            return True, f"Thiocyanate with substituent(s): {', '.join(substituents)}"

    return True, "Unsubstituted thiocyanate"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26955',
                          'name': 'thiocyanates',
                          'definition': 'Esters of thiocyanic acid with '
                                        'general formula RSC#N.',
                          'parents': ['CHEBI:33261', 'CHEBI:35352']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.0,
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
    'num_false_positives': 23,
    'num_true_negatives': 183902,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.041666666666666664,
    'recall': 1.0,
    'f1': 0.07999999999999999,
    'accuracy': 0.9998749497080347}