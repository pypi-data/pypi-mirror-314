"""
Classifies: CHEBI:33694 biomacromolecule
"""
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors
from rdkit.Chem import rdMolDescriptors

def is_biomacromolecule(smiles: str):
    """
    Determines if a molecule is a biomacromolecule.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a biomacromolecule, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if molecule contains only C, H, O, N, P, S atoms
    allowed_atoms = set('CHONPS')
    atom_counts = Chem.Mol.GetAtomCountDict(mol)
    if any(atom not in allowed_atoms for atom in atom_counts):
        return False, "Molecule contains atoms other than C, H, O, N, P, S"

    # Check for common biomacromolecular substructures
    biomacro_patterns = [
        Chem.MolFromSmarts("OC(=O)C"),  # Carboxylic acid
        Chem.MolFromSmarts("NC(=O)C"),  # Amide
        Chem.MolFromSmarts("OC(=O)N"),  # Carbamate
        Chem.MolFromSmarts("OP(=O)(O)O"),  # Phosphate
        Chem.MolFromSmarts("O[C@H]1[C@H](O)[C@@H](O)[C@H](O)[C@@H]1O"),  # Pyranose
        Chem.MolFromSmarts("C1=CN=CN=C1"),  # Purine
        Chem.MolFromSmarts("C1=CNC=N1"),  # Pyrimidine
    ]

    if not any(mol.HasSubstructMatch(pattern) for pattern in biomacro_patterns):
        return False, "No common biomacromolecular substructures found"

    # Check for high molecular weight
    mw = Descriptors.MolWt(mol)
    if mw < 500:
        return False, "Molecular weight too low for a macromolecule"

    return True, "Molecule is classified as a biomacromolecule"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33694',
                          'name': 'biomacromolecule',
                          'definition': 'A macromolecule formed by a living '
                                        'organism.',
                          'parents': ['CHEBI:33839', 'CHEBI:50860']},
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
    'error': "type object 'Mol' has no attribute 'GetAtomCountDict'",
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