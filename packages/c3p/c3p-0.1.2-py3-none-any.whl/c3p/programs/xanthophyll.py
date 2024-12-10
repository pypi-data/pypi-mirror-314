"""
Classifies: CHEBI:27325 xanthophyll
"""
from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_xanthophyll(smiles: str):
    """
    Determines if a molecule is a xanthophyll, a subclass of carotenoids consisting of the oxygenated carotenes.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a xanthophyll, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains at least one oxygen atom
    if not any(atom.GetSymbol() == 'O' for atom in mol.GetAtoms()):
        return False, "No oxygen atoms found"

    # Check if the molecule is a carotenoid
    num_rings = rdMolDescriptors.CalcNumRings(mol)
    num_aromatic_rings = rdMolDescriptors.CalcNumAromaticRings(mol)
    if num_rings > 0 or num_aromatic_rings > 0:
        return False, "Contains rings, not a carotenoid"

    num_carbon_atoms = len([atom for atom in mol.GetAtoms() if atom.GetSymbol() == 'C'])
    if num_carbon_atoms < 20:
        return False, "Less than 20 carbon atoms, not a carotenoid"

    num_conjugated_double_bonds = Descriptors.NumAllConjonedDoubleBondsDescriptor(mol)
    if num_conjugated_double_bonds < 7:
        return False, "Less than 7 conjugated double bonds, not a carotenoid"

    return True, "Molecule is a xanthophyll, an oxygenated carotenoid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:27325',
                          'name': 'xanthophyll',
                          'definition': 'A subclass of carotenoids consisting '
                                        'of the oxygenated carotenes.',
                          'parents': ['CHEBI:23044']},
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
    'error': "module 'rdkit.Chem.Descriptors' has no attribute "
             "'NumAllConjonedDoubleBondsDescriptor'",
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': None}