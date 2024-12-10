"""
Classifies: CHEBI:32877 primary amine
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_primary_amine(smiles: str):
    """
    Determines if a molecule is a primary amine.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a primary amine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Get the number of nitrogen atoms
    num_nitrogen = sum(atom.GetAtomicNum() == 7 for atom in mol.GetAtoms())

    # Primary amines have only one nitrogen atom
    if num_nitrogen != 1:
        return False, "Molecule does not have exactly one nitrogen atom"

    # Get the nitrogen atom
    nitrogen_atom = [atom for atom in mol.GetAtoms() if atom.GetAtomicNum() == 7][0]

    # Primary amines have three substituents on the nitrogen atom
    if len(nitrogen_atom.GetNeighbors()) != 3:
        return False, "Nitrogen atom does not have three substituents"

    # One of the substituents should be hydrogen
    if not any(neighbor.GetSymbol() == 'H' for neighbor in nitrogen_atom.GetNeighbors()):
        return False, "Nitrogen atom does not have a hydrogen substituent"

    # Check if the other substituents are hydrocarbyl groups
    hydrocarbyl_groups = []
    for neighbor in nitrogen_atom.GetNeighbors():
        if neighbor.GetSymbol() != 'H':
            hydrocarbyl_group = Chem.MolFragmentToSmiles(mol, [neighbor.GetIdx()], bondsToUse=[mol.GetBondBetweenAtoms(neighbor.GetIdx(), nitrogen_atom.GetIdx()).GetIdx()])
            hydrocarbyl_groups.append(hydrocarbyl_group)

    hydrocarbyl_groups_str = ', '.join(hydrocarbyl_groups)
    return True, f"Primary amine with hydrocarbyl groups: {hydrocarbyl_groups_str}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:32877',
                          'name': 'primary amine',
                          'definition': 'A compound formally derived from '
                                        'ammonia by replacing one hydrogen '
                                        'atom by a hydrocarbyl group.',
                          'parents': ['CHEBI:32952', 'CHEBI:50994']},
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
    'num_false_positives': 5,
    'num_true_negatives': 183769,
    'num_false_negatives': 16,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9998857391588226}