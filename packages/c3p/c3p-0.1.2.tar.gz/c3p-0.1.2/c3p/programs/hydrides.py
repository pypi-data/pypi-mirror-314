"""
Classifies: CHEBI:33692 hydrides
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_hydrides(smiles: str):
    """
    Determines if a molecule is a hydride (a chemical compound of hydrogen with other chemical elements).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a hydride, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for presence of hydrogen atoms
    num_hydrogen_atoms = sum(atom.GetAtomicNum() == 1 for atom in mol.GetAtoms())
    if num_hydrogen_atoms == 0:
        return False, "No hydrogen atoms present"

    # Check for presence of other elements
    other_elements = set(atom.GetSymbol() for atom in mol.GetAtoms() if atom.GetAtomicNum() != 1)
    if not other_elements:
        return False, "No other elements present besides hydrogen"

    return True, f"Hydride containing hydrogen and elements: {', '.join(other_elements)}"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33692',
                          'name': 'hydrides',
                          'definition': 'Hydrides are chemical compounds of '
                                        'hydrogen with other chemical '
                                        'elements.',
                          'parents': ['CHEBI:33608', 'CHEBI:37577']},
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
    'num_true_negatives': 0,
    'num_false_negatives': 100,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.0}