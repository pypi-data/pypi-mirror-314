"""
Classifies: CHEBI:33642 cyclic olefin
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_cyclic_olefin(smiles: str):
    """
    Determines if a molecule is a cyclic olefin.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a cyclic olefin, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule is cyclic
    ring_info = mol.GetRingInfo()
    if not ring_info.AtomRings():
        return False, "Molecule is not cyclic"

    # Check if the molecule has at least one double bond
    num_double_bonds = rdMolDescriptors.CalcNumRings(mol) - rdMolDescriptors.CalcNumAromaticRings(mol)
    if num_double_bonds == 0:
        return False, "Molecule does not contain any double bonds"

    # Check if the molecule contains only C and H atoms
    atoms = [atom.GetSymbol() for atom in mol.GetAtoms()]
    if any(atom not in ['C', 'H'] for atom in atoms):
        return False, "Molecule contains atoms other than C and H"

    return True, "Molecule is a cyclic olefin"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33642',
                          'name': 'cyclic olefin',
                          'definition': 'The inclusive term for any cyclic '
                                        'hydrocarbon having any number of '
                                        'double bonds.',
                          'parents': ['CHEBI:33641', 'CHEBI:33654']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: 'Mol' object has no attribute 'GetNumRings'",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 15,
    'num_false_positives': 100,
    'num_true_negatives': 28641,
    'num_false_negatives': 6,
    'num_negatives': None,
    'precision': 0.13043478260869565,
    'recall': 0.7142857142857143,
    'f1': 0.2205882352941176,
    'accuracy': 0.9963145817397956}