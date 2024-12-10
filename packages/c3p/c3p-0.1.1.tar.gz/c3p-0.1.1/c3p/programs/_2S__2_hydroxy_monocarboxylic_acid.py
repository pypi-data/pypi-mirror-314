"""
Classifies: CHEBI:17375 (2S)-2-hydroxy monocarboxylic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors


def is__2S__2_hydroxy_monocarboxylic_acid(smiles: str):
    """
    Determines if a molecule is a (2S)-2-hydroxy monocarboxylic acid.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a (2S)-2-hydroxy monocarboxylic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for carboxylic acid group
    carboxylic_acid_smarts = "[$(C(=O)O)]"
    carboxylic_acid_atoms = mol.GetSubstructMatches(Chem.MolFromSmarts(carboxylic_acid_smarts))
    if not carboxylic_acid_atoms:
        return False, "No carboxylic acid group found"

    # Check for hydroxyl group
    hydroxyl_smarts = "[OX1H]"
    hydroxyl_atoms = mol.GetSubstructMatches(Chem.MolFromSmarts(hydroxyl_smarts))
    if not hydroxyl_atoms:
        return False, "No hydroxyl group found"

    # Check if the hydroxyl group is attached to carbon 2
    carboxylic_acid_atom = mol.GetAtomWithIdx(carboxylic_acid_atoms[0][0])
    carboxylic_acid_carbon = carboxylic_acid_atom.GetNeighbors()[0]
    hydroxyl_carbon = mol.GetAtomWithIdx(hydroxyl_atoms[0][0]).GetNeighbors()[0]
    if carboxylic_acid_carbon.GetIdx() != hydroxyl_carbon.GetIdx():
        return False, "Hydroxyl group not attached to carbon 2"

    # Check for (S)-configuration
    chiral_atom = hydroxyl_carbon
    if chiral_atom.GetChiralTag() != Chem.ChiralType.CHI_TETRAHEDRAL_CCW:
        return False, "Carbon 2 not (S)-configured"

    return True, "(2S)-2-hydroxy monocarboxylic acid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17375',
                          'name': '(2S)-2-hydroxy monocarboxylic acid',
                          'definition': 'A 2-hydroxy monocarboxylic acid in '
                                        'which the carbon at position 2 has '
                                        '(S)-configuration.',
                          'parents': ['CHEBI:49302']},
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
    'error': 'tuple index out of range',
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