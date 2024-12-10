"""
Classifies: CHEBI:27283 very long-chain fatty acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors

def is_very_long_chain_fatty_acid(smiles: str):
    """
    Determines if a molecule is a very long-chain fatty acid (chain length > C22).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a very long-chain fatty acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Get the number of atoms in the molecule
    num_atoms = mol.GetNumAtoms()

    # Get the number of carbon atoms in the molecule
    num_carbon_atoms = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')

    # Filter out non-fatty acids
    if mol.GetNumAtoms() < 23:
        return False, "Chain length is too short (< C23)"

    # Check for the presence of a carboxyl group
    carboxyl_found = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O':
            neighbors = atom.GetNeighbors()
            if len(neighbors) == 1 and neighbors[0].GetSymbol() == 'C':
                carboxyl_found = True
                break

    if not carboxyl_found:
        return False, "No carboxyl group found"

    # Check if the molecule is a very long-chain fatty acid
    if num_carbon_atoms > 22:
        if num_carbon_atoms > 27:
            return True, "Ultra-long-chain fatty acid (> C27)"
        else:
            return True, "Very long-chain fatty acid (> C22)"

    return False, "Chain length is too short (< C23)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:27283',
                          'name': 'very long-chain fatty acid',
                          'definition': 'A fatty acid which has a chain length '
                                        'greater than C22. Very long-chain '
                                        'fatty acids which have a chain length '
                                        'greater than C27 are also known as '
                                        'ultra-long-chain fatty acids.',
                          'parents': ['CHEBI:35366']},
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
    'num_true_positives': 17,
    'num_false_positives': 100,
    'num_true_negatives': 136,
    'num_false_negatives': 8,
    'num_negatives': None,
    'precision': 0.1452991452991453,
    'recall': 0.68,
    'f1': 0.23943661971830987,
    'accuracy': 0.5862068965517241}