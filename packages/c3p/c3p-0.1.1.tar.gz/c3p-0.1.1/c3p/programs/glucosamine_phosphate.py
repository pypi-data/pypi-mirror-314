"""
Classifies: CHEBI:24269 glucosamine phosphate
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_glucosamine_phosphate(smiles: str):
    """
    Determines if a molecule is a glucosamine phosphate (a hexosamine phosphate having glucosamine as the amino sugar component).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a glucosamine phosphate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if it's a hexosamine phosphate
    if not Descriptors.NumHeteroatoms(mol) == 3:
        return False, "Not a hexosamine phosphate (incorrect number of heteroatoms)"

    if not Descriptors.NumHeterocycles(mol) == 2:
        return False, "Not a hexosamine phosphate (incorrect number of heterocycles)"

    # Check if it's glucosamine
    ring_atoms = mol.GetRingInfo().AtomRings()[0]
    ring_atoms = [mol.GetAtomWithIdx(idx) for idx in ring_atoms]
    ring_atoms = [atom for atom in ring_atoms if atom.GetSymbol() != 'O']

    if len(ring_atoms) != 6:
        return False, "Not a glucosamine phosphate (incorrect ring size)"

    if not all(atom.GetSymbol() in ['C', 'N'] for atom in ring_atoms):
        return False, "Not a glucosamine phosphate (incorrect ring atom types)"

    if not any(atom.GetSymbol() == 'N' for atom in ring_atoms):
        return False, "Not a glucosamine phosphate (no nitrogen in ring)"

    return True, "Glucosamine phosphate"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24269',
                          'name': 'glucosamine phosphate',
                          'definition': 'A hexosamine phosphate having '
                                        'glucosamine as the amino sugar '
                                        'component.',
                          'parents': ['CHEBI:24584']},
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
             "'NumHeterocycles'",
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