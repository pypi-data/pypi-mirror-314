"""
Classifies: CHEBI:27124 trimethoxyflavone
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors

def is_trimethoxyflavone(smiles: str):
    """
    Determines if a molecule is a trimethoxyflavone (a flavone with three methoxy groups).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a trimethoxyflavone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains a flavone scaffold
    flavone_scaffold = Chem.MolFromSmarts('c1cc(-c2c(ccc(O)c2O)oc2ccccc2=O)ccc1')
    if not mol.HasSubstructMatch(flavone_scaffold):
        return False, "Not a flavone scaffold"

    # Count the number of methoxy groups
    methoxy_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O' and len(atom.GetNeighbors()) == 2 and atom.GetNeighbors()[0].GetSymbol() == 'C' and atom.GetNeighbors()[1].GetSymbol() == 'C')

    if methoxy_count == 3:
        return True, "Trimethoxyflavone"
    else:
        return False, f"Not a trimethoxyflavone (found {methoxy_count} methoxy groups)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:27124',
                          'name': 'trimethoxyflavone',
                          'definition': 'A methoxyflavone that is flavone '
                                        'substituted by three methoxy groups.',
                          'parents': ['CHEBI:25241']},
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
    'num_true_negatives': 183901,
    'num_false_negatives': 3,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999836871411171}