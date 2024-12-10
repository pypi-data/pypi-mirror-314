"""
Classifies: CHEBI:27116 trihydroxyflavone
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_trihydroxyflavone(smiles: str):
    """
    Determines if a molecule is a trihydroxyflavone (any hydroxyflavone carrying three hydroxy groups at unspecified positions).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a trihydroxyflavone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if it is a flavone
    isFlavone = rdMolDescriptors.CalcPAFlavoneDescriptor(mol)
    if not isFlavone:
        return False, "Not a flavone"

    # Count the number of hydroxy groups
    num_hydroxy = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O' and atom.GetTotalNumHs() == 1)

    if num_hydroxy == 3:
        return True, "Trihydroxyflavone"
    elif num_hydroxy < 3:
        return False, "Not enough hydroxy groups"
    else:
        return False, "Too many hydroxy groups"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:27116',
                          'name': 'trihydroxyflavone',
                          'definition': 'Any  hydroxyflavone carrying three '
                                        'hydroxy groups at unspecified '
                                        'positions.',
                          'parents': ['CHEBI:24698']},
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
    'error': "module 'rdkit.Chem.rdMolDescriptors' has no attribute "
             "'CalcPAFlavoneDescriptor'",
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