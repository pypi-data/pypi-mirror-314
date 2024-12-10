"""
Classifies: CHEBI:144785 omega-linoleoyloxy-O-ultra-long chain acylceramide
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_omega_linoleoyloxy_O_ultra_long_chain_acylceramide(smiles: str):
    """
    Determines if a molecule is an omega-linoleoyloxy-O-ultra-long chain acylceramide,
    defined as 'A ceramide with no defined sphingoid base and a linoleoyl group esterified to a N-omega-hydroxyacyl chain length greater than C27'.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an omega-linoleoyloxy-O-ultra-long chain acylceramide, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of a linoleoyl group
    linoleoyl_smarts = '[C@@H](CC/C=C\C/C=C\CCCCCC(=O)O)'
    linoleoyl_match = mol.GetSubstructMatches(Chem.MolFromSmarts(linoleoyl_smarts))
    if not linoleoyl_match:
        return False, "No linoleoyl group found"

    # Check for the presence of an N-omega-hydroxyacyl chain length greater than C27
    ultra_long_chain_smarts = '[NH]C(=O)CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCO'
    ultra_long_chain_match = mol.GetSubstructMatches(Chem.MolFromSmarts(ultra_long_chain_smarts))
    if not ultra_long_chain_match:
        return False, "No N-omega-hydroxyacyl chain length greater than C27 found"

    # Check for the absence of a defined sphingoid base
    sphingoid_base_smarts = '[NH][C@@H](CO)[C@@H](O)[C@@H](O)[C@@H](O)[C@@H](O)[C@@H](O)[C@@H](O)[C@@H](O)[C@@H](O)[C@@H](O)[C@@H](O)'
    sphingoid_base_match = mol.GetSubstructMatches(Chem.MolFromSmarts(sphingoid_base_smarts))
    if sphingoid_base_match:
        return False, "Defined sphingoid base found"

    return True, "Molecule is an omega-linoleoyloxy-O-ultra-long chain acylceramide"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:144785',
                          'name': 'omega-linoleoyloxy-O-ultra-long chain '
                                  'acylceramide',
                          'definition': 'A ceramide with no defined sphingoid '
                                        'base and a linoleoyl group esterified '
                                        'to a N-omega-hydroxyacyl chain length '
                                        'greater than C27',
                          'parents': ['CHEBI:17761', 'CHEBI:50860']},
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
    'num_true_negatives': 183930,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999945631785833}