"""
Classifies: CHEBI:138141 17alpha-hydroxy-C21-steroid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_17alpha_hydroxy_C21_steroid(smiles: str):
    """
    Determines if a molecule is a 17alpha-hydroxy-C21-steroid.

    A 17alpha-hydroxy-C21-steroid is defined as:
    Any C21-steroid carrying a hydroxy substituent at the 17alpha-position. 
    Note that individual examples may have ring substituents at other positions 
    and/or contain double bonds, aromatic A-rings, expanded/contracted rings etc., 
    so the formula and mass may vary from that given for the generic structure.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a 17alpha-hydroxy-C21-steroid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check number of atoms
    if mol.GetNumAtoms() != 21:
        return False, "Molecule does not have 21 atoms (not a C21-steroid)"

    # Check for 17alpha-hydroxy group
    atom_17 = mol.GetAtomWithIdx(16)  # 17th atom is at index 16 in RDKit
    if atom_17.GetAtomicNum() != 8 or not atom_17.GetIsAromatic():  # Oxygen atom, not aromatic
        return False, "No hydroxy group at position 17alpha"

    # Check for steroid backbone
    ring_info = mol.GetRingInfo()
    rings = ring_info.AtomRings()
    if len(rings) < 4:
        return False, "Less than 4 rings (not a steroid)"

    # Check for cyclopentane rings
    cyclopentane_rings = [ring for ring in rings if len(ring) == 5]
    if len(cyclopentane_rings) != 3:
        return False, "Not 3 cyclopentane rings (not a steroid)"

    # Check for cyclohexane ring
    cyclohexane_rings = [ring for ring in rings if len(ring) == 6]
    if len(cyclohexane_rings) != 1:
        return False, "Not 1 cyclohexane ring (not a steroid)"

    # If all checks pass, it's a 17alpha-hydroxy-C21-steroid
    return True, "17alpha-hydroxy-C21-steroid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:138141',
                          'name': '17alpha-hydroxy-C21-steroid',
                          'definition': 'Any C21-steroid carrying a hydroxy '
                                        'substituent at the 17alpha-position. '
                                        'Note that individual examples may '
                                        'have ring substituents at other '
                                        'positions and/or contain double '
                                        'bonds, aromatic A-rings, '
                                        'expanded/contracted rings etc., so '
                                        'the formula and mass may vary from '
                                        'that given for the generic structure.',
                          'parents': ['CHEBI:35342', 'CHEBI:61313']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.8,
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
    'num_true_negatives': 183925,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999945630307842}