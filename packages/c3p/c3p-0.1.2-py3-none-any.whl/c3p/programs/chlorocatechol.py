"""
Classifies: CHEBI:23138 chlorocatechol
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_chlorocatechol(smiles: str):
    """
    Determines if a molecule is a chlorocatechol (i.e., a catechol substituted with at least one chloro group).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a chlorocatechol, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if molecule contains at least one chlorine atom
    if sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'Cl') == 0:
        return False, "No chlorine atoms found"

    # Check if molecule contains catechol substructure
    catechol_pattern = Chem.MolFromSmarts('c1c(O)c(O)ccc1')
    if not mol.HasSubstructMatch(catechol_pattern):
        return False, "Catechol substructure not found"

    # If both conditions are met, it's a chlorocatechol
    return True, "Molecule is a chlorocatechol"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23138',
                          'name': 'chlorocatechol',
                          'definition': 'Any member of the class of catechols '
                                        'that is catechol substituted by at '
                                        'least one chloro group.',
                          'parents': ['CHEBI:23132', 'CHEBI:33566']},
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
    'num_true_negatives': 25673,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 1.0,
    'f1': 0.0196078431372549,
    'accuracy': 0.9961201210522231}