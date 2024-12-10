"""
Classifies: CHEBI:194303 omega-hydroxy-medium-chain fatty acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_omega_hydroxy_medium_chain_fatty_acid(smiles: str):
    """
    Determines if a molecule is an omega-hydroxy-medium-chain fatty acid.

    An omega-hydroxy-medium-chain fatty acid is defined as a fatty acid with a
    chain length ranging from C6 to C12 and with a terminal hydroxyl group.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an omega-hydroxy-medium-chain fatty acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Get the number of carbon atoms
    num_carbons = Descriptors.HeavyAtomCount(mol) - Descriptors.HeteroAtomCount(mol)

    # Check if the chain length is between C6 and C12
    if num_carbons < 6 or num_carbons > 12:
        return False, f"Chain length is {num_carbons}, not in the range C6-C12"

    # Check if the molecule contains a carboxylic acid group
    carboxylic_acid_smarts = "[C](=O)[O;H,-]"
    hits = mol.GetSubstructMatches(Chem.MolFromSmarts(carboxylic_acid_smarts))
    if not hits:
        return False, "No carboxylic acid group found"

    # Check if the molecule contains a terminal hydroxyl group
    terminal_hydroxyl_smarts = "[OH]"
    hits = mol.GetSubstructMatches(Chem.MolFromSmarts(terminal_hydroxyl_smarts))
    if not hits:
        return False, "No terminal hydroxyl group found"

    # Check if the carboxylic acid and hydroxyl groups are at opposite ends
    carbonyl_idx = hits[0][0]
    hydroxyl_idx = hits[1][0]
    path = AllChem.GetShortestPath(mol, carbonyl_idx, hydroxyl_idx)
    if len(path) != num_carbons:
        return False, "Carboxylic acid and hydroxyl groups are not at opposite ends"

    return True, "Molecule is an omega-hydroxy-medium-chain fatty acid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:194303',
                          'name': 'omega-hydroxy-medium-chain fatty acid',
                          'definition': 'A omega-hydroxy-fatty acid with a '
                                        'chain length ranging from C6 to C12.',
                          'parents': ['CHEBI:10615', 'CHEBI:59554']},
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
             "'HeteroAtomCount'",
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