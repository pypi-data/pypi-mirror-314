"""
Classifies: CHEBI:33702 polyatomic cation
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_polyatomic_cation(smiles: str):
    """
    Determines if a molecule is a polyatomic cation (a cation consisting of more than one atom).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a polyatomic cation, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule has a formal charge
    charge = AllChem.GetFormalCharge(mol)
    if charge <= 0:
        return False, "Molecule does not have a positive formal charge"

    # Check if the molecule consists of more than one atom
    num_atoms = mol.GetNumAtoms()
    if num_atoms <= 1:
        return False, "Molecule consists of only one atom"

    # If the molecule has a positive charge and more than one atom, it is a polyatomic cation
    return True, "Polyatomic cation"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33702',
                          'name': 'polyatomic cation',
                          'definition': 'A cation consisting of more than one '
                                        'atom.',
                          'parents': ['CHEBI:36358', 'CHEBI:36916']},
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
    'num_true_positives': 53,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 100,
    'num_negatives': None,
    'precision': 1.0,
    'recall': 0.3464052287581699,
    'f1': 0.5145631067961165,
    'accuracy': 0.3464052287581699}