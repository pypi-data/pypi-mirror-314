"""
Classifies: CHEBI:29067 carboxylic acid anion
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_carboxylic_acid_anion(smiles: str):
    """
    Determines if a molecule is a carboxylic acid anion.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a carboxylic acid anion, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of a carboxylate group (-COO-)
    carboxylate_smarts = "[O-;X1]C(=O)[O-;X2]"
    carboxylate_match = mol.GetSubstructMatches(Chem.MolFromSmarts(carboxylate_smarts))
    if not carboxylate_match:
        return False, "No carboxylate group found"

    # Check if the molecule contains any other ionizable groups
    ionizable_smarts = "[N+,N-,O+,O-,S+,S-,P+,P-]"
    ionizable_match = mol.GetSubstructMatches(Chem.MolFromSmarts(ionizable_smarts))
    ionizable_match = [match for match in ionizable_match if match not in carboxylate_match]
    if ionizable_match:
        return False, "Molecule contains other ionizable groups"

    return True, "Carboxylic acid anion"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:29067',
                          'name': 'carboxylic acid anion',
                          'definition': 'The conjugate base formed when the '
                                        'carboxy group of a carboxylic acid is '
                                        'deprotonated.',
                          'parents': ['CHEBI:25696', 'CHEBI:35406']},
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
    'num_true_negatives': 0,
    'num_false_negatives': 100,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.0}