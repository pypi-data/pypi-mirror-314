"""
Classifies: CHEBI:26546 rhamnose
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_rhamnose(smiles: str):
    """
    Determines if a molecule is a rhamnose (a deoxymannose sugar that is the 6-deoxy derivative of hexose).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a rhamnose, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of 6 carbon atoms and 5 oxygen atoms
    if not (mol.GetNumAtoms() == 16 and mol.GetNumHeavyAtoms() == 11):
        return False, "Incorrect number of atoms for rhamnose"

    # Check for the presence of a 6-membered ring
    rings = mol.GetRingInfo().AtomRings()
    ring_sizes = [len(ring) for ring in rings]
    if 6 not in ring_sizes:
        return False, "No 6-membered ring found"

    # Check for the presence of a deoxy group (CH3 group)
    has_deoxy_group = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C' and atom.GetDegree() == 1:
            has_deoxy_group = True
            break

    if not has_deoxy_group:
        return False, "No deoxy group (CH3) found"

    # Check for the presence of 5 hydroxyl groups (-OH)
    hydroxyl_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O' and atom.GetDegree() == 1)
    if hydroxyl_count != 5:
        return False, "Incorrect number of hydroxyl (-OH) groups"

    return True, "Molecule is a rhamnose"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26546',
                          'name': 'rhamnose',
                          'definition': 'A deoxymannose sugar that is the '
                                        '6-deoxy derivative of hexose.',
                          'parents': ['CHEBI:33983']},
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
    'num_false_positives': 0,
    'num_true_negatives': 183922,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9999945629421008}