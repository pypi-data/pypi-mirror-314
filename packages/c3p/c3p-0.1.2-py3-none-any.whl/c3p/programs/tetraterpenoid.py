"""
Classifies: CHEBI:26935 tetraterpenoid
"""
from rdkit import Chem
from rdkit.Chem import Descriptors

def is_tetraterpenoid(smiles: str):
    """
    Determines if a molecule is a tetraterpenoid.

    Tetraterpenoids are defined as any terpenoid derived from a tetraterpene (C40 skeleton),
    which may have undergone rearrangements or modifications (e.g., removal of methyl groups).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a tetraterpenoid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Calculate the number of carbon atoms
    num_carbon = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C')

    # Check if the number of carbon atoms is around 40 (+/- 5)
    if not 35 <= num_carbon <= 45:
        return False, "Number of carbon atoms not around 40 (tetraterpenoid range)"

    # Check if the molecule contains any rings
    rings = mol.GetRingInfo().AtomRings()
    if not rings:
        return False, "No rings found (tetraterpenoids are expected to have rings)"

    # Check if the molecule has specific functional groups or structural features
    # Tetraterpenoids can have a wide variety of structures, so this check is optional
    # and may not be reliable for all cases

    # Example: Check for the presence of a conjugated double bond system
    num_double_bonds = sum(1 for bond in mol.GetBonds() if bond.GetBondType() == Chem.BondType.DOUBLE)
    num_conjugated_double_bonds = Descriptors.NumAromaticRings(mol)
    if num_double_bonds > 0 and num_conjugated_double_bonds > 0:
        return True, "Molecule contains conjugated double bond system (characteristic of tetraterpenoids)"
    else:
        return True, "Molecule classified as tetraterpenoid based on carbon count and ring presence"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26935',
                          'name': 'tetraterpenoid',
                          'definition': 'Any terpenoid derived from a '
                                        'tetraterpene. The term includes '
                                        'compounds in which the C40 skeleton '
                                        'of the parent tetraterpene has been '
                                        'rearranged or modified by the removal '
                                        'of one or more skeletal atoms '
                                        '(generally methyl groups).',
                          'parents': ['CHEBI:26873']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: module 'rdkit.Chem.Descriptors' has no "
               "attribute 'ConjugatedPiElectronsDetector'",
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 16,
    'num_false_positives': 100,
    'num_true_negatives': 1671,
    'num_false_negatives': 9,
    'num_negatives': None,
    'precision': 0.13793103448275862,
    'recall': 0.64,
    'f1': 0.2269503546099291,
    'accuracy': 0.9393095768374164}