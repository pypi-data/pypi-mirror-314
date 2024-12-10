"""
Classifies: CHEBI:27856 acetamide
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_acetamide(smiles: str):
    """
    Determines if a molecule is an acetamide, a member of the class of acetamides that results from the formal condensation of acetic acid with ammonia.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an acetamide, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find all acetamide substructures
    acetamide_pattern = Chem.MolFromSmarts('C(=O)N')
    matches = mol.GetSubstructMatches(acetamide_pattern)

    if not matches:
        return False, "No acetamide substructure found"

    # Check if the acetamide substructure is not part of a larger ring
    for match in matches:
        atom1 = mol.GetAtomWithIdx(match[0])
        atom2 = mol.GetAtomWithIdx(match[1])
        if atom1.IsInRing() or atom2.IsInRing():
            continue
        else:
            # Check if the carbonyl carbon is connected to a methyl group
            methyl_pattern = Chem.MolFromSmarts('C[C](=O)N')
            methyl_match = mol.GetSubstructMatch(methyl_pattern)
            if methyl_match:
                return True, "Molecule contains an acetamide substructure"

    return False, "No acetamide substructure found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:27856',
                          'name': 'acetamide',
                          'definition': 'A member of the class of acetamides '
                                        'that results from the formal '
                                        'condensation of acetic acid with '
                                        'ammonia.',
                          'parents': [   'CHEBI:22160',
                                         'CHEBI:29347',
                                         'CHEBI:83628']},
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
    'num_true_positives': 2,
    'num_false_positives': 100,
    'num_true_negatives': 293,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0196078431372549,
    'recall': 1.0,
    'f1': 0.038461538461538464,
    'accuracy': 0.7468354430379747}