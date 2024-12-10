"""
Classifies: CHEBI:33453 organic heterocyclyl group
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors

def is_organic_heterocyclyl_group(smiles: str):
    """
    Determines if a molecule is an organic heterocyclyl group.

    An organic heterocyclyl group is defined as a univalent group formed by removing
    a hydrogen atom from any ring atom of an organic heterocyclic compound.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an organic heterocyclyl group, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule has at least one ring
    if not mol.GetRingInfo().NumRings():
        return False, "No rings found"

    # Check if the molecule contains at least one heteroatom
    heteroatom_count = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() not in [1, 6])
    if heteroatom_count == 0:
        return False, "No heteroatoms found"

    # Check if the molecule has exactly one radical (*) position
    radical_atoms = [atom for atom in mol.GetAtoms() if atom.GetNumRadicalElectrons() > 0]
    if len(radical_atoms) != 1:
        return False, "Incorrect number of radical positions"

    # Check if the radical position is on a ring atom
    radical_atom = radical_atoms[0]
    if not any(radical_atom.GetIdx() in ring for ring in mol.GetRingInfo().AtomRings()):
        return False, "Radical position is not on a ring atom"

    return True, "Molecule is an organic heterocyclyl group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33453',
                          'name': 'organic heterocyclyl group',
                          'definition': 'A univalent group formed by removing '
                                        'a hydrogen atom from any ring atom of '
                                        'an organic heterocyclic compound.',
                          'parents': ['CHEBI:33249', 'CHEBI:48271']},
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
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 0,
    'num_false_positives': 29,
    'num_true_negatives': 183869,
    'num_false_negatives': 3,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9998259933333696}