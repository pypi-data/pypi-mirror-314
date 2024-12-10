"""
Classifies: CHEBI:24960 ketoaldehyde
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_ketoaldehyde(smiles: str):
    """
    Determines if a molecule is a ketoaldehyde (i.e., contains both an aldehydic and ketonic group).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a ketoaldehyde, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find all aldehyde and ketone groups
    aldehydes = [atom.GetIdx() for atom in mol.GetAtoms() if atom.GetSymbol() == 'C' and atom.GetHybridization() == Chem.HybridizationType.SP2 and len(atom.GetNeighbors()) == 2 and any(neighbor.GetSymbol() == 'O' and neighbor.GetIsAromatic() is False for neighbor in atom.GetNeighbors())]
    ketones = [atom.GetIdx() for atom in mol.GetAtoms() if atom.GetSymbol() == 'C' and atom.GetHybridization() == Chem.HybridizationType.SP2 and len(atom.GetNeighbors()) == 3 and any(neighbor.GetSymbol() == 'O' and neighbor.GetIsAromatic() is False for neighbor in atom.GetNeighbors())]

    if not aldehydes or not ketones:
        return False, "No aldehyde or ketone groups found"

    return True, "Molecule contains both an aldehyde and ketone group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24960',
                          'name': 'ketoaldehyde',
                          'definition': 'Any compound that has an aldehydic '
                                        'and ketonic group in the same '
                                        'molecule.',
                          'parents': ['CHEBI:17087', 'CHEBI:17478']},
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
    'num_true_positives': 1,
    'num_false_positives': 100,
    'num_true_negatives': 4647,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 1.0,
    'f1': 0.0196078431372549,
    'accuracy': 0.97893850042123}