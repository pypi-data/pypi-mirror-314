"""
Classifies: CHEBI:26822 sulfide
"""
from rdkit import Chem
from rdkit.Chem import Descriptors

def is_sulfide(smiles: str):
    """
    Determines if a molecule is a sulfide, defined as any sulfur molecular entity
    that involves either covalently bonded or anionic sulfur.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a sulfide, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of sulfur atoms
    if not any(atom.GetSymbol() == 'S' for atom in mol.GetAtoms()):
        return False, "No sulfur atoms present"

    # Check for covalently bonded or anionic sulfur
    sulfur_atoms = [atom for atom in mol.GetAtoms() if atom.GetSymbol() == 'S']
    for sulfur_atom in sulfur_atoms:
        if sulfur_atom.GetFormalCharge() == -1:
            return True, "Molecule contains anionic sulfur"
        elif any(bond.GetBondType() == Chem.BondType.SINGLE for bond in sulfur_atom.GetBonds()):
            return True, "Molecule contains covalently bonded sulfur"

    return False, "No covalently bonded or anionic sulfur found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26822',
                          'name': 'sulfide',
                          'definition': 'Any sulfur molecular entity that '
                                        'involves either covalently bonded or '
                                        'anionic sulfur.',
                          'parents': ['CHEBI:26835']},
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
    'num_true_positives': 72,
    'num_false_positives': 100,
    'num_true_negatives': 676,
    'num_false_negatives': 2,
    'num_negatives': None,
    'precision': 0.4186046511627907,
    'recall': 0.972972972972973,
    'f1': 0.5853658536585366,
    'accuracy': 0.88}