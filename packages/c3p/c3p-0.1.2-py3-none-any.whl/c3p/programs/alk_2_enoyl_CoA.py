"""
Classifies: CHEBI:15469 alk-2-enoyl-CoA
"""
from rdkit import Chem
from rdkit.Chem import Descriptors

def is_alk_2_enoyl_CoA(smiles: str):
    """
    Determines if a molecule is an alk-2-enoyl-CoA, which is an unsaturated fatty acyl-CoA that results from the
    formal condensation of the thiol group of coenzyme A with the carboxy group of any alpha,beta-unsaturated fatty acid.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an alk-2-enoyl-CoA, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for presence of CoA substructure
    coa_pattern = Chem.MolFromSmarts('C(=O)SCCNC(=O)CCNC(=O)[C@H](O)[C@H](O)[C@H](O)COP(=O)(O)OP(=O)(O)OC[C@@H]1O[C@H]([C@H](O)[C@@H]1OP(=O)(O)O)n1cnc2c(N)ncnc12')
    if mol.HasSubstructMatch(coa_pattern) is False:
        return False, "Molecule does not contain the CoA substructure"

    # Check for presence of alpha,beta-unsaturated carbonyl group
    alkene_carbonyl_pattern = Chem.MolFromSmarts('C=CC(=O)')
    if mol.HasSubstructMatch(alkene_carbonyl_pattern) is False:
        return False, "Molecule does not contain an alpha,beta-unsaturated carbonyl group"

    # Check for presence of fatty acid chain
    fatty_acid_pattern = Chem.MolFromSmarts('CCCCCCC')
    if mol.HasSubstructMatch(fatty_acid_pattern) is False:
        return False, "Molecule does not contain a fatty acid chain"

    return True, "Molecule is an alk-2-enoyl-CoA"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:15469',
                          'name': 'alk-2-enoyl-CoA',
                          'definition': 'An unsaturated fatty acyl-CoA that '
                                        'results from the formal condensation '
                                        'of the thiol group of coenzyme A with '
                                        'the carboxy group of any '
                                        'alpha,beta-unsaturated fatty acid.',
                          'parents': ['CHEBI:19573', 'CHEBI:51006']},
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
    'num_true_negatives': 183925,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999945630307842}