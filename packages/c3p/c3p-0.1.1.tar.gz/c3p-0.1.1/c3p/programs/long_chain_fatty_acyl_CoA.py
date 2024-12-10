"""
Classifies: CHEBI:33184 long-chain fatty acyl-CoA
"""
from rdkit import Chem

def is_long_chain_fatty_acyl_CoA(smiles: str):
    """
    Determines if a molecule is a long-chain fatty acyl-CoA (C13 to C22).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a long-chain fatty acyl-CoA, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"
    
    # Find the CoA moiety
    coa_smarts = '[C@@H]1([N@H]2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCCO)[C@@H]([C@H]1O)OP(O)(O)=O)(O)=O)(O)=O'
    coa_matches = mol.GetSubstructMatches(Chem.MolFromSmarts(coa_smarts))
    if not coa_matches:
        return False, "No CoA moiety found"
    
    # Find the fatty acyl chain
    acyl_smarts = '[CX3](=[OX1])C([CX3])([CX3])[CX3]'
    acyl_matches = mol.GetSubstructMatches(Chem.MolFromSmarts(acyl_smarts))
    if not acyl_matches:
        return False, "No fatty acyl chain found"
    
    # Check the length of the fatty acyl chain
    acyl_atom_idx = acyl_matches[0][0]
    acyl_chain_length = sum(1 for _ in Chem.Mol.GetAtomWithIdx(mol, acyl_atom_idx).GetDescendants())
    if acyl_chain_length < 13 or acyl_chain_length > 22:
        return False, f"Fatty acyl chain length is {acyl_chain_length}, not in the range C13 to C22"
    
    return True, f"Long-chain fatty acyl-CoA with chain length C{acyl_chain_length}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33184',
                          'name': 'long-chain fatty acyl-CoA',
                          'definition': 'A fatty acyl-CoA that results from '
                                        'the formal condensation of the thiol '
                                        'group of coenzyme A with the carboxy '
                                        'group of any long-chain (C13 to C22) '
                                        'fatty acid.',
                          'parents': ['CHEBI:37554']},
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
    'num_true_negatives': 183728,
    'num_false_negatives': 20,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9998911552778805}