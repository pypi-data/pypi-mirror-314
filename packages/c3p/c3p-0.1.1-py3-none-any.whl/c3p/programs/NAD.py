"""
Classifies: CHEBI:13389 NAD
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_NAD(smiles: str):
    """
    Determines if a molecule is a NAD (Nicotinamide-Adenine Dinucleotide).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a NAD, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of the nicotinamide and adenine substructures
    nicotinamide_pattern = Chem.MolFromSmarts('NC(=O)c1ncc[n+]c1')
    adenine_pattern = Chem.MolFromSmarts('Nc1ncnc2n(c1)c(nc2)N')

    if not mol.HasSubstructMatch(nicotinamide_pattern):
        return False, "Nicotinamide substructure not found"

    if not mol.HasSubstructMatch(adenine_pattern):
        return False, "Adenine substructure not found"

    # Check for the presence of the phosphate group
    phosphate_pattern = Chem.MolFromSmarts('OP(=O)(O)O')

    if not mol.HasSubstructMatch(phosphate_pattern):
        return False, "Phosphate group not found"

    # Check for the presence of the ribose sugar
    ribose_pattern = Chem.MolFromSmarts('OC1C(O)C(O)C(O)C1O')

    if not mol.HasSubstructMatch(ribose_pattern):
        return False, "Ribose sugar not found"

    return True, "The molecule is a NAD (Nicotinamide-Adenine Dinucleotide)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:13389',
                          'name': 'NAD',
                          'definition': 'Abbreviation for nicotinamide-adenine '
                                        'dinucleotide when its oxidation state '
                                        'is unknown or unspecified. It is used '
                                        'in metabolic pathways like glycolysis '
                                        'and citric acid cycle.',
                          'parents': ['CHEBI:25524']},
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