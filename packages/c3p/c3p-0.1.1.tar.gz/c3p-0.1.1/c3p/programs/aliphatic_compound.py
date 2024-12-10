"""
Classifies: CHEBI:33653 aliphatic compound
"""
from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_aliphatic_compound(smiles: str):
    """
    Determines if a molecule is an aliphatic compound, defined as any acyclic or cyclic, saturated or unsaturated
    carbon compound, excluding aromatic compounds.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an aliphatic compound, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains any aromatic rings
    if mol.GetAromaticRingInfo().AromaticRings:
        return False, "Molecule contains aromatic rings, which are not aliphatic"

    # Check if the molecule contains any carbon atoms
    has_carbon = any(atom.GetSymbol() == 'C' for atom in mol.GetAtoms())
    if not has_carbon:
        return False, "Molecule does not contain any carbon atoms"

    # If the molecule passes the above checks, it is considered an aliphatic compound
    return True, "Molecule is an aliphatic compound"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33653',
                          'name': 'aliphatic compound',
                          'definition': 'Any acyclic or cyclic, saturated or '
                                        'unsaturated carbon compound, '
                                        'excluding aromatic compounds.',
                          'parents': ['CHEBI:50860']},
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
    'error': "'Mol' object has no attribute 'GetAromaticRingInfo'",
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