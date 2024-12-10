"""
Classifies: CHEBI:32955 epoxide
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_epoxide(smiles: str):
    """
    Determines if a molecule contains an epoxide group,
    defined as a cyclic ether with a 3-membered ring containing an oxygen atom.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule contains an epoxide group, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find all rings
    rings = mol.GetRingInfo().AtomRings()

    # Check if any ring has size 3 and contains an oxygen atom
    for ring in rings:
        if len(ring) == 3:
            atoms = [mol.GetAtomWithIdx(idx) for idx in ring]
            if any(atom.GetSymbol() == 'O' for atom in atoms):
                return True, "Molecule contains an epoxide group"

    return False, "Molecule does not contain an epoxide group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:32955',
                          'name': 'epoxide',
                          'definition': 'Any cyclic ether in which the oxygen '
                                        'atom forms part of a 3-membered ring.',
                          'parents': ['CHEBI:37407']},
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
    'num_true_positives': 82,
    'num_false_positives': 100,
    'num_true_negatives': 5944,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.45054945054945056,
    'recall': 0.9879518072289156,
    'f1': 0.6188679245283019,
    'accuracy': 0.9835155867471846}