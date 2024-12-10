"""
Classifies: CHEBI:157766 2-hydroxy-fatty acyl-CoA(4-)
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_2_hydroxy_fatty_acyl_CoA_4__(smiles: str):
    """
    Determines if a molecule is a 2-hydroxy-fatty acyl-CoA(4-).

    A fatty acyl-CoA that is hydroxylated at position 2 of the acyl chain, major species at pH 7.3.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a 2-hydroxy-fatty acyl-CoA(4-), False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains a CoA moiety
    if not 'CoA' in Chem.MolToSmarts(mol):
        return False, "Molecule does not contain a CoA moiety"

    # Check if the molecule contains a long acyl chain
    acyl_chain_length = rdMolDescriptors.CalcMolWt(mol) - rdMolDescriptors.CalcMolWt(Chem.MolFromSmarts('[CoA]'))
    if acyl_chain_length < 180:
        return False, "Acyl chain is too short (< C12)"

    # Check if the molecule has a hydroxyl group at position 2 of the acyl chain
    smarts_pattern = '[CoA][C;H2][C;H1]([OH])[C]'
    if not mol.HasSubstructMatch(Chem.MolFromSmarts(smarts_pattern)):
        return False, "No hydroxyl group at position 2 of the acyl chain"

    return True, "Molecule is a 2-hydroxy-fatty acyl-CoA(4-)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:157766',
                          'name': '2-hydroxy-fatty acyl-CoA(4-)',
                          'definition': 'A fatty acyl-CoA that is hydroxylated '
                                        'at position 2 of the acyl chain, '
                                        'major species at pH 7.3.',
                          'parents': ['CHEBI:77636']},
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
    'num_false_positives': 0,
    'num_true_negatives': 183924,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999945630012234}