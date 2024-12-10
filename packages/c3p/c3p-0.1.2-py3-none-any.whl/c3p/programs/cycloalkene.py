"""
Classifies: CHEBI:33643 cycloalkene
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_cycloalkene(smiles: str):
    """
    Determines if a molecule is a cycloalkene (an unsaturated monocyclic hydrocarbon having at least one endocyclic double bond).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a cycloalkene, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule has only one ring
    rings = mol.GetRingInfo().AtomRings()
    if len(rings) != 1:
        return False, "Molecule does not have exactly one ring"

    # Check if the ring is cycloalkene
    ring_atoms = set(rings[0])
    has_double_bond = False
    for bond in mol.GetBonds():
        if bond.GetBondType() == Chem.BondType.DOUBLE:
            atom1 = bond.GetBeginAtom().GetIdx()
            atom2 = bond.GetEndAtom().GetIdx()
            if atom1 in ring_atoms and atom2 in ring_atoms:
                has_double_bond = True
                break

    if not has_double_bond:
        return False, "Ring does not contain an endocyclic double bond"

    # Check if the ring contains only carbon and hydrogen atoms
    for atom_idx in ring_atoms:
        atom = mol.GetAtomWithIdx(atom_idx)
        if atom.GetSymbol() not in ['C', 'H']:
            return False, "Ring contains non-carbon and non-hydrogen atoms"

    return True, "Molecule is a cycloalkene"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33643',
                          'name': 'cycloalkene',
                          'definition': 'An unsaturated monocyclic hydrocarbon '
                                        'having at least one endocyclic double '
                                        'bond.',
                          'parents': ['CHEBI:33664', 'CHEBI:36403']},
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
    'num_true_positives': 3,
    'num_false_positives': 100,
    'num_true_negatives': 10411,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.02912621359223301,
    'recall': 1.0,
    'f1': 0.05660377358490566,
    'accuracy': 0.9904888719802168}