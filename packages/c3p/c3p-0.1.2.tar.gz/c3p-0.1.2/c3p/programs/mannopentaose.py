"""
Classifies: CHEBI:149464 mannopentaose
"""
from rdkit import Chem
from typing import Tuple

def is_mannopentaose(smiles: str) -> Tuple[bool, str]:
    """
    Determines if a molecule is a mannopentaose (a pentasaccharide composed of 5 mannose moieties).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a mannopentaose, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Count the number of mannose residues
    mannose_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'C' and atom.GetDegree() == 4)

    if mannose_count != 5:
        return False, f"The molecule contains {mannose_count} mannose residues, but a mannopentaose should have 5"

    # Check if all mannose residues are connected in a single chain
    ring_atoms = set()
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C' and atom.GetDegree() == 4:
            ring_atoms.add(atom.GetIdx())

    all_connected = True
    visited = set()
    queue = [next(iter(ring_atoms))]
    while queue:
        current = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)
        for neighbor in [n.GetIdx() for n in mol.GetAtomWithIdx(current).GetNeighbors()]:
            if neighbor in ring_atoms:
                queue.append(neighbor)

    if len(visited) != mannose_count:
        all_connected = False

    if all_connected:
        return True, "The molecule is a mannopentaose"
    else:
        return False, "The mannose residues are not connected in a single chain"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:149464',
                          'name': 'mannopentaose',
                          'definition': 'Any pentasaccharide composed of 5 '
                                        'mannose moieties.',
                          'parents': ['CHEBI:25174', 'CHEBI:35369']},
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
    'num_true_positives': 0,
    'num_false_positives': 32,
    'num_true_negatives': 183888,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9998205751382387}