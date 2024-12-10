"""
Classifies: CHEBI:143516 ultra-long-chain 3-oxoacyl-CoA(4-)
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_ultra_long_chain_3_oxoacyl_CoA_4__(smiles: str):
    """
    Determines if a molecule is an ultra-long-chain 3-oxoacyl-CoA(4-).
    An ultra-long-chain 3-oxoacyl-CoA(4-) is defined as any very long-chain
    3-oxoacyl-CoA(4-) in which the 3-oxoacyl group has a chain length greater than C27.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an ultra-long-chain 3-oxoacyl-CoA(4-), False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of CoA(4-) substructure
    CoA_pattern = Chem.MolFromSmarts('C(C(=O)NCCC(=O)NCCC(=O)O)O[P@](=O)(O)[O-].O[P@](=O)(O)[O-].O[C@H]1[C@@H]([C@@H](O[P@](O)(=O)O)O1)n1cnc2c(N)ncnc12')
    if not mol.HasSubstructMatch(CoA_pattern):
        return False, "Molecule does not contain CoA(4-) substructure"

    # Check for the presence of 3-oxoacyl group
    oxoacyl_pattern = Chem.MolFromSmarts('CC(=O)C')
    if not mol.HasSubstructMatch(oxoacyl_pattern):
        return False, "Molecule does not contain 3-oxoacyl group"

    # Check for the chain length of the 3-oxoacyl group
    chain_length = rdMolDescriptors.CalcTPSA(mol)
    if chain_length <= 27:
        return False, f"Chain length of 3-oxoacyl group is {chain_length}, which is not greater than C27"

    return True, "Molecule is an ultra-long-chain 3-oxoacyl-CoA(4-)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:143516',
                          'name': 'ultra-long-chain 3-oxoacyl-CoA(4-)',
                          'definition': 'Any very long-chain '
                                        '3-oxoacyl-CoA(4-)in which the '
                                        '3-oxoacyl group has a chain length '
                                        'greater than C27.',
                          'parents': ['CHEBI:90725']},
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
    'num_true_negatives': 183919,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999945628534145}