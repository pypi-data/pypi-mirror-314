"""
Classifies: CHEBI:24741 hydroxyproline
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_hydroxyproline(smiles: str):
    """
    Determines if a molecule is a hydroxyproline (proline derivative with at least one hydroxy group).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a hydroxyproline, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains a proline ring
    ring_info = mol.GetRingInfo()
    proline_ring = False
    for ring in ring_info.AtomRings():
        if len(ring) == 4:
            ring_atoms = [mol.GetAtomWithIdx(idx) for idx in ring]
            if sum(1 for atom in ring_atoms if atom.GetAtomicNum() == 7) == 1:  # Check for one nitrogen
                proline_ring = True
                break

    if not proline_ring:
        return False, "No proline ring found"

    # Check for at least one hydroxy group
    hydroxy_groups = sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 8 and atom.GetTotalNumHs() == 1)

    if hydroxy_groups == 0:
        return False, "No hydroxy groups found"

    return True, f"Hydroxyproline with {hydroxy_groups} hydroxy group(s)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24741',
                          'name': 'hydroxyproline',
                          'definition': 'A proline derivative that is proline '
                                        'substituted by at least one hydroxy '
                                        'group.',
                          'parents': [   'CHEBI:24662',
                                         'CHEBI:26273',
                                         'CHEBI:46701',
                                         'CHEBI:46773']},
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
    'num_false_positives': 100,
    'num_true_negatives': 5721,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9826520096186877}