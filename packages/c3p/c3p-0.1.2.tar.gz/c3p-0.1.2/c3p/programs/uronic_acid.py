"""
Classifies: CHEBI:27252 uronic acid
"""
from rdkit import Chem
from rdkit.Chem import Descriptors

def is_uronic_acid(smiles: str):
    """
    Determines if a molecule is a uronic acid.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a uronic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Count carboxyl groups
    num_carboxyl = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O' and sum(mol.GetAtomWithIdx(n).GetFormalCharge() for n in atom.GetNeighbors()) == -1)

    # Count hydroxyl groups
    num_hydroxyl = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O' and atom.GetHybridization() == Chem.HybridizationType.SP3 and sum(mol.GetAtomWithIdx(n).GetFormalCharge() for n in atom.GetNeighbors()) == 0)

    # Uronic acids must have at least one carboxyl and one hydroxyl group
    if num_carboxyl < 1 or num_hydroxyl < 1:
        return False, "No carboxyl or hydroxyl group found"

    # Uronic acids must have at least one ring
    if mol.GetRingInfo().NumRings() < 1:
        return False, "No ring found"

    # Uronic acids must contain at least one oxygen in the ring
    ring_atoms = set()
    for ring in mol.GetRingInfo().AtomRings():
        for atom_idx in ring:
            ring_atoms.add(atom_idx)
            atom = mol.GetAtomWithIdx(atom_idx)
            if atom.GetSymbol() == 'O':
                return True, "Uronic acid detected"

    return False, "No oxygen found in the ring"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:27252',
                          'name': 'uronic acid',
                          'definition': 'A carbohydrate acid formally derived '
                                        'by oxidation to a carboxy group of '
                                        'the terminal -CH2OH group of any '
                                        'aldose or ketose.',
                          'parents': [   'CHEBI:25384',
                                         'CHEBI:33720',
                                         'CHEBI:35381']},
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
    'error': 'Python argument types in\n'
             '    Mol.GetAtomWithIdx(Mol, Atom)\n'
             'did not match C++ signature:\n'
             '    GetAtomWithIdx(RDKit::ROMol {lvalue} self, unsigned int idx)',
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': None}