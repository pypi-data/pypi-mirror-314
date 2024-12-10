"""
Classifies: CHEBI:142772 Aspidosperma alkaloid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_Aspidosperma_alkaloid(smiles: str):
    """
    Determines if a molecule is an Aspidosperma alkaloid.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an Aspidosperma alkaloid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for at least one indole ring
    indole_ring = Chem.MolFromSmarts('c1ccc2c(c1)cnc2')
    is_indole = mol.HasSubstructMatch(indole_ring)
    if not is_indole:
        return False, "No indole ring found"

    # Check for tryptamine substructure
    tryptamine = Chem.MolFromSmarts('c1ccc2c(c1)cnc2CCNC')
    is_tryptamine = mol.HasSubstructMatch(tryptamine)
    if not is_tryptamine:
        return False, "No tryptamine substructure found"

    # Check for C19 or C20 skeleton
    num_atoms = mol.GetNumAtoms()
    if num_atoms not in [19, 20]:
        return False, "Incorrect number of atoms for Aspidosperma alkaloid"

    # Check for seconloganin-derived C9 or C10 unit
    seconloganin_c9 = Chem.MolFromSmarts('C1CCC2C(C1)CC(CO2)C')
    seconloganin_c10 = Chem.MolFromSmarts('C1CCC2C(C1)CC(CO2)CC')
    is_seconloganin = mol.HasSubstructMatch(seconloganin_c9) or mol.HasSubstructMatch(seconloganin_c10)
    if not is_seconloganin:
        return False, "No seconloganin-derived C9 or C10 unit found"

    return True, "Aspidosperma alkaloid detected"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:142772',
                          'name': 'Aspidosperma alkaloid',
                          'definition': 'Any member of a group of indole '
                                        'alkaloids based on a C19 or C20 '
                                        'skeleton formed by condensation of '
                                        'tryptamine with a rearranged '
                                        'seconloganin-derived C9 or C10 unit. '
                                        'The Aspidosperma alkaloids constitute '
                                        'the largest group of indole alkaloids '
                                        '(currently ca. 220 alkaloids) and may '
                                        'be divided into several sub-groups.',
                          'parents': ['CHEBI:38958']},
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