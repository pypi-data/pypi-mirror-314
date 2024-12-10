"""
Classifies: CHEBI:139111 alpha-galactosylsphingamide
"""
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors, rdMolDescriptors

def is_alpha_galactosylsphingamide(smiles: str):
    """
    Determines if a molecule is an alpha-galactosylsphingamide.
    
    Args:
        smiles (str): SMILES string of the molecule
        
    Returns:
        bool: True if the molecule is an alpha-galactosylsphingamide, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Check for the presence of a galactose moiety
    galactose_smarts = '[OX2][C@@H]1[C@H]([C@@H]([C@H]([C@H](O1)O)O)O)O'
    galactose_match = mol.HasSubstructMatch(Chem.MolFromSmarts(galactose_smarts))
    if not galactose_match:
        return False, "No galactose moiety found"
    
    # Check for the presence of an amide group
    amide_smarts = 'C(=O)N'
    amide_match = mol.HasSubstructMatch(Chem.MolFromSmarts(amide_smarts))
    if not amide_match:
        return False, "No amide group found"
    
    # Check for the presence of a long alkyl chain
    alkyl_chain_smarts = '[C;H3][C;H2]([C;H2])[C;H2][C;H2][C;H2][C;H2][C;H2][C;H2][C;H2][C;H2]'
    alkyl_chain_match = mol.HasSubstructMatch(Chem.MolFromSmarts(alkyl_chain_smarts))
    if not alkyl_chain_match:
        return False, "No long alkyl chain found"
    
    return True, "The molecule is an alpha-galactosylsphingamide"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:139111',
                          'name': 'alpha-galactosylsphingamide',
                          'definition': 'A galactolipid in which the side '
                                        'chain of a galactosylphytosphingosine '
                                        'has been modified by amidation. Some '
                                        'alpha-galactosylsphingamides have '
                                        'been shown to exhibit antigenic '
                                        'properties.',
                          'parents': ['CHEBI:5254']},
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