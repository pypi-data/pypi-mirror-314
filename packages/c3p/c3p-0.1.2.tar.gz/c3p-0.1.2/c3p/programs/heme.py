"""
Classifies: CHEBI:30413 heme
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_heme(smiles: str):
    """
    Determines if a molecule is a heme (tetrapyrrolic chelate of iron).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a heme, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for presence of iron atom
    has_iron = any(atom.GetSymbol() == 'Fe' for atom in mol.GetAtoms())
    if not has_iron:
        return False, "No iron atom found"

    # Check for porphyrin ring system
    porphyrin_ring_info = mol.GetRingInfo().IsAtomInRingOfSize(18)
    has_porphyrin_ring = any(porphyrin_ring_info)

    if not has_porphyrin_ring:
        return False, "No 18-membered ring (porphyrin ring) found"

    # Check if iron is chelated by the porphyrin ring
    iron_atom = next(atom for atom in mol.GetAtoms() if atom.GetSymbol() == 'Fe')
    iron_neighbors = iron_atom.GetNeighbors()
    porphyrin_ring_atoms = [mol.GetAtomWithIdx(idx) for idx in range(mol.GetNumAtoms()) if porphyrin_ring_info[idx]]
    is_chelated = all(neighbor in porphyrin_ring_atoms for neighbor in iron_neighbors)

    if not is_chelated:
        return False, "Iron atom is not chelated by the porphyrin ring"

    return True, "Molecule is a heme (tetrapyrrolic chelate of iron)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:30413',
                          'name': 'heme',
                          'definition': 'A heme is any tetrapyrrolic chelate '
                                        'of iron.',
                          'parents': [   'CHEBI:25216',
                                         'CHEBI:33892',
                                         'CHEBI:33909']},
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
             '    RingInfo.IsAtomInRingOfSize(RingInfo, int)\n'
             'did not match C++ signature:\n'
             '    IsAtomInRingOfSize(RDKit::RingInfo {lvalue} self, unsigned '
             'int idx, unsigned int size)',
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