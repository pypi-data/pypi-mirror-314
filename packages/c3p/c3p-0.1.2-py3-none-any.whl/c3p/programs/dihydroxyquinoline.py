"""
Classifies: CHEBI:26507 dihydroxyquinoline
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_dihydroxyquinoline(smiles: str):
    """
    Determines if a molecule is a dihydroxyquinoline (any hydroxyquinoline in which the number of hydroxy substituents is specified as two).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a dihydroxyquinoline, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for a quinoline core
    quinoline_ring_info = mol.GetRingInfo().IsAtomInNgRingOfSize(5, 6)
    if not any(quinoline_ring_info):
        return False, "No quinoline ring system found"

    # Count the number of hydroxy (-OH) groups
    hydroxy_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O' and atom.GetTotalNumHs() == 1)

    if hydroxy_count == 2:
        return True, "Molecule is a dihydroxyquinoline"
    else:
        return False, f"Molecule has {hydroxy_count} hydroxy substituents, not 2"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26507',
                          'name': 'dihydroxyquinoline',
                          'definition': 'Any hydroxyquinoline in which the '
                                        'number of hydroxy substituents is '
                                        'specified as two.',
                          'parents': ['CHEBI:38774']},
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
    'error': "'RingInfo' object has no attribute 'IsAtomInNgRingOfSize'",
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