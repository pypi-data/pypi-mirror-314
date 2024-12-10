"""
Classifies: CHEBI:33589 boranes
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_borane(smiles: str):
    """
    Determines if a molecule is a borane (molecular hydrides of boron).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a borane, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Get the number of boron and hydrogen atoms
    num_boron = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'B')
    num_hydrogen = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'H')

    # Check if it contains boron and hydrogen
    if num_boron == 0 or num_hydrogen == 0:
        return False, "Molecule does not contain boron and hydrogen"

    # Check if it contains other elements
    other_atoms = [atom for atom in mol.GetAtoms() if atom.GetSymbol() not in ['B', 'H']]
    if other_atoms:
        return False, "Molecule contains atoms other than boron and hydrogen"

    # Check if the hydrogen and boron atoms are connected
    hydrogen_neighbors = set()
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'H':
            for neighbor in atom.GetNeighbors():
                if neighbor.GetSymbol() == 'B':
                    hydrogen_neighbors.add(neighbor.GetIdx())

    # If all boron atoms have at least one hydrogen neighbor, it's a borane
    boron_atoms = [atom.GetIdx() for atom in mol.GetAtoms() if atom.GetSymbol() == 'B']
    if set(boron_atoms).issubset(hydrogen_neighbors):
        return True, "Molecule is a borane"
    else:
        return False, "Boron atoms are not connected to hydrogen atoms"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33589',
                          'name': 'boranes',
                          'definition': 'The molecular hydrides of boron.',
                          'parents': ['CHEBI:33588']},
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
    'error': "name 'is_boranes' is not defined",
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0,
    'f1': 0,
    'accuracy': None}