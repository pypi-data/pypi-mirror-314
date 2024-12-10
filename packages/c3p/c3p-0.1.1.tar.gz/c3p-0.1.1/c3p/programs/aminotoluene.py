"""
Classifies: CHEBI:22531 aminotoluene
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_aminotoluene(smiles: str):
    """
    Determines if a molecule is an aminotoluene (toluene with one or more amino groups).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an aminotoluene, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of a toluene substructure
    toluene_pattern = Chem.MolFromSmarts('c1ccc(C)cc1')
    if not mol.HasSubstructMatch(toluene_pattern):
        return False, "Toluene substructure not found"

    # Check for the presence of at least one amino group
    amino_pattern = Chem.MolFromSmarts('N')
    if not mol.HasSubstructMatch(amino_pattern):
        return False, "No amino groups found"

    # Count the number of amino groups
    amino_groups = sum(atom.GetSymbol() == 'N' for atom in mol.GetAtoms())

    if amino_groups > 0:
        return True, f"Aminotoluene with {amino_groups} amino group(s)"
    else:
        return False, "No amino groups found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22531',
                          'name': 'aminotoluene',
                          'definition': 'Any member of the class of  toluenes '
                                        'carrying one or more amino groups.',
                          'parents': ['CHEBI:27024', 'CHEBI:48975']},
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
    'num_true_negatives': 263,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 1.0,
    'f1': 0.0196078431372549,
    'accuracy': 0.7252747252747253}