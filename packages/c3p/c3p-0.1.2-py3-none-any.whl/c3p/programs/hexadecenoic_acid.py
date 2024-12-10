"""
Classifies: CHEBI:24548 hexadecenoic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors

def is_hexadecenoic_acid(smiles: str):
    """
    Determines if a molecule is a hexadecenoic acid (C16 straight-chain monounsaturated fatty acid with one C=C double bond).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a hexadecenoic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for exactly one double bond
    if Descriptors.BondCountDescriptors.NumAliphaticDoubleBonds(mol) != 1:
        return False, "Does not contain exactly one double bond"

    # Check for exactly 16 carbon atoms
    if Descriptors.HeavyAtomMolWt(mol) != 256.424:
        return False, "Does not contain 16 carbon atoms"

    # Check for a carboxylic acid group
    carboxyl_pattern = Chem.MolFromSmarts('C(=O)O')
    if not mol.HasSubstructMatch(carboxyl_pattern):
        return False, "Does not contain a carboxylic acid group"

    # Check for a straight chain
    sssr = Chem.GetSymmSSSR(mol)
    if len(sssr) != 1:
        return False, "Not a straight chain"

    # Check for exactly one double bond in the chain
    double_bond_pattern = Chem.MolFromSmarts('C=C')
    double_bonds = mol.GetSubstructMatches(double_bond_pattern)
    if len(double_bonds) != 1:
        return False, "Does not contain exactly one double bond in the chain"

    return True, "Molecule is a hexadecenoic acid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24548',
                          'name': 'hexadecenoic acid',
                          'definition': 'A C16 straight-chain monounsaturated '
                                        'fatty acid having one C=C double '
                                        'bond.',
                          'parents': [   'CHEBI:15904',
                                         'CHEBI:25413',
                                         'CHEBI:53339',
                                         'CHEBI:59202']},
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
    'error': "module 'rdkit.Chem.Descriptors' has no attribute "
             "'BondCountDescriptors'",
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