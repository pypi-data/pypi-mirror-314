"""
Classifies: CHEBI:22926 bromohydrocarbon
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_bromohydrocarbon(smiles: str):
    """
    Determines if a molecule is a bromohydrocarbon (a compound derived from a hydrocarbon by replacing a hydrogen atom with a bromine atom).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a bromohydrocarbon, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains bromine atoms
    if not any(atom.GetSymbol() == 'Br' for atom in mol.GetAtoms()):
        return False, "No bromine atoms present"

    # Check if the molecule contains carbon atoms
    if not any(atom.GetSymbol() == 'C' for atom in mol.GetAtoms()):
        return False, "No carbon atoms present"

    # Check if the molecule contains hydrogen atoms
    if not any(atom.GetSymbol() == 'H' for atom in mol.GetAtoms()):
        return False, "No hydrogen atoms present"

    # Check if the molecule is a hydrocarbon with bromine substitutions
    is_hydrocarbon = all(atom.GetSymbol() in ['C', 'H'] for atom in mol.GetAtoms())
    if is_hydrocarbon:
        num_bromine = sum(atom.GetSymbol() == 'Br' for atom in mol.GetAtoms())
        return True, f"Bromohydrocarbon with {num_bromine} bromine substitution(s)"
    else:
        return False, "Not a bromohydrocarbon (contains other elements besides C, H, and Br)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22926',
                          'name': 'bromohydrocarbon',
                          'definition': 'A compound derived from a hydrocarbon '
                                        'by replacing a hydrogen atom with a '
                                        'bromine atom.',
                          'parents': ['CHEBI:24472', 'CHEBI:37141']},
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
    'num_true_negatives': 183920,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.999994562882977}