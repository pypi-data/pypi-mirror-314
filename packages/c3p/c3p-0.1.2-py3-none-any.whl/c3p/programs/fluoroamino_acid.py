"""
Classifies: CHEBI:24068 fluoroamino acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_fluoroamino_acid(smiles: str):
    """
    Determines if a molecule is a fluoroamino acid (an organofluorine compound consisting
    of an amino acid substituted by a fluoro group).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a fluoroamino acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of a carboxylic acid group
    carboxylic_acid_present = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O' and atom.GetDegree() == 1:
            neighbor = atom.GetNeighbors()[0]
            if neighbor.GetSymbol() == 'C' and neighbor.GetDegree() == 3:
                carboxylic_acid_present = True
                break

    if not carboxylic_acid_present:
        return False, "No carboxylic acid group found"

    # Check for the presence of an amino group
    amino_group_present = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'N' and atom.GetDegree() == 3:
            amino_group_present = True
            break

    if not amino_group_present:
        return False, "No amino group found"

    # Check for the presence of at least one fluorine atom
    fluorine_present = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'F':
            fluorine_present = True
            break

    if not fluorine_present:
        return False, "No fluorine atom found"

    return True, "The molecule is a fluoroamino acid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24068',
                          'name': 'fluoroamino acid',
                          'definition': 'An organofluorine compound that '
                                        'consists of an amino acid substituted '
                                        'by a fluoro group.',
                          'parents': ['CHEBI:24470', 'CHEBI:37143']},
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
    'num_false_positives': 100,
    'num_true_negatives': 3139,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9688271604938271}