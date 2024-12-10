"""
Classifies: CHEBI:33273 polyatomic anion
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_polyatomic_anion(smiles: str):
    """
    Determines if a molecule is a polyatomic anion (an anion consisting of more than one atom).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a polyatomic anion, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule has a negative total charge
    total_charge = Chem.GetFormalCharge(mol)
    if total_charge >= 0:
        return False, "Molecule does not have a negative total charge"

    # Check if the molecule consists of more than one atom
    num_atoms = mol.GetNumAtoms()
    if num_atoms == 1:
        return False, "Molecule consists of a single atom"

    # Check for specific functional groups or substructures
    smarts_patterns = ['[O-]', '[N-]', '[S-]', '[P-]']  # Add more patterns as needed
    for pattern in smarts_patterns:
        if mol.HasSubstructMatch(Chem.MolFromSmarts(pattern)):
            return True, f"Molecule contains the {pattern} polyatomic anion group"

    return True, "Molecule is a polyatomic anion based on total charge and number of atoms"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33273',
                          'name': 'polyatomic anion',
                          'definition': 'An anion consisting of more than one '
                                        'atom.',
                          'parents': ['CHEBI:22563', 'CHEBI:36358']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: 'Mol' object has no attribute "
               "'GetFormalCharge'",
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 482,
    'num_false_positives': 100,
    'num_true_negatives': 3243,
    'num_false_negatives': 6,
    'num_negatives': None,
    'precision': 0.8281786941580757,
    'recall': 0.9877049180327869,
    'f1': 0.9009345794392524,
    'accuracy': 0.9723309840772644}