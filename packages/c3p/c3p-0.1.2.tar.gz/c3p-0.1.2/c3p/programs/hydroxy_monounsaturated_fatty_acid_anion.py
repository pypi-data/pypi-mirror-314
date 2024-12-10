"""
Classifies: CHEBI:131870 hydroxy monounsaturated fatty acid anion
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_hydroxy_monounsaturated_fatty_acid_anion(smiles: str):
    """
    Determines if a molecule is a hydroxy monounsaturated fatty acid anion.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a hydroxy monounsaturated fatty acid anion, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for carboxylate anion group
    carboxylate_pattern = Chem.MolFromSmarts("[C]([O-])=O")
    if not mol.HasSubstructMatch(carboxylate_pattern):
        return False, "No carboxylate anion group found"

    # Check for monounsaturation
    num_double_bonds = Descriptors.NumHDosityNodes(mol)
    if num_double_bonds != 1:
        return False, "Not monounsaturated"

    # Check for hydroxy group(s)
    hydroxy_pattern = Chem.MolFromSmarts("[O;H]")
    if not mol.HasSubstructMatch(hydroxy_pattern):
        return False, "No hydroxy group found"

    # Check for linear carbon chain
    carbon_chain = Chem.MolFromSmarts("[C;H3][C;H2][C;H2][C;H2][C;H2][C;H2][C;H2][C;H2][C;H2][C;H2][C;H2][C;H2][C;H2][C;H2][C;H2][C;H2]")
    if not mol.HasSubstructMatch(carbon_chain):
        return False, "Not a linear carbon chain"

    return True, "Molecule is a hydroxy monounsaturated fatty acid anion"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:131870',
                          'name': 'hydroxy monounsaturated fatty acid anion',
                          'definition': 'Any monounsaturated fatty acid anion '
                                        'carrying one or more hydroxy '
                                        'substituents.',
                          'parents': ['CHEBI:59835', 'CHEBI:82680']},
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
    'success': False,
    'best': True,
    'error': "module 'rdkit.Chem.Descriptors' has no attribute "
             "'NumHDosityNodes'",
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': None}