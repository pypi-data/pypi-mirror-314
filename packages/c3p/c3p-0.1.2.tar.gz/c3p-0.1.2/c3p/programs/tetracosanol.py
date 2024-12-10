"""
Classifies: CHEBI:205576 tetracosanol
"""
From rdkit import Chem
from rdkit.Chem import Descriptors

def is_tetracosanol(smiles: str):
    """
    Determines if a molecule is a tetracosanol (a fatty alcohol with an unbranched saturated chain of 24 carbon atoms and a hydroxy group at any position).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a tetracosanol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule has exactly 24 carbon atoms
    num_carbon_atoms = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')
    if num_carbon_atoms != 24:
        return False, "Molecule does not have 24 carbon atoms"

    # Check if the molecule has a single hydroxy group
    num_hydroxy_groups = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O' and sum(bond.GetBondTypeAsDouble() == 1.0 for bond in atom.GetBonds()) == 1)
    if num_hydroxy_groups != 1:
        return False, "Molecule does not have a single hydroxy group"

    # Check if the carbon chain is unbranched and saturated
    sssr = Chem.GetSymmSSSR(mol)
    if len(sssr) != 1 or any(bond.GetBondTypeAsDouble() != 1.0 for bond in mol.GetBonds()):
        return False, "Molecule has a branched or unsaturated carbon chain"

    return True, "Molecule is a tetracosanol"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:205576',
                          'name': 'tetracosanol',
                          'definition': 'A fatty alcohol consisting of a '
                                        'hydroxy function at any position of '
                                        'an unbranched saturated chain of '
                                        'twenty-four carbon atoms.',
                          'parents': [   'CHEBI:134179',
                                         'CHEBI:50584',
                                         'CHEBI:78142']},
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
    'success': False,
    'best': True,
    'error': 'invalid syntax (<string>, line 1)',
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0,
    'f1': 0,
    'accuracy': None}