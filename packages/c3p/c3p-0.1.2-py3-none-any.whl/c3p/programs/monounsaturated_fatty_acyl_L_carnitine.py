"""
Classifies: CHEBI:133446 monounsaturated fatty acyl-L-carnitine
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_monounsaturated_fatty_acyl_L_carnitine(smiles: str):
    """
    Determines if a molecule is a monounsaturated fatty acyl-L-carnitine.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a monounsaturated fatty acyl-L-carnitine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for presence of carnitine substructure
    carnitine = Chem.MolFromSmarts('[N+](C)(C)(C)C[C@@H](O)C([O-])=O')
    if mol.GetSubstructMatches(carnitine) == ():
        return False, "Carnitine substructure not found"

    # Check for presence of monounsaturated fatty acyl chain
    monounsaturated_chain = Chem.MolFromSmarts('C=CC')
    if mol.GetSubstructMatches(monounsaturated_chain) == ():
        return False, "No monounsaturated fatty acyl chain found"

    # Check for ester bond between carnitine and fatty acyl chain
    ester_bond = Chem.MolFromSmarts('C(=O)OC')
    if mol.GetSubstructMatches(ester_bond) == ():
        return False, "No ester bond found between carnitine and fatty acyl chain"

    return True, "Molecule is a monounsaturated fatty acyl-L-carnitine"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:133446',
                          'name': 'monounsaturated fatty acyl-L-carnitine',
                          'definition': 'An O-acylcarnitine in which the R is '
                                        'a monounsaturated fatty acyl chain.',
                          'parents': ['CHEBI:176910', 'CHEBI:75659']},
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
    'num_true_negatives': 183927,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999945630899048}